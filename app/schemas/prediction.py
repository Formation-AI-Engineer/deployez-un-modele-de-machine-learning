"""Pydantic schemas for prediction input/output."""

from datetime import datetime
from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class Genre(str, Enum):
    F = "F"
    M = "M"


class HeureSupplementaires(str, Enum):
    OUI = "Oui"
    NON = "Non"


class FrequenceDeplacement(str, Enum):
    AUCUN = "Aucun"
    OCCASIONNEL = "Occasionnel"
    FREQUENT = "Frequent"


class StatutMarital(str, Enum):
    CELIBATAIRE = "Célibataire"
    MARIE = "Marié(e)"
    DIVORCE = "Divorcé(e)"


class Departement(str, Enum):
    CONSULTING = "Consulting"
    RESSOURCES_HUMAINES = "Ressources Humaines"
    RECHERCHE_DEVELOPPEMENT = "Recherche & Développement"


class Poste(str, Enum):
    CADRE_COMMERCIAL = "Cadre Commercial"
    CONSULTANT = "Consultant"
    DIRECTEUR_TECHNIQUE = "Directeur Technique"
    MANAGER = "Manager"
    REPRESENTANT_COMMERCIAL = "Représentant Commercial"
    RESSOURCES_HUMAINES = "Ressources Humaines"
    SENIOR_MANAGER = "Senior Manager"
    TECH_LEAD = "Tech Lead"
    ANALYSTE_DONNEES = "Analyste Données"


class DomaineEtude(str, Enum):
    ENTREPREUNARIAT = "Entrepreunariat"
    INFRA_CLOUD = "Infra & Cloud"
    MARKETING = "Marketing"
    RESSOURCES_HUMAINES = "Ressources Humaines"
    TRANSFORMATION_DIGITALE = "Transformation Digitale"
    DATA_SCIENCE = "Data Science"


class PredictionInput(BaseModel):
    """Input data for attrition prediction — raw employee features."""

    age: int = Field(..., ge=18, le=65, example=35, description="Âge de l'employé")
    genre: Genre = Field(..., example="M", description="Genre (F/M)")
    revenu_mensuel: int = Field(
        ..., ge=1000, le=50000, example=5000, description="Revenu mensuel (€)"
    )
    nombre_experiences_precedentes: int = Field(
        ..., ge=0, le=15, example=3, description="Nombre d'expériences précédentes"
    )
    annee_experience_totale: int = Field(
        ..., ge=0, le=45, example=10, description="Années d'expérience totale"
    )
    annees_dans_l_entreprise: int = Field(
        ..., ge=0, le=40, example=5, description="Années dans l'entreprise"
    )
    satisfaction_employee_environnement: int = Field(
        ..., ge=1, le=4, example=3, description="Satisfaction environnement (1-4)"
    )
    satisfaction_employee_nature_travail: int = Field(
        ..., ge=1, le=4, example=3, description="Satisfaction nature du travail (1-4)"
    )
    satisfaction_employee_equipe: int = Field(
        ..., ge=1, le=4, example=3, description="Satisfaction équipe (1-4)"
    )
    satisfaction_employee_equilibre_pro_perso: int = Field(
        ..., ge=1, le=4, example=2, description="Satisfaction équilibre pro/perso (1-4)"
    )
    note_evaluation_actuelle: int = Field(
        ..., ge=1, le=4, example=3, description="Note évaluation actuelle (1-4)"
    )
    note_evaluation_precedente: int = Field(
        ..., ge=1, le=4, example=3, description="Note évaluation précédente (1-4)"
    )
    heure_supplementaires: HeureSupplementaires = Field(
        ..., example="Non", description="Fait des heures supplémentaires"
    )
    augementation_salaire_precedente: float = Field(
        ..., ge=0, le=30, example=12.0, description="Augmentation salaire précédente (%)"
    )
    nombre_participation_pee: int = Field(
        ..., ge=0, le=10, example=2, description="Nombre de participations au PEE"
    )
    nb_formations_suivies: int = Field(
        ..., ge=0, le=10, example=3, description="Nombre de formations suivies"
    )
    distance_domicile_travail: int = Field(
        ..., ge=0, le=60, example=10, description="Distance domicile-travail (km)"
    )
    niveau_education: int = Field(
        ..., ge=1, le=5, example=3, description="Niveau d'éducation (1-5)"
    )
    frequence_deplacement: FrequenceDeplacement = Field(
        ..., example="Occasionnel", description="Fréquence de déplacement"
    )
    annees_depuis_la_derniere_promotion: int = Field(
        ..., ge=0, le=15, example=1, description="Années depuis la dernière promotion"
    )
    statut_marital: StatutMarital = Field(..., example="Marié(e)", description="Statut marital")
    departement: Departement = Field(..., example="Consulting", description="Département")
    poste: Poste = Field(..., example="Consultant", description="Poste occupé")
    domaine_etude: DomaineEtude = Field(..., example="Data Science", description="Domaine d'étude")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
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
            ]
        }
    }


class PredictionOutput(BaseModel):
    """Prediction result."""

    prediction_id: int = Field(
        ..., description="Identifiant de la prédiction en base (clé pour GET /predictions/{id})"
    )
    prediction: Literal["Oui", "Non"] = Field(
        ..., description="Prédiction : l'employé va-t-il quitter l'entreprise ?"
    )
    probability: float = Field(..., ge=0, le=1, description="Probabilité de départ (entre 0 et 1)")
    risk_level: Literal["faible", "modéré", "élevé"] = Field(
        ..., description="Niveau de risque de départ"
    )
    threshold: float = Field(
        ...,
        ge=0,
        le=1,
        description="Seuil utilisé pour classer Oui/Non (probabilité ≥ seuil = Oui)",
    )
    model_version: str = Field(..., description="Version du modèle ayant généré la prédiction")
    timestamp: datetime = Field(..., description="Horodatage de la prédiction")


class ModelInfo(BaseModel):
    """Model metadata."""

    model_name: str
    model_version: str
    algorithm: str
    features_count: int
    target: str
    description: str
