from requests import PreparedRequest, Response

from requests_stats.recorder.base import Recording


class InMemoryRecorder:
    def __init__(self) -> None:
        self.recordings: dict[PreparedRequest, Response] = {}

    def record(self, request: PreparedRequest, response: Response) -> None:
        self.recordings[request] = response

    def load(self) -> list[Recording]:
        return [
            Recording(
                method=request.method or "",
                url=request.path_url,  # TODO: also contains params
                response_code=response.status_code,
                duration=response.elapsed.total_seconds(),
            )
            for request, response in self.recordings.items()
        ]
