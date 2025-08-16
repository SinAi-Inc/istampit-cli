# iStampit CLI — Blockchain Timestamp Verification (OpenTimestamps)

[![PyPI - Version](https://img.shields.io/pypi/v/istampit-cli?logo=pypi)](https://pypi.org/project/istampit-cli/)
[![PyPI - Python Versions](https://img.shields.io/pypi/pyversions/istampit-cli)](https://pypi.org/project/istampit-cli/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/istampit-cli?color=blue)](https://pypistats.org/packages/istampit-cli)
[![License](https://img.shields.io/pypi/l/istampit-cli)](https://opensource.org/licenses/MIT)
[![Publish Status](https://github.com/SinAi-Inc/istampit-cli/actions/workflows/publish.yml/badge.svg)](https://github.com/SinAi-Inc/istampit-cli/actions/workflows/publish.yml)
[![OpenSSF Scorecard](https://img.shields.io/ossf-scorecard/github.com/SinAi-Inc/istampit-cli?label=openssf%20scorecard&logo=OpenSSF)](https://securityscorecards.dev/viewer/?uri=github.com/SinAi-Inc/istampit-cli)

Lightweight CLI around the official [OpenTimestamps](https://opentimestamps.org) client to **stamp, verify, upgrade, and inspect** cryptographic timestamp proofs (".ots" receipts) for your files — privacy‑first, Bitcoin‑anchored proof‑of‑existence.

---

## ✨ Features

* ✅ Free & open‑source (MIT wrapper, underlying libs LGPL-3.0)
* ✅ Privacy‑first — only hashes leave your machine
* ✅ Trustless & permanent — proofs anchor into Bitcoin
* ✅ Works offline — create receipts without network
* ✅ `--json` output for automation & CI

---

## 📦 Install

```bash
pip install istampit-cli
# or for isolated usage:
pipx install istampit-cli
```

---

## 🚀 Usage

```bash
# Create a timestamp receipt
istampit stamp path/to/file.pdf          # → creates file.pdf.ots

# Verify a receipt
istampit verify path/to/file.pdf.ots     # checks proof against Bitcoin

# Upgrade a receipt (fetch newer attestations)
istampit upgrade path/to/file.pdf.ots    # rewrites upgraded proof

# Inspect a receipt
istampit info path/to/file.pdf.ots       # shows operations/attestations
```

Add `--json` to any command for machine‑readable output.

---

## 🔢 Exit Codes

* `0` → success
* non‑zero → failure (error message on stderr)

---

## 📚 Resources

* 🌐 Website: <https://iStampit.io>
* 🧾 Public Ledger: <https://iStampit.io/ledger>
* 🐙 Source / Issues: <https://github.com/SinAi-Inc/istampit-cli>

---

## 📜 License

* Wrapper code: MIT
* OpenTimestamps libraries: LGPL-3.0

---

**Provable Innovation, Free for Everyone.**
Empowering developers, researchers, and creators with simple, reliable, and verifiable timestamp proofs.
