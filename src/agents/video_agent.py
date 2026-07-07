"""
JITSE Multi-Agent System — Video Agent (Multimodal).
"""
import json
from src.agents.base_agent import BaseAgent
from src.knowledge.jks_engine import jks_engine_instance

class VideoAgent(BaseAgent):
    """
    Agent spécialisé dans l'analyse de vidéos de présentation.
    (Computer Vision / Audio / NLP)
    """
    
    @property
    def agent_id(self) -> str:
        return "video-agent"
        
    @property
    def system_prompt(self) -> str:
        return (
            "Tu es l'Agent Vidéo de JITSE. Ton objectif est d'analyser la vidéo "
            "de présentation d'un prestataire. Tu dois évaluer le niveau de professionnalisme, "
            "la cohérence du discours et la maîtrise déclarée des compétences techniques. "
            "Sois permissif sur la qualité visuelle de la vidéo (souvent réalisée "
            "au smartphone), mais très attentif à l'assurance et à la cohérence du propos."
        )

    async def analyze_video(self, profession_category: str, video_url: str) -> dict:
        """
        Extrait les caractéristiques de la vidéo (Transcription, Émotion, Professionnalisme)
        via des modèles spécialisés d'IA.
        """
        if not video_url:
            return {"score": 0.0, "has_video": False, "transcription": ""}
            
        context = jks_engine_instance.get_evaluation_context(profession_category)
        
        prompt = f"""
        Metier ciblé: {context['profession']}
        
        Analyse la vidéo pour détecter:
        1. Le niveau de confiance en soi (Confiance dans le discours).
        2. Les mots clés techniques cités (doivent être en lien avec: {context['group']}).
        3. Le professionnalisme global de l'attitude.
        
        La qualité vidéo et audio peut être basique. Ne pénalise pas un bruit de fond, 
        du moment que le discours reste clair.
        """
        
        # En production :
        # - Extraction Audio -> Whisper pour la transcription (gère FR, EN, Pidgin)
        # - Keyframe extraction -> Vision Model pour l'analyse visuelle
        # - Agent LLM -> Combine Transcription + Meta Visuels pour le score final.
        await self.execute(prompt=prompt)
        
        return {
            "score": 80.0,
            "has_video": True,
            "transcription": "Bonjour, je m'appelle Paul, je suis menuisier depuis 10 ans et je fabrique des meubles sur mesure...",
            "detailed_analysis": "Le prestataire s'exprime clairement et utilise un vocabulaire technique adéquat."
        }
