# Étape 1 — Mettre en place la gestion de version et la collaboration

## Objectif
Poser les fondations du projet : un environnement de travail structuré, une collaboration fluide, un suivi précis des modifications et une traçabilité complète du développement.

## Prérequis
- [x] Connaissances de base de Git
- [x] Compréhension des workflows de collaboration
- [x] Notions de gestion de versions (SemVer)
- [x] Compte créé sur GitHub

## Tâches à réaliser

### 1. Initialisation du dépôt
- [x] Créer un dépôt distant GitHub
- [x] Cloner le dépôt en local
- [x] Ajouter un `.gitignore` Python/ML (venv, __pycache__, .env, artefacts ML, etc.)
- [x] Configurer `user.name` et `user.email` (déjà fait globalement)
- [x] Premier commit initial (`chore: initial project scaffold`)

### 2. Structure du projet
- [x] Créer une arborescence claire :
    ```
    ├── app/              # code de l'API
    │   ├── routes/
    │   ├── services/
    │   └── schemas/
    ├── db/               # scripts DB, modèles ORM (étape 4)
    ├── models/           # modèle ML sérialisé (gitignored)
    ├── data/             # datasets (gitignored)
    ├── tests/
    │   ├── unit/
    │   └── functional/
    ├── docs/             # suivi par étape
    ├── .github/workflows/# CI/CD (étape 2)
    ├── pyproject.toml
    ├── README.md
    └── .gitignore
    ```
- [x] Créer un `pyproject.toml` (PEP 621 + hatchling, préférence utilisateur)
- [x] Figer les dépendances avec bornes min/max

### 3. Conventions & workflow
- [x] Conventions de branches : `main`, `dev`, `feature/`, `fix/`, `docs/`
- [x] Conventions de commits : Conventional Commits
- [x] Documenter dans le README
- [x] Créer la branche `dev` en plus de `main`

### 4. README initial
- [x] Titre, description du projet
- [x] Section installation (clone, venv, `pip install -e ".[dev]"`)
- [x] Section utilisation (placeholder)
- [x] Prérequis techniques (Python 3.11+, PostgreSQL 14+)
- [x] Auteur / licence

### 5. Gestion des versions
- [x] Poser le premier tag `v0.1.0` (annotated) et pousser vers origin
- [x] Documenter la stratégie SemVer dans le README

## Résultats attendus
- [x] Dépôt Git bien structuré avec `pyproject.toml`
- [x] Historique de commits clair
- [x] Branche `dev` en plus de `main`
- [x] README complet avec instructions d'installation
- [x] Conventions définies et documentées

## Points de vigilance
- **Gestion des conflits** : utiliser un outil de résolution intégré à l'IDE
- Commits atomiques et descriptifs (pas de "wip", "fix", "update")
- Ne JAMAIS committer de secrets (.env, clés API)

## Outils
- Git
- GitHub / GitLab
- Éditeur de code avec intégration Git (PyCharm / VS Code)

## Ressources
- Documentation Git officielle
- Guide de bonnes pratiques de versionnage
- Cours OpenClassrooms : "Gérez du code avec Git et GitHub" + "Devenez un expert de Git et GitHub"

## Checkpoint mentor
À la fin de cette étape, faire le point avec le mentor pour valider la structure et les conventions avant de passer à l'étape 2.

## Statut global étape : **TERMINÉE** — checkpoint mentor recommandé avant étape 2.
