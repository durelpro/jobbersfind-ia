"""
JITSE Scoring Calculators — Algorithmes de calcul des 6 scores fondamentaux.

Référence : ia.md — Volume 1, Partie 4 (section 3)

Ce module contient les calculateurs isolés pour chaque type de score.
L'idée est de séparer la logique mathématique.
"""

from typing import List

from src.domain.value_objects.score import ScoreValue, ScoreContribution
from src.domain.value_objects.weighting import WeightingProfile


class SkillEvidenceScoreCalculator:
    """
    Calcule le Skill Evidence Score (Compétences observables).
    Référence : ia.md ligne 1341-1360
    """
    @staticmethod
    def calculate(
        portfolio_quality_score: float,
        video_professional_score: float,
    ) -> ScoreValue:
        # Poids interne pour évaluer la compétence (indépendant des poids du métier)
        # On donne très lourdement la priorité aux réalisations.
        score = (portfolio_quality_score * 0.8) + (video_professional_score * 0.2)
        
        contributions = [
            ScoreContribution("Qualité des réalisations", portfolio_quality_score * 0.8, "portfolio"),
            ScoreContribution("Présentation professionnelle", video_professional_score * 0.2, "video")
        ]
        
        return ScoreValue(
            value=score,
            label="Skill Evidence Score",
            explanation="Basé à 80% sur les réalisations et 20% sur la présentation.",
            positive_factors=tuple([c.factor_name for c in contributions if c.is_positive]),
            negative_factors=()
        )


class EvidenceIndexCalculator:
    """
    Calcule l'Evidence Index (Richesse et diversité des preuves).
    Référence : ia.md ligne 1361-1390
    """
    @staticmethod
    def calculate(
        has_video: bool,
        portfolio_count: int,
        has_before_after: bool,
        document_count: int,
    ) -> ScoreValue:
        points = 0.0
        contributions: List[ScoreContribution] = []

        # Vidéo : forte augmentation, mais pas pénalisante si absente (0%)
        if has_video:
            points += 30.0
            contributions.append(ScoreContribution("Vidéo de présentation présente", 30.0, "video"))
        
        # Portfolio : échelle algorithmique (ex. 1-2 = faible, 5+ = excellent)
        if portfolio_count >= 10:
            p_pts = 40.0
            contributions.append(ScoreContribution("Portfolio très riche (>10)", p_pts, "portfolio"))
        elif portfolio_count >= 5:
            p_pts = 25.0
            contributions.append(ScoreContribution("Portfolio conséquent", p_pts, "portfolio"))
        elif portfolio_count >= 1:
            p_pts = 10.0
            contributions.append(ScoreContribution("Quelques réalisations", p_pts, "portfolio"))
        else:
            p_pts = 0.0

        points += p_pts

        if has_before_after:
            points += 15.0
            contributions.append(ScoreContribution("Preuves Avant/Après", 15.0, "portfolio"))
            
        if document_count > 0:
            points += min(15.0, document_count * 5.0)
            contributions.append(ScoreContribution(f"Documents d'appui ({document_count})", min(15.0, document_count * 5.0), "document"))

        score = min(100.0, points)

        return ScoreValue(
            value=score,
            label="Evidence Index",
            explanation="Mesure la quantité et la diversité des informations vérifiables.",
            positive_factors=tuple([c.factor_name for c in contributions]),
            negative_factors=() if portfolio_count > 0 else ("Aucune preuve visuelle (portfolio)",)
        )


class FraudRiskCalculator:
    """
    Calcule le Fraud Risk Index (Probabilité d'incohérence).
    Référence : ia.md ligne 1407-1419
    """
    @staticmethod
    def calculate(
        inconsistencies_count: int,
        has_ai_generated_images: bool,
        has_internet_stolen_images: bool,
        has_mismatch_category: bool,
    ) -> ScoreValue:
        risk = 0.0
        contributions: List[ScoreContribution] = []

        if has_internet_stolen_images:
            risk += 80.0
            contributions.append(ScoreContribution("Images volées sur internet", 80.0, "fraud"))
            
        if has_ai_generated_images:
            risk += 60.0
            contributions.append(ScoreContribution("Images générées par IA", 60.0, "fraud"))

        if has_mismatch_category:
            risk += 40.0
            contributions.append(ScoreContribution("Incohérence majeure de métier", 40.0, "coherence"))

        risk += (inconsistencies_count * 10)
        if inconsistencies_count > 0:
            contributions.append(ScoreContribution(f"{inconsistencies_count} mineures incohérences", inconsistencies_count * 10, "coherence"))

        score = min(100.0, risk)

        return ScoreValue(
            value=score,
            label="Fraud Risk Index",
            explanation="Ce score n'est pas un jugement humain, il cible exclusivement les incohérences de preuves.",
            positive_factors=(),
            negative_factors=tuple([c.factor_name for c in contributions])
        )


class TrustScoreCalculator:
    """
    Calcule le Grand Score : le Trust Score final.
    C'est le sommet du framework qui intègre les pondérations.
    Référence : ia.md ligne 1321-1340
    """
    @staticmethod
    def calculate(
        weighting: WeightingProfile,
        portfolio_score: float,
        video_score: float,
        coherence_score: float,
        profile_score: float,
        document_bonus_score: float,
        fraud_penalty: float,
    ) -> ScoreValue:
        
        # 1. Calcul de base en fonction du métier
        base_score = (
            portfolio_score * weighting.portfolio_weight +
            video_score * weighting.video_weight +
            coherence_score * weighting.coherence_weight +
            profile_score * weighting.profile_weight
        )
        
        # 2. Ajout du bonus document (les documents ne sont JAMAIS requis pour un bon score, ils ajoutent max 5-15%)
        # On calcule le bonus en fonction du poids alloué
        bonus_points = document_bonus_score * weighting.document_weight
        
        # 3. Application du malus (fraud_risk_index)
        # Un risque de 100 enlève la moitié des points de confiance (par exemple).
        penalty_ratio = max(0.0, 1.0 - (fraud_penalty / 100.0))
        
        final_score = (base_score + bonus_points) * penalty_ratio
        
        # S'assurer que le score reste dans les limites [0, 100]
        final_score_clamped = max(0.0, min(100.0, final_score))

        return ScoreValue(
            value=final_score_clamped,
            label="Trust Score",
            explanation=f"Pondération spécifique au métier : {weighting.label}.",
            positive_factors=(), # Sera rempli par l'Explainable AI Engine
            negative_factors=()  # Sera rempli par l'Explainable AI Engine
        )
