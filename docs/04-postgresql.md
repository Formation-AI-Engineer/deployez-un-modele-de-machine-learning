# Étape 4 — Insérer le dataset et le gérer via PostgreSQL

## Objectif
Créer une base PostgreSQL via un script SQL (ou Python) pour y insérer le dataset complet.
**Toutes les interactions avec le modèle ML devront passer par la base de données** : inputs envoyés au modèle et outputs générés doivent être enregistrés dans des tables dédiées.

L'interaction avec la DB peut rester **entièrement locale** pour simplifier.

## Prérequis
- [ ] Connaissance de base de PostgreSQL et des concepts relationnels
- [ ] Familiarité avec un ORM (SQLAlchemy recommandé)
- [ ] Compréhension des interactions API ↔ base de données
- [ ] Dataset du projet P3 ou P4 disponible
- [ ] PostgreSQL installé en local (ou conteneur Docker)

## Tâches à réaliser

### 1. Modélisation de la base
- [ ] Concevoir le schéma des tables nécessaires :
  - Table `dataset` (données brutes source)
  - Table `predictions_input` (inputs envoyés au modèle)
  - Table `predictions_output` (outputs générés par le modèle)
  - (Optionnel) Table de liaison ou colonne FK entre input/output
  - (Optionnel) Table `model_metadata` (version, date d'entraînement)
- [ ] Identifier les types de colonnes, clés primaires, contraintes
- [ ] Produire un schéma UML (diagramme) → à placer dans `docs/` ou `db/`

### 2. Scripts de création
- [ ] Créer `db/create_db.py` OU `db/schema.sql`
- [ ] Script de création de la base (CREATE DATABASE)
- [ ] Script de création des tables (CREATE TABLE)
- [ ] Script d'insertion du dataset (import du CSV d'origine)
- [ ] Documenter comment exécuter ces scripts

### 3. Intégration avec l'API (SQLAlchemy)
- [ ] Installer `sqlalchemy` + `psycopg2-binary` (ou `psycopg[binary]` v3)
- [ ] Créer `db/database.py` : engine + session
- [ ] Créer `db/models.py` : modèles ORM correspondant aux tables
- [ ] Créer une dépendance FastAPI `get_db()` pour injecter la session
- [ ] Gérer la configuration via variables d'environnement (`.env` + Pydantic Settings)

### 4. Enregistrement systématique des échanges
- [ ] À chaque appel de `/predict` : enregistrer l'input dans la DB
- [ ] Enregistrer l'output (prédiction + timestamp + version modèle)
- [ ] Lier input et output par une clé
- [ ] Gérer les erreurs pour ne jamais laisser d'état incohérent (transactions)

### 5. Endpoints d'interrogation
- [ ] `GET /predictions` : liste des prédictions récentes (avec pagination)
- [ ] `GET /predictions/{id}` : détail d'une prédiction
- [ ] (Optionnel) `GET /stats` : statistiques simples (nb prédictions, etc.)

### 6. Données d'exemple
- [ ] Fournir un jeu d'exemples d'entrées (SQL ou CSV) pour tester
- [ ] Script de seed optionnel

### 7. Documentation technique
- [ ] Documenter la structure des tables
- [ ] Expliquer le choix technique (pourquoi PostgreSQL, pourquoi SQLAlchemy)
- [ ] Fournir des exemples d'interactions (requêtes, usage API)

## Résultats attendus
- [ ] Schéma UML de la BDD
- [ ] Script SQL ou `create_db.py`
- [ ] Dataset inséré et correctement structuré
- [ ] Enregistrement systématique des inputs/outputs dans des tables dédiées
- [ ] Traçabilité complète des échanges API ↔ DB
- [ ] Exemples d'entrées fournis

## Points de vigilance
- **Sécurité des données** : pas de credentials en dur, gestion fine des accès
- **Cohérence** : garantir que chaque prédiction est bien persistée (transaction atomique)
- **Performance** : indexer les colonnes de recherche si volume élevé
- Séparer la connexion DB de la logique métier

## Outils
- PostgreSQL
- SQLAlchemy (ou autre ORM)
- Alternative : Psycopg 3

## Ressources
- Documentation officielle PostgreSQL
- Tutoriels et guides SQLAlchemy
- Documentation Psycopg 3

## Checkpoint mentor
À la fin de cette étape, faire le point avec le mentor pour valider le schéma DB et l'intégration API ↔ DB.

## Statut global étape : **À FAIRE**
