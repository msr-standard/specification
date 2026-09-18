# AGENTS.md — generating an MSR JSON manifest

Instructions for AI agents (any model) asked to create or update an `msr.json`
for a software project. Humans are welcome to read it too.

## What MSR JSON is

MSR JSON is an open, vendor-neutral metadata protocol for software, APIs, AI
agents and MCP servers, created by Antonio Santos. A publisher describes a
product once, in a manifest served from the product's own domain:

```
https://<product-domain>/.well-known/msr.json
```

Software registries and directories (for example mysoftrank.com), package
managers and AI discovery engines read that file instead of scraping a product
page. There is no central registry to apply to: publishing the file *is* the
listing.

| What | Where |
| --- | --- |
| This repository — the source of truth | <https://github.com/msr-standard/specification> |
| Canonical schema URL (goes in `$schema`) | `https://msr-standard.org/schemas/msr-2.0.json` |
| Schema file to validate against | `schemas/msr-2.0.json` in this repository |
| Six complete, valid examples | `examples/*.json` in this repository |
| Human-readable site | <https://msr-standard.org> |

If anything below disagrees with `schemas/msr-2.0.json`, the schema wins. Read
enum values from the schema itself — never from memory, and never from this
file.

## The protocol block is constant

Every MSR JSON 2.0 manifest carries the same `protocol` block. Copy it verbatim;
only `canonical_url` changes, to the manifest's own public URL:

```json
"protocol": {
  "name": "MSR JSON",
  "version": "2.0.0",
  "author": "Antonio Santos",
  "specification_license": "CC-BY-4.0",
  "reference_implementation_license": "MIT",
  "canonical_url": "https://<product-domain>/.well-known/msr.json"
}
```

`protocol.author` names the author of the **protocol**, not of the product
being described. The product's owner goes in `entity.vendor`.

## Procedure

1. **Read the project before writing anything.** Take the product name,
   domain, version, license, deployment model and interfaces from the project
   itself: `pyproject.toml` / `package.json`, `LICENSE`, `CHANGELOG.md`,
   `docker-compose.yml`, the README, route definitions, OpenAPI files. Every
   value must trace to something you read or something the owner told you.
2. **Ask for what the project cannot tell you** — typically the public domain,
   the vendor's legal name and country, and the pricing model. Do not guess
   them.
3. **Start from the closest example** in `examples/` (`saas`, `api`,
   `mcp-server`, `ai-agent`, `open-source`, `desktop`) rather than from a blank
   file, and replace every value.
4. **Omit what you cannot support.** Only five top-level keys are required
   (`$schema`, `protocol`, `entity`, `capabilities`, `releases`). An optional
   field left out is correct; an optional field filled with an invented value
   is a defect.
5. **Validate. Zero errors is the only acceptable result** — see below.
6. **Publish** at `/.well-known/msr.json` on the product's domain, served as
   `application/json` with `Access-Control-Allow-Origin: *`.

## Never invent — these are defects, not placeholders

A manifest is a trust artifact. Registries and agents act on it without a human
checking. The following have all shipped wrongly before; each one is a bug:

- **`releases.latest.artifacts[].sha256`** — only a digest computed from the
  real, published file. Never a placeholder, never a pattern, never a digest of
  something else. If there is no published artifact, omit `artifacts`.
- **`trust.domain_verification.status: "verified"`** — only after the
  verification actually succeeded. Before that, use `"pending"`, or omit
  `trust` entirely.
- **URLs** (`support_url`, `status_page`, `changelog_url`, `spec_url`,
  `endpoint`, webhooks) — only URLs that exist and answer. Omit the field
  otherwise.
- **Interfaces** — declare `mcp`, `openapi`, `graphql` or `grpc` only when the
  project really exposes them, with their real URLs.
- **A copy of the schema inside the project.** Reference the canonical URL;
  never vendor, embed or hand-edit `msr-2.0.json` into another codebase. A
  second copy maintained by hand once accumulated 81 divergences under the same
  version number.

## Traps the schema will catch — and why they happen

- `entity.license.commercial_terms` and `capabilities.pricing.model` are
  **different enums**. `"usage"` is valid for `pricing.model` and invalid for
  `commercial_terms`.
- `entity.slug` is lowercase kebab-case: `^[a-z0-9]+(?:-[a-z0-9]+)*$`.
- `entity.domain` is a bare hostname — no scheme, no path, no trailing dot.
- `entity.descriptions` is keyed by language; each language requires `summary`
  (max 256 characters). `tagline` is optional (max 140).
- `vendor.country_code` is ISO 3166-1 alpha-2 in upper case (`BR`, not `br`).
- `published_at` / `verified_at` are RFC 3339 date-times with a timezone:
  `2026-09-17T00:00:00Z`.
- The schema is strict: `additionalProperties: false` at every level. A field
  that is not in the schema is an error, not an extension.

## Validate

Until `msr-standard.org` serves HTTPS, validate against the schema in this
repository. Either tool works:

```bash
# Python
pip install jsonschema
curl -sSfo /tmp/msr-2.0.json \
  https://raw.githubusercontent.com/msr-standard/specification/main/schemas/msr-2.0.json
python -c "
import json, sys
from jsonschema import Draft202012Validator
schema = json.load(open('/tmp/msr-2.0.json'))
manifest = json.load(open(sys.argv[1]))
errors = sorted(Draft202012Validator(schema).iter_errors(manifest), key=lambda e: list(e.path))
for e in errors: print('/'.join(map(str, e.path)) or '(root)', '->', e.message)
if errors: sys.exit(1)
print('valid: 0 errors')
" .well-known/msr.json
```

```bash
# Standalone CLI
pip install check-jsonschema
check-jsonschema --schemafile \
  https://raw.githubusercontent.com/msr-standard/specification/main/schemas/msr-2.0.json \
  .well-known/msr.json
```

The `$schema` field inside the manifest still points at the canonical
`https://msr-standard.org/schemas/msr-2.0.json`. Only the validator fetches the
file from GitHub.

## Report back

When you hand the manifest over, state: the file path, the validation command
you ran and its result, which optional fields you **omitted and why**, and any
value the owner still has to confirm. "Valid" without the command output is an
impression, not evidence.
