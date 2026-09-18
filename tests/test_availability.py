# version: 1.0.0 | build: 2026-09-18 | update: 2026-09-18
"""RFC-0006: geographic and language availability, in the v2.1 draft schema.

The block lives only in the draft. Stable 2.0 manifests are untouched, and the
2.0 schema must keep rejecting the block, because adding a property to a closed
object would change what validates.
"""

import copy
import json
import pathlib

import pytest
from jsonschema import Draft202012Validator

ROOT = pathlib.Path(__file__).resolve().parent.parent
DRAFT_SCHEMA = ROOT / "schemas" / "msr-2.1-draft.json"
STABLE_SCHEMA = ROOT / "schemas" / "msr-2.0.json"

AVAILABILITY = {
    "regions": ["019", "150"],
    "countries": ["AO", "MZ"],
    "excluded_countries": ["CU"],
    "languages": ["pt-BR", "en", "es-419", "zh-Hant-TW"],
    "data_residency": ["BR", "150"],
}


def _load(path):
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def draft():
    schema = _load(DRAFT_SCHEMA)
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


@pytest.fixture
def manifest():
    data = _load(ROOT / "examples" / "saas.json")
    data["$schema"] = "https://msr-standard.org/schemas/msr-2.1-draft.json"
    data["capabilities"]["availability"] = copy.deepcopy(AVAILABILITY)
    return data


def _errors(validator, data):
    return [e.message for e in validator.iter_errors(data)]


def test_full_availability_block_validates(draft, manifest):
    assert not _errors(draft, manifest)


def test_worldwide_is_declared_with_region_001(draft, manifest):
    manifest["capabilities"]["availability"] = {"regions": ["001"]}
    assert not _errors(draft, manifest)


def test_manifest_without_availability_still_validates(draft, manifest):
    del manifest["capabilities"]["availability"]
    assert not _errors(draft, manifest)


@pytest.mark.parametrize(
    "field, value",
    [
        ("regions", ["999"]),          # not an M49 region
        ("regions", ["076"]),          # M49 country code (Brazil), not a region
        ("regions", ["Europe"]),       # names are not codes
        ("countries", ["br"]),         # ISO 3166-1 is uppercase
        ("countries", ["BRA"]),        # alpha-3 is not accepted
        ("excluded_countries", ["150"]),
        ("languages", ["pt_BR"]),      # BCP 47 uses a hyphen
        ("languages", ["Portuguese"]),
        ("data_residency", ["eu"]),
        ("data_residency", ["999"]),
        ("regions", []),               # an empty list declares nothing
        ("languages", ["en", "en"]),
    ],
)
def test_invalid_values_are_rejected(draft, manifest, field, value):
    manifest["capabilities"]["availability"][field] = value
    assert _errors(draft, manifest), f"{field}={value!r} should not validate"


def test_eu_is_accepted_for_data_residency(draft, manifest):
    """EU is ISO 3166-1 exceptionally reserved and a CLDR region; M49 150 is
    all of Europe, which is not the same legal perimeter for data protection."""
    manifest["capabilities"]["availability"]["data_residency"] = ["EU"]
    assert not _errors(draft, manifest)


def test_unknown_availability_key_is_rejected(draft, manifest):
    manifest["capabilities"]["availability"]["continents"] = ["Europe"]
    assert any("Additional properties" in m for m in _errors(draft, manifest))


def test_empty_availability_block_is_rejected(draft, manifest):
    manifest["capabilities"]["availability"] = {}
    assert _errors(draft, manifest)


def test_description_keys_must_be_language_tags(draft, manifest):
    manifest["entity"]["descriptions"]["pt-BR"] = {"summary": "Resumo."}
    assert not _errors(draft, manifest)
    manifest["entity"]["descriptions"]["portuguese"] = {"summary": "Resumo."}
    assert _errors(draft, manifest)


def test_stable_schema_still_rejects_the_block(manifest):
    """2.0 is closed: the block cannot leak into stable manifests."""
    stable = Draft202012Validator(_load(STABLE_SCHEMA))
    manifest["$schema"] = "https://msr-standard.org/schemas/msr-2.0.json"
    assert any("Additional properties" in m for m in _errors(stable, manifest))
