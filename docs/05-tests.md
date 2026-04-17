# Étape 5 — Développer des tests unitaires et fonctionnels

## Objectif
Garantir la fiabilité et la robustesse du modèle ML et de son API via une suite complète de tests :
- **Tests unitaires** : validation des composants individuels
- **Tests fonctionnels** : évaluation du modèle en conditions réelles

## Prérequis
- [x] Connaissance des principes de tests unitaires
- [x] Compréhension approfondie du modèle ML utilisé
- [x] Familiarité avec Pytest
- [x] Jeux de données représentatifs disponibles

## Tâches à réaliser

### 1. Mise en place
- [x] Installer `pytest`, `pytest-cov`, `httpx` (optional-dependencies `dev` dans `pyproject.toml`)
- [x] Créer l'arborescence `tests/`
  ```
  tests/
  ├── __init__.py
  ├── conftest.py                     # fixtures partagées (SQLite test DB, client, sample_input)
  ├── unit/
  │   ├── test_schemas.py
  │   ├── test_preprocessing.py
  │   ├── test_service.py
  │   └── test_db_models.py
  └── functional/
      ├── test_api_health.py
      ├── test_api_predict.py
      └── test_api_predictions.py
  ```
- [x] Configurer `pyproject.toml` (`[tool.pytest.ini_options]` + `[tool.coverage.*]`)

### 2. Fixtures
- [x] Fixture `client` : TestClient FastAPI
- [x] Fixture `db_session` : SQLite file-based isolé (nettoyé entre tests)
- [x] Fixture `sample_input` : payload valide pour `/predict`
- [x] Fixture `sample_employee` : insère un `Dataset` pour tester `/predict/employee/{id}`
- [x] Fixture `engine` session-scoped pour bootstrapper le schéma une fois
- [ ] Fixture dédiée `loaded_model` (inutile — le singleton `load_model()` est partagé)

### 3. Tests unitaires
- [x] **Schemas Pydantic** : input valide, bornes min/max, énums, champ manquant
- [x] **Model loader** : singleton `load_model()` renvoie la même instance
- [x] **Service de prédiction** : shape du résultat, seuil, cohérence `risk_level`, persistance
- [x] **Preprocessing** : colonnes attendues, encodage binaire/ordinal/one-hot, features engineered
- [x] **Modèles ORM** : insert/lecture `Dataset` + `Prediction`, contrainte `id_employee` unique

### 4. Tests fonctionnels (API)
- [x] `GET /health` retourne 200
- [x] `GET /` redirige vers `/docs`
- [x] `GET /model/info` retourne les métadonnées attendues
- [x] `POST /predict` avec input valide → 200 + prédiction
- [x] `POST /predict` avec input invalide → 422 (age hors bornes, énum invalide, champ manquant)
- [x] `POST /predict/employee/{id}` → 200 si employé existe, 404 sinon
- [x] Flux end-to-end : predict → vérifier l'écriture en DB
- [x] `GET /predictions` liste + pagination (`skip`, `limit`)
- [x] `GET /predictions/{id}` détail + 404 si inconnu

### 5. Cas limites et erreurs
- [x] Input partiel / mal typé (couvert par les tests `/predict` et schemas)
- [x] Valeurs extrêmes (min/max via paramétrage Pydantic)
- [x] Employé inconnu → 404 géré
- [x] Prédiction inconnue → 404 géré
- [ ] DB indisponible → non testé (sortirait du scope unitaire)
- [ ] Modèle absent → non testé (le CI assure la présence de l'artefact)

### 6. Couverture
- [x] Lancer `pytest --cov=app --cov-report=term-missing`
- [x] Couverture atteinte : **88 %** (objectif ≥ 80 %)
- [x] Rapport HTML générable via `--cov-report=html`
- [x] Commande `pytest --cov=app` déjà intégrée au pipeline CI (`ci-cd.yml`)

### 7. Reproductibilité
- [x] Pas d'aléa introduit par les tests (entrées déterministes)
- [x] Tests isolés (fixture `_clean_tables` autouse, scope function)
- [x] Nettoyage DB entre tests (TRUNCATE des tables avant chaque test)

## Résultats attendus
- [x] Scripts de tests unitaires ET fonctionnels (51 tests)
- [x] Suite couvrant cas critiques + scénarios d'erreur (422, 404)
- [x] Rapport de couverture généré (pytest-cov, 88 %)
- [x] Points faibles identifiés : branches `risk_level` rarement activées avec le profil type
- [x] Tests intégrés au pipeline CI (job `test` dans `ci-cd.yml`)

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

## Statut global étape : **TERMINÉE** — 51 tests, couverture 88 %, intégrée à la CI.
