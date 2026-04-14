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

- [Statut](#statut)
- [Architecture](#architecture)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Tests](#tests)
- [Déploiement](#déploiement)
- [Structure du projet](#structure-du-projet)
- [Conventions](#conventions)
- [Documentation](#documentation)

## Statut

Projet en cours de construction — voir [`docs/00-overview.md`](docs/00-overview.md) pour le suivi détaillé par étape.

## Architecture

À compléter : schéma global API ↔ DB ↔ Modèle.

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
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Installer les dépendances (runtime + dev)
pip install -e ".[dev]"
```

## Utilisation

### En local (développement)

```bash
# Activer l'environnement virtuel
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Lancer l'API en local
uvicorn app.main:app --reload
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
│   ├── routes/           # Endpoints
│   ├── services/         # Logique métier (prédiction)
│   └── schemas/          # Modèles Pydantic
├── db/                   # Scripts base de données, modèles ORM
├── models/               # Modèles ML sérialisés (gitignored)
├── data/                 # Données (gitignored)
├── tests/
│   ├── unit/             # Tests unitaires
│   └── functional/       # Tests fonctionnels / end-to-end
├── docs/                 # Documentation et suivi par étape
├── .github/workflows/    # Pipeline CI/CD (ci-cd.yml)
├── pyproject.toml        # Dépendances et configuration
└── README.md
```

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
