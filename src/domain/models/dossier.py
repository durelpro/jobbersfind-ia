"""
JITSE Dossier — Le conteneur d'entrée pour l'évaluation.

Référence : ia.md — Volume 1, Partie 3 (section 3)

Le moteur IA reçoit un objet "Dossier" qui regroupe
toutes les preuves fournies par le prestataire.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class MediaAsset:
    """Représente une preuve média (image, vidéo, pdf)."""
    id: str
    url: str
    media_type: str        # 'image', 'video', 'document'
    mime_type: str         # 'image/jpeg', 'video/mp4', etc.
    size_bytes: int
    metadata: dict = field(default_factory=dict)


@dataclass
class ProfileData:
    """Données du profil déclaratif fournies par le prestataire."""
    description: str = ""
    years_of_experience: int = 0
    location: str = ""
    services_offered: list[str] = field(default_factory=list)
    declared_skills: list[str] = field(default_factory=list)
    languages: list[str] = field(default_factory=list)


@dataclass
class Dossier:
    """
    Le dossier complet soumis au Trust Engine.

    Contient la vidéo (optionnelle mais forte), le portfolio (images),
    le profil déclaratif, et les documents (bonus).
    """
    dossier_id: str
    provider_id: str
    profession_category: str

    profile: ProfileData

    # -- Preuves --
    presentation_video: Optional[MediaAsset] = None
    portfolio_images: list[MediaAsset] = field(default_factory=list)
    documents: list[MediaAsset] = field(default_factory=list)

    def has_video(self) -> bool:
        """Indique si une vidéo de présentation est présente."""
        return self.presentation_video is not None

    def portfolio_size(self) -> int:
        """Nombre d'images fournies dans le portfolio."""
        return len(self.portfolio_images)

    def has_documents(self) -> bool:
        """Indique si des documents bonus ont été soumis."""
        return len(self.documents) > 0

    def get_evidence_count(self) -> int:
        """Calcule le nombre total de preuves soumises."""
        count = self.portfolio_size()
        if self.has_video():
            count += 1
        count += len(self.documents)
        return count
