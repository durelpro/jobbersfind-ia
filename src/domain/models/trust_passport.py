"""
JITSE Trust Passport — Le livrable final du moteur IA.

Référence : ia.md — Volume 1, Partie 4 (section 11)

Le Trust Passport n'est pas seulement une note.
C'est un document vivant complet qui contient les 6 scores,
le niveau de confiance global, et les badges de validation.
Il évolue dans le temps au fil des nouvelles réalisations.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from src.domain.enums.trust_enums import TrustLevel, FraudRiskLevel, AIConfidenceLevel
from src.domain.value_objects.score import ScoreValue


@dataclass
class TrustPassport:
    """
    Le Trust Passport (Passeport de Confiance).

    C'est la structure de données finale que retourne l'IA après
    l'analyse complète d'un dossier.
    """
    provider_id: str                      # ID du prestataire
    profession_category: str              # Code du métier principal
    created_at: datetime                  # Date de première création
    last_analysis_at: datetime            # Date de dernière analyse IA

    # --- Les 6 indicateurs fondamentaux ---
    trust_score: float                    # Score global [0-100]
    trust_level: TrustLevel               # Niveau (ex: EXCELLENT)

    skill_evidence_score: float           # Compétence démontrée [0-100]
    evidence_index: float                 # Richesse des preuves [0-100]
    profile_quality_score: float          # Qualité du profil [0-100]

    fraud_risk_index: float               # Risque détecté [0-100]
    fraud_risk_level: FraudRiskLevel      # Niveau de risque

    ai_confidence_level: AIConfidenceLevel # Certitude de l'IA (Low/Fair/Very)
    uncertainty_score: float              # Niveau d'incertitude numérique [0-100]

    # --- Métriques factuelles ---
    analyzed_realizations_count: int = 0  # Nb de réalisations (portfolio) analysées
    validated_professions_count: int = 1  # Nb de métiers validés

    # --- Badges de validation (Bonus) ---
    badges: dict[str, bool] = field(default_factory=lambda: {
        "identity_verified": False,
        "phone_verified": False,
        "email_verified": False,
        "documents_verified": False,
        "references_verified": False,
    })

    # --- Explication (Explainable AI) ---
    ai_recommendation: str = ""           # Recommandation automatique (texte)
    ai_explanation: str = ""              # Synthèse texte ("Forces détectées...")

    def update_badge(self, badge_name: str, status: bool = True) -> None:
        """Met à jour un badge de vérification."""
        if badge_name in self.badges:
            self.badges[badge_name] = status

    def to_dict(self) -> dict:
        """Sérialisation pour l'API / Base de données."""
        return {
            "provider_id": self.provider_id,
            "profession_category": self.profession_category,
            "created_at": self.created_at.isoformat(),
            "last_analysis_at": self.last_analysis_at.isoformat(),
            "trust_score": self.trust_score,
            "trust_level": self.trust_level.value,
            "skill_evidence_score": self.skill_evidence_score,
            "evidence_index": self.evidence_index,
            "profile_quality_score": self.profile_quality_score,
            "fraud_risk_index": self.fraud_risk_index,
            "fraud_risk_level": self.fraud_risk_level.value,
            "ai_confidence_level": self.ai_confidence_level.value,
            "uncertainty_score": self.uncertainty_score,
            "analyzed_realizations_count": self.analyzed_realizations_count,
            "validated_professions_count": self.validated_professions_count,
            "badges": self.badges,
            "ai_recommendation": self.ai_recommendation,
        }
