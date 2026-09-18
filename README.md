<!-- version: 1.5.0 | build: 2026-09-17 | update: 2026-09-18 -->
# MSR JSON — Specification

[![validate](https://github.com/msrjson/specification/actions/workflows/validate.yml/badge.svg)](https://github.com/msrjson/specification/actions/workflows/validate.yml)
[![Specification: CC-BY-4.0](https://img.shields.io/badge/specification-CC--BY--4.0-blue.svg)](LICENSE-SPEC)
[![Tooling: MIT](https://img.shields.io/badge/tooling-MIT-green.svg)](LICENSE)

The normative artifacts of the **MSR JSON** open metadata protocol: the JSON
Schemas, the reference manifests and the RFCs, ratified and in draft.

This repository is the **single source of truth**. <https://msrjson.org>
serves these files and consumes this repository directly; it never keeps its
own copy. If the two ever disagree, this repository is right.

- Schema file: **<https://msrjson.org/schemas/msr-2.0.json>**
- Schema identifier (`$id`, and what a manifest puts in `$schema`):
  `https://msr-standard.org/schemas/msr-2.0.json`. It is an identifier, not a
  download location: that domain does not serve the file today.

## What MSR JSON is

A publisher describes their software once, in a manifest hosted on their own
domain:

```
https://your-domain.example/.well-known/msr.json
```

Registries, package managers and AI discovery engines read that manifest instead
of scraping a product page. There is no central registry to apply to, no
gatekeeper and no vendor who owns the format.

## Contents

| Path | What it is |
| --- | --- |
| `schemas/msr-2.0.json` | The canonical schema (JSON Schema Draft 2020-12), strict: unknown properties are rejected |
| `schemas/msr-1.1.json` | Legacy v1.1, kept for the PAD XML migration bridge |
| `schemas/msr-2.1-draft.json` | Experimental v2.1 draft — not ratified, do not author against it |
| `examples/*.json` | Six reference manifests, one per entity type, each validating with zero errors |
| `rfc/rfc-0001..0003.html` | The ratified RFCs |
| `rfc/rfc-0006.html` | Working draft: geographic and language availability, in the v2.1 draft only |
| `tests/` | The conformance suite below |

## The MSR JSON repositories

| Repository | What it is | Status |
| --- | --- | --- |
| **specification** | This repository — the source of truth | Published |
| [msr-validator](https://github.com/msrjson/msr-validator) | Reference validator library, in Python | Not yet released |
| [msr-cli](https://github.com/msrjson/msr-cli) | Reference command-line tool, the `msr` command | Not yet released |

Dependencies point one way only: `msr-cli` uses `msr-validator`, which bundles
the schema from a pinned release of this repository. This repository depends on
nothing. No other repository may keep its own copy of the schema.

## Generating a manifest with an AI agent

[AGENTS.md](AGENTS.md) is written for AI agents of any model asked to create an
`msr.json` for a project: what the protocol is, the constant `protocol` block, the
procedure, the values that must never be invented, and a tested validation
command.

## Verify the standard yourself

Nothing here is taken on trust. The suite checks that the canonical schema is
well-formed Draft 2020-12, that its `$id` is the canonical URL, that all six
examples validate with zero errors, and that manifests which should be rejected
are in fact rejected:

```bash
pip install -r requirements-test.txt
python -m pytest tests -q
```

No container, no network, no project-specific tooling. It runs the same way in
CI on every push and pull request.

To validate a manifest of your own:

```bash
pip install check-jsonschema
check-jsonschema \
  --schemafile https://msrjson.org/schemas/msr-2.0.json \
  .well-known/msr.json
```

## Changelog

Every change to the specification and to this repository is recorded in
[CHANGELOG.md](CHANGELOG.md), with its effect on what validates.

## Changing the protocol

Schema changes do not land as pull requests against `schemas/`. They go through
the RFC process: write the proposal in `rfc/`, following the shape of the
ratified ones, with the schema diff and the security considerations stated
explicitly. Two independent implementations must demonstrate interoperability
before a 30-day call for consensus.

A change that alters *what validates* is a MAJOR version under the compatibility
policy. Additive, backwards-compatible changes are MINOR. See
<https://msrjson.org/governance/>.

Typos, broken examples and documentation corrections are ordinary pull requests
and are welcome as such.

## Author

**MSR JSON was created and authored by Antonio Santos** — Esplanada, Bahia,
Brazil — author of the Craft Engine framework. Contact: snarthost@gmail.com.
Full statement in [AUTHORS](AUTHORS).

Attribution to the author is a condition of the CC-BY-4.0 license the
specification is published under. Authorship and stewardship are deliberately
separate: the protocol is authored by one person and governed in the open,
through the RFC process and the neutrality charter.

## Licensing

Dual-licensed, deliberately:

- **Specification text, schemas, examples, RFCs** — [CC-BY-4.0](LICENSE-SPEC).
  Free to implement, quote and translate, with attribution. It cannot be
  privatized, patented or encumbered by fees.
- **Tests and CI** — [MIT](LICENSE).

The scope of each license is stated in [NOTICE](NOTICE).

Implementing MSR JSON requires no permission, no fee and no registration.
