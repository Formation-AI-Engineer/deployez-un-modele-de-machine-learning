"""Unit tests — prediction service (inference + persistence)."""

from app.services import prediction as service


def test_load_model_returns_singleton():
    a = service.load_model()
    b = service.load_model()
    assert a is b


def test_predict_returns_expected_shape(sample_input):
    result = service.predict(sample_input)
    assert set(result) == {
        "prediction",
        "probability",
        "risk_level",
        "threshold",
        "model_version",
    }
    assert result["prediction"] in ("Oui", "Non")
    assert 0.0 <= result["probability"] <= 1.0
    assert result["risk_level"] in ("faible", "modéré", "élevé")
    assert result["threshold"] == service.THRESHOLD
    assert result["model_version"] == service.MODEL_VERSION


def test_predict_risk_level_consistent_with_probability(sample_input):
    result = service.predict(sample_input)
    p = result["probability"]
    if p < 0.3:
        assert result["risk_level"] == "faible"
    elif p < 0.6:
        assert result["risk_level"] == "modéré"
    else:
        assert result["risk_level"] == "élevé"


def test_predict_decision_threshold(sample_input):
    result = service.predict(sample_input)
    assert (result["probability"] >= service.THRESHOLD) == (result["prediction"] == "Oui")


def test_get_model_info_shape():
    info = service.get_model_info()
    assert {"model_name", "model_version", "algorithm", "features_count", "target"} <= set(info)
    assert info["features_count"] > 0


def test_predict_and_record_persists(db_session, sample_input):
    result = service.predict_and_record(sample_input, db_session)
    assert "prediction_id" in result
    assert "timestamp" in result

    from db.models import Prediction

    rows = db_session.query(Prediction).all()
    assert len(rows) == 1
    row = rows[0]
    assert row.id == result["prediction_id"]
    assert row.prediction == result["prediction"]
    assert row.age == sample_input["age"]


def test_predict_by_employee_id_unknown_returns_none(db_session):
    assert service.predict_by_employee_id(db_session, id_employee=999999) is None


def test_predict_by_employee_id_records_prediction(db_session, sample_employee):
    result = service.predict_by_employee_id(db_session, sample_employee.id_employee)
    assert result is not None
    assert result["id_employee"] == sample_employee.id_employee
    assert "prediction_id" in result

    from db.models import Prediction

    assert db_session.query(Prediction).count() == 1
