"""
JITSE Profile Intelligence Engine — Moteur NLP pour l'analyse des textes.
"""
from dataclasses import dataclass
from typing import Any

from src.domain.interfaces.engine import ITrustEngineComponent, IEngineAnalysisReport
from src.domain.models.dossier import Dossier

@dataclass
class ProfileAnalysisReport(IEngineAnalysisReport):
    quality_score: float
    confidence: float
    is_success: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "quality_score": self.quality_score,
            "confidence": self.confidence
        }
        
    @property
    def engine_confidence(self) -> float:
        return self.confidence

    @property
    def is_usable(self) -> bool:
        return self.is_success


class ProfileIntelligenceEngine(ITrustEngineComponent[ProfileAnalysisReport]):
    """
    Analyse les textes déclaratifs du profil (NLP).
    """
    @property
    def engine_name(self) -> str:
        return "ProfileIntelligenceEngine"

    async def analyze(self, dossier: Dossier) -> ProfileAnalysisReport:
        score = 0.0
        if len(dossier.profile.description) > 50:
            score += 40.0
        if dossier.profile.services_offered:
            score += 30.0
        if dossier.profile.years_of_experience > 0:
            score += 30.0
            
        return ProfileAnalysisReport(
            quality_score=min(100.0, score),
            confidence=95.0,
            is_success=True
        )
