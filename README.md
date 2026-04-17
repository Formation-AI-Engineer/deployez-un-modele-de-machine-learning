---
title: Deploy ML Model
emoji: 🚀
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
---

# Déployez un modèle de Machine Learning

[![CI/CD](https://github.com/Formation-AI-Engineer/deployez-un-modele-de-machine-learning/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/Formation-AI-Engineer/deployez-un-modele-de-machine-learning/actions/workflows/ci-cd.yml)
[![Coverage](https://img.shields.io/badge/coverage-88%25-brightgreen)](#tests)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](pyproject.toml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](#licence)

Projet 5 du parcours **AI Engineer** — déploiement en production d'un modèle de Machine Learning pour le client fictif **Futurisys**.

L'objectif : exposer un modèle ML via une API FastAPI, persister les échanges dans une base PostgreSQL, garantir la qualité avec une suite de tests Pytest, et automatiser le déploiement via un pipeline CI/CD (GitHub Actions + Hugging Face Spaces).

Le modèle sous-jacent est détaillé dans la [fiche technique](docs/07-model-card.md).

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

### Exemples d'appels API

Les exemples ci-dessous ciblent l'instance locale Docker Compose (port 7860). Adapter le hôte si besoin.

**Health check**

```bash
curl http://localhost:7860/health
# {"status":"ok"}
```

**Métadonnées du modèle**

```bash
curl http://localhost:7860/model/info
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

**Prédiction à partir d'un employé existant** (`POST /predict/employee/{id_employee}`) — nécessite d'avoir seedé la table `dataset` :

```bash
curl -X POST http://localhost:7860/predict/employee/1
```

**Historique des prédictions**

```bash
curl "http://localhost:7860/predictions?skip=0&limit=10"
curl http://localhost:7860/predictions/42
```

**Depuis Python**

```python
import httpx

payload = {"age": 35, "genre": "M", "revenu_mensuel": 5000, ...}  # 24 champs
response = httpx.post("http://localhost:7860/predict", json=payload)
response.raise_for_status()
print(response.json())
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

# Un fichier ou un test précis
pytest tests/unit/test_schemas.py
pytest tests/functional/test_api_predict.py::test_predict_valid_input_returns_200
```

Les tests sont exécutés automatiquement en CI (job `test` dans `.github/workflows/ci-cd.yml`). Le détail des cas couverts est dans [`docs/05-tests.md`](docs/05-tests.md).

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
| `DATABASE_URL` | URL PostgreSQL utilisée par les tests CI (optionnel — les tests tombent sur SQLite via `conftest.py`) |
| `HF_TOKEN` | Token HF avec scope *write* sur le Space |
| `HF_SPACE_ID` | Identifiant du Space cible (ex. `Formation-AI-Engineer/deployez-un-modele-de-machine-learning`) |

### Mécanique du déploiement

Le job `deploy` force-push le contenu du repo Git vers le repo Git du Space Hugging Face. Le Space, configuré en mode **Docker**, build l'image à partir du `Dockerfile` à la racine, qui :

1. Installe les dépendances Python (`pip install .`)
2. Lance `scripts/train_model.py` pour régénérer `models/catboost_attrition.cbm` (le `.cbm` n'est pas versionné)
3. Expose l'API sur le port `7860` (convention HF Spaces)

### Rollback

Redéployer un tag antérieur :
```bash
git push --force hf <tag>:main
```

Ou `git revert <commit>` sur `main` — le pipeline redéploie automatiquement.

## Authentification et sécurisation

**Statut actuel (POC) : l'API n'a pas d'authentification.** Tout client ayant l'URL du Space peut appeler les endpoints.

### Ce qui est déjà en place

- **Validation stricte des entrées** : Pydantic refuse tout payload invalide (types, bornes, énums), réponse `422` explicite. Protège contre les injections via le schéma d'API.
- **Secrets hors du code** : `DATABASE_URL`, `HF_TOKEN`, `HF_SPACE_ID` chargés depuis l'environnement. `.env` et `.env.*` gitignorés. Seul `.env.example` est versionné comme template.
- **Secrets CI** : passés via `${{ secrets.XXX }}` dans GitHub Actions, jamais loggés.
- **Transactions DB** : chaque prédiction est persistée atomiquement — pas d'état incohérent possible.
- **Protection de branche** : `main` protégée, merge impossible sans CI verte.
- **Dépendances figées** avec bornes min/max dans `pyproject.toml`.

### Ce qui serait à ajouter pour la production

| Contrôle | Piste |
|---|---|
| Authentification API | Clé d'API en header (`X-API-Key`) ou OAuth2 / JWT selon le contexte d'appel |
| Rate limiting | `slowapi` côté FastAPI, ou reverse proxy (nginx / Cloudflare) |
| Journalisation structurée | `structlog` + export vers un agrégateur (Datadog, Grafana Loki…) |
| Chiffrement au repos | PostgreSQL managé avec chiffrement natif (pas de PII brutes dans les CSV d'exemple, mais à anticiper) |
| Audit RGPD | Les features incluent `genre`, `statut_marital`, `age` — base légale et durée de conservation à formaliser avant usage réel |
| Monitoring modèle | Suivi de dérive (distribution `probability`, proportion `Oui`) — voir [fiche modèle](docs/07-model-card.md) |

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
| ★ | Fiche technique du modèle | [07-model-card.md](docs/07-model-card.md) |

## Licence

MIT

## Auteur

Lamine Camara — formation AI Engineer (OpenClassrooms)
