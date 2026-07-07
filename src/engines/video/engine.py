"""
JITSE Video Intelligence Engine — Moteur d'analyse comportementale (Vidéo).
"""
from dataclasses import dataclass
from typing import Any

from src.domain.interfaces.engine import ITrustEngineComponent, IEngineAnalysisReport
from src.domain.models.dossier import Dossier

@dataclass
class VideoAnalysisReport(IEngineAnalysisReport):
    professionalism_score: float
    confidence: float
    is_success: bool
    has_video: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "professionalism_score": self.professionalism_score,
            "confidence": self.confidence,
            "has_video": self.has_video
        }
        
    @property
    def engine_confidence(self) -> float:
        return self.confidence

    @property
    def is_usable(self) -> bool:
        return self.is_success


class VideoIntelligenceEngine(ITrustEngineComponent[VideoAnalysisReport]):
    """
    Analyse la vidéo de présentation pour déterminer le professionnalisme.
    """
    def __init__(self):
        from src.agents.video_agent import VideoAgent
        self.agent = VideoAgent()

    @property
    def engine_name(self) -> str:
        return "VideoIntelligenceEngine"

    async def analyze(self, dossier: Dossier) -> VideoAnalysisReport:
        has_video = dossier.has_video()
        video_url = dossier.presentation_video.url if has_video else ""
        
        # Appel de l'Agent Video
        agent_result = await self.agent.analyze_video(
            profession_category=dossier.profession_category,
            video_url=video_url
        )
        
        return VideoAnalysisReport(
            professionalism_score=agent_result.get("score", 0.0),
            confidence=90.0 if has_video else 0.0,
            is_success=agent_result.get("status", "") != "failed",
            has_video=agent_result.get("has_video", False)
        )
