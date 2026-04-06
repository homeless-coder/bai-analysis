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

# Ruta para datos procesados (puedes ajustar el nombre de archivo según tu flujo)
DATA_PROCESSED = os.getenv("DATA_PROCESSED_PATH")