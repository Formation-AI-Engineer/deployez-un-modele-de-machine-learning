"""Seed the database — import the merged HR dataset into the 'dataset' table."""

from pathlib import Path

from app.preprocessing import load_and_merge
from db.database import SessionLocal, engine
from db.models import Base, Dataset

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def seed():
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)

    df = load_and_merge(
        sirh_path=str(DATA_DIR / "extrait_sirh.csv"),
        eval_path=str(DATA_DIR / "extrait_eval.csv"),
        sondage_path=str(DATA_DIR / "extrait_sondage.csv"),
    )

    db = SessionLocal()
    try:
        existing = db.query(Dataset).count()
        if existing > 0:
            print(f"Dataset table already has {existing} rows — skipping seed.")
            return

        rows = []
        for _, row in df.iterrows():
            rows.append(
                Dataset(
                    id_employee=int(row["id_employee"]),
                    age=int(row["age"]),
                    genre=row["genre"],
                    revenu_mensuel=int(row["revenu_mensuel"]),
                    statut_marital=row["statut_marital"],
                    departement=row["departement"],
                    poste=row["poste"],
                    nombre_experiences_precedentes=int(row["nombre_experiences_precedentes"]),
                    annee_experience_totale=int(row["annee_experience_totale"]),
                    annees_dans_l_entreprise=int(row["annees_dans_l_entreprise"]),
                    satisfaction_employee_environnement=int(
                        row["satisfaction_employee_environnement"]
                    ),
                    satisfaction_employee_nature_travail=int(
                        row["satisfaction_employee_nature_travail"]
                    ),
                    satisfaction_employee_equipe=int(row["satisfaction_employee_equipe"]),
                    satisfaction_employee_equilibre_pro_perso=int(
                        row["satisfaction_employee_equilibre_pro_perso"]
                    ),
                    note_evaluation_actuelle=int(row["note_evaluation_actuelle"]),
                    note_evaluation_precedente=int(row["note_evaluation_precedente"]),
                    heure_supplementaires=row["heure_supplementaires"],
                    augementation_salaire_precedente=float(row["augementation_salaire_precedente"]),
                    nombre_participation_pee=int(row["nombre_participation_pee"]),
                    nb_formations_suivies=int(row["nb_formations_suivies"]),
                    distance_domicile_travail=int(row["distance_domicile_travail"]),
                    niveau_education=int(row["niveau_education"]),
                    domaine_etude=row["domaine_etude"],
                    frequence_deplacement=row["frequence_deplacement"],
                    annees_depuis_la_derniere_promotion=int(
                        row["annees_depuis_la_derniere_promotion"]
                    ),
                    a_quitte_l_entreprise=row["a_quitte_l_entreprise"],
                )
            )

        db.add_all(rows)
        db.commit()
        print(f"Inserted {len(rows)} rows into 'dataset' table.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
