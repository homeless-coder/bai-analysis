import ast
import json

import pandas as pd


def _parse_answers_value(value):
    """Convierte una celda de respuestas en una lista de valores."""
    if isinstance(value, list):
        return value

    if pd.isna(value):
        return []

    if isinstance(value, str):
        text = value.strip()
        if not text:
            return []

        for parser in (json.loads, ast.literal_eval):
            try:
                parsed = parser(text)
                if isinstance(parsed, list):
                    return parsed
            except (ValueError, SyntaxError, json.JSONDecodeError, TypeError):
                continue

        return [part.strip() for part in text.split(",") if part.strip()]

    return [value]


def parse_answers_column(df: pd.DataFrame, column: str = "answers") -> pd.DataFrame:
    """Parsea la columna de respuestas a listas."""
    parsed_df = df.copy()
    parsed_df[column] = parsed_df[column].apply(_parse_answers_value)
    return parsed_df


def expand_bai_answers(df: pd.DataFrame, column: str = "answers") -> pd.DataFrame:
    """Expande las respuestas BAI en columnas BAI_1 a BAI_21."""
    expanded_df = df.copy()
    answers_expanded = pd.DataFrame(expanded_df[column].tolist(), index=expanded_df.index)
    answers_expanded.columns = [f"BAI_{idx}" for idx in range(1, len(answers_expanded.columns) + 1)]
    return pd.concat([expanded_df, answers_expanded], axis=1)
