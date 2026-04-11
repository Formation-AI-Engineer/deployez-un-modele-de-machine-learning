# Étape 5 — Développer des tests unitaires et fonctionnels

## Objectif
Garantir la fiabilité et la robustesse du modèle ML et de son API via une suite complète de tests :
- **Tests unitaires** : validation des composants individuels
- **Tests fonctionnels** : évaluation du modèle en conditions réelles

## Prérequis
- [ ] Connaissance des principes de tests unitaires
- [ ] Compréhension approfondie du modèle ML utilisé
- [ ] Familiarité avec Pytest
- [ ] Jeux de données représentatifs disponibles

## Tâches à réaliser

### 1. Mise en place
- [ ] Installer `pytest`, `pytest-cov`, `httpx` (pour tester FastAPI)
- [ ] Créer l'arborescence `tests/`
  ```
  tests/
  ├── __init__.py
  ├── conftest.py          # fixtures partagées
  ├── unit/
  │   ├── test_schemas.py
  │   ├── test_model.py
  │   └── test_db_models.py
  └── functional/
      ├── test_api_health.py
      ├── test_api_predict.py
      └── test_api_db_flow.py
  ```
- [ ] Configurer `pytest.ini` ou `pyproject.toml` (testpaths, options)

### 2. Fixtures
- [ ] Fixture `client` : TestClient FastAPI
- [ ] Fixture `db_session` : base de test (SQLite in-memory ou Postgres test)
- [ ] Fixture `sample_input` : exemple d'input valide
- [ ] Fixture `invalid_input` : exemples d'inputs invalides
- [ ] Fixture `loaded_model` : modèle ML chargé

### 3. Tests unitaires
- [ ] **Schemas Pydantic** : validation des inputs valides/invalides, types, bornes
- [ ] **Model loader** : chargement du modèle, erreurs si fichier absent
- [ ] **Service de prédiction** : prédiction sur input connu → output attendu
- [ ] **Modèles ORM** : création, contraintes, relations
- [ ] **Helpers / utils** : fonctions utilitaires isolées

### 4. Tests fonctionnels (API)
- [ ] `GET /health` retourne 200
- [ ] `GET /model/info` retourne les métadonnées attendues
- [ ] `POST /predict` avec input valide → 200 + prédiction
- [ ] `POST /predict` avec input invalide → 422 + message clair
- [ ] `POST /predict` avec input hors domaine → erreur gérée
- [ ] Flux end-to-end : predict → vérifier l'écriture en DB
- [ ] `GET /predictions` retourne la liste avec les prédictions insérées

### 5. Cas limites et erreurs
- [ ] Input vide / partiel / mal typé
- [ ] Valeurs extrêmes (min/max)
- [ ] Volume important (si pertinent)
- [ ] DB indisponible → gestion propre
- [ ] Modèle absent → message clair

### 6. Couverture
- [ ] Lancer `pytest --cov=app --cov-report=term-missing --cov-report=html`
- [ ] Viser une couverture significative (ex : > 80%)
- [ ] Sauvegarder le rapport HTML dans `htmlcov/`
- [ ] Ajouter la commande au pipeline CI (étape 2)

### 7. Reproductibilité
- [ ] Fixer les seeds aléatoires si nécessaire
- [ ] Tests isolés les uns des autres (pas de dépendances d'ordre)
- [ ] Nettoyage DB entre tests (fixtures `scope="function"`)

## Résultats attendus
- [ ] Scripts de tests unitaires ET fonctionnels
- [ ] Suite couvrant cas critiques + scénarios d'erreur
- [ ] Rapport de couverture généré (pytest-cov)
- [ ] Points faibles identifiés et corrigés
- [ ] Tests intégrés au pipeline CI

## Points de vigilance
- **Complétude** de la couverture des scénarios
- **Reproductibilité** des résultats (pas de flakiness)
- **Présence** de tous les rapports de tests dans les livrables

## Outils
- Pytest
- Pytest-cov (couverture)
- Pydantic
- HTTPX / TestClient FastAPI

## Ressources
- Documentation Pytest
- Documentation sur la couverture de tests

## Checkpoint mentor
À la fin de cette étape, faire le point avec le mentor pour valider la suite de tests et la couverture.

## Statut global étape : **À FAIRE**
