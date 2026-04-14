"""FastAPI application — ML model deployment for attrition prediction."""

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.routes.predict import router as predict_router
from app.services.prediction import load_model

app = FastAPI(
    title="API Prédiction d'Attrition — TechNova Partners",
    description=(
        "API de déploiement du modèle de machine learning de prédiction d'attrition "
        "des employés. Projet 5 — Formation AI Engineer.\n\n"
        "**Modèle** : CatBoostClassifier entraîné sur les données RH (Projet 4).\n\n"
        "**Endpoints principaux** :\n"
        "- `POST /predict` : prédiction de départ pour un employé\n"
        "- `GET /model/info` : métadonnées du modèle\n"
        "- `GET /health` : vérification de l'état de l'API"
    ),
    version="0.1.0",
)

app.include_router(predict_router)


@app.on_event("startup")
def startup():
    """Load the ML model once at startup."""
    load_model()


@app.get("/", include_in_schema=False)
def root():
    """Redirect to Swagger UI."""
    return RedirectResponse(url="/docs")


@app.get(
    "/health",
    summary="Health check",
    description="Vérifie que l'API est opérationnelle.",
    tags=["Santé"],
)
def health():
    return {"status": "ok"}
