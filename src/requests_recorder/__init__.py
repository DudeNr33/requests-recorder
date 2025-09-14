import sqlite3
from urllib.parse import urlparse
from typing import Mapping, Protocol


from requests.adapters import HTTPAdapter, Retry
from requests import PreparedRequest, Response


class Recorder(Protocol):
    def record(self, request: PreparedRequest, response: Response) -> None: ...


class DoNothingRecorder:
    def record(self, request: PreparedRequest, response: Response) -> None:
        return


class InMemoryRequestRecorder:
    def __init__(self) -> None:
        self.recordings: dict[PreparedRequest, Response] = {}

    def record(self, request: PreparedRequest, response: Response) -> None:
        self.recordings[request] = response


class SQLiteRequestRecorder:
    def __init__(self) -> None:
        self.connection = sqlite3.connect("requests.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            "CREATE TABLE requests(host, url, params, duration, response_status)"
        )

    def record(self, request: PreparedRequest, response: Response) -> None:
        parsed = urlparse(request.url)
        self.cursor.execute(
            f"INSERT INTO requests VALUES ('{parsed.hostname}', '{parsed.path}', '{parsed.params}', {response.elapsed.total_seconds()}, {response.status_code})"
        )
        self.connection.commit()


class RecordingHTTPAdapter(HTTPAdapter):
    def __init__(
        self,
        pool_connections: int = 10,
        pool_maxsize: int = 10,
        max_retries: Retry | int | None = 0,
        pool_block: bool = False,
        recorder: Recorder = DoNothingRecorder(),
    ) -> None:
        super().__init__(pool_connections, pool_maxsize, max_retries, pool_block)
        self.recorder = recorder

    def send(
        self,
        request: PreparedRequest,
        stream: bool = False,
        timeout: None | float | tuple[float, float] | tuple[float, None] = None,
        verify: bool | str = True,
        cert: None | bytes | str | tuple[bytes | str, bytes | str] = None,
        proxies: Mapping[str, str] | None = None,
    ) -> Response:
        response = super().send(request, stream, timeout, verify, cert, proxies)
        self.recorder.record(request, response)
        return response
