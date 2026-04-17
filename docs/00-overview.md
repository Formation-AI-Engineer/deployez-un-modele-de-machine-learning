# Projet 5 — Déployez un modèle de Machine Learning

## Contexte
Mission freelance pour **Futurisys** (DT : Aurélien).
Objectif : rendre un modèle ML opérationnel et accessible via une API performante, en respectant les bonnes pratiques d'ingénierie logicielle.

**Résultat final attendu** : un Proof of Concept (POC) fonctionnel présenté en soutenance.

## Choix du modèle
- [ ] Choisir le modèle à déployer :
  - Option A : Projet 3 — Anticipez les besoins en consommations de bâtiment
  - Option B : Projet 4 — Classifiez automatiquement des informations
- [ ] Récupérer le modèle entraîné + dataset associé
- [ ] Documenter le choix dans le README

## Compétences visées
- Développement d'API avec FastAPI
- Tests unitaires avec Pytest
- Gestion de versions avec Git
- Conteneurisation / pipelines CI/CD
- Gestion d'une base PostgreSQL

## Livrables globaux
- [ ] Dépôt Git structuré
  - [ ] Code source complet
  - [ ] `requirements.txt` (ou équivalent)
  - [ ] Historique de commits clair, branches dédiées, tags de version
  - [ ] README complet (installation, utilisation, déploiement, auth, sécurité)
- [ ] API FastAPI fonctionnelle et déployée
  - [ ] Documentation Swagger/OpenAPI intégrée
  - [ ] Endpoints, schémas, exemples d'appels documentés
- [ ] Suite de tests
  - [ ] Tests Pytest (cas critiques + scénarios d'erreur)
  - [ ] Rapport de couverture (pytest-cov)
- [ ] Base PostgreSQL fonctionnelle
  - [ ] Script SQL ou `create_db.py`
  - [ ] Schéma UML / documentation des tables
  - [ ] Exemples d'entrées (SQL ou CSV avec inputs/outputs)
  - [ ] Scripts d'interrogation et d'interaction avec le modèle
- [ ] Pipeline CI/CD
  - [ ] Fichier YAML GitHub Actions
  - [ ] Gestion des environnements (dev / test / prod)
  - [ ] Gestion des secrets
- [ ] Support de présentation pour la soutenance

## Découpage en étapes
| # | Étape | Fichier | Statut |
|---|-------|---------|--------|
| 1 | Gestion de version & collaboration | [01-git-versioning.md](01-git-versioning.md) | À faire |
| 2 | Configuration CI/CD | [02-cicd.md](02-cicd.md) | Terminée |
| 3 | Développement de l'API | [03-api-fastapi.md](03-api-fastapi.md) | Terminée |
| 4 | Base de données PostgreSQL | [04-postgresql.md](04-postgresql.md) | Terminée |
| 5 | Tests unitaires & fonctionnels | [05-tests.md](05-tests.md) | Terminée |
| 6 | Documentation | [06-documentation.md](06-documentation.md) | À faire |

## Avant de démarrer (recommandations mission)
- [x] Lire toute la mission et ses documents liés
- [ ] Prendre des notes sur ce qui est compris
- [ ] Préparer une liste de questions pour la première session de mentorat
- [ ] Suivre les cours Git/GitHub associés
- [ ] Consulter la ressource Hugging Face Spaces Overview

## Points de contrôle mentor
Des pauses de vérification sont prévues à la fin des étapes 1, 3, 4 et 5. Faire le point avec le mentor avant de passer à la suite.
