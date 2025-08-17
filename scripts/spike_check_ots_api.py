#!/usr/bin/env python
from __future__ import annotations
import importlib, inspect, json, sys

def safe_import(name: str):
    try:
        return importlib.import_module(name)
    except Exception as e:  # noqa: BLE001
        print(json.dumps({"module": name, "import": "error", "error": str(e)}))
        return None

report = {}
modules = [
    "opentimestamps",
    "opentimestamps.client",
    "opentimestamps.core",
    "opentimestamps.core.op",
    "opentimestamps.core.timestamp",
    "opentimestamps.core.serialize",
]
for m in modules:
    mod = safe_import(m)
    if not mod:
        continue
    attrs = {}
    for attr in ["OpSHA256", "DetachedTimestampFile", "Timestamp", "BytesSerializationContext", "StreamSerializationContext"]:
        if hasattr(mod, attr):
            obj = getattr(mod, attr)
            info = {"type": type(obj).__name__}
            try:
                if inspect.isclass(obj) or inspect.isfunction(obj):
                    info["signature"] = str(inspect.signature(obj))
            except Exception:  # noqa: BLE001
                pass
            attrs[attr] = info
    report[m] = attrs

# Try constructing objects if available
construct = {}
try:
    from opentimestamps.core.op import OpSHA256  # type: ignore
    construct["OpSHA256_present"] = True
except Exception as e:  # noqa: BLE001
    construct["OpSHA256_present"] = False
    construct["OpSHA256_error"] = str(e)

try:
    from opentimestamps.core.timestamp import DetachedTimestampFile  # type: ignore
    if "OpSHA256_present" in construct and construct["OpSHA256_present"]:
        op = OpSHA256()
        # 32 zero bytes digest sample
        digest = bytes.fromhex("00"*32)
        dtf = DetachedTimestampFile(op, digest)
        construct["DetachedTimestampFile_init"] = True
        # Probe serialize patterns
        ser_patterns = {}
        for call in ["dtf.serialize()", "dtf.serialize(None)"]:
            try:
                result = eval(call)  # noqa: S307
                ser_patterns[call] = {
                    "returned_type": type(result).__name__,
                    "returned_len": len(result) if hasattr(result, "__len__") else None,
                }
            except Exception as e:  # noqa: BLE001
                ser_patterns[call] = {"error": str(e)}
        construct["serialize_attempts"] = ser_patterns
    else:
        construct["DetachedTimestampFile_init"] = False
except Exception as e:  # noqa: BLE001
    construct["DetachedTimestampFile_error"] = str(e)

print(json.dumps({"modules": report, "construct": construct}, indent=2))
