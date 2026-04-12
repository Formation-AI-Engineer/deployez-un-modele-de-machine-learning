"""Prediction routes."""

from fastapi import APIRouter

from app.schemas.prediction import ModelInfo, PredictionInput, PredictionOutput
from app.services.prediction import get_model_info, predict

router = APIRouter(tags=["Prédiction"])


@router.post(
    "/predict",
    response_model=PredictionOutput,
    summary="Prédire le risque d'attrition d'un employé",
    description=(
        "Prend les données RH d'un employé en entrée et retourne une prédiction "
        "de départ (Oui/Non), la probabilité associée, et le niveau de risque."
    ),
)
def predict_attrition(data: PredictionInput) -> PredictionOutput:
    result = predict(data.model_dump())
    return PredictionOutput(**result)


@router.get(
    "/model/info",
    response_model=ModelInfo,
    summary="Informations sur le modèle",
    description="Retourne les métadonnées du modèle déployé (version, algorithme, features).",
)
def model_info() -> ModelInfo:
    return ModelInfo(**get_model_info())
