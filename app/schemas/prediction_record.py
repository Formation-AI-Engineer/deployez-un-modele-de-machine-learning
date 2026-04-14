"""Pydantic schemas for prediction records (DB read)."""

from datetime import datetime

from pydantic import BaseModel


class PredictionRecord(BaseModel):
    """A stored prediction — input + output + metadata."""

    id: int
    created_at: datetime
    model_version: str

    # Input
    age: int
    genre: str
    revenu_mensuel: int
    nombre_experiences_precedentes: int
    annee_experience_totale: int
    annees_dans_l_entreprise: int
    satisfaction_employee_environnement: int
    satisfaction_employee_nature_travail: int
    satisfaction_employee_equipe: int
    satisfaction_employee_equilibre_pro_perso: int
    note_evaluation_actuelle: int
    note_evaluation_precedente: int
    heure_supplementaires: str
    augementation_salaire_precedente: float
    nombre_participation_pee: int
    nb_formations_suivies: int
    distance_domicile_travail: int
    niveau_education: int
    frequence_deplacement: str
    annees_depuis_la_derniere_promotion: int
    statut_marital: str
    departement: str
    poste: str
    domaine_etude: str

    # Output
    prediction: str
    probability: float
    risk_level: str

    model_config = {"from_attributes": True}
