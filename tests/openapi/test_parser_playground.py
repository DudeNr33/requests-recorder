"""
Not a real unit test, more to play around with the functionality of the openapi3-parser library.
"""

from pathlib import Path

import pytest
from openapi_parser import parse
from openapi_parser.specification import Specification

OPENAPI_SPEC = Path(__file__).parent / "petstore_openapi.json"


@pytest.fixture
def spec() -> Specification:
    return parse(str(OPENAPI_SPEC.resolve()))


def test_get_paths(spec: Specification):
    assert len(spec.paths) == 13


def test_get_all_endpoints_and_methods(spec: Specification):
    endpoints = []
    for path in spec.paths:
        for operation in path.operations:
            for response in operation.responses:
                endpoints.append((operation.method.name, path.url, response.code))
    assert len(endpoints) == 64
