# Étape 6 — Documenter le modèle de Machine Learning

## Objectif
Créer une documentation complète et accessible permettant aux utilisateurs et aux développeurs de **comprendre, utiliser et maintenir** le modèle ML et son API.

## Prérequis
- [ ] Compétences rédactionnelles techniques
- [ ] Compréhension approfondie du projet
- [ ] Toutes les étapes précédentes quasi terminées

## Tâches à réaliser

### 1. README principal du repo
- [x] Titre + badges (CI, couverture, Python, licence)
- [x] Description courte + contexte projet (Futurisys)
- [x] Schéma d'architecture (Mermaid — composants + flux `/predict`)
- [x] Section **Installation** (prérequis, clone, venv, deps, `.env`)
- [x] Section **Utilisation** (local, Docker, Compose) + exemples curl / Python pour les 4 endpoints
- [x] Section **Déploiement** (pipeline CI/CD, secrets, HF Spaces, rollback)
- [x] Section **Authentification et sécurisation** (état POC + contrôles production à prévoir)
- [x] Section **Tests** (commandes, couverture 88 %, lien vers `05-tests.md`)
- [x] Section **Conventions** (branches, Conventional Commits, SemVer)
- [x] Licence, auteur
- [ ] Screenshot Swagger (facultatif — à capturer manuellement)

### 2. Documentation de l'API
- [x] Swagger/OpenAPI (`/docs`) complet et à jour (réponses + exemples via Pydantic)
- [x] Chaque endpoint a : description, paramètres, exemples, codes retour (dans les docstrings FastAPI)
- [x] Exemples `curl` et Python fournis dans le README
- [ ] Export d'un snapshot `openapi.json` (facultatif — accessible live sur `/openapi.json`)

### 3. Documentation technique du modèle
- [x] Fiche technique du modèle : [`docs/07-model-card.md`](07-model-card.md)
  - [x] Origine (Projet 4)
  - [x] Type d'algorithme (CatBoostClassifier)
  - [x] Features d'entrée (24 champs bruts → 40 features après preprocessing)
  - [x] Cible / sortie (Oui/Non + probabilité + risk_level)
  - [x] Métriques de performance sur jeu de test (accuracy 0.79, recall 0.68, ROC AUC 0.81)
  - [x] Limites connues (dataset synthétique, biais potentiels, pas d'explicabilité)
- [x] Protocole de **mise à jour régulière** du modèle (section dédiée dans la fiche)
- [x] Procédure de redéploiement (README + fiche)
- [x] Procédure de monitoring suggérée (section dans la fiche)

### 4. Documentation de l'architecture
- [x] Schéma global (Mermaid dans README : API ↔ DB ↔ Modèle)
- [x] Flux de données d'un appel `/predict` (séquence Mermaid)
- [x] Description des composants (README)
- [x] Justification des choix techniques (tableau stack dans README)
- [x] Schéma ERD de la base (Mermaid dans `04-postgresql.md`)

### 5. Documentation développeur (optionnel MkDocs/Sphinx)
- [ ] MkDocs / Sphinx — non mis en place (Markdown GitHub suffit pour le POC)

### 6. Finalisation
- [x] Relecture de la documentation (cohérence README ↔ docs/ ↔ fiche modèle)
- [x] Un nouveau dev peut installer et lancer le projet en suivant le README
- [x] Un utilisateur peut appeler l'API avec les exemples fournis
- [x] `docs/` reflète l'état final du projet (tableau de suivi à jour)

### 7. Support de présentation soutenance
- [ ] Créer le support de présentation pour Aurélien — *à faire dans un outil dédié (Slides / Canva) ; contenu déjà structuré dans le projet*
- [ ] Contenu suggéré :
  - Contexte et objectif
  - Modèle choisi et pourquoi (cf. fiche modèle)
  - Architecture globale (cf. README)
  - Démo API (Swagger live sur HF Space)
  - CI/CD et déploiement (cf. README section Déploiement)
  - Tests et couverture (51 tests, 88 %)
  - Retours d'expérience / améliorations (cf. section Sécurisation)

## Résultats attendus
- [x] Documentation de l'API (Swagger + README avec exemples)
- [x] Documentation technique du modèle, performances, maintenance ([fiche](07-model-card.md))
- [x] README informatif sur le repo git et son déploiement
- [ ] Support de présentation soutenance — à construire dans l'outil de présentation

## Points de vigilance
- **Clarté et exhaustivité** des explications
- La doc doit être **à jour** au moment de la soutenance
- Tester les instructions d'installation sur un environnement propre

## Outils
- Swagger / OpenAPI (intégré à FastAPI)
- Markdown (README)
- MkDocs (documentation)
- Sphinx (documentation Python)

## Ressources
- Template de README de qualité
- Documentation MkDocs
- Documentation Sphinx

## Fiche d'autoévaluation
Consulter la fiche d'autoévaluation de la mission avant l'envoi des livrables pour s'assurer que rien n'a été oublié.

## Statut global étape : **QUASI TERMINÉE** — reste le support de soutenance (à faire dans un outil de présentation) et un screenshot Swagger facultatif.
