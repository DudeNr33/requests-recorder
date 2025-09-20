from requests import PreparedRequest, Response


class InMemoryRecorder:
    def __init__(self) -> None:
        self.recordings: dict[PreparedRequest, Response] = {}

    def record(self, request: PreparedRequest, response: Response) -> None:
        self.recordings[request] = response
