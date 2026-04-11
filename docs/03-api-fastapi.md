# Étape 3 — Développement de l'API

## Objectif
Créer une API avec **FastAPI** (ou Gradio) pour exposer le modèle de machine learning.
Valider les données entrantes avec **Pydantic**, configurer les endpoints nécessaires pour retourner les prédictions, et tester chaque endpoint individuellement.

## Prérequis
- [ ] Compréhension claire du modèle ML choisi (P3 ou P4)
- [ ] Expérience de base avec Python et les API REST
- [ ] Modèle entraîné disponible (fichier `.pkl`, `.joblib`, etc.)

## Tâches à réaliser

### 1. Préparation du modèle
- [ ] Récupérer le modèle entraîné du projet P3 ou P4
- [ ] Sérialiser le modèle (joblib / pickle) si ce n'est pas déjà fait
- [ ] Identifier les features d'entrée attendues (noms, types, plages)
- [ ] Identifier le format de sortie (classe, probabilité, valeur numérique)
- [ ] Créer un module `model_loader.py` qui charge le modèle au démarrage

### 2. Structure de l'API
- [ ] Créer l'arborescence `app/`
  ```
  app/
  ├── __init__.py
  ├── main.py          # point d'entrée FastAPI
  ├── schemas.py       # modèles Pydantic (input/output)
  ├── routes/          # endpoints
  ├── services/        # logique métier (prédiction)
  └── config.py        # settings (Pydantic Settings)
  ```
- [ ] Installer FastAPI + uvicorn (`fastapi`, `uvicorn[standard]`)

### 3. Schémas Pydantic
- [ ] Définir le schéma d'input (validation stricte : types, bornes, champs requis)
- [ ] Définir le schéma d'output (prédiction + métadonnées éventuelles)
- [ ] Ajouter des exemples dans `model_config` / `Field(..., example=...)` pour Swagger
- [ ] Gérer les messages d'erreur de validation clairs

### 4. Endpoints
- [ ] `GET /` ou `GET /health` : healthcheck (API up)
- [ ] `GET /model/info` : métadonnées du modèle (version, features attendues)
- [ ] `POST /predict` : endpoint principal de prédiction
- [ ] (Optionnel) `POST /predict/batch` : prédictions multiples
- [ ] Codes HTTP appropriés (200, 422 validation, 500 erreur interne)

### 5. Gestion des erreurs
- [ ] Handler global pour les `ValidationError`
- [ ] Handler pour les erreurs de prédiction (input incohérent avec le modèle)
- [ ] Logs structurés (au moins par prédiction)

### 6. Documentation Swagger
- [ ] Vérifier que `/docs` expose Swagger UI
- [ ] Vérifier que `/redoc` expose ReDoc
- [ ] Enrichir les docstrings des endpoints (title, summary, description)
- [ ] Ajouter des `response_model` et des `responses` détaillées

### 7. Tests manuels
- [ ] Lancer l'API en local (`uvicorn app.main:app --reload`)
- [ ] Tester chaque endpoint individuellement (Swagger UI / curl / httpie)
- [ ] Vérifier les cas d'erreurs de validation
- [ ] Vérifier un cas nominal et un cas limite

## Résultats attendus
- [ ] API fonctionnelle exposant le modèle ML
- [ ] Endpoints documentés via Swagger/OpenAPI
- [ ] Validation robuste des données d'entrée avec Pydantic
- [ ] Chaque endpoint testé individuellement

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

## Statut global étape : **À FAIRE**
