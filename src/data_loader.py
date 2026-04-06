import pandas as pd
from pathlib import Path

def load_excel(path: str | Path) -> pd.DataFrame:
    """Carga un archivo Excel y retorna un DataFrame de pandas."""
    return pd.read_excel(path)
