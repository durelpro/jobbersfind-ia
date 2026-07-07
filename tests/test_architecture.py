import pytest
import asyncio
from datetime import datetime, timezone

from src.domain.models.dossier import Dossier, ProfileData, MediaAsset
from src.domain.enums.profession_enums import ProfessionCategory
from src.engines.orchestrator import JITSEOrchestrator

@pytest.mark.asyncio
async def test_full_dossier_orchestration():
    """
    Test de validation de l'architecture fonctionnelle (Volume 1).
    Vérifie que l'orchestrateur peut coordonner les 7 moteurs et 
    produire un TrustPassport valide.
    """
    # 1. Création d'un dossier fictif
    profile = ProfileData(
        description="Maçon expérimenté, je construis des maisons depuis 10 ans.",
        years_of_experience=10,
        location="Douala",
        services_offered=["Gros oeuvre", "Fondations", "Finitions"],
        declared_skills=["Lecture de plan", "Béton armé"]
    )

    dossier = Dossier(
        dossier_id="DOS-1234",
        provider_id="PROV-5678",
        profession_category=ProfessionCategory.MASON.value,
        profile=profile,
        presentation_video=MediaAsset(id="vid_1", url="http://vid.mp4", media_type="video", mime_type="video/mp4", size_bytes=1024),
        portfolio_images=[
            MediaAsset(id="img_1", url="http://img1.jpg", media_type="image", mime_type="image/jpeg", size_bytes=100),
            MediaAsset(id="img_2", url="http://img2.jpg", media_type="image", mime_type="image/jpeg", size_bytes=100),
            MediaAsset(id="img_3", url="http://img3.jpg", media_type="image", mime_type="image/jpeg", size_bytes=100),
            MediaAsset(id="img_4", url="http://img4.jpg", media_type="image", mime_type="image/jpeg", size_bytes=100),
            MediaAsset(id="img_5", url="http://img5.jpg", media_type="image", mime_type="image/jpeg", size_bytes=100),
            MediaAsset(id="img_6", url="http://img6.jpg", media_type="image", mime_type="image/jpeg", size_bytes=100)
        ],
        documents=[]
    )

    # 2. Instanciation de l'orchestrateur
    orchestrator = JITSEOrchestrator()

    # 3. Analyse
    passport = await orchestrator.analyze_provider_dossier(dossier)

    # 4. Assertions de base
    assert passport is not None
    assert passport.provider_id == "PROV-5678"
    assert passport.profession_category == "mason"
    
    # Vérification des scores (les valeurs exactes dépendent de nos moteurs fictifs)
    assert 0 <= passport.trust_score <= 100
    assert 0 <= passport.skill_evidence_score <= 100
    assert passport.ai_recommendation != ""
    assert passport.ai_explanation != ""

    print(f"\n--- PASSPORT FINAL ---")
    print(f"Trust Score: {passport.trust_score}")
    print(f"Confiance IA: {passport.ai_confidence_level.value}")
    print(f"Recommandation: {passport.ai_recommendation}")
    print(f"Explication: {passport.ai_explanation}")
