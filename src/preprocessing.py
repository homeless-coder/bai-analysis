import pandas as pd

def parse_answers_column(df: pd.DataFrame, column: str = "answers") -> pd.DataFrame:
    """Ejemplo de función para parsear una columna de respuestas."""
    # Implementación de ejemplo: separa respuestas por comas
    df[column] = df[column].astype(str).str.split(',')
    return df

def expand_bai_answers(df: pd.DataFrame, column: str = "answers") -> pd.DataFrame:
    """Ejemplo de función para expandir respuestas BAI."""
    # Implementación de ejemplo: crea columnas dummy para cada respuesta
    answers_expanded = df[column].apply(pd.Series)
    answers_expanded = answers_expanded.add_prefix(f"{column}_")
    return pd.concat([df, answers_expanded], axis=1)
