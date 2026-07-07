"""
JITSE API — Sécurité et authentification.

Ce module gère l'authentification entre la plateforme principale JobbersFind
et le moteur JITSE (Server-to-Server communication).
"""
import os
from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader

API_KEY_NAME = "X-JITSE-API-KEY"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def get_api_key(api_key_header: str = Security(api_key_header)):
    """
    Vérifie que la requête provient bien des serveurs de la plateforme JobbersFind.
    """
    # En production, définir la vraie clé dans les variables d'environnement
    EXPECTED_API_KEY = os.getenv("JITSE_INTERNAL_API_KEY", "dev-secret-key-1234")
    
    if not api_key_header or api_key_header != EXPECTED_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès refusé : Clé d'API JITSE invalide ou manquante."
        )
    return api_key_header
