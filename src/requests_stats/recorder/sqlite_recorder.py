import sqlite3
from urllib.parse import urlparse

from requests import PreparedRequest, Response

from requests_stats.recorder.base import Recording


class SQLiteRecorder:
    def __init__(self, filepath: str = "requests.db") -> None:  # TODO: make pathlike
        self.connection = sqlite3.connect(filepath)
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            "CREATE TABLE requests(method, url, params, duration, response_status)"
        )

    def record(self, request: PreparedRequest, response: Response) -> None:
        parsed = urlparse(request.url)
        self.cursor.execute(
            "INSERT INTO requests VALUES (?, ?, ?, ?, ?)",
            [
                request.method,
                parsed.path,
                parsed.params,
                response.elapsed.total_seconds(),
                response.status_code,
            ],
        )
        self.connection.commit()

    def load(self) -> list[Recording]:
        results = self.cursor.execute("SELECT * FROM requests")
        return [
            Recording(method=x[0], url=x[1], response_code=x[4], duration=x[3])
            for x in results
        ]
