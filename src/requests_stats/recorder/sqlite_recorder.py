import sqlite3
from urllib.parse import urlparse

from requests import PreparedRequest, Response


class SQLiteRecorder:
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
