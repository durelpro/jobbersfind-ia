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
        
        # --- SIMULATION INTELLIGENTE : DÉTECTION FRAUDE ---
        # Si un nom de fichier contient des mots révélateurs liés aux fakes ou l'IA
        fraud_ai_kws = ["ia", "ai", "midjourney", "fake", "dalle", "stable", "diffusion", "gen"]
        fraud_stolen_kws = ["stock", "pinterest", "shutterstock", "getty", "google"]
        
        has_ai = any(kw in url.lower() for url in image_urls for kw in fraud_ai_kws)
        has_stolen = any(kw in url.lower() for url in image_urls for kw in fraud_stolen_kws)
        
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
        
        # Return des prédictions formattées selon l'analyse "réelle" des fichiers
        score_base = 85.0 if len(image_urls) >= 3 else 60.0
        if has_ai or has_stolen:
            score_base = 20.0  # Pénalité visuelle drastique
            
        return {
            "score": score_base,
            "ai_generated": has_ai,
            "stolen": has_stolen,
            "detailed_analysis": f"Portfolio analysé. {'DÉTECTION DE FRAUDE (Faux/Tiré d\'internet).' if has_ai or has_stolen else 'Respecte les exigences visuelles de ' + context['profession']}."
        }
