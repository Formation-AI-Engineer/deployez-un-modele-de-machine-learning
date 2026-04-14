# Journal de bord — Projet 5 : Déployez un modèle de Machine Learning

Ce document retrace **pas à pas** tout le travail réalisé, les choix techniques effectués, et le raisonnement derrière chaque décision.

---

## Contexte du projet

**Mission** : déployer un modèle de machine learning en production pour le client fictif **Futurisys** (directeur technique : Aurélien).

**Modèle choisi** : le modèle du **Projet 4** — prédiction d'attrition des employés chez TechNova Partners. C'est un problème de **classification binaire** : un employé va-t-il quitter l'entreprise (Oui/Non) ?

**Algorithme retenu** : `CatBoostClassifier` avec des hyperparamètres optimisés par `RandomizedSearchCV` dans le notebook P4.

**Plateforme de déploiement** : Hugging Face Spaces (Docker blank template) — URL : https://huggingface.co/spaces/lcamara/deployMLModel

---

## Étape 1 — Gestion de version et collaboration

### 1.1 Création et clonage du dépôt

**Action** : clonage du dépôt GitHub vide `Formation-AI-Engineer/deployez-un-modele-de-machine-learning`.

**Pourquoi** : la mission exige un dépôt Git structuré avec un historique clair. Partir d'un dépôt distant (plutôt que `git init` local) garantit que la remote est configurée dès le départ et facilite la collaboration.

```bash
git clone git@github.com:Formation-AI-Engineer/deployez-un-modele-de-machine-learning.git repo
```

### 1.2 Création du `.gitignore`

**Action** : rédaction d'un `.gitignore` complet et spécifique au projet.

**Pourquoi** : éviter de committer des fichiers qui n'ont rien à faire dans un dépôt :
- **Environnements virtuels** (`.venv/`, `venv/`) : chaque développeur crée le sien localement.
- **Secrets** (`.env`, `*.pem`) : **JAMAIS de credentials dans Git**. C'est une règle de sécurité non-négociable.
- **Artefacts ML** (`*.pkl`, `*.joblib`, `*.cbm`) : les modèles sérialisés sont lourds et reproductibles via le script d'entraînement. On les régénère plutôt que de les versionner.
- **Cache Python** (`__pycache__/`) : fichiers générés automatiquement, inutiles dans le dépôt.
- **IDE** (`.idea/`, `.vscode/`) : configuration spécifique à chaque développeur.
- **Logs CatBoost** (`catboost_info/`) : dossier de logs d'entraînement, non pertinent pour le dépôt.

Les fichiers CSV du dataset (`data/*.csv`) sont **volontairement trackés** car ils sont petits (~220 KB au total) et nécessaires pour l'entraînement dans le Dockerfile.

### 1.3 Structure du projet

**Action** : création d'une arborescence claire et modulaire.

```
├── app/                  # Code de l'API FastAPI
│   ├── routes/           # Endpoints (chaque fichier = un groupe de routes)
│   ├── services/         # Logique métier (prédiction, chargement modèle)
│   └── schemas/          # Modèles Pydantic (validation entrées/sorties)
├── db/                   # Scripts DB, modèles ORM (étape 4)
├── models/               # Modèle ML sérialisé (.cbm, gitignored)
├── data/                 # Datasets CSV (trackés car petits)
├── tests/
│   ├── unit/             # Tests unitaires isolés
│   └── functional/       # Tests end-to-end de l'API
├── scripts/              # Scripts utilitaires (entraînement, seed DB, etc.)
├── docs/                 # Documentation et suivi par étape
├── .github/workflows/    # Pipelines CI/CD
├── pyproject.toml        # Dépendances et configuration outillage
├── Dockerfile            # Image Docker pour HF Spaces
├── README.md             # Point d'entrée documentation
└── .gitignore
```

**Pourquoi cette structure** :
- **Séparation des responsabilités** : le code API (`app/`), les tests (`tests/`), les données (`data/`), les scripts (`scripts/`) et la documentation (`docs/`) sont clairement séparés. Un nouveau développeur comprend immédiatement où chercher.
- **`app/` avec sous-dossiers** : on suit le pattern courant FastAPI — `routes` (endpoints), `schemas` (validation Pydantic), `services` (logique métier). Cela évite un fichier `main.py` monolithique de 500 lignes.
- **`tests/unit/` vs `tests/functional/`** : distinction claire entre les tests qui vérifient un composant isolé et ceux qui testent le flux complet (appel API → prédiction → réponse).
- **`scripts/`** : on ne met pas le script d'entraînement dans `app/` car ce n'est pas du code qui tourne en production — c'est un utilitaire qu'on lance une fois pour générer le modèle.

### 1.4 Choix de `pyproject.toml` (et non `requirements.txt`)

**Action** : création d'un `pyproject.toml` au format PEP 621 avec le build backend `hatchling`.

**Pourquoi `pyproject.toml`** :
- C'est le **standard moderne** (PEP 621, adopté par pip, uv, hatch, poetry, etc.). `requirements.txt` est encore utilisé mais c'est un format plus ancien et moins expressif.
- On peut y déclarer **tout au même endroit** : métadonnées du projet, dépendances, configuration de Pytest, Ruff, coverage, etc. Pas besoin de `setup.cfg`, `pytest.ini`, `.flake8` séparés.
- Les **dépendances optionnelles** (`[dev]`, `[docs]`) permettent à un utilisateur d'installer uniquement ce dont il a besoin : `pip install .` pour la prod, `pip install ".[dev]"` pour le développement.

**Pourquoi `hatchling`** : c'est un build backend simple, rapide, et sans configuration lourde. Il supporte nativement PEP 621. Plus léger que Poetry (qui impose son propre écosystème) tout en étant plus moderne que setuptools.

**Stratégie de versioning des dépendances** : on utilise des bornes `>=min,<max` (ex : `fastapi>=0.115,<1.0`). Cela signifie :
- On accepte les mises à jour mineures/patch (corrections de bugs, nouvelles features non-breaking).
- On se protège des changements majeurs (breaking changes).

### 1.5 Conventions de branches et commits

**Action** : définition et documentation dans le README de conventions claires.

**Branches** :
- `main` : branche stable, protégée (la CI doit passer avant merge)
- `dev` : branche d'intégration, point de départ des features
- `feature/<nom>` : une branche par fonctionnalité
- `fix/<nom>` : corrections de bugs
- `docs/<nom>` : documentation uniquement

**Pourquoi ce workflow** : c'est un dérivé simplifié de **Git Flow**. `main` reste toujours dans un état déployable. Le développement se fait sur `dev` puis les features sont mergées dans `dev`, puis `dev` dans `main` quand c'est stable. Cela évite de casser `main` avec du code en cours.

**Commits** : format [Conventional Commits](https://www.conventionalcommits.org/fr/v1.0.0/) :
```
<type>(<scope>): <description>
```
Types utilisés : `feat`, `fix`, `docs`, `test`, `refactor`, `chore`, `ci`.

**Pourquoi** : un historique de commits lisible permet de comprendre l'évolution du projet sans lire chaque diff. C'est aussi ce que les évaluateurs vont regarder.

### 1.6 Tag `v0.1.0`

**Action** : création d'un tag annoté `v0.1.0` sur le premier commit de `main`.

**Pourquoi** : la mission demande explicitement l'utilisation de tags pour la gestion des versions. On suit **SemVer** (Semantic Versioning) :
- `0.1.0` = version initiale, structure du projet en place, pas encore de fonctionnalité.
- Le `0.x.x` indique que le projet est en développement actif (pas encore stable pour la prod).

Un tag **annoté** (vs léger) contient un message et un auteur — c'est la bonne pratique pour les releases.

```bash
git tag -a v0.1.0 -m "v0.1.0 — initial project scaffold"
git push origin v0.1.0
```

---

## Étape 2 — Configuration CI/CD

### 2.1 Pipeline CI/CD unifié : `.github/workflows/ci-cd.yml`

**Action** : création d'un workflow GitHub Actions **unique** déclenché sur `push` (main, dev, tags `v*`) et `pull_request` (main).

**Pourquoi un seul fichier** (et non `ci.yml` + `cd.yml` séparés) : avec deux fichiers, les workflows se déclenchaient en parallèle — le CD pouvait déployer avant même que la CI ne finisse. En fusionnant tout dans un seul workflow avec `needs`, on garantit l'ordre d'exécution : lint → tests → deploy. C'est aussi plus simple à maintenir.

**Architecture du pipeline** :
```
push/PR → [Job: lint] → [Job: test] → [Job: deploy]
```

Chaque job dépend du précédent (`needs`). Si le lint échoue, les tests ne se lancent pas. Si les tests échouent, pas de déploiement.

**Job `lint`** :
1. Checkout du code
2. Installation Python 3.11 + cache pip (accélère les runs suivants)
3. `ruff check .` : vérifie les erreurs de style et les imports inutilisés
4. `ruff format --check .` : vérifie le formatage sans modifier les fichiers

**Pourquoi Ruff** (et non flake8/black/isort) : Ruff remplace flake8, isort ET black en un seul outil, écrit en Rust, **100x plus rapide**. C'est devenu le standard de facto en 2024-2026. Un seul outil = une seule config dans `pyproject.toml`.

**Job `test`** :
1. Installation identique
2. `pytest --cov=app --cov-report=term-missing --cov-report=xml` : exécution des tests avec rapport de couverture
3. Upload du rapport XML comme artefact (exploitable par d'autres outils si besoin)

**Pourquoi le cache pip** : sans cache, chaque run télécharge et installe toutes les dépendances (~2-3 min). Avec le cache, c'est quasi-instantané si le `pyproject.toml` n'a pas changé. La clé de cache est basée sur le hash du fichier : `${{ hashFiles('pyproject.toml') }}`.

**Job `deploy`** :
1. Checkout du code (avec `fetch-depth: 0` pour l'historique complet)
2. Push vers le dépôt Git du Space HF via HTTPS

Le job `deploy` ne s'exécute que sur `main` ou un tag `v*` (condition `if`). Sur `dev` ou les PR, seuls lint + test tournent.

**Mécanisme de déploiement** : on pousse le code directement dans le dépôt Git du Space HF. C'est le mode de déploiement natif de HF Spaces — quand le repo du Space reçoit un push, il rebuild automatiquement le Docker et relance l'app.

**Secrets utilisés** :
- `HF_TOKEN` : token d'authentification Hugging Face (accès en écriture)
- `HF_SPACE_ID` : identifiant du Space (`lcamara/deployMLModel`)

### 2.3 Fichier `.env.example`

**Action** : création d'un `.env.example` documentant les variables d'environnement nécessaires.

**Pourquoi `.env.example`** (et non `.env`) : le `.env` contient les vraies valeurs (tokens, mots de passe) et est **gitignored**. Le `.env.example` contient des valeurs fictives et sert de **documentation** pour tout développeur qui clone le projet — il sait immédiatement quelles variables configurer.

```env
DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/ml_deploy
HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxx
HF_SPACE_ID=Formation-AI-Engineer/deployez-un-modele-de-machine-learning
APP_ENV=dev  # dev | test | prod
```

### 2.4 Test placeholder

**Action** : création d'un `tests/unit/test_placeholder.py` minimal (`assert True`).

**Pourquoi** : le pipeline CI exécute `pytest` à chaque push. Sans aucun test, pytest retourne une erreur (exit code 5 = "no tests collected") et le pipeline échoue. Le placeholder garantit que la CI passe dès le premier push, en attendant les vrais tests (étape 5).

### 2.5 Ce qui reste à faire manuellement (hors code)

Certaines actions ne peuvent pas être scriptées et doivent être faites via l'interface GitHub/HF :
1. **Protection de la branche `main`** sur GitHub (Settings > Branches)
2. **Création des secrets** dans GitHub Actions (Settings > Secrets)
3. **Test du déploiement E2E** vers HF Spaces

---

## Étape 3 — Développement de l'API FastAPI

### 3.1 Analyse du notebook P4

**Démarche** : avant d'écrire la moindre ligne de code pour l'API, j'ai lu en détail le notebook du Projet 4 pour comprendre :

1. **Comment les données sont chargées et fusionnées** :
   - 3 fichiers CSV (`extrait_sirh.csv`, `extrait_eval.csv`, `extrait_sondage.csv`)
   - Nettoyage : la colonne `augementation_salaire_precedente` contient des valeurs comme `"11 %"` → nettoyées en `11.0`
   - Fusion par jointure interne sur `id_employee`
   - Suppression de colonnes constantes (toujours la même valeur → aucune information)

2. **Comment les features sont construites** (feature engineering) :
   - `ratio_anciennete_experience` = ancienneté / expérience totale
   - `satisfaction_moyenne` = moyenne des 4 scores de satisfaction
   - `ecart_evaluation` = note actuelle − note précédente
   - `anciennete_sans_promotion` = ancienneté − années depuis dernière promotion

3. **Comment les variables catégorielles sont encodées** :
   - Binaire : `genre` (F→0, M→1), `heure_supplementaires` (Non→0, Oui→1)
   - Ordinal : `frequence_deplacement` (Aucun→0, Occasionnel→1, Frequent→2)
   - One-hot : `statut_marital`, `departement`, `poste`, `domaine_etude` (avec `drop_first=True`)

4. **Le modèle final** :
   - `CatBoostClassifier` avec hyperparamètres optimisés : `iterations=300, depth=4, learning_rate=0.01, l2_leaf_reg=10, border_count=32, auto_class_weights='Balanced'`
   - Seuil de décision = 0.5 (le seuil optimal ~0.5066 n'apportait aucun gain significatif)
   - Pas de Pipeline sklearn — tout est fait manuellement

5. **Les 40 features exactes** attendues par le modèle après encoding.

**Pourquoi cette analyse est critique** : si l'API envoie au modèle des features dans un ordre différent, ou avec un encoding différent, les prédictions seront **fausses mais silencieuses** (pas d'erreur, juste des résultats incohérents). C'est un piège classique du déploiement ML.

### 3.2 Script d'entraînement : `scripts/train_model.py`

**Action** : création d'un script autonome qui reproduit exactement le pipeline du notebook.

**Pourquoi un script séparé** (et non le notebook directement) :
- Un notebook n'est pas exécutable dans un pipeline CI/CD ou un Dockerfile de manière fiable.
- Le script est **déterministe** : `random_seed=42`, `test_size=0.2`, `stratify=y` — on obtient toujours le même résultat.
- Il produit un fichier `.cbm` (format natif CatBoost) qui est plus compact et rapide à charger qu'un pickle.

**Format `.cbm`** : CatBoost a son propre format de sérialisation, optimisé pour le chargement rapide. Avantage par rapport à `joblib`/`pickle` : pas de dépendance à la version exacte de scikit-learn, et sécurité (pickle peut exécuter du code arbitraire à la désérialisation).

**Résultats de l'entraînement** :
- Train accuracy : 84.69%
- Test accuracy : 78.91%
- Écart (overfitting gap) : ~5.8% — acceptable, le modèle généralise correctement.

### 3.3 Preprocessing : `app/preprocessing.py`

**Action** : reproduction exacte du pipeline de preprocessing du notebook, sous deux formes :

1. **`load_and_merge()` + `prepare_features()` + `encode_features()`** : pour l'entraînement en batch (utilisé par `train_model.py`).

2. **`preprocess_single(data: dict)`** : pour la prédiction unitaire via l'API. Prend un dictionnaire de features brutes (valeurs humaines lisibles) et retourne un DataFrame à 1 ligne avec les 40 features encodées dans le bon ordre.

**Pourquoi `preprocess_single` en plus** : lors de l'entraînement, `pd.get_dummies()` crée les colonnes one-hot automatiquement à partir de toutes les valeurs présentes dans le dataset. Mais pour une prédiction unitaire, si un employé est "Marié(e)", `get_dummies` ne créerait que la colonne `statut_marital_Marié(e)` et oublierait `statut_marital_Divorcé(e)`. On doit donc créer **toutes** les 40 colonnes manuellement et mettre à 1 la bonne.

**`EXPECTED_FEATURES`** : liste ordonnée des 40 noms de features telle que le modèle les attend. C'est la **source de vérité** — on réordonne toujours le DataFrame selon cette liste avant de prédire. Si une colonne manque, elle est remplie à 0 (ce qui correspond à la catégorie de référence pour les one-hot).

### 3.4 Schemas Pydantic : `app/schemas/prediction.py`

**Action** : définition de `PredictionInput`, `PredictionOutput`, et `ModelInfo` avec validation stricte.

**Choix de design** :

- **Enums pour les catégorielles** : plutôt que d'accepter n'importe quelle string, on utilise des `Enum` Python (`Genre`, `Departement`, `Poste`, etc.). Avantages :
  - Swagger UI affiche un dropdown avec les valeurs possibles → meilleure UX
  - Erreur 422 immédiate si la valeur n'est pas dans la liste → pas de surprise silencieuse
  - Documentation auto-générée

- **Bornes numériques** (`ge`, `le` sur les `Field`) : `age` doit être entre 18 et 65, `satisfaction_*` entre 1 et 4, etc. Cela empêche l'envoi de valeurs absurdes qui donneraient des prédictions sans sens.

- **`example` sur chaque champ** : Swagger UI pré-remplit le formulaire d'essai avec ces valeurs → un utilisateur peut tester l'API en un clic.

- **`PredictionOutput` avec `risk_level`** : en plus de la prédiction brute (Oui/Non) et de la probabilité, on ajoute un **niveau de risque** humainement lisible (faible/modéré/élevé). C'est plus actionnable pour un RH que `probability: 0.4237`.

### 3.5 Service de prédiction : `app/services/prediction.py`

**Action** : module qui charge le modèle et exécute les prédictions.

**Pattern singleton** pour le chargement du modèle :
```python
_model: CatBoostClassifier | None = None

def load_model():
    global _model
    if _model is None:
        _model = CatBoostClassifier()
        _model.load_model(str(MODEL_PATH))
    return _model
```

**Pourquoi** : charger un modèle CatBoost depuis le disque prend ~100ms. Si on le rechargeait à chaque requête, on ajouterait 100ms de latence inutile. Le singleton charge le modèle **une seule fois** au démarrage (`@app.on_event("startup")`) et le réutilise ensuite.

**Niveaux de risque** : seuils choisis pragmatiquement :
- `< 0.3` → faible
- `0.3 à 0.6` → modéré
- `> 0.6` → élevé

### 3.6 Routes : `app/routes/predict.py`

**Action** : 2 endpoints dans un router dédié.

| Endpoint | Méthode | Rôle |
|----------|---------|------|
| `/predict` | POST | Prédiction d'attrition pour un employé |
| `/model/info` | GET | Métadonnées du modèle (version, algo, nb features) |

**Pourquoi un router séparé** : FastAPI permet de grouper les routes par `APIRouter`. Cela rend le code modulaire — on pourra ajouter des routes DB (étape 4) dans un fichier séparé sans toucher aux routes de prédiction.

### 3.7 Point d'entrée : `app/main.py`

**Action** : configuration de l'application FastAPI.

Points notables :
- **Description riche** : le titre, la description et la version apparaissent sur Swagger UI (`/docs`). C'est la première chose qu'un utilisateur voit.
- **`@app.on_event("startup")`** : charge le modèle au démarrage. Si le fichier `.cbm` est absent, l'API crash immédiatement avec un message clair plutôt que de crasher à la première requête.
- **`/health`** : endpoint de healthcheck standard. C'est ce que les orchestrateurs (Docker, Kubernetes, HF Spaces) utilisent pour savoir si l'API est vivante.

### 3.8 Dockerfile

**Action** : image Docker multi-étapes optimisée.

```dockerfile
FROM python:3.10-slim
# ... install deps, copy code, train model
EXPOSE 7860
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
```

**Choix techniques** :
- **`python:3.10-slim`** : image légère (~150 MB vs ~900 MB pour l'image complète). Suffisante pour notre usage.
- **Port 7860** : c'est le port par défaut attendu par Hugging Face Spaces.
- **`RUN python scripts/train_model.py`** dans le Dockerfile : le modèle est entraîné à la construction de l'image. Avantage : pas besoin de stocker le fichier `.cbm` dans Git (il est gitignored). Inconvénient : le build prend quelques secondes de plus.
- **Copie du `pyproject.toml` d'abord** : Docker met en cache les couches. Si seul le code change (pas les dépendances), Docker réutilise la couche d'installation des deps → build beaucoup plus rapide.

### 3.9 Tests manuels

Avant de committer, j'ai vérifié **chaque endpoint** en local :

```bash
# Lancement
uvicorn app.main:app --port 8000

# Health check
curl http://localhost:8000/health
# → {"status":"ok"}

# Info modèle
curl http://localhost:8000/model/info
# → {"model_name":"CatBoost Attrition Classifier", ...}

# Prédiction — profil à risque (jeune, insatisfait, heures sup, célibataire)
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{...}'
# → {"prediction":"Oui","probability":0.8609,"risk_level":"élevé"}

# Prédiction — profil stable (expérimenté, satisfait, pas d'heures sup, marié)
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{...}'
# → {"prediction":"Non","probability":0.1321,"risk_level":"faible"}

# Validation — input invalide (age: 200, champs manquants)
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{"age":200}'
# → 422 avec messages d'erreur détaillés pour chaque champ
```

Les prédictions sont cohérentes avec les connaissances métier sur l'attrition : un profil jeune, insatisfait, avec des heures supplémentaires est bien identifié comme à risque élevé.

---

## Historique Git

| Commit | Type | Description |
|--------|------|-------------|
| `06244a6` | `chore` | Initial project scaffold (structure, pyproject.toml, README, docs/) |
| `a8187fc` | `docs` | Mark git/versioning step as completed |
| `863735b` | `ci` | Add GitHub Actions CI/CD pipelines (ci.yml, cd.yml, .env.example) |
| `1e9994d` | `feat` | Add FastAPI app with CatBoost attrition prediction |

**Tag** : `v0.1.0` sur le commit initial.

**Branches** : `main`, `dev`, `feature/cicd`, `feature/api`.

---

## Prochaines étapes

| # | Étape | Statut |
|---|-------|--------|
| 1 | Gestion de version & collaboration | **Terminée** |
| 2 | Configuration CI/CD | **Quasi terminée** (reste config manuelle GitHub/HF) |
| 3 | Développement de l'API | **Terminée** |
| 4 | Base de données PostgreSQL | À faire |
| 5 | Tests unitaires & fonctionnels | À faire |
| 6 | Documentation | À faire |
