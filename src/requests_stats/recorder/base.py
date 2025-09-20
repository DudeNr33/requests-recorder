from typing import Protocol


from requests import PreparedRequest, Response


class Recorder(Protocol):
    def record(self, request: PreparedRequest, response: Response) -> None: ...


class DoNothingRecorder:
    def record(self, request: PreparedRequest, response: Response) -> None:
        return
