# Étape 6 — Documenter le modèle de Machine Learning

## Objectif
Créer une documentation complète et accessible permettant aux utilisateurs et aux développeurs de **comprendre, utiliser et maintenir** le modèle ML et son API.

## Prérequis
- [ ] Compétences rédactionnelles techniques
- [ ] Compréhension approfondie du projet
- [ ] Toutes les étapes précédentes quasi terminées

## Tâches à réaliser

### 1. README principal du repo
- [ ] Utiliser le template README fourni dans les ressources
- [ ] Titre + badges (CI, couverture, licence, version)
- [ ] Description courte + contexte projet (Futurisys)
- [ ] Screenshot / schéma d'architecture
- [ ] Section **Installation**
  - [ ] Prérequis (Python, PostgreSQL, etc.)
  - [ ] Clonage, venv, dépendances
  - [ ] Configuration des variables d'environnement
- [ ] Section **Utilisation**
  - [ ] Lancement en local
  - [ ] Exemples d'appels API
- [ ] Section **Déploiement** (Hugging Face Spaces ou autre)
- [ ] Section **Authentification et sécurisation**
- [ ] Section **Tests** (comment lancer, comment lire la couverture)
- [ ] Section **Contribution** (conventions de branches/commits)
- [ ] Licence, auteur, remerciements

### 2. Documentation de l'API
- [ ] Vérifier que Swagger/OpenAPI (`/docs`) est complet et à jour
- [ ] Chaque endpoint a : description, paramètres, exemples, codes retour
- [ ] Exporter un snapshot OpenAPI (`openapi.json`) si utile
- [ ] Ajouter des exemples `curl` / `httpie` / Python dans la doc

### 3. Documentation technique du modèle
- [ ] Fiche technique du modèle :
  - [ ] Origine (P3 ou P4)
  - [ ] Type d'algorithme
  - [ ] Features d'entrée (liste + types + contraintes)
  - [ ] Cible / sortie
  - [ ] Métriques de performance (sur jeu de test)
  - [ ] Limites connues
- [ ] Protocole de **mise à jour régulière** du modèle
- [ ] Procédure de redéploiement
- [ ] Procédure de monitoring (si applicable)

### 4. Documentation de l'architecture
- [ ] Schéma global (API ↔ DB ↔ Modèle)
- [ ] Description des composants
- [ ] Justification des choix techniques (FastAPI, PostgreSQL, SQLAlchemy, HF Spaces)
- [ ] Flux de données (d'un appel API jusqu'au stockage DB)

### 5. Documentation développeur (optionnel MkDocs/Sphinx)
- [ ] Mettre en place MkDocs ou Sphinx si souhaité
- [ ] Générer automatiquement la doc depuis les docstrings
- [ ] Publier sur GitHub Pages / HF Spaces

### 6. Finalisation
- [ ] Relire la documentation pour clarté et exhaustivité
- [ ] Vérifier qu'un nouveau développeur peut installer et lancer le projet en suivant le README
- [ ] Vérifier qu'un utilisateur peut appeler l'API avec les exemples fournis
- [ ] S'assurer que le dossier `docs/` reflète l'état final du projet

### 7. Support de présentation soutenance
- [ ] Créer le support de présentation pour Aurélien
- [ ] Contenu suggéré :
  - Contexte et objectif
  - Modèle choisi et pourquoi
  - Architecture globale
  - Démo API
  - CI/CD et déploiement
  - Tests et couverture
  - Retours d'expérience / améliorations possibles

## Résultats attendus
- [ ] Documentation de l'API (Swagger + README)
- [ ] Documentation technique du modèle, performances, maintenance
- [ ] README informatif sur le repo git et son déploiement
- [ ] Support de présentation soutenance

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

## Statut global étape : **À FAIRE**
