"""
JITSE Decision Engine — Recommandations pour le Dashboard.

Traduit les scores complexes en états de décision actionnables.
"""
from dataclasses import dataclass
from src.domain.models.trust_passport import TrustPassport
from src.domain.enums.trust_enums import FraudRiskLevel, TrustLevel

@dataclass
class DecisionOutcome:
    status: str       # "AUTO_VALIDATED", "MANUAL_REVIEW", "AUTO_REJECTED"
    urgency: str      # "NORMAL", "HIGH"
    reason: str 
    next_steps: list[str]

class DecisionEngine:
    """
    Système qui ne calcule pas les scores mais prend les scores du passeport 
    pour déterminer l'état du dossier sur la plateforme.
    """
    
    def determine_outcome(self, passport: TrustPassport) -> DecisionOutcome:
        # 1. Rejet automatique (si on utilise le mode d'auto-rejet, rare selon nos principes)
        if passport.fraud_risk_level in [FraudRiskLevel.CRITICAL, FraudRiskLevel.HIGH]:
            return DecisionOutcome(
                status="MANUAL_REVIEW",
                urgency="HIGH",
                reason="Risque de fraude critique détecté. Nécessite une inspection visuelle immédiate.",
                next_steps=["Bloquer la publication", "Alerter la modération niveau 2"]
            )
            
        # 2. Validation avec confiance absolue
        if passport.trust_level == TrustLevel.EXCELLENT and passport.fraud_risk_index < 10:
            return DecisionOutcome(
                status="AUTO_VALIDATED",
                urgency="NORMAL",
                reason="Ensemble de preuves très robuste et cohérent, aucune fraude détectée.",
                next_steps=["Publier le profil", "Attribuer les badges de confiance"]
            )
            
        # 3. Cas nominal : Review Manuel Assisté
        return DecisionOutcome(
            status="MANUAL_REVIEW",
            urgency="NORMAL",
            reason="Score intermédiaire. Les preuves ont été rassemblées pour évaluation humaine.",
            next_steps=["Inspection rapide des images", "Validation manuelle un-clic"]
        )
