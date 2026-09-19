<!-- version: 1.2.0 | build: 2026-09-18 | update: 2026-09-19 -->
# Changelog

Changes to the MSR JSON specification and to this repository.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning: [SemVer](https://semver.org/spec/v2.0.0.html), governed by the
compatibility policy at <https://msrjson.org/governance/>: a change that
alters what validates is MAJOR; a backwards-compatible addition is MINOR; a
non-normative clarification is PATCH.

## [Unreleased]

**Nothing here changes what validates against 2.0.0**: every manifest valid
against 2.0.0 is still valid, and every invalid one is still invalid. The one
normative change is to the unratified v2.1 draft schema.

### Added

- RFC 0007 (working draft), *Software Registry Conformance, Ingestion & Interoperability Specification*:
  specifies normative requirements for software registries and crawlers (Zero-Account URL Ingestion,
  SSRF and DoS network protection, semantic cache polling via ETag/If-Modified-Since, PAD JSON transition
  dialect normalization, domain authority/claim verification, and the zero-drift rule prohibiting canonical
  schema forking).
- RFC 0006 (working draft), *Geographic and Language Availability*: an optional
  `capabilities.availability` object in `schemas/msr-2.1-draft.json` with
  `regions` (UN M49), `countries` and `excluded_countries` (ISO 3166-1
  alpha-2), `languages` and `support_languages` (BCP 47), `currencies` (ISO 4217)
  and `data_residency` (country, M49 region or `EU`). An absent field means not declared, never worldwide. The same draft
  requires `entity.descriptions` keys to be BCP 47 tags. Covered by
  `tests/test_availability.py`, which also asserts that the 2.0 schema keeps
  rejecting the block.
- `README.md` and `AGENTS.md` point to where the files are served today,
  `https://msrjson.org`, and to the repositories under `github.com/msrjson`.
  The validation commands fetched `https://msr-standard.org/schemas/msr-2.0.json`,
  which answers 404; they now fetch it from `msrjson.org`. The schema `$id` is
  unchanged and is described as an identifier, not a download location.
- `AGENTS.md` tells agents not to put `capabilities.availability` in a 2.0
  manifest, and that `vendor.country_code` is the vendor's seat, not a market.

- `AGENTS.md` — instructions for AI agents of any model asked to generate an
  `msr.json`: the constant `protocol` block, a procedure that derives every
  value from the project, the values that must never be invented, and a
  validation command tested against a valid and an invalid manifest.
- `AUTHORS` and `NOTICE`, crediting Antonio Santos as the author of the
  protocol and stating the scope of each license.
- `LICENSE` (MIT, for the tests and CI) and `LICENSE-SPEC` (CC-BY-4.0, full
  legal text, for the specification, schemas, examples and RFCs). The dual
  license had been claimed on the website but existed in no file.
- A conformance suite that runs from a plain checkout, with no container and no
  network, and a GitHub Actions workflow running it on every push and pull
  request.
- A test that the canonical schema's `$id` is the canonical URL, so a fork
  cannot silently become a second protocol.

### Changed

- The project is named **MSR JSON** everywhere it names itself: RFC page titles
  and logo text say "MSR JSON" instead of "MSR Standard".

- **The canonical domain is `msrjson.org`.** The `$id` of `msr-1.1.json`,
  `msr-2.0.json` and `msr-2.1-draft.json`, the `$schema` of the six reference
  manifests, the RFC canonical links, `AUTHORS`, `README.md` and `AGENTS.md`
  move from `https://msr-standard.org` to `https://msrjson.org`, the address the
  files are actually served from. What validates does not change: `$schema` is
  a URI, not a constant, and a test asserts that a manifest naming the former
  identifier still validates. Registries treat the former URL as an alias.

- `protocol.author` in the six reference manifests names Antonio Santos, the
  author of the protocol, instead of a working group. The field names who wrote
  the **protocol**; a product's owner goes in `entity.vendor`.

## [2.0.0] — 2026-09-17

The current stable protocol. First version published in this repository.

RFC 0001: consolidation of the entity archetype, native MCP and AI descriptors,
integer minor currency units, and Ed25519 trust signatures.

## Earlier versions

Recorded on the specification page, which predates this repository. Their
history is not in this repository's git log.

- **1.1.0** — 2025-11-20 — legacy bridge. Added webhook synchronization headers
  and JSON Schema validation. Its schema is `schemas/msr-1.1.json`.
- **1.0.0** — 2024-04-10 — deprecated. The initial JSON translation of the
  legacy ASP PAD XML standard.
