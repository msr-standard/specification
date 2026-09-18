# MSR JSON — Specification

[![validate](https://github.com/msr-standard/specification/actions/workflows/validate.yml/badge.svg)](https://github.com/msr-standard/specification/actions/workflows/validate.yml)
[![Specification: CC-BY-4.0](https://img.shields.io/badge/specification-CC--BY--4.0-blue.svg)](LICENSE-SPEC)
[![Tooling: MIT](https://img.shields.io/badge/tooling-MIT-green.svg)](LICENSE)

The normative artifacts of the **MSR JSON** open metadata protocol: the JSON
Schemas, the reference manifests and the ratified RFCs.

This repository is the **single source of truth**. <https://msr-standard.org>
serves these files at their canonical URLs and consumes this repository directly;
it never keeps its own copy. If the two ever disagree, this repository is right.

Canonical schema: **<https://msr-standard.org/schemas/msr-2.0.json>**

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
| `tests/` | The conformance suite below |

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
  --schemafile https://msr-standard.org/schemas/msr-2.0.json \
  .well-known/msr.json
```

## Changing the protocol

Schema changes do not land as pull requests against `schemas/`. They go through
the RFC process: write the proposal in `rfc/`, following the shape of the
ratified ones, with the schema diff and the security considerations stated
explicitly. Two independent implementations must demonstrate interoperability
before a 30-day call for consensus.

A change that alters *what validates* is a MAJOR version under the compatibility
policy. Additive, backwards-compatible changes are MINOR. See
<https://msr-standard.org/governance/>.

Typos, broken examples and documentation corrections are ordinary pull requests
and are welcome as such.

## Licensing

Dual-licensed, deliberately:

- **Specification text, schemas, examples, RFCs** — [CC-BY-4.0](LICENSE-SPEC).
  Free to implement, quote and translate, with attribution. It cannot be
  privatized, patented or encumbered by fees.
- **Tests and CI** — [MIT](LICENSE).

The scope of each license is stated in [NOTICE](NOTICE).

Implementing MSR JSON requires no permission, no fee and no registration.
