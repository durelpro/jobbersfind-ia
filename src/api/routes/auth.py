"""
JITSE API — Routes de Simulation d'Authentification (IAM).

Fournit un système d'approbation asynchrone (Human-in-the-loop)
pour sécuriser l'accès au tableau de bord.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])

class AuthCredentials(BaseModel):
    email: str
    password: str

# Base de données en mémoire pour le fonctionnement Serverless
users_db = {
    # Compte Administrateur par défaut (Gère les validations)
    "admin@jobbersfind.com": {
        "password": "admin",
        "role": "admin",
        "approved": True
    }
}

@router.post("/register")
async def register(user: AuthCredentials):
    """Demande de création de compte. Nécessite une approbation Admin."""
    if user.email in users_db:
        raise HTTPException(status_code=400, detail="Un compte avec cet email existe déjà.")
    
    users_db[user.email] = {
        "password": user.password,
        "role": "user",
        "approved": False
    }
    return {"status": "pending", "message": "Compte créé ! En attente d'approbation d'un administrateur."}

@router.post("/login")
async def login(user: AuthCredentials):
    """Se connecte au dashboard. Bloque les utilisateurs non approuvés."""
    if user.email not in users_db:
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect.")
    
    db_user = users_db[user.email]
    if db_user["password"] != user.password:
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect.")
        
    if not db_user["approved"]:
        raise HTTPException(status_code=403, detail="Votre accès n'a pas encore été approuvé par l'administrateur.")
        
    return {
        "message": "Connexion réussie.",
        "session": {
            "email": user.email,
            "role": db_user["role"]
        }
    }

@router.get("/users/pending")
async def get_pending_users():
    """Génère la liste des utilisateurs en attente pour l'Admin."""
    pending = []
    for email, data in users_db.items():
        if not data["approved"]:
            pending.append({"email": email})
    return {"pending_users": pending}

@router.post("/users/approve/{email}")
async def approve_user(email: str):
    """L'Administrateur valide définitivement un compte utilisateur."""
    if email not in users_db:
        raise HTTPException(status_code=404, detail="Utilisateur inexistant.")
    
    users_db[email]["approved"] = True
    return {"status": "success", "message": f"Le compte {email} est désormais actif !"}

@router.post("/users/change-password")
async def change_password(user: AuthCredentials):
    """Permet à un utilisateur de changer son mot de passe après connexion."""
    if user.email not in users_db:
        raise HTTPException(status_code=404, detail="Utilisateur inexistant.")
    
    users_db[user.email]["password"] = user.password
    return {"status": "success", "message": "Mot de passe modifié avec succès !"}
