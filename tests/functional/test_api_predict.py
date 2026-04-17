"""Functional tests — POST /predict and POST /predict/employee/{id}."""

from db.models import Prediction


def test_predict_valid_input_returns_200(client, sample_input):
    response = client.post("/predict", json=sample_input)
    assert response.status_code == 200

    body = response.json()
    assert body["prediction"] in ("Oui", "Non")
    assert 0.0 <= body["probability"] <= 1.0
    assert body["risk_level"] in ("faible", "modéré", "élevé")
    assert body["model_version"]
    assert body["prediction_id"] > 0
    assert body["timestamp"]


def test_predict_invalid_input_returns_422(client, sample_input):
    sample_input["age"] = 200  # out of allowed range
    response = client.post("/predict", json=sample_input)
    assert response.status_code == 422
    assert "detail" in response.json()


def test_predict_missing_field_returns_422(client, sample_input):
    sample_input.pop("revenu_mensuel")
    response = client.post("/predict", json=sample_input)
    assert response.status_code == 422


def test_predict_invalid_enum_returns_422(client, sample_input):
    sample_input["genre"] = "Autre"
    response = client.post("/predict", json=sample_input)
    assert response.status_code == 422


def test_predict_persists_in_db(client, db_session, sample_input):
    response = client.post("/predict", json=sample_input)
    assert response.status_code == 200
    prediction_id = response.json()["prediction_id"]

    row = db_session.query(Prediction).filter_by(id=prediction_id).one()
    assert row.age == sample_input["age"]
    assert row.prediction == response.json()["prediction"]


def test_predict_by_employee_id_returns_200(client, sample_employee):
    response = client.post(f"/predict/employee/{sample_employee.id_employee}")
    assert response.status_code == 200

    body = response.json()
    assert body["id_employee"] == sample_employee.id_employee
    assert body["prediction"] in ("Oui", "Non")
    assert body["prediction_id"] > 0


def test_predict_by_employee_id_not_found(client):
    response = client.post("/predict/employee/999999")
    assert response.status_code == 404
    assert "introuvable" in response.json()["detail"].lower()


def test_predict_by_employee_id_persists(client, db_session, sample_employee):
    client.post(f"/predict/employee/{sample_employee.id_employee}")
    assert db_session.query(Prediction).count() == 1
