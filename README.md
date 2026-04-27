---
title: Deploy ML Model
emoji: 🚀
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
---

# Déployez un modèle de Machine Learning

Projet 5 du parcours AI Engineer — déploiement en production d'un modèle de Machine Learning pour le client fictif Futurisys.

L'objectif : exposer un modèle ML via une API FastAPI, persister les échanges dans une base PostgreSQL, garantir la qualité avec une suite de tests Pytest, et automatiser le déploiement via un pipeline CI/CD (GitHub Actions + Hugging Face Spaces).

## Démo en ligne

- **Space Hugging Face** : <https://huggingface.co/spaces/lcamara/deployMLModel>
- **Documentation interactive (Swagger UI)** : <https://lcamara-deployMLModel.hf.space/docs>

## Sommaire

- [Prérequis](#prérequis)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Tests](#tests)
- [Déploiement](#déploiement)
- [Structure du projet](#structure-du-projet)
- [Architecture](#architecture)
- [Conventions](#conventions)

## Prérequis

- Python **>= 3.10**
- PostgreSQL **>= 14** (local ou via Docker)
- Git

## Installation

```bash
# Cloner le dépôt
git clone git@github.com:Formation-AI-Engineer/deployez-un-modele-de-machine-learning.git
cd deployez-un-modele-de-machine-learning

# Créer et activer un environnement virtuel
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Installer les dépendances (runtime + dev)
pip install -e ".[dev]"
```

### Configuration

Copier le fichier d'exemple et adapter les valeurs :

```bash
cp .env.example .env
```

Variables disponibles (chargées via `app/config.py` avec pydantic-settings) :

| Variable | Description | Exemple |
|---|---|---|
| `DATABASE_URL` | URL de connexion PostgreSQL | `postgresql+psycopg://user:pwd@localhost:5432/ml_deploy` |
| `APP_ENV` | Environnement applicatif | `dev` \| `test` \| `prod` |

`.env` et `.env.*` sont gitignorés. Seul `.env.example` est versionné comme template.

## Utilisation

### Entraîner le modèle (prérequis)

Le modèle CatBoost sérialisé (`models/catboost_attrition.cbm`) n'est pas versionné. Il faut l'entraîner une fois avant de lancer l'API :

```bash
python3 scripts/train_model.py
```

Les 3 CSV nécessaires (`extrait_sirh.csv`, `extrait_eval.csv`, `extrait_sondage.csv`) sont déjà dans `data/`.

### En local (développement)

**1. Démarrer PostgreSQL** — soit via le service `db` du docker-compose (option la plus simple) :

```bash
docker compose up -d db
```

…soit en utilisant une instance Postgres déjà installée (adapter `DATABASE_URL` dans `.env` en conséquence).

**2. Lancer l'API** :

```bash
source .venv/bin/activate
uvicorn app.main:app --reload
```

Les tables sont créées automatiquement au démarrage (`Base.metadata.create_all` dans `app/main.py`). Aucune migration à lancer.

**3. (Optionnel) Pré-remplir la base** — utile si tu veux interroger le dataset original via SQL ; non requis pour faire des prédictions :

```bash
python3 scripts/seed_db.py
```

### Avec Docker Compose (API + PostgreSQL)

```bash
# Lancer l'ensemble (API + base de données)
docker compose up --build -d

# Importer le dataset dans la base (une seule fois)
docker compose exec api python scripts/seed_db.py

# Arrêter
docker compose down
```

Documentation interactive (Swagger UI) :
- **Local** : <http://localhost:8000/docs>
- **Docker / Compose** : <http://localhost:7860/docs>

### Exemples d'appels API

Les exemples ci-dessous ciblent l'instance locale Docker Compose (port 7860). Adapter le hôte si besoin.

**Health check**

```bash
curl http://localhost:7860/health
# {"status":"ok"}
```

**Prédiction à partir de caractéristiques RH** (`POST /predict`)

```bash
curl -X POST http://localhost:7860/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 35, "genre": "M", "revenu_mensuel": 5000,
    "nombre_experiences_precedentes": 3, "annee_experience_totale": 10,
    "annees_dans_l_entreprise": 5,
    "satisfaction_employee_environnement": 3, "satisfaction_employee_nature_travail": 3,
    "satisfaction_employee_equipe": 3, "satisfaction_employee_equilibre_pro_perso": 2,
    "note_evaluation_actuelle": 3, "note_evaluation_precedente": 3,
    "heure_supplementaires": "Non", "augementation_salaire_precedente": 12.0,
    "nombre_participation_pee": 2, "nb_formations_suivies": 3,
    "distance_domicile_travail": 10, "niveau_education": 3,
    "frequence_deplacement": "Occasionnel", "annees_depuis_la_derniere_promotion": 1,
    "statut_marital": "Marié(e)", "departement": "Consulting",
    "poste": "Consultant", "domaine_etude": "Data Science"
  }'
```

Réponse :

```json
{
  "prediction_id": 42,
  "prediction": "Non",
  "probability": 0.2134,
  "risk_level": "faible",
  "threshold": 0.5,
  "model_version": "1.0.0",
  "timestamp": "2026-04-17T10:42:00Z"
}
```

**Historique des prédictions**

```bash
curl "http://localhost:7860/predictions?skip=0&limit=10"
curl http://localhost:7860/predictions/42
```

## Tests

**51 tests** (unitaires + fonctionnels) couvrent la validation Pydantic, le préprocessing, le service de prédiction, l'ORM et l'ensemble des endpoints. Couverture actuelle : **88 %** (cible ≥ 80 %).

```bash
# Suite complète (SQLite temporaire auto — pas besoin de Postgres)
pytest

# Avec rapport de couverture console
pytest --cov=app --cov-report=term-missing

# Avec rapport HTML → ouvre htmlcov/index.html
pytest --cov=app --cov-report=html
```

Les tests sont exécutés automatiquement en CI (job `test` dans `.github/workflows/ci-cd.yml`).

## Déploiement

L'API est déployée automatiquement sur **Hugging Face Spaces** (type Docker) via GitHub Actions.

### Pipeline CI/CD

Fichier : [`.github/workflows/ci-cd.yml`](.github/workflows/ci-cd.yml)

```
push/PR → lint (ruff) → test (pytest --cov) → deploy (push vers HF Spaces)
```

Déclencheurs :
- `push` sur `dev` → **lint + tests** uniquement (feedback rapide)
- `pull_request` vers `main` → **lint + tests** (gate de merge, CI bloquante)
- `push` sur `main` ou tag `v*` → **lint + tests + déploiement HF**

### Secrets requis (GitHub Settings > Secrets and variables > Actions)

| Secret | Usage |
|---|---|
| `HF_TOKEN` | Token HF avec scope *write* sur le Space |
| `HF_SPACE_ID` | Identifiant du Space cible (ex. `lcamara/deployMLModel`) |

### Mécanique du déploiement

Le job `deploy` force-push le contenu du repo Git vers le repo Git du Space Hugging Face. Le Space, configuré en mode **Docker**, build l'image à partir du `Dockerfile` à la racine, qui :

1. Installe les dépendances Python (`pip install .`)
2. Lance `scripts/train_model.py` pour régénérer `models/catboost_attrition.cbm` (le `.cbm` n'est pas versionné)
3. Expose l'API sur le port `7860` (convention HF Spaces)

### Base de données en production

L'API en prod pointe vers une instance **PostgreSQL managée chez [Neon](https://neon.tech)**. La connexion est fournie au Space via la variable d'environnement `DATABASE_URL` configurée dans les secrets du Space (HF Settings → Variables and secrets).

## Structure du projet

```
.
├── app/                  # Code de l'API FastAPI
│   ├── routers/          # Endpoints (APIRouter)
│   ├── services/         # Logique métier (prédiction)
│   └── schemas/          # Modèles Pydantic
├── db/                   # Scripts base de données, modèles ORM
├── models/               # Modèles ML sérialisés (gitignored, régénérés via train_model.py)
├── data/                 # CSV synthétiques du dataset (trackés ; sous-dossiers raw/interim/processed gitignorés)
├── scripts/              # Scripts utilitaires (train_model.py, seed_db.py)
├── tests/
│   ├── unit/             # Tests unitaires
│   └── functional/       # Tests fonctionnels / end-to-end
├── docs/                 # Documentation technique
├── .github/workflows/    # Pipeline CI/CD (ci-cd.yml)
├── .env.example          # Template des variables d'environnement
├── pyproject.toml        # Dépendances et configuration
└── README.md
```

## Architecture

### Composants

Le client HTTP envoie une requête JSON à l'API FastAPI (servie par Uvicorn). L'API charge le modèle CatBoost une seule fois au démarrage (singleton en mémoire) et utilise SQLAlchemy pour persister chaque prédiction dans PostgreSQL.

### Flux d'une requête `/predict`

1. Le client envoie un `POST /predict` avec un payload JSON.
2. Le router (`app/routers/prediction.py`) valide le payload via le schéma Pydantic `PredictionInput`. Si les types ou bornes ne sont pas respectés, FastAPI retourne `422` immédiatement.
3. Le router appelle le service `predict_and_record(data, db)` (`app/services/prediction.py`).
4. Le service applique le préprocessing (`app/preprocessing.py`), passe les features à CatBoost (`predict_proba`) et récupère la probabilité.
5. Le service insère un enregistrement dans la table `predictions` (input + output + métadonnées) via SQLAlchemy.
6. Le router renvoie au client la réponse sérialisée par `PredictionOutput`.

Couches : `routers/` (HTTP) → `services/` (métier + DB) → `db/models.py` (entités SQLAlchemy). Les `schemas/` (Pydantic) définissent le contrat d'API en entrée/sortie, distincts des entités DB.

Le préprocessing (`app/preprocessing.py`) est partagé entre l'entraînement (`scripts/train_model.py`) et l'inférence pour garantir que les features sont strictement identiques dans les deux cas.

### Stack technique

| Couche | Outils |
|---|---|
| API | FastAPI, Pydantic, Uvicorn |
| ML | CatBoost, scikit-learn, pandas |
| Base de données | PostgreSQL, SQLAlchemy |
| Tests | pytest, pytest-cov |
| Qualité code | ruff |
| CI/CD | GitHub Actions, Hugging Face Spaces (Docker) |

## Conventions

### Branches
- `main` : branche stable, protégée
- `dev` : branche d'intégration
- `feature/<nom>` : nouvelles fonctionnalités
- `fix/<nom>` : corrections de bugs
- `docs/<nom>` : documentation uniquement

### Commits
Format recommandé : [Conventional Commits](https://www.conventionalcommits.org/fr/v1.0.0/)

```
<type>(<scope>): <description>

Exemples :
feat(api): add /predict endpoint
fix(db): handle connection timeout
docs(readme): add installation steps
```

Types courants : `feat`, `fix`, `docs`, `test`, `refactor`, `chore`, `ci`.

### Versioning
[SemVer](https://semver.org/lang/fr/) — tags `vMAJOR.MINOR.PATCH`. Voir la [page Releases](https://github.com/Formation-AI-Engineer/deployez-un-modele-de-machine-learning/releases) pour l'historique des versions.

## Auteur

Lamine Camara — formation AI Engineer (OpenClassrooms)
