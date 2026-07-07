"""
JITSE API — Fichier principal FastAPI (Entrypoint).
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import analysis

app = FastAPI(
    title="JobbersFind AI Trust Engine (JITSE)",
    description="API du moteur d'évaluation de la fiabilité des prestataires",
    version="1.0.0"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # À configurer proprement en prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enregistrement des routeurs
app.include_router(analysis.router)
from src.api.routes import admin
app.include_router(admin.router)

@app.get("/health")
async def health_check():
    """Vérifie que l'API est saine."""
    return {"status": "ok", "service": "JITSE API"}
