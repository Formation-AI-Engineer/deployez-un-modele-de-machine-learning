# Étape 3 — Développement de l'API

## Objectif
Créer une API avec **FastAPI** (ou Gradio) pour exposer le modèle de machine learning.
Valider les données entrantes avec **Pydantic**, configurer les endpoints nécessaires pour retourner les prédictions, et tester chaque endpoint individuellement.

## Prérequis
- [x] Compréhension claire du modèle ML choisi (P4 — CatBoost attrition)
- [x] Expérience de base avec Python et les API REST
- [x] Modèle entraîné disponible (fichier `.cbm` généré par `scripts/train_model.py`)

## Tâches à réaliser

### 1. Préparation du modèle
- [x] Récupérer le modèle entraîné du projet P4
- [x] Sérialiser le modèle (format `.cbm` natif CatBoost via `scripts/train_model.py`)
- [x] Identifier les features d'entrée attendues (40 features, listées dans `app/preprocessing.py`)
- [x] Identifier le format de sortie (classe Oui/Non, probabilité, niveau de risque)
- [x] Créer un module de chargement (`app/services/prediction.py` — singleton au startup)

### 2. Structure de l'API
- [x] Créer l'arborescence `app/`
  ```
  app/
  ├── __init__.py
  ├── main.py          # point d'entrée FastAPI
  ├── preprocessing.py # pipeline de preprocessing (reproduit le notebook P4)
  ├── schemas/         # modèles Pydantic (input/output)
  ├── routes/          # endpoints
  ├── services/        # logique métier (prédiction)
  └── config.py        # settings (Pydantic Settings) — à créer étape 4
  ```
- [x] Installer FastAPI + uvicorn (dans `pyproject.toml`)

### 3. Schémas Pydantic
- [x] Définir le schéma d'input (validation stricte : types, bornes, Enums pour catégorielles)
- [x] Définir le schéma d'output (prédiction + probabilité + niveau de risque)
- [x] Ajouter des exemples dans `Field(..., example=...)` pour Swagger
- [x] Gérer les messages d'erreur de validation clairs (422 automatique via Pydantic)

### 4. Endpoints
- [x] `GET /` : redirige vers `/docs` (Swagger UI)
- [x] `GET /health` : healthcheck (API up)
- [x] `GET /model/info` : métadonnées du modèle (version, features attendues)
- [x] `POST /predict` : endpoint principal de prédiction
- [ ] (Optionnel) `POST /predict/batch` : prédictions multiples
- [x] Codes HTTP appropriés (200, 422 validation)

### 5. Gestion des erreurs
- [x] Handler global pour les `ValidationError` (intégré FastAPI/Pydantic → 422)
- [x] Handler pour les erreurs de prédiction (input incohérent avec le modèle)
- [ ] Logs structurés (au moins par prédiction)

### 6. Documentation Swagger
- [x] Vérifier que `/docs` expose Swagger UI
- [x] Vérifier que `/redoc` expose ReDoc
- [x] Enrichir les docstrings des endpoints (title, summary, description)
- [x] Ajouter des `response_model` et des `responses` détaillées

### 7. Tests manuels
- [x] Lancer l'API en local (`uvicorn app.main:app --reload`)
- [x] Tester chaque endpoint individuellement (curl + Swagger UI)
- [x] Vérifier les cas d'erreurs de validation (422 avec messages détaillés)
- [x] Vérifier un cas nominal et un cas limite (profil à risque + profil stable)

## Résultats attendus
- [x] API fonctionnelle exposant le modèle ML
- [x] Endpoints documentés via Swagger/OpenAPI
- [x] Validation robuste des données d'entrée avec Pydantic
- [x] Chaque endpoint testé individuellement

## Points de vigilance
- **Conformité des données entrantes** avec les attentes du modèle (ordre des features, encodage, normalisation)
- **Gestion des erreurs de validation** : retourner des messages explicites
- Charger le modèle UNE SEULE FOIS au démarrage (pas à chaque requête)
- Penser à la sérialisation JSON des types numpy si nécessaire

## Outils
- FastAPI (ou équivalent)
- Pydantic
- Uvicorn
- Environnement Python configuré

## Ressources
- Documentation FastAPI
- Documentation Gradio
- Documentation Pydantic
- Principes et bonnes pratiques de conception d'API

## Checkpoint mentor
À la fin de cette étape, faire le point avec le mentor pour valider la conception de l'API et son intégration avec le modèle.

## Statut global étape : **TERMINÉE** — déployée sur HF Spaces, reste logs structurés et batch (optionnels).
