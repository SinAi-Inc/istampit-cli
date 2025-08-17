# Changelog

All notable changes to this project will be documented in this file.

## v1.0.3 – Detached hash stamping GA

## v1.0.4 – Serialization fix for detached hash receipts

- Simplified detached hash receipt construction: attach placeholder attestation directly to root timestamp
- Removed nested child timestamp/op to eliminate "empty timestamp" serialization errors in CI
- Added defensive fallback self-op insertion only if attestation addition fails
- Version bump to ensure CI picks up updated editable install

- Added `stamp --hash <sha256-hex>` for detached digest receipts (no file upload required)
- Added `--upgrade` flag to optionally enrich a newly created receipt via calendar attestation
- Structured JSON output for hash mode (`{"receipts":[...],"hash":"<hex>","upgraded":bool}`)
- Added GitHub Actions smoke workflow for hash stamping
- Documentation updates and README cleanups

## v1.0.2

- Introduced experimental hash stamping scaffold (now superseded by GA in 1.0.3)
- Parser enhancements and internal refactors

## v1.0.1

- Initial public release of the CLI with stamp, verify, upgrade, upgrade-all, info commands
