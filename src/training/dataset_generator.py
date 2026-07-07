"""
JITSE AI Training — Dataset Generator Framework.

Ce script sert à synthétiser / manipuler les datasets nécessaires à l'entraînement
et au benchmark des modèles sur les spécificités du marché camerounais.
"""
import json
from dataclasses import asdict
from typing import List, Dict

from src.knowledge.jks_engine import jks_engine_instance
from src.knowledge.ontology import ProfessionKnowledge

class SyntheticDatasetGenerator:
    """
    Générateur de données structurées pour Fine-Tuning ou Evaluation
    basé sur l'ontologie des métiers du JKS.
    """
    
    def __init__(self):
        self.ontology = jks_engine_instance.ontology
        
    def generate_evaluation_prompts(self, profession_id: str, num_samples: int = 10) -> List[Dict]:
        """
        Génère des échantillons DPO (Direct Preference Optimization)
        ou des Prompts de benchmark pour un métier donné.
        """
        profession: ProfessionKnowledge = self.ontology.get_profession(profession_id)
        
        dataset = []
        for i in range(num_samples):
            # Simulation d'un cas positif et négatif pour le dataset
            dataset.append({
                "instruction": f"Analyse le portfolio de ce {profession.name_fr}. {profession.description}",
                "input_images_context": f"Images from a smartphone camera. Scene 1, Scene 2.",
                "expected_positive_analysis": f"Le portfolio valide les critères : {[c.name for c in profession.visual_criteria]}.",
                "expected_fraud_flags": profession.common_frauds[0] if profession.common_frauds else "Aucune fraude."
            })
            
        return dataset

    def export_to_jsonl(self, filepath: str):
        """Exporte l'ensemble des cas générés dans un format prêt pour le Fine-Tuning."""
        all_data = []
        for prof_id in self.ontology.professions.keys():
            all_data.extend(self.generate_evaluation_prompts(prof_id, 2))
            
        # Pour des raisons de simulation on n'écrit pas réellement de gros fichiers ici
        print(f"Dataset de {len(all_data)} exemples prêt à être écrit dans {filepath}")
        return all_data
