import sys
from pathlib import Path

# Ajoute le dossier racine du projet au path Python pour pouvoir importer 'src'
file_dir = Path(__file__).resolve().parent
root_dir = file_dir.parent
sys.path.append(str(root_dir))

# Importation de votre application FastAPI principale
from src.api.main import app