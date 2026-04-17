"""Functional tests — health + meta endpoints."""


def test_root_redirects_to_docs(client):
    response = client.get("/", follow_redirects=False)
    assert response.status_code in (307, 308)
    assert response.headers["location"] == "/docs"


def test_health_returns_ok(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_model_info_shape(client):
    response = client.get("/model/info")
    assert response.status_code == 200
    body = response.json()
    assert {"model_name", "model_version", "algorithm", "features_count", "target"} <= set(body)
    assert body["features_count"] > 0
