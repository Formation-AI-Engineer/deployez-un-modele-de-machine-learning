"""Unit tests — SQLAlchemy ORM models (Dataset, Prediction)."""

import pytest
from sqlalchemy.exc import IntegrityError

from db.models import Dataset, Prediction


def _dataset_kwargs(sample_input, id_employee=1):
    return {
        "id_employee": id_employee,
        **sample_input,
        "a_quitte_l_entreprise": "Non",
    }


def _prediction_kwargs(sample_input):
    return {
        "model_version": "1.0.0",
        **sample_input,
        "prediction": "Non",
        "probability": 0.2,
        "risk_level": "faible",
    }


def test_dataset_insert_and_read(db_session, sample_input):
    ds = Dataset(**_dataset_kwargs(sample_input, id_employee=1))
    db_session.add(ds)
    db_session.commit()

    fetched = db_session.query(Dataset).filter_by(id_employee=1).one()
    assert fetched.age == sample_input["age"]
    assert fetched.a_quitte_l_entreprise == "Non"


def test_dataset_id_employee_unique(db_session, sample_input):
    db_session.add(Dataset(**_dataset_kwargs(sample_input, id_employee=7)))
    db_session.commit()

    db_session.add(Dataset(**_dataset_kwargs(sample_input, id_employee=7)))
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()


def test_prediction_insert_has_defaults(db_session, sample_input):
    pred = Prediction(**_prediction_kwargs(sample_input))
    db_session.add(pred)
    db_session.commit()
    db_session.refresh(pred)

    assert pred.id is not None
    assert pred.created_at is not None
    assert pred.model_version == "1.0.0"
