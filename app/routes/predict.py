"""Prediction routes — predict + history."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.schemas.prediction import ModelInfo, PredictionInput, PredictionOutput
from app.schemas.prediction_record import PredictionRecord
from app.services.prediction import get_model_info, predict
from db.database import get_db
from db.models import Prediction

router = APIRouter(tags=["Prédiction"])


@router.post(
    "/predict",
    response_model=PredictionOutput,
    summary="Prédire le risque d'attrition d'un employé",
    description=(
        "Prend les données RH d'un employé en entrée et retourne une prédiction "
        "de départ (Oui/Non), la probabilité associée, et le niveau de risque. "
        "Chaque prédiction est enregistrée en base de données."
    ),
)
def predict_attrition(data: PredictionInput, db: Session = Depends(get_db)):
    input_data = data.model_dump()
    result = predict(input_data)

    # Persist input + output in DB
    record = Prediction(
        model_version="1.0.0",
        **{k: v.value if hasattr(v, "value") else v for k, v in input_data.items()},
        prediction=result["prediction"],
        probability=result["probability"],
        risk_level=result["risk_level"],
    )
    db.add(record)
    db.commit()

    return PredictionOutput(**result)


@router.get(
    "/model/info",
    response_model=ModelInfo,
    summary="Informations sur le modèle",
    description="Retourne les métadonnées du modèle déployé (version, algorithme, features).",
)
def model_info() -> ModelInfo:
    return ModelInfo(**get_model_info())


@router.get(
    "/predictions",
    response_model=list[PredictionRecord],
    summary="Liste des prédictions récentes",
    description="Retourne les prédictions stockées en base, triées par date décroissante.",
)
def list_predictions(
    skip: int = Query(0, ge=0, description="Nombre d'enregistrements à sauter"),
    limit: int = Query(20, ge=1, le=100, description="Nombre max de résultats"),
    db: Session = Depends(get_db),
):
    return (
        db.query(Prediction).order_by(Prediction.created_at.desc()).offset(skip).limit(limit).all()
    )


@router.get(
    "/predictions/{prediction_id}",
    response_model=PredictionRecord,
    summary="Détail d'une prédiction",
    description="Retourne une prédiction par son ID.",
)
def get_prediction(prediction_id: int, db: Session = Depends(get_db)):
    record = db.query(Prediction).filter(Prediction.id == prediction_id).first()
    if record is None:
        raise HTTPException(status_code=404, detail="Prédiction non trouvée")
    return record
