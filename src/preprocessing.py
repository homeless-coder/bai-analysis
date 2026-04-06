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


def prepare_bai_dataset(
    df: pd.DataFrame,
    columns_to_drop: tuple[str, ...] = ("answers", "email", "name"),
) -> pd.DataFrame:
    """Elimina columnas auxiliares o sensibles del dataset final."""
    prepared_df = df.copy()
    columns_present = [column for column in columns_to_drop if column in prepared_df.columns]
    return prepared_df.drop(columns=columns_present)


def validate_bai_dataset(df: pd.DataFrame, expected_items: int = 21) -> None:
    """Valida que el dataset final tenga la estructura esperada para almacenamiento."""
    expected_bai_columns = [f"BAI_{idx}" for idx in range(1, expected_items + 1)]
    missing_columns = [column for column in expected_bai_columns if column not in df.columns]

    if missing_columns:
        raise ValueError(f"Faltan columnas BAI en el dataset final: {missing_columns}")

    forbidden_columns = [column for column in ("answers", "email", "name") if column in df.columns]
    if forbidden_columns:
        raise ValueError(f"Estas columnas debieron eliminarse antes de guardar: {forbidden_columns}")

    if df.columns.duplicated().any():
        duplicated_columns = df.columns[df.columns.duplicated()].tolist()
        raise ValueError(f"Hay columnas duplicadas en el dataset final: {duplicated_columns}")
