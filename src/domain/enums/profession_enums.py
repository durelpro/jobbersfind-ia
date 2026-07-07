"""
JITSE Profession Enums — Catégories de métiers et niveaux de compétence.

Référence : ia.md — Volume 1, Partie 2 (section 2) et Partie 4 (section 6)

Le Cameroun possède un marché des services extrêmement dynamique.
L'IA adapte automatiquement la pondération selon le métier.
Cette classification est extensible pour de nouveaux métiers.
"""

from enum import Enum


class ProfessionCategory(str, Enum):
    """
    Catégories de professions disponibles sur JobbersFind.

    Référence : ia.md lignes 320-348 (métiers du marché camerounais)
    et lignes 3041-3082 (ontologie des métiers Volume 3.5)

    Organisation hiérarchique :
    ┌────────────────────────────┐
    │  CONSTRUCTION              │
    │  ├── Maçon                 │
    │  ├── Carreleur             │
    │  ├── Coffreur              │
    │  ├── Ferrailleur           │
    │  ├── Charpentier           │
    │  └── Peintre               │
    ├────────────────────────────┤
    │  INSTALLATION              │
    │  ├── Plombier              │
    │  ├── Électricien           │
    │  ├── Frigoriste            │
    │  └── Soudeur               │
    ├────────────────────────────┤
    │  ARTISANAT                 │
    │  ├── Menuisier             │
    │  ├── Couturier             │
    │  └── Décorateur            │
    ├────────────────────────────┤
    │  ESTHÉTIQUE                │
    │  ├── Coiffeur              │
    │  └── Esthéticienne         │
    ├────────────────────────────┤
    │  TECHNOLOGIE               │
    │  ├── Développeur Web       │
    │  ├── Développeur Mobile    │
    │  ├── Graphiste             │
    │  ├── Designer UI/UX        │
    │  ├── Informaticien         │
    │  ├── Réparateur smartphone │
    │  └── Technicien réseau     │
    ├────────────────────────────┤
    │  MÉDIA                     │
    │  ├── Photographe           │
    │  └── Vidéaste              │
    ├────────────────────────────┤
    │  MÉCANIQUE                 │
    │  └── Mécanicien            │
    ├────────────────────────────┤
    │  SERVICES                  │
    │  ├── Agent d'entretien     │
    │  ├── Architecte            │
    │  └── Professeur            │
    └────────────────────────────┘
    """
    # -- Construction --
    MASON = "mason"                           # Maçon
    TILER = "tiler"                           # Carreleur
    FORM_WORKER = "form_worker"               # Coffreur
    STEEL_FIXER = "steel_fixer"               # Ferrailleur
    CARPENTER_ROOF = "carpenter_roof"         # Charpentier
    PAINTER = "painter"                       # Peintre

    # -- Installation --
    PLUMBER = "plumber"                       # Plombier
    ELECTRICIAN = "electrician"               # Électricien
    HVAC_TECHNICIAN = "hvac_technician"       # Frigoriste
    WELDER = "welder"                         # Soudeur

    # -- Artisanat --
    CARPENTER = "carpenter"                   # Menuisier
    TAILOR = "tailor"                         # Couturier
    DECORATOR = "decorator"                   # Décorateur

    # -- Esthétique --
    HAIRDRESSER = "hairdresser"               # Coiffeur
    BEAUTICIAN = "beautician"                 # Esthéticien(ne)

    # -- Technologie --
    WEB_DEVELOPER = "web_developer"           # Développeur Web
    MOBILE_DEVELOPER = "mobile_developer"     # Développeur Mobile
    GRAPHIC_DESIGNER = "graphic_designer"     # Graphiste
    UI_UX_DESIGNER = "ui_ux_designer"         # Designer UI/UX
    IT_TECHNICIAN = "it_technician"           # Informaticien
    PHONE_REPAIR = "phone_repair"             # Réparateur smartphone
    NETWORK_TECHNICIAN = "network_technician" # Technicien réseau

    # -- Média --
    PHOTOGRAPHER = "photographer"             # Photographe
    VIDEOGRAPHER = "videographer"             # Vidéaste

    # -- Mécanique --
    MECHANIC = "mechanic"                     # Mécanicien

    # -- Services --
    CLEANING_AGENT = "cleaning_agent"         # Agent d'entretien
    ARCHITECT = "architect"                   # Architecte
    TEACHER = "teacher"                       # Professeur

    # -- Générique (fallback) --
    OTHER = "other"                           # Autre métier non classifié


class ProfessionGroup(str, Enum):
    """
    Groupes de professions pour la pondération.

    Chaque groupe partage des caractéristiques d'évaluation similaires.
    Permet de regrouper les metiers ayant des critères visuels proches.
    """
    CONSTRUCTION = "construction"
    INSTALLATION = "installation"
    CRAFTSMANSHIP = "craftsmanship"
    AESTHETICS = "aesthetics"
    TECHNOLOGY = "technology"
    MEDIA = "media"
    MECHANICS = "mechanics"
    SERVICES = "services"
    OTHER = "other"


class SkillLevel(str, Enum):
    """
    Niveaux de compétence observables.

    Référence : ia.md lignes 3178-3196 (Volume 3.5)

    IMPORTANT : Ces niveaux ne sont JAMAIS une vérité absolue.
    Ils sont toujours présentés comme une estimation basée sur
    les preuves disponibles.

    ┌─────────────────────────────────────────────────────┐
    │  Débutant       → Travaux simples, peu de finition  │
    │  Intermédiaire  → Travaux corrects, finition moyenne│
    │  Professionnel  → Travaux de qualité, bonne finition│
    │  Expert         → Excellence technique visible       │
    │  Maître Artisan → Réalisations exceptionnelles       │
    └─────────────────────────────────────────────────────┘
    """
    BEGINNER = "beginner"               # Débutant
    INTERMEDIATE = "intermediate"       # Intermédiaire
    PROFESSIONAL = "professional"       # Professionnel
    EXPERT = "expert"                   # Expert
    MASTER_ARTISAN = "master_artisan"   # Maître Artisan

    @staticmethod
    def from_score(score: float) -> "SkillLevel":
        """
        Estime le niveau de compétence à partir d'un score (0-100).

        Args:
            score: Skill Evidence Score entre 0 et 100

        Returns:
            SkillLevel estimé
        """
        if not 0 <= score <= 100:
            raise ValueError(
                f"Le score doit être entre 0 et 100, reçu : {score}"
            )
        if score <= 20:
            return SkillLevel.BEGINNER
        if score <= 45:
            return SkillLevel.INTERMEDIATE
        if score <= 70:
            return SkillLevel.PROFESSIONAL
        if score <= 90:
            return SkillLevel.EXPERT
        return SkillLevel.MASTER_ARTISAN
