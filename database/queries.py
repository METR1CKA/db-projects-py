from typing import List
import re


class Query:
    VALID_IDENTIFIER_REGEX = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")

    @staticmethod
    def validator(identifiers: List[str]) -> bool:
        for id in identifiers:
            if id != "*" and not Query.VALID_IDENTIFIER_REGEX.match(id):
                return False

        return True

    @staticmethod
    def select(columns: List[str], table: str) -> str:
        # Validamos los nombres de las columnas y la tabla
        if not Query.validator(columns + [table]):
            raise ValueError("Error en los nombres de las columnas o la tabla")

        return f"SELECT {', '.join(columns)} FROM {table}"
