from pathlib import Path
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# Ruta desde .env
BAI_DATA_PATH = os.getenv("BAI_DATA_PATH")

# Convertir a Path
BAI_DATA_PATH = BASE_DIR / BAI_DATA_PATH if BAI_DATA_PATH else None

# Directorio para datos procesados
DATA_PROCESSED_DIR = os.getenv("DATA_PROCESSED_DIR")
DATA_PROCESSED_DIR = BASE_DIR / DATA_PROCESSED_DIR if DATA_PROCESSED_DIR else None

# Rutas de datasets derivados
DATA_CLEANED = os.getenv("DATA_CLEANED_PATH")
DATA_CLEANED = (
    BASE_DIR / DATA_CLEANED
    if DATA_CLEANED
    else DATA_PROCESSED_DIR / "BAI_CLEANED.xlsx" if DATA_PROCESSED_DIR else None
)

DATA_PROCESSED = os.getenv("DATA_PROCESSED_PATH")
DATA_PROCESSED = (
    BASE_DIR / DATA_PROCESSED
    if DATA_PROCESSED
    else DATA_PROCESSED_DIR / "BAI_PROCESSED.xlsx" if DATA_PROCESSED_DIR else None
)

# Directorio para figuras generadas
OUTPUTS_FIGURES = BASE_DIR / "outputs" / "figures"
