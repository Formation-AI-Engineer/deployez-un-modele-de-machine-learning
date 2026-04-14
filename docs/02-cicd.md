# Étape 2 — Configurer la CI/CD

## Objectif
Mettre en place une infrastructure d'intégration et de déploiement continus sur une plateforme cloud (Hugging Face Spaces par exemple).
Le pipeline doit garantir la qualité du code, faciliter les tests et permettre un déploiement rapide et fiable du modèle.

## Prérequis
- [x] Compréhension des principes d'intégration continue
- [x] Compréhension des environnements (dev / test / prod)
- [x] Étape 1 terminée (dépôt prêt)
- [ ] Compte Hugging Face (ou équivalent) créé — **action utilisateur requise**

## Tâches à réaliser

### 1. Préparation
- [x] Lister les étapes du pipeline AVANT de les coder
  - Pipeline CI : `lint (ruff check + format)` → `tests (pytest + coverage)` → upload artefacts
  - Pipeline CD : push vers HF Spaces (déclenché sur push main / tag)
- [x] Définir les environnements cibles et leurs déclencheurs
  - `dev` : push sur `dev` → CI uniquement
  - `test` : PR vers `main` → CI (gate avant merge)
  - `prod` : push sur `main` ou tag `v*` → CI + CD (déploiement HF)
- [x] Lister les secrets nécessaires → documentés dans `.env.example`
  - `DATABASE_URL` — chaîne de connexion PostgreSQL
  - `HF_TOKEN` — token d'écriture Hugging Face
  - `HF_SPACE_ID` — identifiant du Space (ex: `user/repo`)

### 2. Pipeline GitHub Actions
- [x] Créer `.github/workflows/ci-cd.yml` — lint + tests + déploiement dans un seul fichier
- [x] Job `lint` : install Python 3.11 + cache pip + `ruff check` + `ruff format --check`
- [x] Job `test` : install + `pytest --cov` + upload du rapport XML (dépend de `lint`)
- [x] Job `deploy` : push vers HF Spaces (dépend de `test`, uniquement sur main / tag `v*`)
- [x] Déclencheurs : `push` (main, dev, tags `v*`) et `pull_request` (main)

### 3. Protection des branches
- [ ] Configurer la branche `main` protégée sur GitHub — **action utilisateur requise**
  - Aller dans Settings > Branches > Add rule > `main`
  - Cocher : *Require status checks to pass before merging* → sélectionner `lint` et `test`
  - (Optionnel) *Require a pull request before merging*
- [ ] Vérifier que la CI bloque bien un merge si les tests échouent

### 4. Gestion des secrets
- [x] Utiliser `${{ secrets.XXX }}` dans les workflows (jamais d'echo direct)
- [x] Documenter la liste des secrets requis dans `.env.example`
- [ ] Créer les secrets dans GitHub Settings > Secrets and variables > Actions — **action utilisateur requise** :
  - `DATABASE_URL`
  - `HF_TOKEN`
  - `HF_SPACE_ID`

### 5. Déploiement Hugging Face Spaces
- [ ] Créer un Space Hugging Face (type Docker ou Gradio) — **action utilisateur requise**
- [x] Workflow de déploiement automatique prêt (`cd.yml`)
- [ ] Configurer le token HF comme secret GitHub (cf. point 4)
- [ ] Tester un premier déploiement bout-en-bout — *après étape 3 (API minimale)*
- [ ] Vérifier que le Space est accessible publiquement

### 6. Standards / documentation
- [x] Standards de code documentés : Ruff (lint + format), conventions dans le README
- [ ] Standards d'expérimentation ML — *à compléter après choix du modèle*
- [x] Workflow de contribution : branches `feature/`, Conventional Commits (README)

## Résultats attendus
- [x] Pipeline CI/CD automatisé fonctionnel (1 workflow unifié)
- [x] Fichier YAML configurant GitHub Actions (ci-cd.yml : lint → test → deploy)
- [x] Tests automatiques exécutés à chaque push/PR
- [ ] Validation avant fusion de branche (protection main — action utilisateur)
- [x] Gestion des environnements en place (dev/test/prod via déclencheurs)
- [x] Secrets documentés + utilisés via `${{ secrets }}` — reste à les créer sur GitHub

## Points de vigilance
- **Temps d'exécution** : si le pipeline dépasse ~10 min, interroger (cache, parallélisation, jobs ciblés)
- **Secrets** : ne jamais les logger, ne jamais les committer
- **Déploiement** : vérifier qu'un rollback est possible

## Outils
- GitHub Actions
- Hugging Face Spaces (ou équivalent)

## Ressources
- Documentation GitHub Actions
- Démarrer avec Hugging Face Spaces
- Cours OpenClassrooms : "Mettez en place l'intégration et la livraison continues avec la démarche DevOps"

## Statut global étape : **QUASI TERMINÉE** — reste 4 actions manuelles (protection main, secrets GitHub, création Space HF, test déploiement E2E).
