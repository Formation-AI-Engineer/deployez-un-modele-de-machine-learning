"""Preprocessing pipeline — reproduces the P4 notebook's prepare_features + encode_features."""

import pandas as pd


def load_and_merge(sirh_path: str, eval_path: str, sondage_path: str) -> pd.DataFrame:
    """Load the 3 CSV files and merge them on id_employee."""
    sirh = pd.read_csv(sirh_path)
    evaluation = pd.read_csv(eval_path)
    sondage = pd.read_csv(sondage_path)

    # Clean evaluation
    evaluation["augementation_salaire_precedente"] = (
        evaluation["augementation_salaire_precedente"]
        .str.replace(" %", "", regex=False)
        .astype(float)
    )
    evaluation["id_employee"] = evaluation["eval_number"].apply(lambda x: int(x.replace("E_", "")))
    evaluation = evaluation.drop(columns=["eval_number"])

    # Clean sondage
    sondage = sondage.rename(columns={"code_sondage": "id_employee"})

    # Drop constant columns
    sirh = sirh.drop(columns=["nombre_heures_travailless"], errors="ignore")
    sondage = sondage.drop(
        columns=["ayant_enfants", "nombre_employee_sous_responsabilite"], errors="ignore"
    )

    # Merge
    df = sirh.merge(evaluation, on="id_employee").merge(sondage, on="id_employee")
    return df


def prepare_features(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """Feature engineering + drop columns. Returns (X, y)."""
    df = df.copy()

    # Target
    y = df["a_quitte_l_entreprise"].map({"Oui": 1, "Non": 0})

    # Engineered features
    df["ratio_anciennete_experience"] = df.apply(
        lambda r: (
            r["annees_dans_l_entreprise"] / r["annee_experience_totale"]
            if r["annee_experience_totale"] != 0
            else 0
        ),
        axis=1,
    )
    df["satisfaction_moyenne"] = df[
        [
            "satisfaction_employee_environnement",
            "satisfaction_employee_nature_travail",
            "satisfaction_employee_equipe",
            "satisfaction_employee_equilibre_pro_perso",
        ]
    ].mean(axis=1)
    df["ecart_evaluation"] = df["note_evaluation_actuelle"] - df["note_evaluation_precedente"]
    df["anciennete_sans_promotion"] = (
        df["annees_dans_l_entreprise"] - df["annees_depuis_la_derniere_promotion"]
    )

    # Drop columns
    cols_to_drop = [
        "a_quitte_l_entreprise",
        "id_employee",
        "niveau_hierarchique_poste",
        "note_evaluation_precedente",
        "annes_sous_responsable_actuel",
        "annees_dans_le_poste_actuel",
    ]
    X = df.drop(columns=cols_to_drop, errors="ignore")
    return X, y


def encode_features(X: pd.DataFrame) -> pd.DataFrame:
    """Encode categorical features — same logic as notebook."""
    X = X.copy()

    # Binary mappings
    X["genre"] = X["genre"].map({"F": 0, "M": 1})
    X["heure_supplementaires"] = X["heure_supplementaires"].map({"Non": 0, "Oui": 1})

    # Ordinal mapping
    X["frequence_deplacement"] = X["frequence_deplacement"].map(
        {"Aucun": 0, "Occasionnel": 1, "Frequent": 2}
    )

    # One-hot encoding
    X = pd.get_dummies(X, drop_first=True, dtype=int)
    return X


# Exact feature order the trained model expects (40 features)
EXPECTED_FEATURES = [
    "age",
    "genre",
    "revenu_mensuel",
    "nombre_experiences_precedentes",
    "annee_experience_totale",
    "annees_dans_l_entreprise",
    "satisfaction_employee_environnement",
    "satisfaction_employee_nature_travail",
    "satisfaction_employee_equipe",
    "satisfaction_employee_equilibre_pro_perso",
    "note_evaluation_actuelle",
    "heure_supplementaires",
    "augementation_salaire_precedente",
    "nombre_participation_pee",
    "nb_formations_suivies",
    "distance_domicile_travail",
    "niveau_education",
    "frequence_deplacement",
    "annees_depuis_la_derniere_promotion",
    "ratio_anciennete_experience",
    "satisfaction_moyenne",
    "ecart_evaluation",
    "anciennete_sans_promotion",
    "statut_marital_Divorcé(e)",
    "statut_marital_Marié(e)",
    "departement_Consulting",
    "departement_Ressources Humaines",
    "poste_Cadre Commercial",
    "poste_Consultant",
    "poste_Directeur Technique",
    "poste_Manager",
    "poste_Représentant Commercial",
    "poste_Ressources Humaines",
    "poste_Senior Manager",
    "poste_Tech Lead",
    "domaine_etude_Entrepreunariat",
    "domaine_etude_Infra & Cloud",
    "domaine_etude_Marketing",
    "domaine_etude_Ressources Humaines",
    "domaine_etude_Transformation Digitale",
]


def preprocess_single(data: dict) -> pd.DataFrame:
    """Preprocess a single prediction input (dict of raw features) into model-ready DataFrame.

    Accepts raw human-readable values and returns a 1-row DataFrame with all 40 encoded features.
    """
    row = pd.DataFrame([data])

    # Binary + ordinal encoding
    row["genre"] = row["genre"].map({"F": 0, "M": 1})
    row["heure_supplementaires"] = row["heure_supplementaires"].map({"Non": 0, "Oui": 1})
    row["frequence_deplacement"] = row["frequence_deplacement"].map(
        {"Aucun": 0, "Occasionnel": 1, "Frequent": 2}
    )

    # Engineered features
    row["ratio_anciennete_experience"] = row.apply(
        lambda r: (
            r["annees_dans_l_entreprise"] / r["annee_experience_totale"]
            if r["annee_experience_totale"] != 0
            else 0
        ),
        axis=1,
    )
    row["satisfaction_moyenne"] = row[
        [
            "satisfaction_employee_environnement",
            "satisfaction_employee_nature_travail",
            "satisfaction_employee_equipe",
            "satisfaction_employee_equilibre_pro_perso",
        ]
    ].mean(axis=1)
    row["ecart_evaluation"] = row["note_evaluation_actuelle"] - row["note_evaluation_precedente"]
    row["anciennete_sans_promotion"] = (
        row["annees_dans_l_entreprise"] - row["annees_depuis_la_derniere_promotion"]
    )

    # One-hot columns — create all expected columns with 0, then set relevant ones to 1
    for col in EXPECTED_FEATURES:
        if col not in row.columns:
            row[col] = 0

    # Set one-hot flags from categorical inputs
    categorical_mappings = {
        "statut_marital": "statut_marital_",
        "departement": "departement_",
        "poste": "poste_",
        "domaine_etude": "domaine_etude_",
    }
    for cat_col, prefix in categorical_mappings.items():
        if cat_col in row.columns:
            value = row[cat_col].iloc[0]
            dummy_col = f"{prefix}{value}"
            if dummy_col in EXPECTED_FEATURES:
                row[dummy_col] = 1
            row = row.drop(columns=[cat_col])

    # Drop columns not needed for prediction
    cols_to_drop = [
        "id_employee",
        "niveau_hierarchique_poste",
        "note_evaluation_precedente",
        "annes_sous_responsable_actuel",
        "annees_dans_le_poste_actuel",
    ]
    row = row.drop(columns=[c for c in cols_to_drop if c in row.columns])

    # Reorder to match training order, fill any missing with 0
    row = row.reindex(columns=EXPECTED_FEATURES, fill_value=0)
    return row
