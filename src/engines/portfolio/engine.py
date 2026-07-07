"""
JITSE Portfolio Intelligence Engine — Moteur d'analyse visuelle des réalisations.
"""
from dataclasses import dataclass
from typing import Any

from src.domain.interfaces.engine import ITrustEngineComponent, IEngineAnalysisReport
from src.domain.models.dossier import Dossier

@dataclass
class PortfolioAnalysisReport(IEngineAnalysisReport):
    portfolio_quality_score: float
    analyzed_images_count: int
    confidence: float
    is_success: bool
    ai_generated_detected: bool = False
    stolen_images_detected: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "portfolio_quality_score": self.portfolio_quality_score,
            "analyzed_images_count": self.analyzed_images_count,
            "confidence": self.confidence,
            "ai_generated_detected": self.ai_generated_detected,
            "stolen_images_detected": self.stolen_images_detected
        }
        
    @property
    def engine_confidence(self) -> float:
        return self.confidence

    @property
    def is_usable(self) -> bool:
        return self.is_success


class PortfolioIntelligenceEngine(ITrustEngineComponent[PortfolioAnalysisReport]):
    """
    Analyse les images du portfolio pour déterminer la qualité du travail.
    (Implémentation fictive pour la V1)
    """
    def __init__(self):
        from src.agents.portfolio_agent import PortfolioVisionAgent
        self.agent = PortfolioVisionAgent()

    @property
    def engine_name(self) -> str:
        return "PortfolioIntelligenceEngine"

    async def analyze(self, dossier: Dossier) -> PortfolioAnalysisReport:
        # Extraction des URLs d'images
        image_urls = [img.url for img in dossier.portfolio_images]
        
        # Appel de l'Agent intelligent au coeur du moteur
        agent_result = await self.agent.analyze_portfolio(
            profession_category=dossier.profession_category,
            image_urls=image_urls
        )
            
        return PortfolioAnalysisReport(
            portfolio_quality_score=agent_result.get("score", 0.0),
            analyzed_images_count=dossier.portfolio_size(),
            confidence=90.0 if agent_result.get("score") > 0 else 0.0,
            is_success=agent_result.get("status", "") != "failed",
            ai_generated_detected=agent_result.get("ai_generated", False),
            stolen_images_detected=agent_result.get("stolen", False)
        )
