"""
JITSE Domain Enums — Toutes les énumérations métier du moteur IA.

Ces enums constituent le vocabulaire partagé entre tous les moteurs.
Ils sont immuables et fortement typés.
"""

from src.domain.enums.trust_enums import (
    TrustLevel,
    FraudRiskLevel,
    AIConfidenceLevel,
    RecommendationType,
    DecisionStatus,
    AnalysisStatus,
)
from src.domain.enums.profession_enums import (
    ProfessionCategory,
    SkillLevel,
)
from src.domain.enums.evidence_enums import (
    EvidenceType,
    EvidenceQuality,
    DocumentType,
)

__all__ = [
    "TrustLevel",
    "FraudRiskLevel",
    "AIConfidenceLevel",
    "RecommendationType",
    "DecisionStatus",
    "AnalysisStatus",
    "ProfessionCategory",
    "SkillLevel",
    "EvidenceType",
    "EvidenceQuality",
    "DocumentType",
]
