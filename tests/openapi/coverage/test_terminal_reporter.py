import json
from textwrap import dedent
from pathlib import Path

import requests
import pytest
from pytest_httpserver import HTTPServer

from requests_stats.adapter import RecordingHTTPAdapter
from requests_stats.recorder.in_memory_recorder import InMemoryRecorder
from requests_stats.openapi.coverage import Coverage
from requests_stats.openapi.terminal_reporter import TerminalReporter


MINIMAL_OPENAPI_SPEC = {
    "openapi": "3.0.0",
    "info": {
        "title": "Minimal API",
        "version": "1.0.0",
    },
    "paths": {
        "/hello": {
            "get": {
                "summary": "Returns a greeting",
                "responses": {
                    "200": {
                        "description": "Successful response",
                    }
                },
            }
        }
    },
}


@pytest.fixture
def minimal_spec(tmp_path: Path) -> str:
    spec_file = tmp_path / "spec.json"
    spec_file.write_text(json.dumps(MINIMAL_OPENAPI_SPEC))
    return str(spec_file.resolve())


def test_single_endpoint_uncovered(capsys, minimal_spec: str):
    # Arrange
    recorder = InMemoryRecorder()

    # Act
    coverage = Coverage(openapi_file_path=minimal_spec)
    coverage.load(recorder)
    reporter = TerminalReporter(coverage)
    reporter.create()

    # Assert
    captured = capsys.readouterr()
    assert captured.out == dedent(
        """
        Covered operations/responses:
            None

        Uncovered operations/responses:
            GET /hello returns 200

        """
    )


def test_single_endpoint_covered(capsys, minimal_spec: str, httpserver: HTTPServer):
    # Arrange
    httpserver.expect_request("/hello").respond_with_json({}, 200)
    session = requests.Session()
    recorder = InMemoryRecorder()
    # recorder = SQLiteRecorder(str(Path(minimal_spec).parent / "requests.db"))
    adapter = RecordingHTTPAdapter(recorder=recorder)
    session.mount(httpserver.url_for(""), adapter)

    # Act
    session.get(httpserver.url_for("/hello"))
    coverage = Coverage(openapi_file_path=minimal_spec)
    coverage.load(recorder)
    reporter = TerminalReporter(coverage)
    reporter.create()

    # Assert
    captured = capsys.readouterr()
    assert captured.out == dedent(
        """
        Covered operations/responses:
            GET /hello returns 200

        Uncovered operations/responses:
            None

        """
    )
