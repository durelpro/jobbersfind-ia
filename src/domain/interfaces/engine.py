"""
JITSE Engine Interfaces — Contrats de base pour tous les moteurs IA.

Référence : ia.md — Volume 1, Partie 3 (section 4)

Le JITSE est composé de 7 grands moteurs. Tous ces moteurs doivent
respecter une interface d'analyse commune ("contrat").
"""

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from src.domain.models.dossier import Dossier

# T = Type du rapport de sortie spécifique au moteur
T = TypeVar("T")


class IEngineAnalysisReport(ABC):
    """
    Interface de base pour les rapports d'analyse générés par les moteurs.
    Chaque moteur définit son propre format de rapport.
    """
    @abstractmethod
    def to_dict(self) -> dict[str, Any]:
        """Convertit le rapport en dictionnaire pour agrégation."""
        pass

    @property
    @abstractmethod
    def engine_confidence(self) -> float:
        """Confiance interne du moteur vis-à-vis de son analyse (0-100)."""
        pass

    @property
    @abstractmethod
    def is_usable(self) -> bool:
        """True si l'analyse a réussi et produit des données exploitables."""
        pass


class ITrustEngineComponent(ABC, Generic[T]):
    """
    Interface abstraite pour un moteur IA spécialisé.
    
    Exemples d'implémentation attendus :
    - VideoIntelligenceEngine
    - PortfolioIntelligenceEngine
    - DocumentVerificationEngine
    - etc.
    """
    
    @property
    @abstractmethod
    def engine_name(self) -> str:
        """Retourne le nom officiel du moteur."""
        pass

    @abstractmethod
    async def analyze(self, dossier: Dossier) -> T:
        """
        Exécute l'analyse spécifique au moteur sur le dossier.
        
        Args:
            dossier: Le dossier du prestataire contenant les preuves.
            
        Returns:
            Le rapport d'analyse spécifique (de type T).
        """
        pass
