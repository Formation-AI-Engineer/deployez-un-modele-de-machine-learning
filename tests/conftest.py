"""Shared pytest fixtures — test DB, API client, sample payloads."""

import os
import tempfile
from pathlib import Path

# Point the app at a temp SQLite file BEFORE importing it — this way
# pydantic-settings picks up the override when `settings` is first created.
_TEST_DB = Path(tempfile.gettempdir()) / "p5_test.db"
if _TEST_DB.exists():
    _TEST_DB.unlink()
os.environ["DATABASE_URL"] = f"sqlite:///{_TEST_DB}"

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from sqlalchemy import create_engine  # noqa: E402
from sqlalchemy.orm import sessionmaker  # noqa: E402

from app.main import app  # noqa: E402
from db.models import Base, Dataset, Prediction  # noqa: E402


@pytest.fixture(scope="session")
def engine():
    """Session-scoped SQLite engine backing the test DB."""
    engine = create_engine(os.environ["DATABASE_URL"])
    Base.metadata.create_all(bind=engine)
    yield engine
    engine.dispose()
    if _TEST_DB.exists():
        _TEST_DB.unlink()


@pytest.fixture(autouse=True)
def _clean_tables(engine):
    """Wipe table rows before every test so each test starts clean."""
    with engine.begin() as conn:
        conn.execute(Prediction.__table__.delete())
        conn.execute(Dataset.__table__.delete())
    yield


@pytest.fixture
def db_session(engine):
    """Direct SQLAlchemy session for unit tests that touch the DB."""
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client():
    """FastAPI TestClient — triggers startup (model load + create_all)."""
    with TestClient(app) as c:
        yield c


@pytest.fixture
def sample_input() -> dict:
    """Valid payload for POST /predict — stable, moderate-risk profile."""
    return {
        "age": 35,
        "genre": "M",
        "revenu_mensuel": 5000,
        "nombre_experiences_precedentes": 3,
        "annee_experience_totale": 10,
        "annees_dans_l_entreprise": 5,
        "satisfaction_employee_environnement": 3,
        "satisfaction_employee_nature_travail": 3,
        "satisfaction_employee_equipe": 3,
        "satisfaction_employee_equilibre_pro_perso": 2,
        "note_evaluation_actuelle": 3,
        "note_evaluation_precedente": 3,
        "heure_supplementaires": "Non",
        "augementation_salaire_precedente": 12.0,
        "nombre_participation_pee": 2,
        "nb_formations_suivies": 3,
        "distance_domicile_travail": 10,
        "niveau_education": 3,
        "frequence_deplacement": "Occasionnel",
        "annees_depuis_la_derniere_promotion": 1,
        "statut_marital": "Marié(e)",
        "departement": "Consulting",
        "poste": "Consultant",
        "domaine_etude": "Data Science",
    }


@pytest.fixture
def sample_employee(db_session, sample_input) -> Dataset:
    """Insert a Dataset row matching sample_input, with a known id_employee."""
    employee = Dataset(
        id_employee=42,
        **sample_input,
        a_quitte_l_entreprise="Non",
    )
    db_session.add(employee)
    db_session.commit()
    db_session.refresh(employee)
    return employee
