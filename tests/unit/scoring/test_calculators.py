import pytest
from datetime import datetime

from src.domain.value_objects.weighting import DEVELOPER_WEIGHTING, MASON_WEIGHTING
from src.engines.scoring.calculators import TrustScoreCalculator, FraudRiskCalculator
from src.domain.enums.trust_enums import TrustLevel, FraudRiskLevel

def test_trust_score_calculator_base():
    """Test standard de calcul sans fraude et avec peu de doc."""
    score = TrustScoreCalculator.calculate(
        weighting=DEVELOPER_WEIGHTING,
        portfolio_score=80.0,  # 80 * 0.60 = 48
        video_score=70.0,      # 70 * 0.15 = 10.5
        coherence_score=90.0,  # 90 * 0.05 = 4.5
        profile_score=85.0,    # 85 * 0.15 = 12.75
        document_bonus_score=0.0, # 0
        fraud_penalty=0.0      # 100% conservé
    )
    # Expected base = 48 + 10.5 + 4.5 + 12.75 = 75.75
    assert score.value == 75.75
    assert score.label == "Trust Score"

def test_trust_score_document_is_only_bonus():
    """DA-001 : Un manque de document ne détruit pas le score, et le doc ajoute un bonus mathématique correct."""
    score_no_doc = TrustScoreCalculator.calculate(
        weighting=MASON_WEIGHTING,
        portfolio_score=100.0,
        video_score=100.0,
        coherence_score=100.0,
        profile_score=100.0,
        document_bonus_score=0.0,
        fraud_penalty=0.0
    )
    # Total des weights sans le doc (poids doc = 0.05 pour le maçon)
    # Donc base_score max = 0.95 * 100 = 95.0
    assert score_no_doc.value == 95.0
    
    score_with_doc = TrustScoreCalculator.calculate(
        weighting=MASON_WEIGHTING,
        portfolio_score=100.0,
        video_score=100.0,
        coherence_score=100.0,
        profile_score=100.0,
        document_bonus_score=100.0,
        fraud_penalty=0.0
    )
    assert score_with_doc.value == 100.0

def test_fraud_calculator():
    """Vérifier que la pénalité de fraude fonctionne sur des cas précis."""
    score = FraudRiskCalculator.calculate(
        inconsistencies_count=0,
        has_ai_generated_images=True,
        has_internet_stolen_images=False,
        has_mismatch_category=False
    )
    assert score.value == 60.0
    
    level = FraudRiskLevel.from_score(score.value)
    assert level == FraudRiskLevel.HIGH

def test_trust_score_penalty():
    """Vérifier que le score principal est effondré par un fort taux de fraude."""
    score = TrustScoreCalculator.calculate(
        weighting=DEVELOPER_WEIGHTING,
        portfolio_score=100.0,
        video_score=100.0,
        coherence_score=100.0,
        profile_score=100.0,
        document_bonus_score=100.0,
        fraud_penalty=80.0  # Conserve seulement 20% des points
    )
    assert score.value == 20.0
