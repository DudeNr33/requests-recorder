import requests
from unittest.mock import MagicMock

from pytest_httpserver import HTTPServer

from requests_stats.adapter import RecordingHTTPAdapter
from requests_stats.recorder.base import Recorder


def test_no_recorder_specified(httpserver: HTTPServer):
    httpserver.expect_request("/test").respond_with_json({}, 200)
    adapter = RecordingHTTPAdapter()
    session = requests.Session()
    session.mount(httpserver.url_for("/test"), adapter)
    response = session.get(httpserver.url_for("/test"))
    assert response.status_code == 200


def test_custom_recorder(httpserver: HTTPServer):
    httpserver.expect_request("/test").respond_with_json({}, 200)
    recorder = MagicMock(spec=Recorder)
    adapter = RecordingHTTPAdapter(recorder=recorder)
    session = requests.Session()
    session.mount(httpserver.url_for("/test"), adapter)
    session.get(httpserver.url_for("/test"))
    recorder.record.assert_called_once()
