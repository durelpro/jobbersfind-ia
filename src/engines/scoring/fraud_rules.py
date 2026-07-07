"""
JITSE Fraud Detection — Rule Engine.

Ce module contient les règles spécifiques pour identifier la fraude
lors de la soumission de preuves.
"""
from dataclasses import dataclass
from typing import List, Optional
from src.domain.models.dossier import Dossier

@dataclass
class FraudFlag:
    code: str
    severity: str  # "LOW", "MEDIUM", "HIGH", "CRITICAL"
    description: str
    points_penalty: float

class FraudRuleEngine:
    """
    Évalue un dossier par rapport à un ensemble de règles heuristiques et d'IA.
    Produit une liste de drapeaux (Flags) de fraude.
    """
    
    def evaluate(self, dossier: Dossier, portfolio_meta: dict, cross_val_meta: dict) -> List[FraudFlag]:
        flags: List[FraudFlag] = []
        
        # 1. Détection d'Images Générées par IA (simulé depuis les métadonnées vision)
        if portfolio_meta.get("ai_generated_detected", False):
            flags.append(
                FraudFlag(
                    code="FRD-IMG-001",
                    severity="CRITICAL",
                    description="Des images générées par intelligence artificielle (Midjourney, DALL-E, etc.) ont été détectées dans le portfolio.",
                    points_penalty=80.0
                )
            )
            
        # 2. Détection d'images volées sur Internet (Reverse Image Search)
        if portfolio_meta.get("stolen_images_detected", False):
            flags.append(
                FraudFlag(
                    code="FRD-IMG-002",
                    severity="CRITICAL",
                    description="Certaines images du portfolio ont été retrouvées sur d'autres sites internet (suspected stock/stolen photo).",
                    points_penalty=100.0
                )
            )
            
        # 3. Incohérence des métiers (Cross Validation)
        inconsistencies = cross_val_meta.get("inconsistencies_count", 0)
        if inconsistencies >= 3:
            flags.append(
                FraudFlag(
                    code="FRD-TXT-001",
                    severity="HIGH",
                    description=f"Le profil présente de nombreuses incohérences déclaratives ({inconsistencies} incohérences).",
                    points_penalty=30.0
                )
            )
            
        if cross_val_meta.get("has_mismatch_category", False):
            flags.append(
                FraudFlag(
                    code="FRD-CAT-001",
                    severity="HIGH",
                    description="Les preuves visuelles ne correspondent pas au métier déclaré.",
                    points_penalty=50.0
                )
            )

        return flags
        
    def compute_total_penalty(self, flags: List[FraudFlag]) -> float:
        """Calcule la pénalité totale (capée à 100)."""
        total = sum(f.points_penalty for f in flags)
        return min(100.0, total)
