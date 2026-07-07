"""
JITSE Cross-Validation Engine — Moteur de vérification de la cohérence globale.
"""
from dataclasses import dataclass
from typing import Any

from src.domain.interfaces.engine import ITrustEngineComponent, IEngineAnalysisReport
from src.domain.models.dossier import Dossier

@dataclass
class CrossValidationReport(IEngineAnalysisReport):
    coherence_score: float
    inconsistencies_count: int
    has_mismatch_category: bool
    confidence: float
    is_success: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "coherence_score": self.coherence_score,
            "inconsistencies_count": self.inconsistencies_count,
            "has_mismatch_category": self.has_mismatch_category,
            "confidence": self.confidence
        }
        
    @property
    def engine_confidence(self) -> float:
        return self.confidence

    @property
    def is_usable(self) -> bool:
        return self.is_success


class CrossValidationEngine(ITrustEngineComponent[CrossValidationReport]):
    """
    Croise les données pour vérifier les incohérences.
    """
    @property
    def engine_name(self) -> str:
        return "CrossValidationEngine"

    async def analyze(self, dossier: Dossier) -> CrossValidationReport:
        # Simulation: Par défaut on considère le dossier très cohérent
        return CrossValidationReport(
            coherence_score=95.0,
            inconsistencies_count=0,
            has_mismatch_category=False,
            confidence=90.0,
            is_success=True
        )
