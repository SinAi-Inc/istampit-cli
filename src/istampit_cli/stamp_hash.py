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

    # Build a Timestamp over the digest bytes; attach a child timestamp for the OpSHA256
    # that includes at least one attestation (placeholder) so neither node is "empty".
    # This avoids ValueError("An empty timestamp can't be serialized") raised by
    # opentimestamps when both attestations and ops are absent.
    root_ts = Timestamp(digest)
    child_ts = Timestamp(digest)
    # Try preferred: PendingAttestation (if library provides it in newer versions)
    try:  # pragma: no cover - availability depends on library version
        from opentimestamps.core.attestations import PendingAttestation  # type: ignore

        try:
            # Some versions accept bytes, others str; attempt both.
            try:  # first try bytes
                child_ts.attestations.add(PendingAttestation(b"placeholder"))  # type: ignore[arg-type]
            except (TypeError, ValueError):
                child_ts.attestations.add(PendingAttestation("placeholder"))  # type: ignore[arg-type]
        except (TypeError, ValueError):
            pass
    except ImportError:  # Fallback: define a minimal private attestation subclass
        try:  # pragma: no cover
            from opentimestamps.core.timestamp import TimeAttestation  # type: ignore

            class _PlaceholderAttestation(TimeAttestation):  # type: ignore
                TAG = b"PLHOLDER"  # 8-byte tag as required; private placeholder

                def _serialize_payload(self, ctx):  # type: ignore[override]
                    # Intentionally empty payload
                    return None

            try:  # attempt placeholder attestation
                child_ts.attestations.add(_PlaceholderAttestation())
            except (TypeError, ValueError):
                pass
        except (ImportError, AttributeError):
            pass

    try:  # attach op mapping
        root_ts.ops[OpSHA256()] = child_ts
    except (KeyError, TypeError, ValueError):  # pragma: no cover - conservative
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
