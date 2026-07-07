"""
JITSE Knowledge System Engine (JKS Engine).

Interface RAG / Base Vectorielle pour fournir au reste du système IA
le contexte d'un métier.
"""
from src.knowledge.ontology import JKS_Ontology, ProfessionKnowledge

class JKSEngine:
    """
    Simule un agent de type Knowledge Graph / RAG.
    Le JKS Engine est interrrogé par le VideoEngine ou le PortfolioEngine
    pour comprendre "ce qu'il faut chercher" pour un métier donné.
    """
    
    def __init__(self):
        self.ontology = JKS_Ontology()
        
    def get_evaluation_context(self, profession_category: str) -> dict:
        """
        Génère un contexte structuré (prompt fragment) utilisé par les autres modèles IA
        pour savoir comment jauger la prestation de cette catégorie.
        """
        profession: ProfessionKnowledge = self.ontology.get_profession(profession_category)
        
        return {
            "profession": profession.name_fr,
            "group": profession.group,
            "instructions": f"Vous évaluez un(e) {profession.name_fr}. {profession.description}",
            "visual_criteria_to_look_for": [
                {"name": c.name, "importance": c.importance_weight, "description": c.description} 
                for c in profession.visual_criteria
            ],
            "fraud_patterns_to_detect": profession.common_frauds
        }

# Instance singleton pour le système
jks_engine_instance = JKSEngine()
