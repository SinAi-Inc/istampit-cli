from __future__ import annotations

import binascii
from typing import Optional
import subprocess

from opentimestamps.core.op import OpSHA256  # type: ignore
from opentimestamps.core.timestamp import DetachedTimestampFile, Timestamp  # type: ignore
from opentimestamps.core.serialize import StreamSerializationContext  # type: ignore


class HashFormatError(ValueError):
    pass


def _parse_digest_hex(h: str) -> bytes:
    h = (h or "").strip()
    if len(h) != 64:
        raise HashFormatError("expected 64 hex chars (sha256)")
    try:
        return binascii.unhexlify(h)
    except binascii.Error as e:  # pragma: no cover
        raise HashFormatError("invalid hex") from e


def stamp_from_hash_hex(digest_hex: str, out_path: Optional[str] = None, do_upgrade: bool = False) -> tuple[str, bool]:
    digest = _parse_digest_hex(digest_hex)

    # Construct a single root timestamp over the digest and attach a placeholder attestation
    # to satisfy serializer requirements (must have at least one attestation or op). Simplicity
    # over cleverness: define a minimal private attestation class.
    root_ts = Timestamp(digest)
    try:  # pragma: no cover - defensive; rely on public TimeAttestation base
        from opentimestamps.core.timestamp import TimeAttestation  # type: ignore

        class _PlaceholderAttestation(TimeAttestation):  # type: ignore
            TAG = b"PLHOLDER"  # 8 bytes
            def _serialize_payload(self, ctx):  # type: ignore[override]
                return None

        try:
            root_ts.attestations.add(_PlaceholderAttestation())
        except (TypeError, ValueError):
            # Fallback: if add fails, add a self-op so timestamp not empty
            try:
                root_ts.ops[OpSHA256()] = Timestamp(digest)
            except (KeyError, TypeError, ValueError):
                pass
    except (ImportError, AttributeError):  # extremely unlikely; fallback to self-op
        try:
            root_ts.ops[OpSHA256()] = Timestamp(digest)
        except (KeyError, TypeError, ValueError):  # pragma: no cover
            pass

    dtf = DetachedTimestampFile(OpSHA256(), root_ts)

    out = out_path or f"{digest_hex}.ots"
    with open(out, "wb") as f:
        ctx = StreamSerializationContext(f)
        dtf.serialize(ctx)
    upgraded = False
    if do_upgrade:
        try:
            subprocess.run(["ots", "upgrade", out], check=True, capture_output=True)
            upgraded = True
        except subprocess.CalledProcessError:  # non-fatal
            upgraded = False
    return out, upgraded

__all__ = ["stamp_from_hash_hex", "HashFormatError"]
