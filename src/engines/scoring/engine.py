"""
JITSE Trust Scoring Engine — Orchestrateur du calcul.

Il implémente ITrustEngineComponent. Il ne regarde pas les preuves
lui-même, il compile les sous-scores de tous les autres moteurs.
(Voir ia.md Ligne 941 : "Ce moteur ne regarde plus les preuves.").
"""

from dataclasses import dataclass
from datetime import datetime, timezone
import uuid

from src.domain.interfaces.engine import ITrustEngineComponent, IEngineAnalysisReport
from src.domain.models.dossier import Dossier
from src.domain.models.trust_passport import TrustPassport
from src.domain.value_objects.weighting import get_weighting_for_profession
from src.domain.enums.trust_enums import TrustLevel, FraudRiskLevel, AIConfidenceLevel
from src.engines.scoring.calculators import (
    TrustScoreCalculator,
    SkillEvidenceScoreCalculator,
    EvidenceIndexCalculator,
    FraudRiskCalculator
)

@dataclass
class TrustScoringReport(IEngineAnalysisReport):
    """Le rapport issu du module de Scoring (contient le passeport)."""
    passport: TrustPassport
    confidence: float
    successful: bool

    def to_dict(self) -> dict:
        return self.passport.to_dict()

    @property
    def engine_confidence(self) -> float:
        return self.confidence

    @property
    def is_usable(self) -> bool:
        return self.successful


class TrustScoringEngine(ITrustEngineComponent[TrustScoringReport]):
    """
    Le moteur final de scoring.

    Il prend en entrée les résultats des 4 autres moteurs principaux:
    - resultats Vision (portfolio)
    - resultats Video
    - resultats Text (profil)
    - resultats OCR / Cross-Validation
    (Pour cette V1, on simulera ces entrées dans la méthode).
    """
    
    @property
    def engine_name(self) -> str:
        return "TrustScoringEngine"

    async def analyze(self, dossier: Dossier) -> TrustScoringReport:
        raise NotImplementedError("Utilisez 'compute_final_passport' en passant les sous-scores.")

    def compute_final_passport(
        self, 
        dossier: Dossier,
        # Sous-scores issus des autres moteurs abstraits passés en arguments:
        raw_portfolio_score: float,
        raw_video_score: float,
        raw_profile_score: float,
        raw_coherence_score: float,
        raw_document_bonus: float,
        inconsistencies_count: int,
        has_ai_generated: bool,
        has_stolen_images: bool,
        has_mismatch_category: bool,
    ) -> TrustScoringReport:
        """
        Calcule le Trust Passport. (IA.md - Lignes 941-964)
        """
        weighting = get_weighting_for_profession(dossier.profession_category)

        # 1. Calculs des index métier indépendants
        fraud_score_val = FraudRiskCalculator.calculate(
            inconsistencies_count=inconsistencies_count,
            has_ai_generated_images=has_ai_generated,
            has_internet_stolen_images=has_stolen_images,
            has_mismatch_category=has_mismatch_category
        )

        evidence_score_val = EvidenceIndexCalculator.calculate(
            has_video=dossier.has_video(),
            portfolio_count=dossier.portfolio_size(),
            has_before_after=False, # simplif.
            document_count=len(dossier.documents)
        )

        skill_score_val = SkillEvidenceScoreCalculator.calculate(
            portfolio_quality_score=raw_portfolio_score,
            video_professional_score=raw_video_score
        )

        # 2. Le Grand Trust Score.
        trust_score_val = TrustScoreCalculator.calculate(
            weighting=weighting,
            portfolio_score=raw_portfolio_score,
            video_score=raw_video_score,
            coherence_score=raw_coherence_score,
            profile_score=raw_profile_score,
            document_bonus_score=raw_document_bonus,
            fraud_penalty=fraud_score_val.value
        )
        
        # 3. Calcul de la certitude IA (si pas de fraude et pas mal de data, = High)
        ai_confidence = 100.0 - (fraud_score_val.value * 0.5)
        if evidence_score_val.value < 20: 
            ai_confidence -= 30.0
        ai_confidence_clamped = max(0.0, min(100.0, ai_confidence))

        # 4. Construction du Passport Final
        now = datetime.now(timezone.utc)
        passport = TrustPassport(
            provider_id=dossier.provider_id,
            profession_category=dossier.profession_category,
            created_at=now,
            last_analysis_at=now,
            trust_score=round(trust_score_val.value, 2),
            trust_level=TrustLevel.from_score(trust_score_val.value),
            skill_evidence_score=round(skill_score_val.value, 2),
            evidence_index=round(evidence_score_val.value, 2),
            profile_quality_score=round(raw_profile_score, 2),
            fraud_risk_index=round(fraud_score_val.value, 2),
            fraud_risk_level=FraudRiskLevel.from_score(fraud_score_val.value),
            ai_confidence_level=AIConfidenceLevel.from_score(ai_confidence_clamped),
            uncertainty_score=round(100.0 - ai_confidence_clamped, 2),
            analyzed_realizations_count=dossier.portfolio_size(),
            badges={},
        )
        
        return TrustScoringReport(
            passport=passport,
            confidence=ai_confidence_clamped,
            successful=True
        )
