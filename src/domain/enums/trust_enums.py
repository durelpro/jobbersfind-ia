"""
JITSE Trust Enums — Niveaux de confiance, risque et décisions.

Référence : ia.md — Volume 1, Partie 4 (sections 7, 8, 9)

Ces enums définissent les classifications officielles du moteur IA.
Chaque seuil est documenté et correspond exactement à la spécification.
"""

from enum import Enum


class TrustLevel(str, Enum):
    """
    Niveaux de confiance du Trust Score.

    Référence : ia.md lignes 1638-1652
    ┌─────────────┬──────────────┐
    │  Score       │  Niveau      │
    ├─────────────┼──────────────┤
    │  0–20        │  Très faible │
    │  21–40       │  Faible      │
    │  41–60       │  Moyen       │
    │  61–80       │  Bon         │
    │  81–90       │  Très bon    │
    │  91–100      │  Excellent   │
    └─────────────┴──────────────┘
    """
    VERY_LOW = "very_low"        # 0–20
    LOW = "low"                  # 21–40
    MEDIUM = "medium"            # 41–60
    GOOD = "good"                # 61–80
    VERY_GOOD = "very_good"      # 81–90
    EXCELLENT = "excellent"      # 91–100

    @staticmethod
    def from_score(score: float) -> "TrustLevel":
        """
        Convertit un score numérique (0-100) en niveau de confiance.

        Args:
            score: Score entre 0 et 100

        Returns:
            TrustLevel correspondant

        Raises:
            ValueError: Si le score est hors limites [0, 100]
        """
        if not 0 <= score <= 100:
            raise ValueError(
                f"Le score doit être entre 0 et 100, reçu : {score}"
            )
        if score <= 20:
            return TrustLevel.VERY_LOW
        if score <= 40:
            return TrustLevel.LOW
        if score <= 60:
            return TrustLevel.MEDIUM
        if score <= 80:
            return TrustLevel.GOOD
        if score <= 90:
            return TrustLevel.VERY_GOOD
        return TrustLevel.EXCELLENT


class FraudRiskLevel(str, Enum):
    """
    Niveaux de risque de fraude.

    Référence : ia.md lignes 1654-1670
    ┌───────────────┬──────────────┐
    │  Score fraude  │  Niveau      │
    ├───────────────┼──────────────┤
    │  0–15          │  Très faible │
    │  16–30         │  Faible      │
    │  31–50         │  Moyen       │
    │  51–70         │  Élevé       │
    │  >70           │  Critique    │
    └───────────────┴──────────────┘

    IMPORTANT : Ce n'est jamais un jugement sur la personne.
    Uniquement sur la cohérence et l'authenticité des preuves.
    """
    VERY_LOW = "very_low"        # 0–15
    LOW = "low"                  # 16–30
    MEDIUM = "medium"            # 31–50
    HIGH = "high"                # 51–70
    CRITICAL = "critical"        # >70

    @staticmethod
    def from_score(score: float) -> "FraudRiskLevel":
        """
        Convertit un score de risque de fraude (0-100) en niveau.

        Args:
            score: Score entre 0 et 100

        Returns:
            FraudRiskLevel correspondant

        Raises:
            ValueError: Si le score est hors limites [0, 100]
        """
        if not 0 <= score <= 100:
            raise ValueError(
                f"Le score doit être entre 0 et 100, reçu : {score}"
            )
        if score <= 15:
            return FraudRiskLevel.VERY_LOW
        if score <= 30:
            return FraudRiskLevel.LOW
        if score <= 50:
            return FraudRiskLevel.MEDIUM
        if score <= 70:
            return FraudRiskLevel.HIGH
        return FraudRiskLevel.CRITICAL


class AIConfidenceLevel(str, Enum):
    """
    Niveau de certitude de l'IA dans son analyse.

    Référence : ia.md lignes 1420-1436
    L'IA doit annoncer honnêtement son niveau de certitude.
    Cette transparence rend le système plus crédible.
    """
    VERY_CONFIDENT = "very_confident"      # L'IA dispose de preuves solides
    FAIRLY_CONFIDENT = "fairly_confident"  # Preuves suffisantes, quelques lacunes
    LOW_CONFIDENCE = "low_confidence"      # Preuves insuffisantes ou ambiguës

    @staticmethod
    def from_score(score: float) -> "AIConfidenceLevel":
        """
        Convertit un score de confiance IA (0-100) en niveau.

        Args:
            score: Score entre 0 et 100

        Returns:
            AIConfidenceLevel correspondant
        """
        if not 0 <= score <= 100:
            raise ValueError(
                f"Le score doit être entre 0 et 100, reçu : {score}"
            )
        if score >= 75:
            return AIConfidenceLevel.VERY_CONFIDENT
        if score >= 45:
            return AIConfidenceLevel.FAIRLY_CONFIDENT
        return AIConfidenceLevel.LOW_CONFIDENCE


class RecommendationType(str, Enum):
    """
    Types de recommandations automatiques du moteur.

    Référence : ia.md lignes 1672-1721
    Ces recommandations sont des AIDES à la décision,
    JAMAIS des décisions définitives.

    ┌──────────────────────────────────────────────────────────┐
    │  Trust Score 94   → APPROUVER                           │
    │  Trust Score 72   → VALIDATION MANUELLE                 │
    │  Trust Score 55   → DEMANDER DES PREUVES COMPLÉMENTAIRES│
    │  Fraud Risk 82    → SUSPENDRE ET OUVRIR REVUE ADMIN     │
    └──────────────────────────────────────────────────────────┘
    """
    APPROVE = "approve"
    APPROVE_WITH_MONITORING = "approve_with_monitoring"
    MANUAL_REVIEW = "manual_review"
    REQUEST_MORE_EVIDENCE = "request_more_evidence"
    SUSPEND_FOR_REVIEW = "suspend_for_review"
    TEMPORARY_REJECTION = "temporary_rejection"


class DecisionStatus(str, Enum):
    """
    Statut de la décision administrative finale.

    Le système IA produit une recommandation.
    L'administrateur prend la décision finale (Human-in-the-Loop).
    """
    PENDING = "pending"                    # En attente d'analyse IA
    AI_ANALYZED = "ai_analyzed"            # Analyse IA terminée
    UNDER_REVIEW = "under_review"          # En cours de revue admin
    APPROVED = "approved"                  # Approuvé par admin
    APPROVED_MONITORED = "approved_monitored"  # Approuvé sous surveillance
    MORE_EVIDENCE_NEEDED = "more_evidence_needed"  # Preuves complémentaires demandées
    SUSPENDED = "suspended"                # Dossier suspendu
    REJECTED = "rejected"                  # Rejeté temporairement
    APPEALED = "appealed"                  # Contestation en cours


class AnalysisStatus(str, Enum):
    """
    Statut du pipeline d'analyse IA.

    Référence : ia.md lignes 992-1044 (Pipeline IA)
    Chaque étape du pipeline a un statut distinct.
    """
    QUEUED = "queued"                      # En file d'attente
    PREPROCESSING = "preprocessing"        # Prétraitement en cours
    VIDEO_ANALYSIS = "video_analysis"      # Analyse vidéo en cours
    PORTFOLIO_ANALYSIS = "portfolio_analysis"  # Analyse portfolio en cours
    DOCUMENT_ANALYSIS = "document_analysis"    # Analyse documents en cours
    PROFILE_ANALYSIS = "profile_analysis"      # Analyse profil en cours
    CROSS_VALIDATION = "cross_validation"      # Croisement des preuves
    SCORING = "scoring"                        # Calcul des scores
    FRAUD_DETECTION = "fraud_detection"        # Détection de fraude
    EXPLANATION_GENERATION = "explanation_generation"  # Génération des explications
    COMPLETED = "completed"                # Analyse terminée
    FAILED = "failed"                      # Échec de l'analyse
    PARTIALLY_COMPLETED = "partially_completed"  # Analyse partielle (données manquantes)
