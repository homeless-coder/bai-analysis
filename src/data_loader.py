import pandas as pd
from pathlib import Path

def load_excel(path: str | Path) -> pd.DataFrame:
    """Carga un archivo Excel y retorna un DataFrame de pandas."""
    return pd.read_excel(path)


def load_csv(path: str | Path, **kwargs) -> pd.DataFrame:
    """Carga un archivo CSV y retorna un DataFrame de pandas."""
    return pd.read_csv(path, **kwargs)
