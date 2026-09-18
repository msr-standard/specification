# version: 1.0.0 | build: 2026-09-18 | update: 2026-09-18
"""Conformance suite for the MSR JSON normative artifacts.

Everything here runs from a plain checkout with no container, no network and no
project-specific tooling, so anyone who forks this repository can verify the
standard for themselves:

    pip install -r requirements-test.txt
    python -m pytest tests -q
"""

import glob
import json
import os
import pathlib

import pytest
from jsonschema import Draft202012Validator

ROOT = pathlib.Path(__file__).resolve().parent.parent
CANONICAL_SCHEMA = ROOT / "schemas" / "msr-2.0.json"


@pytest.fixture(scope="session")
def msr_schema():
    schema_data = json.loads(CANONICAL_SCHEMA.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema_data)
    return schema_data


@pytest.fixture(scope="session")
def validator(msr_schema):
    return Draft202012Validator(msr_schema)


@pytest.fixture(scope="session")
def saas_manifest():
    return json.loads((ROOT / "examples" / "saas.json").read_text(encoding="utf-8"))


def test_canonical_schema_is_valid_draft_2020_12(msr_schema):
    """Ensure schemas/msr-2.0.json is well-formed Draft 2020-12 JSON Schema."""
    assert msr_schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    assert msr_schema["title"] == "MSR JSON Protocol Schema"
    assert "$id" in msr_schema
    assert "required" in msr_schema


def test_canonical_schema_id_is_the_canonical_url(msr_schema):
    """Project rule 1: every schema reference resolves to the canonical URL."""
    assert msr_schema["$id"] == "https://msr-standard.org/schemas/msr-2.0.json", (
        "The $id is how a manifest names the schema it was authored against. "
        "A fork that changes it silently creates a second, incompatible protocol."
    )


def test_all_example_manifests_strictly_validate(validator):
    """Project rule 4: every manifest in examples/ validates with 0 errors."""
    example_files = sorted(glob.glob(str(ROOT / "examples" / "*.json")))
    assert len(example_files) == 6, f"Expected 6 examples, found {len(example_files)}"

    for file_path in example_files:
        manifest_data = json.loads(pathlib.Path(file_path).read_text(encoding="utf-8"))
        errors = list(validator.iter_errors(manifest_data))
        assert not errors, (
            f"{os.path.basename(file_path)} validation failed: "
            f"{[e.message for e in errors]}"
        )


def test_negative_missing_required_fields(validator):
    """Ensure manifests missing required top-level keys are rejected."""
    bad_manifest = {
        "$schema": "https://msr-standard.org/schemas/msr-2.0.json",
        "protocol": {
            "name": "MSR JSON",
            "version": "2.0.0",
            "author": "Test",
            "specification_license": "CC-BY-4.0",
            "reference_implementation_license": "MIT",
        },
    }
    errors = list(validator.iter_errors(bad_manifest))
    assert errors
    missing = [e.message for e in errors if "is a required property" in e.message]
    assert any("entity" in m for m in missing)


def test_negative_invalid_protocol_name(validator, saas_manifest):
    """Ensure protocol.name must be exactly 'MSR JSON'."""
    manifest = dict(saas_manifest)
    manifest["protocol"] = {**manifest["protocol"], "name": "Wrong Protocol"}
    errors = list(validator.iter_errors(manifest))
    assert any("MSR JSON" in e.message for e in errors)


def test_negative_invalid_slug_syntax(validator, saas_manifest):
    """Ensure entity.slug must be lowercase kebab-case."""
    manifest = dict(saas_manifest)
    manifest["entity"] = {**manifest["entity"], "slug": "INVALID_SLUG_With_Upper!"}
    errors = list(validator.iter_errors(manifest))
    assert errors


def test_negative_invalid_deployment_type(validator, saas_manifest):
    """Ensure capabilities.deployment only contains allowed enum values."""
    manifest = json.loads(json.dumps(saas_manifest))
    manifest["capabilities"]["deployment"].append("quantum-teleport")
    errors = list(validator.iter_errors(manifest))
    assert errors


def test_negative_additional_properties_forbidden(validator, saas_manifest):
    """Ensure unknown root properties are strictly rejected."""
    manifest = dict(saas_manifest)
    manifest["unknown_payload_property"] = True
    errors = list(validator.iter_errors(manifest))
    assert any("Additional properties are not allowed" in e.message for e in errors)
