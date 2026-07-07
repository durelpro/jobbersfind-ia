@echo off
echo =======================================================
echo Lancement de JobbersFind Intelligent Trust Engine (JITSE)
echo =======================================================

echo Verification de l'environnement virtuel...
if not exist "venv\Scripts\activate.bat" (
    echo [INFO] Creer l'environnement virtuel avec: python -m venv venv
    echo [INFO] Puis installer les recquis: pip install -r requirements.txt
    exit /b 1
)

echo Activation de l'environnement virtuel...
call venv\Scripts\activate.bat

echo Lancement du serveur FastAPI...
uvicorn src.api.main:app --reload --host 127.0.0.1 --port 8000

pause
