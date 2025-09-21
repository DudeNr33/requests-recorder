from textwrap import dedent
from requests_stats.openapi.coverage import Coverage


class TerminalReporter:
    def __init__(self, coverage: Coverage) -> None:
        self.coverage = coverage

    def create(self) -> None:
        print(
            dedent(
                f"""
                Covered operations/responses:
                    {"\n\t".join(f"{x[0]} {x[1]} returns {x[2]}" for x in self.coverage.covered) if self.coverage.covered else "None"}

                Uncovered operations/responses:
                    {"\n\t".join(f"{x[0]} {x[1]} returns {x[2]}" for x in self.coverage.uncovered) if self.coverage.uncovered else "None"}
                """
            )
        )
