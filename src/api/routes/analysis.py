"""
JITSE API — Endpoints pour l'analyse de dossiers.
"""
from fastapi import APIRouter, HTTPException
from src.api.schemas.dossier_dto import DossierSubmissionRequest, TrustPassportResponse
from src.domain.models.dossier import Dossier, ProfileData, MediaAsset
from src.engines.orchestrator import JITSEOrchestrator

router = APIRouter(prefix="/api/v1/analysis", tags=["Analysis"])
orchestrator = JITSEOrchestrator()

@router.post("/submit", response_model=TrustPassportResponse)
async def submit_dossier_for_analysis(request: DossierSubmissionRequest):
    """
    Soumet un dossier d'un prestataire pour analyse multimodale par JITSE.
    Retourne le TrustPassport final avec les scores et l'explicabilité.
    """
    try:
        # 1. Mapping DTO vers Domain Model (Dossier)
        domain_profile = ProfileData(
            description=request.profile.description,
            years_of_experience=request.profile.years_of_experience,
            location=request.profile.location,
            services_offered=request.profile.services_offered,
            declared_skills=request.profile.declared_skills,
            languages=request.profile.languages
        )
        
        presentation_video = None
        if request.presentation_video:
            presentation_video = MediaAsset(**request.presentation_video.model_dump())
            
        portfolio_images = [MediaAsset(**img.model_dump()) for img in request.portfolio_images]
        documents = [MediaAsset(**doc.model_dump()) for doc in request.documents]
        
        domain_dossier = Dossier(
            dossier_id=request.dossier_id,
            provider_id=request.provider_id,
            profession_category=request.profession_category,
            profile=domain_profile,
            presentation_video=presentation_video,
            portfolio_images=portfolio_images,
            documents=documents
        )

        # 2. Exécution de l'orchestrateur IA JITSE
        passport = await orchestrator.analyze_provider_dossier(domain_dossier)
        
        # 3. Retour de la réponse (mapping du passeport)
        return TrustPassportResponse(
            provider_id=passport.provider_id,
            profession_category=passport.profession_category,
            trust_score=passport.trust_score,
            trust_level=passport.trust_level.value,
            skill_evidence_score=passport.skill_evidence_score,
            evidence_index=passport.evidence_index,
            profile_quality_score=passport.profile_quality_score,
            fraud_risk_index=passport.fraud_risk_index,
            fraud_risk_level=passport.fraud_risk_level.value,
            ai_confidence_level=passport.ai_confidence_level.value,
            ai_recommendation=passport.ai_recommendation,
            analyzed_realizations_count=passport.analyzed_realizations_count
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'analyse IA : {str(e)}")
