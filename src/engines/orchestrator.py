"""
JITSE Master Orchestrator — Le cœur qui relie tous les moteurs.

Référence : ia.md — Volume 1, Partie 3
Le flux d'analyse complet.
"""
from src.domain.models.dossier import Dossier
from src.engines.portfolio.engine import PortfolioIntelligenceEngine
from src.engines.video.engine import VideoIntelligenceEngine
from src.engines.profile.engine import ProfileIntelligenceEngine
from src.engines.document.engine import DocumentVerificationEngine
from src.engines.cross_validation.engine import CrossValidationEngine
from src.engines.scoring.engine import TrustScoringEngine
from src.engines.explainability.engine import ExplainabilityEngine
from src.domain.models.trust_passport import TrustPassport


class JITSEOrchestrator:
    """
    Haut niveau de contrôle pour lancer le workflow d'analyse IA.
    """
    def __init__(self):
        self.portfolio_engine = PortfolioIntelligenceEngine()
        self.video_engine = VideoIntelligenceEngine()
        self.profile_engine = ProfileIntelligenceEngine()
        self.document_engine = DocumentVerificationEngine()
        self.cross_val_engine = CrossValidationEngine()
        self.scoring_engine = TrustScoringEngine()
        self.explainability_engine = ExplainabilityEngine()

    async def analyze_provider_dossier(self, dossier: Dossier) -> TrustPassport:
        """
        Analyse complète d'un dossier et génération du passeport.
        """
        # 1. Lancement des analyses en parallèle (simulé par un await séquentiel pour l'instant)
        portfolio_report = await self.portfolio_engine.analyze(dossier)
        video_report = await self.video_engine.analyze(dossier)
        profile_report = await self.profile_engine.analyze(dossier)
        document_report = await self.document_engine.analyze(dossier)
        
        # 2. Validation croisée
        cross_val_report = await self.cross_val_engine.analyze(dossier)

        # 3. Calcul du passeport (Trust Scoring Engine)
        scoring_report = self.scoring_engine.compute_final_passport(
            dossier=dossier,
            raw_portfolio_score=portfolio_report.portfolio_quality_score,
            raw_video_score=video_report.professionalism_score,
            raw_profile_score=profile_report.quality_score,
            raw_coherence_score=cross_val_report.coherence_score,
            raw_document_bonus=document_report.document_bonus_score,
            inconsistencies_count=cross_val_report.inconsistencies_count,
            has_ai_generated=portfolio_report.ai_generated_detected,
            has_stolen_images=portfolio_report.stolen_images_detected,
            has_mismatch_category=cross_val_report.has_mismatch_category
        )
        passport = scoring_report.passport

        # 4. Génération de l'explicabilité
        exp_report = self.explainability_engine.generate_explanation(passport)
        passport.ai_recommendation = exp_report.recommendation
        passport.ai_explanation = exp_report.explanation

        return passport
