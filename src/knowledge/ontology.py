"""
JITSE Knowledge System — Ontologie des métiers.

Structuration hiérarchique des groupes de métiers et de leurs critères
d'évaluation spécifiques pour le marché camerounais.
"""
from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class VisualCriterion:
    """Un critère visuel qu'une intelligence artificielle doit repérer dans un portfolio."""
    name: str
    description: str
    importance_weight: float  # De 0.0 à 1.0
    examples: List[str]

@dataclass
class ProfessionKnowledge:
    """La base de connaissance liée à une profession."""
    profession_id: str
    name_fr: str
    group: str
    description: str
    visual_criteria: List[VisualCriterion] = field(default_factory=list)
    common_frauds: List[str] = field(default_factory=list)
    
class JKS_Ontology:
    """
    Registre statique (ou simulé RAG) de la base de connaissances métiers.
    """
    
    def __init__(self):
        self.professions: Dict[str, ProfessionKnowledge] = {}
        self._initialize_base_ontology()
        
    def _initialize_base_ontology(self):
        # 1. Maçon
        self.professions["mason"] = ProfessionKnowledge(
            profession_id="mason",
            name_fr="Maçon",
            group="Construction",
            description="Spécialiste du gros oeuvre, fondations et élévation de murs.",
            visual_criteria=[
                VisualCriterion(
                    name="Qualité de l'alignement",
                    description="Alignement horizontal et vertical des briques/parpaings.",
                    importance_weight=0.8,
                    examples=["Murs droits", "Utilisation de fil à plomb visible"]
                ),
                VisualCriterion(
                    name="Propreté des joints",
                    description="Régularité et propreté du mortier entre les briques.",
                    importance_weight=0.6,
                    examples=["Joints lisses", "Peu de débordement de ciment"]
                )
            ],
            common_frauds=["Utilisation de photos de chantiers industriels européens trouvées sur Google Images."]
        )
        
        # 2. Développeur Web
        self.professions["web_developer"] = ProfessionKnowledge(
            profession_id="web_developer",
            name_fr="Développeur Web",
            group="Technologie",
            description="Créateur de sites web, applications et plateformes e-commerce.",
            visual_criteria=[
                VisualCriterion(
                    name="Design Rétina / UI",
                    description="Aspect moderne et espacements cohérents sur les captures d'écran.",
                    importance_weight=0.7,
                    examples=["Tableaux de bord propres", "Responsive design visible"]
                ),
                VisualCriterion(
                    name="Code Source / Déploiement",
                    description="Preuve d'un environnement Github, Vercel ou terminal.",
                    importance_weight=0.5,
                    examples=["Capture d'un IDE", "Logs de déploiement réussis"]
                )
            ],
            common_frauds=["Capture d'écran de thèmes Wordpress payants non personnalisés."]
        )
        
    def get_profession(self, profession_id: str) -> ProfessionKnowledge:
        """Récupère l'ontologie d'un métier spécifique. Retourne un métier générique si introuvable."""
        return self.professions.get(profession_id, ProfessionKnowledge(
            profession_id="other", name_fr="Autre", group="Générique", description="Métier non classifié."
        ))
