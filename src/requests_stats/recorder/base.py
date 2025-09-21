from typing import Protocol, NamedTuple


from requests import PreparedRequest, Response


class Recording(NamedTuple):
    method: str
    url: str
    response_code: int
    duration: float


class Recorder(Protocol):
    def record(self, request: PreparedRequest, response: Response) -> None: ...
    def load(self) -> list[Recording]: ...


class DoNothingRecorder:
    def record(self, request: PreparedRequest, response: Response) -> None:
        return
