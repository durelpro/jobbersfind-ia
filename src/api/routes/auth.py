"""
JITSE API — Routes de Simulation d'Authentification (IAM).
"""
import re
from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])

# Configuration du hachage de mot de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthCredentials(BaseModel):
    email: EmailStr
    password: str

class PasswordChange(BaseModel):
    email: EmailStr
    old_password: str
    new_password: str

# Base de données simulée (Remplacez par PostgreSQL/Supabase en production)
users_db = {
    "admin@jobbersfind.com": {
        "password": pwd_context.hash("admin1234"),  # Mot de passe haché
        "role": "admin",
        "approved": True
    }
}

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password):
    return pwd_context.hash(password)

# --- ROUTES ---

@router.post("/register")
async def register(user: AuthCredentials):
    """Demande de création de compte. Nécessite une approbation Admin."""
    if user.email in users_db:
        raise HTTPException(status_code=400, detail="Un compte avec cet email existe déjà.")
    
    users_db[user.email] = {
        "password": hash_password(user.password),
        "role": "user",
        "approved": False
    }
    return {"status": "pending", "message": "Compte créé ! En attente d'approbation d'un administrateur."}

@router.post("/login")
async def login(user: AuthCredentials):
    """Se connecte au dashboard. Bloque les utilisateurs non approuvés."""
    db_user = users_db.get(user.email)
    
    if not db_user or not verify_password(user.password, db_user["password"]):
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
    """Génère la liste des utilisateurs en attente."""
    pending = [{"email": email} for email, data in users_db.items() if not data["approved"]]
    return {"pending_users": pending}

@router.post("/users/approve/{email}")
async def approve_user(email: str):
    """Validation d'un compte utilisateur."""
    if email not in users_db:
        raise HTTPException(status_code=404, detail="Utilisateur inexistant.")
    
    users_db[email]["approved"] = True
    return {"status": "success", "message": f"Le compte {email} est désormais actif !"}

@router.post("/users/change-password")
async def change_password(data: PasswordChange):
    """Permet à un utilisateur de changer son mot de passe en vérifiant l'ancien."""
    db_user = users_db.get(data.email)
    if not db_user or not verify_password(data.old_password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Ancien mot de passe ou email incorrect.")
    
    users_db[data.email]["password"] = hash_password(data.new_password)
    return {"status": "success", "message": "Mot de passe modifié avec succès !"}