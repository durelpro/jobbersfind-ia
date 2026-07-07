"""
JITSE API — DTOs (Data Transfer Objects) pour les requêtes et réponses.

Ces modèles Pydantic servent à valider les données envoyées par le client.
"""
from pydantic import BaseModel, Field
from typing import List, Optional

class MediaAssetDTO(BaseModel):
    id: str
    url: str
    media_type: str
    mime_type: str
    size_bytes: int

class ProfileDataDTO(BaseModel):
    description: str = ""
    years_of_experience: int = 0
    location: str = ""
    services_offered: List[str] = []
    declared_skills: List[str] = []
    languages: List[str] = []

class DossierSubmissionRequest(BaseModel):
    """
    Payload reçu lors d'une demande d'analyse de dossier par JITSE.
    """
    dossier_id: str
    provider_id: str
    profession_category: str
    profile: ProfileDataDTO
    presentation_video: Optional[MediaAssetDTO] = None
    portfolio_images: List[MediaAssetDTO] = []
    documents: List[MediaAssetDTO] = []

class TrustPassportResponse(BaseModel):
    """
    Réponse formatée du passeport de confiance.
    """
    provider_id: str
    profession_category: str
    trust_score: float
    trust_level: str
    skill_evidence_score: float
    evidence_index: float
    profile_quality_score: float
    fraud_risk_index: float
    fraud_risk_level: str
    ai_confidence_level: str
    ai_recommendation: str
    analyzed_realizations_count: int
