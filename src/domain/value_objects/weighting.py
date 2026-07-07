"""
JITSE Weighting Value Object — Pondération dynamique par métier.

Référence : ia.md — Volume 1, Partie 4 (sections 5, 6)

Philosophie :
    "Toutes les professions ne doivent pas avoir la même pondération."
    Un photographe est jugé principalement sur son portfolio (70 %),
    tandis qu'un professeur est jugé principalement sur sa vidéo (35 %).

Pondération par défaut :
    ┌──────────────────────────────────────┐
    │  Portfolio (réalisations)    : 45 %  │
    │  Vidéo de présentation      : 25 %  │
    │  Cohérence globale          : 15 %  │
    │  Qualité du profil          : 10 %  │
    │  Documents complémentaires  : 5 %   │
    └──────────────────────────────────────┘
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class WeightingProfile:
    """
    Profil de pondération pour un métier donné.

    La somme de tous les poids DOIT être égale à 1.0 (100%).
    Chaque poids est validé dans [0.0, 1.0].

    Attributes:
        profession_code: Code du métier (ProfessionCategory.value)
        portfolio_weight: Poids des réalisations (photos)
        video_weight: Poids de la vidéo de présentation
        coherence_weight: Poids de la cohérence globale
        profile_weight: Poids de la qualité du profil
        document_weight: Poids des documents (bonus)
        label: Nom lisible du profil de pondération
    """
    profession_code: str
    portfolio_weight: float
    video_weight: float
    coherence_weight: float
    profile_weight: float
    document_weight: float
    label: str = ""

    def __post_init__(self) -> None:
        """Validation stricte : tous les poids dans [0, 1], somme = 1.0."""
        weights = [
            self.portfolio_weight,
            self.video_weight,
            self.coherence_weight,
            self.profile_weight,
            self.document_weight,
        ]
        for w in weights:
            if not 0.0 <= w <= 1.0:
                raise ValueError(
                    f"Chaque poids doit être entre 0.0 et 1.0, reçu : {w}"
                )
        total = sum(weights)
        if not (0.99 <= total <= 1.01):
            raise ValueError(
                f"La somme des poids doit être 1.0 (100%), "
                f"reçu : {total:.4f}"
            )

    def to_dict(self) -> dict[str, float]:
        """Retourne les poids sous forme de dictionnaire."""
        return {
            "portfolio": self.portfolio_weight,
            "video": self.video_weight,
            "coherence": self.coherence_weight,
            "profile": self.profile_weight,
            "document": self.document_weight,
        }


# =========================================================================
# PROFILS DE PONDÉRATION PRÉDÉFINIS
#
# Référence : ia.md lignes 1506-1627
# Chaque métier a sa propre pondération.
# L'IA adaptera automatiquement la pondération selon le métier.
# =========================================================================

DEFAULT_WEIGHTING = WeightingProfile(
    profession_code="default",
    portfolio_weight=0.45,
    video_weight=0.25,
    coherence_weight=0.15,
    profile_weight=0.10,
    document_weight=0.05,
    label="Pondération par défaut",
)

DEVELOPER_WEIGHTING = WeightingProfile(
    profession_code="web_developer",
    portfolio_weight=0.60,
    video_weight=0.15,
    coherence_weight=0.05,
    profile_weight=0.15,
    document_weight=0.05,
    label="Développeur — Portfolio priorisé",
)

MASON_WEIGHTING = WeightingProfile(
    profession_code="mason",
    portfolio_weight=0.50,
    video_weight=0.25,
    coherence_weight=0.10,
    profile_weight=0.10,
    document_weight=0.05,
    label="Maçon — Réalisations et présentation",
)

PHOTOGRAPHER_WEIGHTING = WeightingProfile(
    profession_code="photographer",
    portfolio_weight=0.70,
    video_weight=0.10,
    coherence_weight=0.05,
    profile_weight=0.10,
    document_weight=0.05,
    label="Photographe — Portfolio dominant",
)

TEACHER_WEIGHTING = WeightingProfile(
    profession_code="teacher",
    portfolio_weight=0.25,
    video_weight=0.35,
    coherence_weight=0.10,
    profile_weight=0.20,
    document_weight=0.10,
    label="Professeur — Vidéo et profil priorisés",
)

HAIRDRESSER_WEIGHTING = WeightingProfile(
    profession_code="hairdresser",
    portfolio_weight=0.55,
    video_weight=0.20,
    coherence_weight=0.10,
    profile_weight=0.10,
    document_weight=0.05,
    label="Coiffeur — Réalisations visuelles",
)

ELECTRICIAN_WEIGHTING = WeightingProfile(
    profession_code="electrician",
    portfolio_weight=0.45,
    video_weight=0.25,
    coherence_weight=0.10,
    profile_weight=0.10,
    document_weight=0.10,
    label="Électricien — Documents sécurité valorisés",
)

GRAPHIC_DESIGNER_WEIGHTING = WeightingProfile(
    profession_code="graphic_designer",
    portfolio_weight=0.65,
    video_weight=0.10,
    coherence_weight=0.05,
    profile_weight=0.15,
    document_weight=0.05,
    label="Graphiste — Portfolio créatif dominant",
)

MECHANIC_WEIGHTING = WeightingProfile(
    profession_code="mechanic",
    portfolio_weight=0.45,
    video_weight=0.25,
    coherence_weight=0.15,
    profile_weight=0.10,
    document_weight=0.05,
    label="Mécanicien — Réalisations et vidéo",
)

TAILOR_WEIGHTING = WeightingProfile(
    profession_code="tailor",
    portfolio_weight=0.60,
    video_weight=0.15,
    coherence_weight=0.10,
    profile_weight=0.10,
    document_weight=0.05,
    label="Couturier — Créations visuelles",
)

PLUMBER_WEIGHTING = WeightingProfile(
    profession_code="plumber",
    portfolio_weight=0.45,
    video_weight=0.25,
    coherence_weight=0.15,
    profile_weight=0.10,
    document_weight=0.05,
    label="Plombier — Réalisations et présentation",
)

ARCHITECT_WEIGHTING = WeightingProfile(
    profession_code="architect",
    portfolio_weight=0.50,
    video_weight=0.15,
    coherence_weight=0.10,
    profile_weight=0.10,
    document_weight=0.15,
    label="Architecte — Portfolio et documents valorisés",
)


# Registre de toutes les pondérations indexées par profession
WEIGHTING_REGISTRY: dict[str, WeightingProfile] = {
    "default": DEFAULT_WEIGHTING,
    "web_developer": DEVELOPER_WEIGHTING,
    "mobile_developer": DEVELOPER_WEIGHTING,
    "mason": MASON_WEIGHTING,
    "tiler": MASON_WEIGHTING,
    "form_worker": MASON_WEIGHTING,
    "steel_fixer": MASON_WEIGHTING,
    "carpenter_roof": MASON_WEIGHTING,
    "painter": MASON_WEIGHTING,
    "photographer": PHOTOGRAPHER_WEIGHTING,
    "videographer": PHOTOGRAPHER_WEIGHTING,
    "teacher": TEACHER_WEIGHTING,
    "hairdresser": HAIRDRESSER_WEIGHTING,
    "beautician": HAIRDRESSER_WEIGHTING,
    "electrician": ELECTRICIAN_WEIGHTING,
    "hvac_technician": ELECTRICIAN_WEIGHTING,
    "graphic_designer": GRAPHIC_DESIGNER_WEIGHTING,
    "ui_ux_designer": GRAPHIC_DESIGNER_WEIGHTING,
    "mechanic": MECHANIC_WEIGHTING,
    "tailor": TAILOR_WEIGHTING,
    "decorator": TAILOR_WEIGHTING,
    "plumber": PLUMBER_WEIGHTING,
    "welder": PLUMBER_WEIGHTING,
    "architect": ARCHITECT_WEIGHTING,
    "carpenter": MASON_WEIGHTING,
    "it_technician": DEVELOPER_WEIGHTING,
    "phone_repair": DEVELOPER_WEIGHTING,
    "network_technician": DEVELOPER_WEIGHTING,
    "cleaning_agent": DEFAULT_WEIGHTING,
    "other": DEFAULT_WEIGHTING,
}


def get_weighting_for_profession(profession_code: str) -> WeightingProfile:
    """
    Récupère le profil de pondération adapté à un métier.

    Si le métier n'est pas dans le registre, retourne la pondération
    par défaut. Ne lance jamais d'exception.

    Args:
        profession_code: Code du métier (ProfessionCategory.value)

    Returns:
        WeightingProfile adapté au métier
    """
    return WEIGHTING_REGISTRY.get(profession_code, DEFAULT_WEIGHTING)
