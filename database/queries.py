from typing import List


class Query:
    @staticmethod
    def select(columns: List[str], table: str) -> str:
        return f"SELECT {', '.join(columns)} FROM {table}"
