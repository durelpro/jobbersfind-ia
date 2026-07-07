"""
JITSE API — Endpoints du Dashboard Administrateur (Human-in-the-Loop).

Permet aux modérateurs humains de récupérer l'explicabilité et prendre les décisions finales.
"""
from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any

from src.api.middleware.security import get_api_key

router = APIRouter(prefix="/api/v1/admin", tags=["Admin Dashboard"])

# On s'assure que cet endpoint est protégé
@router.get("/dossiers/{provider_id}/decision-support", dependencies=[Depends(get_api_key)])
async def get_dossier_decision_support(provider_id: str):
    """
    Récupère le rapport détaillé d'un dossier pour l'interface administrateur.
    Ceci permet au modérateur humain de valider ou refuser le profil.
    """
    # Logique fictive pour l'instant : en production, on récupère le TrustPassport depuis une BDD
    return {
        "provider_id": provider_id,
        "human_in_the_loop_required": True,
        "ai_flags": [
            {"type": "FRAUD_RISK", "level": "LOW", "detail": "Aucune incohérence majeure détectée"},
            {"type": "SKILL_EVIDENCE", "level": "HIGH", "detail": "Portfolio riche et pertinent (12 photos)"}
        ],
        "decision_options": [
            "VALIDATE_PROFILE",
            "REQUEST_MORE_EVIDENCE",
            "REJECT_FRAUDULEUX"
        ],
        "message": "En attente de la décision d'un administrateur certifié."
    }

@router.post("/dossiers/{provider_id}/decision", dependencies=[Depends(get_api_key)])
async def submit_human_decision(provider_id: str, decision: Dict[str, Any]):
    """
    Permet à l'administrateur d'enregistrer la décision finale.
    Le Trust Engine pourra utiliser ces feedbacks pour s'améliorer (Learning Agent).
    """
    # Par exemple decision = {"status": "VALIDATED", "admin_id": "ADM-1", "notes": "OK pour moi."}
    if "status" not in decision:
        raise HTTPException(status_code=400, detail="Le statut de la décision est manquant.")
        
    return {
        "provider_id": provider_id,
        "action": "DECISION_RECORDED",
        "final_status": decision["status"],
        "learning_feedback_sent": True
    }
