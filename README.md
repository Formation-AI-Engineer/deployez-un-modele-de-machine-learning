---
title: Deploy ML Model
emoji: 🚀
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
---

# Déployez un modèle de Machine Learning

Projet 5 du parcours **AI Engineer** — déploiement en production d'un modèle de Machine Learning pour le client fictif **Futurisys**.

L'objectif : exposer un modèle ML via une API FastAPI, persister les échanges dans une base PostgreSQL, garantir la qualité avec une suite de tests Pytest, et automatiser le déploiement via un pipeline CI/CD (GitHub Actions + Hugging Face Spaces).

## Sommaire

- [Prérequis](#prérequis)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Tests](#tests)
- [Déploiement](#déploiement)
- [Structure du projet](#structure-du-projet)
- [Architecture](#architecture)
- [Conventions](#conventions)
- [Documentation](#documentation)

## Prérequis

- Python **>= 3.10**
- PostgreSQL **>= 14** (local ou via Docker)
- Git
- (Optionnel) Compte Hugging Face pour le déploiement

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
| `HF_TOKEN` | Token Hugging Face (déploiement uniquement, pas runtime) | `hf_xxx...` |
| `HF_SPACE_ID` | ID du Space cible | `lcamara/deployMLModel` |

`.env` et `.env.*` sont gitignorés. Seul `.env.example` est versionné comme template.

## Utilisation

### Entraîner le modèle (prérequis)

Le modèle CatBoost sérialisé (`models/catboost_attrition.cbm`) n'est pas versionné. Il faut l'entraîner une fois avant de lancer l'API :

```bash
python scripts/train_model.py
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
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

uvicorn app.main:app --reload
```

Les tables sont créées automatiquement au démarrage (`Base.metadata.create_all` dans `app/main.py`). Aucune migration à lancer.

**3. (Optionnel) Pré-remplir la base** — utile si tu veux interroger le dataset original via SQL ; non requis pour faire des prédictions :

```bash
python scripts/seed_db.py
```

### Avec Docker (API seule)

```bash
# Construire l'image
docker build -t attrition-api .

# Lancer le conteneur
docker run -p 7860:7860 attrition-api
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

Documentation interactive disponible sur :
- **Local** : http://localhost:8000/docs (Swagger UI) / http://localhost:8000/redoc
- **Docker / Compose** : http://localhost:7860/docs (Swagger UI) / http://localhost:7860/redoc

## Tests

```bash
# Suite complète avec couverture
pytest --cov=app --cov-report=term-missing --cov-report=html
```

Le rapport HTML de couverture est généré dans `htmlcov/`.

## Déploiement

*À compléter — Hugging Face Spaces via GitHub Actions (étape 2).*

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
├── docs/                 # Documentation et suivi par étape
├── .github/workflows/    # Pipeline CI/CD (ci-cd.yml)
├── .env.example          # Template des variables d'environnement
├── pyproject.toml        # Dépendances et configuration
└── README.md
```

## Architecture

### Composants

```mermaid
flowchart LR
    Client[Client HTTP] -->|JSON| API[FastAPI / Uvicorn]
    API --> Model[(CatBoost<br/>chargé en mémoire)]
    API --> DB[(PostgreSQL<br/>via SQLAlchemy)]
```

L'API FastAPI charge le modèle CatBoost une seule fois au démarrage (singleton) et persiste chaque prédiction dans PostgreSQL.

### Flux d'une requête `/predict`

```mermaid
sequenceDiagram
    participant C as Client
    participant R as routers/prediction.py
    participant S as services/prediction.py
    participant M as CatBoost
    participant DB as PostgreSQL

    C->>R: POST /predict (JSON)
    R->>R: Validation Pydantic (PredictionInput)
    R->>S: predict_and_record(data, db)
    S->>M: predict_proba(X)
    M-->>S: probabilité
    S->>DB: INSERT prediction
    S-->>R: dict résultat
    R-->>C: PredictionOutput (JSON)
```

Couches : `routers/` (HTTP) → `services/` (métier + DB) → `db/models.py` (entités SQLAlchemy). Les `schemas/` (Pydantic) définissent le contrat d'API en entrée/sortie, distincts des entités DB.

### Deux pipelines

**Training (offline)** — exécuté une fois, avant le déploiement :

```
data/*.csv → app/preprocessing.py → scripts/train_model.py → models/catboost_attrition.cbm
```

**Serving (online)** — à chaque requête :

```
HTTP → schema Pydantic → preprocessing (même logique) → modèle (singleton) → réponse + INSERT DB
```

Le préprocessing est partagé entre les deux pipelines (`app/preprocessing.py`) pour garantir que les features vues à l'inférence sont strictement identiques à celles vues à l'entraînement.

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
[SemVer](https://semver.org/lang/fr/) — tags `vMAJOR.MINOR.PATCH`.

## Documentation

Le dossier [`docs/`](docs/) contient le suivi détaillé des 6 étapes de la mission :

| # | Étape | Fichier |
|---|-------|---------|
| 0 | Vue d'ensemble | [00-overview.md](docs/00-overview.md) |
| 1 | Gestion de version | [01-git-versioning.md](docs/01-git-versioning.md) |
| 2 | CI/CD | [02-cicd.md](docs/02-cicd.md) |
| 3 | API FastAPI | [03-api-fastapi.md](docs/03-api-fastapi.md) |
| 4 | PostgreSQL | [04-postgresql.md](docs/04-postgresql.md) |
| 5 | Tests | [05-tests.md](docs/05-tests.md) |
| 6 | Documentation | [06-documentation.md](docs/06-documentation.md) |

## Licence

MIT

## Auteur

Lamine Camara — formation AI Engineer (OpenClassrooms)
