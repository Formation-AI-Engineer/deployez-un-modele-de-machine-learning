"""Functional tests — GET /predictions and GET /predictions/{id}."""


def test_predictions_list_empty(client):
    response = client.get("/predictions")
    assert response.status_code == 200
    assert response.json() == []


def test_predictions_list_after_inserts(client, sample_input):
    client.post("/predict", json=sample_input)
    client.post("/predict", json=sample_input)

    response = client.get("/predictions")
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 2
    # Ordered by created_at desc — most recent first; both share same input
    assert body[0]["age"] == sample_input["age"]


def test_predictions_list_pagination(client, sample_input):
    for _ in range(3):
        client.post("/predict", json=sample_input)

    response = client.get("/predictions", params={"skip": 1, "limit": 1})
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_predictions_get_by_id(client, sample_input):
    create_response = client.post("/predict", json=sample_input)
    prediction_id = create_response.json()["prediction_id"]

    response = client.get(f"/predictions/{prediction_id}")
    assert response.status_code == 200
    body = response.json()
    assert body["id"] == prediction_id
    assert body["age"] == sample_input["age"]


def test_predictions_get_by_id_not_found(client):
    response = client.get("/predictions/999999")
    assert response.status_code == 404
    assert "trouvée" in response.json()["detail"].lower()
