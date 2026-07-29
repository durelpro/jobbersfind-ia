import sys
from pathlib import Path

# Ajoute le dossier racine du projet au path Python pour charger 'src'
file_dir = Path(__file__).resolve().parent
root_dir = file_dir.parent
sys.path.append(str(root_dir))

# Import de l'application FastAPI principale
from src.api.main import app

# Vercel utilise cette variable 'app' comme point d'entrée ASGI