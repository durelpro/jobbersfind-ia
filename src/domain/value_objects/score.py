"""
JITSE Score Value Object — Représentation immuable d'un score.

Un score est un Value Object au sens DDD : il n'a pas d'identité propre,
seulement une valeur. Deux scores identiques sont interchangeables.

Chaque score est borné [0, 100] et porte des métadonnées :
- sa valeur numérique
- le niveau textuel correspondant
- les facteurs positifs et négatifs qui l'expliquent
- le poids de la contribution au score global
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class ScoreValue:
    """
    Valeur de score immuable avec validation.

    Un score est toujours compris entre 0.0 et 100.0.
    Le champ `weight` représente le poids de ce score dans l'agrégation.

    Attributes:
        value: Score numérique entre 0.0 et 100.0
        weight: Poids du score dans l'agrégation (0.0 à 1.0)
        label: Label lisible du score
        positive_factors: Liste des facteurs ayant augmenté le score
        negative_factors: Liste des facteurs ayant diminué le score
        explanation: Explication textuelle du score pour l'admin
    """
    value: float
    weight: float = 1.0
    label: str = ""
    positive_factors: tuple[str, ...] = field(default_factory=tuple)
    negative_factors: tuple[str, ...] = field(default_factory=tuple)
    explanation: str = ""

    def __post_init__(self) -> None:
        """Validation stricte des bornes après initialisation."""
        if not 0.0 <= self.value <= 100.0:
            raise ValueError(
                f"Le score doit être entre 0.0 et 100.0, reçu : {self.value}"
            )
        if not 0.0 <= self.weight <= 1.0:
            raise ValueError(
                f"Le poids doit être entre 0.0 et 1.0, reçu : {self.weight}"
            )

    @property
    def weighted_value(self) -> float:
        """Retourne la valeur pondérée du score."""
        return self.value * self.weight

    def with_explanation(
        self,
        explanation: str,
        positive_factors: Optional[tuple[str, ...]] = None,
        negative_factors: Optional[tuple[str, ...]] = None,
    ) -> ScoreValue:
        """
        Crée un nouveau ScoreValue avec explications ajoutées.

        Comme frozen=True, on retourne une nouvelle instance.
        """
        return ScoreValue(
            value=self.value,
            weight=self.weight,
            label=self.label,
            positive_factors=positive_factors or self.positive_factors,
            negative_factors=negative_factors or self.negative_factors,
            explanation=explanation,
        )


@dataclass(frozen=True)
class ScoreContribution:
    """
    Contribution individuelle d'un facteur à un score.

    Utilisé pour l'Explainable AI : chaque facteur montre
    exactement combien de points il a ajouté ou retiré.

    Référence : ia.md lignes 1755-1764
    Exemple :
        Portfolio : +28 points
        Cohérence vidéo / profil : +18 points
        Documents absents : -2 points
    """
    factor_name: str           # Nom du facteur (ex: "Portfolio riche")
    points: float              # Points ajoutés (+ ou -)
    category: str              # Catégorie (portfolio, video, profile, document, coherence)
    description: str = ""      # Description détaillée
    evidence_used: str = ""    # Preuve ayant servi à ce calcul

    @property
    def is_positive(self) -> bool:
        """True si ce facteur a un impact positif."""
        return self.points >= 0

    @property
    def is_negative(self) -> bool:
        """True si ce facteur a un impact négatif."""
        return self.points < 0
