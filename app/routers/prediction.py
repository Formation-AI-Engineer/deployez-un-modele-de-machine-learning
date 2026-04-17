"""Prediction routes — predict + history."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.schemas.prediction import (
    EmployeePredictionOutput,
    ModelInfo,
    PredictionInput,
    PredictionOutput,
)
from app.schemas.prediction_record import PredictionRecord
from app.services import prediction as prediction_service
from db.database import get_db

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
def predict_attrition(data: PredictionInput, db: Session = Depends(get_db)) -> PredictionOutput:
    result = prediction_service.predict_and_record(data.model_dump(), db)
    return PredictionOutput(**result)


@router.post(
    "/predict/employee/{id_employee}",
    response_model=EmployeePredictionOutput,
    summary="Prédire l'attrition à partir d'un identifiant employé",
    description=(
        "Recherche l'employé dans la base RH (table `dataset`) et exécute la prédiction "
        "sur ses caractéristiques. La prédiction est également enregistrée dans l'historique."
    ),
)
def predict_by_employee(
    id_employee: int, db: Session = Depends(get_db)
) -> EmployeePredictionOutput:
    result = prediction_service.predict_by_employee_id(db, id_employee)
    if result is None:
        raise HTTPException(
            status_code=404,
            detail=f"Employé {id_employee} introuvable dans la base RH.",
        )
    return EmployeePredictionOutput(**result)


@router.get(
    "/model/info",
    response_model=ModelInfo,
    summary="Informations sur le modèle",
    description="Retourne les métadonnées du modèle déployé (version, algorithme, features).",
)
def model_info() -> ModelInfo:
    return ModelInfo(**prediction_service.get_model_info())


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
    return prediction_service.list_recent(db, skip=skip, limit=limit)


@router.get(
    "/predictions/{prediction_id}",
    response_model=PredictionRecord,
    summary="Détail d'une prédiction",
    description="Retourne une prédiction par son ID.",
)
def get_prediction(prediction_id: int, db: Session = Depends(get_db)):
    record = prediction_service.get_by_id(db, prediction_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Prédiction non trouvée")
    return record
