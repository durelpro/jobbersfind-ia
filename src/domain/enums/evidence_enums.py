"""
JITSE Evidence Enums — Types de preuves et qualité des preuves.

Référence : ia.md — Volume 1, Partie 3 (section 4) et Partie 4 (sections 3, 4)

Philosophie fondamentale :
    "Une preuve vaut plus qu'une promesse."
    Les réalisations et leur cohérence priment sur les déclarations.

    Les documents administratifs ne sont JAMAIS éliminatoires.
    Ils servent uniquement comme BONUS de confiance.
"""

from enum import Enum


class EvidenceType(str, Enum):
    """
    Types de preuves que le prestataire peut fournir.

    Référence : ia.md lignes 536-544 (ce que le prestataire fournit)
    et lignes 3251-3283 (bibliothèque des preuves, Volume 3.5)

    Classement par force probante (du plus fort au plus faible) :
    ┌────────────────────────────────────────────┐
    │  TRÈS FORTES                               │
    │  ├── Portfolio photos (réalisations)        │
    │  ├── Avant/Après                           │
    │  ├── Vidéo de présentation                 │
    │  └── Prototype / Application live          │
    ├────────────────────────────────────────────┤
    │  FORTES                                    │
    │  ├── Site web / GitHub                     │
    │  ├── Références clients                    │
    │  └── Contrats / Factures                   │
    ├────────────────────────────────────────────┤
    │  MOYENNES                                  │
    │  ├── Plans / Schémas                       │
    │  └── Certificats / Licences               │
    ├────────────────────────────────────────────┤
    │  BONUS (jamais requis)                     │
    │  ├── Carte nationale                       │
    │  ├── Diplômes                              │
    │  └── Documents administratifs              │
    └────────────────────────────────────────────┘
    """
    # -- Preuves visuelles (très fortes) --
    PORTFOLIO_PHOTO = "portfolio_photo"         # Photo de réalisation
    BEFORE_AFTER = "before_after"               # Photo avant/après
    PRESENTATION_VIDEO = "presentation_video"   # Vidéo de présentation
    PROTOTYPE = "prototype"                     # Prototype ou application live
    WORK_IN_PROGRESS = "work_in_progress"       # Photo de travail en cours

    # -- Preuves professionnelles (fortes) --
    WEBSITE = "website"                         # Site web personnel
    GITHUB_REPO = "github_repo"                 # Dépôt GitHub
    CLIENT_REFERENCE = "client_reference"       # Référence client
    CONTRACT = "contract"                       # Contrat signé
    INVOICE = "invoice"                         # Facture

    # -- Preuves techniques (moyennes) --
    PLAN = "plan"                               # Plan / Schéma
    CERTIFICATE = "certificate"                 # Certificat professionnel
    LICENSE = "license"                         # Licence professionnelle

    # -- Documents administratifs (bonus uniquement) --
    IDENTITY_DOCUMENT = "identity_document"     # Carte nationale / Passeport
    DIPLOMA = "diploma"                         # Diplôme
    BUSINESS_REGISTER = "business_register"     # Registre de commerce
    TAX_ID = "tax_id"                           # Numéro contribuable
    TRADE_LICENSE = "trade_license"             # Patente


class EvidenceQuality(str, Enum):
    """
    Qualité d'une preuve individuelle après analyse.

    Le moteur évalue chaque preuve soumise et lui attribue
    un niveau de qualité. Cela permet de pondérer l'impact
    de chaque preuve sur le score global.
    """
    EXCELLENT = "excellent"       # Preuve très solide, claire et vérifiable
    GOOD = "good"                 # Preuve correcte, exploitable
    FAIR = "fair"                 # Preuve exploitable mais qualité limitée
    POOR = "poor"                 # Preuve difficile à exploiter (floue, coupée)
    UNUSABLE = "unusable"         # Preuve inutilisable (corrompue, trop faible)
    SUSPICIOUS = "suspicious"    # Preuve potentiellement manipulée


class DocumentType(str, Enum):
    """
    Types de documents administratifs (tous FACULTATIFS).

    Référence : ia.md lignes 870-886 (Document Verification Engine)

    DÉCISION D'ARCHITECTURE N°1 (ia.md ligne 420-425) :
    Les documents administratifs ne sont JAMAIS une condition
    d'accès à une bonne évaluation.
    Ils servent UNIQUEMENT comme BONUS de confiance.
    """
    NATIONAL_ID = "national_id"               # Carte Nationale d'Identité
    PASSPORT = "passport"                     # Passeport
    DRIVERS_LICENSE = "drivers_license"       # Permis de conduire
    ATTESTATION = "attestation"               # Attestation
    DIPLOMA = "diploma"                       # Diplôme
    BUSINESS_REGISTER = "business_register"   # Registre de commerce
    TRADE_LICENSE = "trade_license"           # Patente
    TAXPAYER_ID = "taxpayer_id"               # Numéro contribuable
    PROFESSIONAL_CARD = "professional_card"   # Carte professionnelle
    OTHER = "other"                           # Autre document
