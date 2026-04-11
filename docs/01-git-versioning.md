# Étape 1 — Mettre en place la gestion de version et la collaboration

## Objectif
Poser les fondations du projet : un environnement de travail structuré, une collaboration fluide, un suivi précis des modifications et une traçabilité complète du développement.

## Prérequis
- [ ] Connaissances de base de Git (commandes, concepts)
- [ ] Compréhension des workflows de collaboration (feature branch, PR, etc.)
- [ ] Notions de gestion de versions (SemVer)
- [ ] Compte créé sur GitHub (ou GitLab)

## Tâches à réaliser

### 1. Initialisation du dépôt
- [ ] Créer un dépôt distant (GitHub/GitLab)
- [ ] Initialiser le dépôt local (`git init` / clone)
- [ ] Ajouter un `.gitignore` adapté Python (venv, __pycache__, .env, *.pkl si gros, etc.)
- [ ] Configurer `user.name` et `user.email`
- [ ] Premier commit initial

### 2. Structure du projet
- [ ] Créer une arborescence claire (ne pas tout mettre à la racine)
  - Exemple suggéré :
    ```
    ├── app/              # code de l'API
    ├── models/           # modèle ML sérialisé + wrappers
    ├── db/               # scripts DB, migrations
    ├── tests/            # tests Pytest
    ├── docs/             # documentation
    ├── .github/workflows/# CI/CD
    ├── requirements.txt
    ├── README.md
    └── .gitignore
    ```
- [ ] Créer un `requirements.txt` (ou `pyproject.toml` / `poetry`)
- [ ] Figer les versions des dépendances

### 3. Conventions & workflow
- [ ] Définir la convention de nommage des branches (ex : `feature/`, `fix/`, `docs/`)
- [ ] Définir la convention de messages de commit (ex : Conventional Commits)
- [ ] Documenter ces conventions dans le README ou un `CONTRIBUTING.md`
- [ ] Créer au moins une branche `dev` en plus de `main`

### 4. README initial
- [ ] Titre, description du projet
- [ ] Section installation (cloner, créer venv, installer deps)
- [ ] Section utilisation (placeholder pour l'instant)
- [ ] Prérequis techniques (Python version, PostgreSQL, etc.)
- [ ] Auteur / licence

### 5. Gestion des versions
- [ ] Poser un premier tag (ex : `v0.1.0`) une fois la structure initiale prête
- [ ] Documenter la stratégie de versioning (SemVer recommandé)

## Résultats attendus
- [ ] Dépôt Git bien structuré avec `requirements.txt`
- [ ] Historique de commits clair et significatif
- [ ] Au moins une branche de feature en plus de `main`
- [ ] README complet avec instructions d'installation
- [ ] Conventions de branches définies

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

## Statut global étape : **À FAIRE**
