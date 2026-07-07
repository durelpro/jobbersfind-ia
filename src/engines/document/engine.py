"""
JITSE Document Verification Engine — Moteur d'analyse des documents d'appui (Bonus).
"""
from dataclasses import dataclass
from typing import Any

from src.domain.interfaces.engine import ITrustEngineComponent, IEngineAnalysisReport
from src.domain.models.dossier import Dossier

@dataclass
class DocumentAnalysisReport(IEngineAnalysisReport):
    document_bonus_score: float
    confidence: float
    is_success: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "document_bonus_score": self.document_bonus_score,
            "confidence": self.confidence
        }
        
    @property
    def engine_confidence(self) -> float:
        return self.confidence

    @property
    def is_usable(self) -> bool:
        return self.is_success


class DocumentVerificationEngine(ITrustEngineComponent[DocumentAnalysisReport]):
    """
    Analyse les documents d'appui (certificats, CNI, etc.)
    A noter que ce moteur apporte uniquement un bonus et non un malus s'ils sont absents.
    """
    @property
    def engine_name(self) -> str:
        return "DocumentVerificationEngine"

    async def analyze(self, dossier: Dossier) -> DocumentAnalysisReport:
        score = 0.0
        doc_count = len(dossier.documents)
        if doc_count > 0:
            score = min(100.0, doc_count * 25.0)  # max 100
            
        return DocumentAnalysisReport(
            document_bonus_score=score,
            confidence=85.0 if doc_count > 0 else 0.0,
            is_success=True
        )
