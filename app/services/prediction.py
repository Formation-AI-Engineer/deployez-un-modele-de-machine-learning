"""Prediction service — loads model, runs inference, persists results."""

from pathlib import Path

from catboost import CatBoostClassifier
from sqlalchemy.orm import Session

from app.preprocessing import EXPECTED_FEATURES, preprocess_single
from db.models import Prediction

MODEL_VERSION = "1.0.0"
THRESHOLD = 0.5
MODEL_PATH = Path(__file__).resolve().parent.parent.parent / "models" / "catboost_attrition.cbm"

_model: CatBoostClassifier | None = None


def load_model() -> CatBoostClassifier:
    """Load the CatBoost model from disk (singleton)."""
    global _model
    if _model is None:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                f"Model file not found at {MODEL_PATH}. Run 'python scripts/train_model.py' first."
            )
        _model = CatBoostClassifier()
        _model.load_model(str(MODEL_PATH))
    return _model


def predict(data: dict) -> dict:
    """Run prediction on a single input.

    Args:
        data: dict of raw employee features (human-readable values).

    Returns:
        dict with prediction, probability, and risk_level.
    """
    model = load_model()

    # Preprocess
    X = preprocess_single(data)

    # Predict
    proba = model.predict_proba(X)[0]
    prob_leave = float(proba[1])
    prediction = "Oui" if prob_leave >= THRESHOLD else "Non"

    # Risk level
    if prob_leave < 0.3:
        risk_level = "faible"
    elif prob_leave < 0.6:
        risk_level = "modéré"
    else:
        risk_level = "élevé"

    return {
        "prediction": prediction,
        "probability": round(prob_leave, 4),
        "risk_level": risk_level,
        "threshold": THRESHOLD,
        "model_version": MODEL_VERSION,
    }


def get_model_info() -> dict:
    """Return model metadata."""
    return {
        "model_name": "CatBoost Attrition Classifier",
        "model_version": MODEL_VERSION,
        "algorithm": "CatBoostClassifier (tuned, balanced class weights)",
        "features_count": len(EXPECTED_FEATURES),
        "target": "a_quitte_l_entreprise (Oui/Non)",
        "description": (
            "Modèle de prédiction d'attrition des employés, entraîné sur les données "
            "RH de TechNova Partners (Projet 4). Classification binaire : l'employé "
            "va-t-il quitter l'entreprise ?"
        ),
    }


def predict_and_record(data: dict, db: Session) -> dict:
    """Run prediction and persist input + output in DB."""
    result = predict(data)
    record = Prediction(
        model_version=MODEL_VERSION,
        **{k: v.value if hasattr(v, "value") else v for k, v in data.items()},
        prediction=result["prediction"],
        probability=result["probability"],
        risk_level=result["risk_level"],
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return {
        **result,
        "prediction_id": record.id,
        "timestamp": record.created_at,
    }


def list_recent(db: Session, skip: int = 0, limit: int = 20) -> list[Prediction]:
    """Return predictions stored in DB, most recent first."""
    return (
        db.query(Prediction).order_by(Prediction.created_at.desc()).offset(skip).limit(limit).all()
    )


def get_by_id(db: Session, prediction_id: int) -> Prediction | None:
    """Return a prediction by its ID, or None if not found."""
    return db.query(Prediction).filter(Prediction.id == prediction_id).first()
