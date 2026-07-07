"""
JITSE Multi-Agent System — Portfolio Agent (Vision).
"""
import json
from src.agents.base_agent import BaseAgent
from src.knowledge.jks_engine import jks_engine_instance

class PortfolioVisionAgent(BaseAgent):
    """
    Agent spécialisé dans l'analyse de portfolios d'images.
    (Computer Vision / Multimodal)
    """
    
    @property
    def agent_id(self) -> str:
        return "portfolio-vision-agent"
        
    @property
    def system_prompt(self) -> str:
        return (
            "Tu es l'Agent Vision de JITSE, spécialiste de l'évaluation professionnelle "
            "en contexte africain (marché informel). Ton travail est d'analyser les images "
            "de réalisations et de noter la crédibilité et le niveau de compétence métier. "
            "Ne juge pas sur la beauté de la photo ou l'arrière-plan, mais sur la qualité de l'exécution."
        )

    async def analyze_portfolio(self, profession_category: str, image_urls: list[str]) -> dict:
        """
        Génère une analyse détaillée du portfolio en injectant les connaissances métier (JKS).
        """
        if not image_urls:
            return {"score": 0.0, "ai_generated": False, "stolen": False}
            
        # 1. Récupération du contexte via le RAG / JKS Engine
        context = jks_engine_instance.get_evaluation_context(profession_category)
        
        # 2. Construction dynamique du prompt
        prompt = f"""
        Metier ciblé: {context['profession']}
        Instructions: {context['instructions']}
        
        Cherche spécifiquement ces critères visuels:
        {json.dumps(context['visual_criteria_to_look_for'], indent=2)}
        
        Vérifie particulièrement ces patterns de fraude:
        {json.dumps(context['fraud_patterns_to_detect'], indent=2)}
        
        Effectue l'analyse sur les {len(image_urls)} images fournies.
        """
        
        # 3. Exécution (Simulée) du LLM Multimodal
        await self.execute(prompt=prompt, image_urls=image_urls)
        
        # Return des prédictions formatées (Mock)
        # En production, ce serait un parsing des résultats json structurés du LLM.
        return {
            "score": 85.0 if len(image_urls) >= 3 else 60.0,
            "ai_generated": False,
            "stolen": False,
            "detailed_analysis": f"Le portfolio respecte bien les exigences du métier de {context['profession']}."
        }
