"""
JITSE Multi-Agent System — Base Agent.

Définit le fonctionnement commun de tous les agents IA du système (LLM wrapper).
"""
from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseAgent(ABC):
    """
    Structure de base d'un Agent IA. 
    Il possède un nom métier, un prompt system et une méthode pour exécuter une tâche.
    """
    def __init__(self, model_name: str = "gpt-4o"):
        self.model_name = model_name

    @property
    @abstractmethod
    def agent_id(self) -> str:
        """Identifiant unique de l'agent."""
        pass
        
    @property
    @abstractmethod
    def system_prompt(self) -> str:
        """Le prompt de base qui conditionne le comportement de l'agent."""
        pass

    async def execute(self, prompt: str, image_urls: list[str] = None) -> Dict[str, Any]:
        """
        Simule l'appel à l'API du LLM (OpenAI, Anthropic, Gemini, etc.).
        Dans l'implémentation finale, ceci effectuera la vraie requête HTTP/SDK.
        """
        # Logging de simulation
        print(f"[{self.agent_id}] Analyse en cours avec le modèle {self.model_name}...")
        
        # Le code spécifique de chaque agent wrapera cet appel.
        # Retour simulé pour JITSE
        return {"status": "success", "raw_llm_output": "Analyse effectuée avec succès."}
