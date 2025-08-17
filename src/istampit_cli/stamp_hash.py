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

    # Build Timestamp over digest bytes then wrap in DetachedTimestampFile with OpSHA256
    ts = Timestamp(digest)
    dtf = DetachedTimestampFile(OpSHA256(), ts)

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
