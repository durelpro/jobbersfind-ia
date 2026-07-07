"""
JITSE Explainability Engine — Moteur d'explication (Explainable AI - XAI).
"""
from dataclasses import dataclass
from typing import Any

from src.domain.interfaces.engine import ITrustEngineComponent, IEngineAnalysisReport
from src.domain.models.dossier import Dossier
from src.domain.models.trust_passport import TrustPassport

@dataclass
class ExplainabilityReport(IEngineAnalysisReport):
    recommendation: str
    explanation: str
    confidence: float
    is_success: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "recommendation": self.recommendation,
            "explanation": self.explanation,
            "confidence": self.confidence
        }
        
    @property
    def engine_confidence(self) -> float:
        return self.confidence

    @property
    def is_usable(self) -> bool:
        return self.is_success


class ExplainabilityEngine:
    """
    Ce moteur ne respecte pas strictement l'interface ITrustEngineComponent classique,
    car il prend en entrée le TrustPassport et non (ou en plus de) le Dossier.
    """
    
    @property
    def engine_name(self) -> str:
        return "ExplainabilityEngine"

    def generate_explanation(self, passport: TrustPassport) -> ExplainabilityReport:
        # XAI (Explainable AI) : Justification algorithmique des scores
        positive_factors = []
        improvement_areas = []

        if passport.skill_evidence_score >= 75:
            positive_factors.append("Compétences visuellement prouvées (Portfolio de haute qualité).")
            
        if passport.evidence_index >= 60:
            positive_factors.append("Excellente diversité des preuves fournies (portfolio + vidéo + docs).")
        elif passport.evidence_index < 30:
            improvement_areas.append("Manque de preuves tangibles (ajouter plus d'images ou une vidéo).")

        if passport.profile_quality_score < 50:
            improvement_areas.append("Le profil déclaratif est incomplet ou trop bref.")
        else:
            positive_factors.append("Profil déclaratif clair et bien renseigné.")

        # Construction de la recommandation globale
        if passport.trust_score >= 75:
            rec = "Prestataire hautement recommandé. Validation automatique suggérée."
        elif passport.trust_score >= 45:
            rec = "Prestataire fiable, mais des preuves additionnelles renforceraient la crédibilité."
        else:
            rec = "Prudence. Profil disposant de trop peu de preuves pour assurer une fiabilité."

        # Remplacement de l'explication par une synthèse construite
        exp_parts = ["Ce score est justifié par :"]
        for p in positive_factors:
            exp_parts.append(f"- [+] {p}")
        for i in improvement_areas:
            exp_parts.append(f"- [-] {i}")
            
        exp = "\n".join(exp_parts)
            
        if passport.fraud_risk_index > 40:
            rec = "⚠️ ALERTE : Le système a détecté un risque d'anomalie/fraude. Review manuel bloquant."
            exp += f"\n\n🚨 Risque de fraude évalué à {passport.fraud_risk_index}%. Anomalies détectées lors de la cross-validation."
            
        return ExplainabilityReport(
            recommendation=rec,
            explanation=exp,
            confidence=95.0,
            is_success=True
        )
