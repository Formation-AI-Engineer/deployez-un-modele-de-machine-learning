"""Unit tests — Pydantic input validation."""

import pytest
from pydantic import ValidationError

from app.schemas.prediction import PredictionInput, PredictionOutput


def test_valid_input_accepted(sample_input):
    parsed = PredictionInput(**sample_input)
    assert parsed.age == sample_input["age"]
    assert parsed.genre.value == "M"


@pytest.mark.parametrize(
    "field,value",
    [
        ("age", 17),  # below min (18)
        ("age", 66),  # above max (65)
        ("revenu_mensuel", 500),  # below min (1000)
        ("revenu_mensuel", 60000),  # above max (50000)
        ("niveau_education", 0),  # below min (1)
        ("niveau_education", 6),  # above max (5)
        ("satisfaction_employee_environnement", 5),  # above max (4)
        ("augementation_salaire_precedente", -1.0),  # below min (0)
    ],
)
def test_out_of_range_rejected(sample_input, field, value):
    sample_input[field] = value
    with pytest.raises(ValidationError):
        PredictionInput(**sample_input)


@pytest.mark.parametrize(
    "field,value",
    [
        ("genre", "X"),
        ("heure_supplementaires", "Jamais"),
        ("frequence_deplacement", "Jamais"),
        ("statut_marital", "PACS"),
        ("departement", "IT"),
        ("poste", "CEO"),
        ("domaine_etude", "Art"),
    ],
)
def test_invalid_enum_rejected(sample_input, field, value):
    sample_input[field] = value
    with pytest.raises(ValidationError):
        PredictionInput(**sample_input)


def test_missing_field_rejected(sample_input):
    sample_input.pop("age")
    with pytest.raises(ValidationError):
        PredictionInput(**sample_input)


def test_prediction_output_probability_range():
    with pytest.raises(ValidationError):
        PredictionOutput(
            prediction_id=1,
            prediction="Oui",
            probability=1.5,
            risk_level="élevé",
            threshold=0.5,
            model_version="1.0.0",
            timestamp="2026-04-17T10:00:00",
        )
