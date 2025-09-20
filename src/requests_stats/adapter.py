from typing import Mapping

from requests.adapters import HTTPAdapter, Retry
from requests import PreparedRequest, Response

from requests_stats.recorder.base import Recorder, DoNothingRecorder


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
