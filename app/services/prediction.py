"""Prediction service — loads model and runs inference."""

from pathlib import Path

from catboost import CatBoostClassifier

from app.preprocessing import EXPECTED_FEATURES, preprocess_single

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
    prediction = "Oui" if prob_leave >= 0.5 else "Non"

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
    }


def get_model_info() -> dict:
    """Return model metadata."""
    return {
        "model_name": "CatBoost Attrition Classifier",
        "model_version": "1.0.0",
        "algorithm": "CatBoostClassifier (tuned, balanced class weights)",
        "features_count": len(EXPECTED_FEATURES),
        "target": "a_quitte_l_entreprise (Oui/Non)",
        "description": (
            "Modèle de prédiction d'attrition des employés, entraîné sur les données "
            "RH de TechNova Partners (Projet 4). Classification binaire : l'employé "
            "va-t-il quitter l'entreprise ?"
        ),
    }
