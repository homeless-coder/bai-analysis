import pandas as pd
from pathlib import Path

def load_excel(path: str | Path, **kwargs) -> pd.DataFrame:
    """Carga un archivo Excel y retorna un DataFrame de pandas."""
    return pd.read_excel(path, **kwargs)


def load_csv(path: str | Path, **kwargs) -> pd.DataFrame:
    """Carga un archivo CSV y retorna un DataFrame de pandas."""
    return pd.read_csv(path, **kwargs)


def load_table(path: str | Path, **kwargs) -> pd.DataFrame:
    """Carga un archivo tabular soportado segun su extension."""
    path = Path(path)
    suffix = path.suffix.lower()

    if suffix in {".xlsx", ".xls"}:
        return load_excel(path, **kwargs)

    if suffix == ".csv":
        return load_csv(path, **kwargs)

    raise ValueError(f"Formato de archivo no soportado: {path.suffix}")
