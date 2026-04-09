from pathlib import Path
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


def _resolve_from_env(env_var: str, default: str | None = None) -> Path | None:
    """Resuelve una ruta relativa al proyecto desde una variable de entorno."""
    value = os.getenv(env_var, default)
    return BASE_DIR / value if value else None

# Ruta desde .env
BAI_DATA_PATH = _resolve_from_env("BAI_DATA_PATH")

# Directorio para datos procesados
DATA_PROCESSED_DIR = _resolve_from_env("DATA_PROCESSED_DIR")

# Rutas de datasets derivados
DATA_CLEANED = _resolve_from_env(
    "DATA_CLEANED_PATH",
    "data/processed/BAI_CLEANED.xlsx",
)
DATA_PROCESSED = _resolve_from_env(
    "DATA_PROCESSED_PATH",
    "data/processed/BAI_PROCESSED.xlsx",
)
SYMPTOM_CORRELATIONS_PATH = _resolve_from_env(
    "SYMPTOM_CORRELATIONS_PATH",
    "data/processed/symptom_correlations.csv",
)

# Directorio para figuras generadas
OUTPUTS_FIGURES = BASE_DIR / "outputs" / "figures"
