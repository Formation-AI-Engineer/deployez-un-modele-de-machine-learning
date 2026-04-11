# Étape 2 — Configurer la CI/CD

## Objectif
Mettre en place une infrastructure d'intégration et de déploiement continus sur une plateforme cloud (Hugging Face Spaces par exemple).
Le pipeline doit garantir la qualité du code, faciliter les tests et permettre un déploiement rapide et fiable du modèle.

## Prérequis
- [ ] Compréhension des principes d'intégration continue
- [ ] Compréhension des environnements (dev / test / prod)
- [ ] Étape 1 terminée (dépôt prêt)
- [ ] Compte Hugging Face (ou équivalent) créé

## Tâches à réaliser

### 1. Préparation
- [ ] Lister les étapes du pipeline AVANT de les coder
  - Exemple : lint → tests unitaires → build → déploiement
- [ ] Définir les environnements cibles et leurs déclencheurs
  - `dev` : push sur `dev`
  - `test` : PR vers `main`
  - `prod` : tag ou push sur `main`
- [ ] Lister les secrets nécessaires (tokens HF, DB URL, etc.)

### 2. Pipeline GitHub Actions
- [ ] Créer `.github/workflows/ci.yml`
- [ ] Job : installation Python + cache des dépendances
- [ ] Job : lint (ruff / flake8) — optionnel mais recommandé
- [ ] Job : exécution des tests Pytest (sera étoffé à l'étape 5)
- [ ] Job : rapport de couverture
- [ ] Déclencheurs : `push` et `pull_request`

### 3. Protection des branches
- [ ] Configurer la branche `main` protégée
- [ ] Exiger que la CI passe avant merge
- [ ] Exiger au moins une review (si collab) ou self-review

### 4. Gestion des secrets
- [ ] Créer les secrets dans GitHub Settings > Secrets
- [ ] Ne JAMAIS les exposer dans les logs (pas de `echo` direct)
- [ ] Utiliser `${{ secrets.XXX }}` dans les workflows
- [ ] Documenter la liste des secrets requis (sans les valeurs)

### 5. Déploiement Hugging Face Spaces
- [ ] Créer un Space Hugging Face pour le projet
- [ ] Ajouter un workflow de déploiement automatique (push vers HF)
- [ ] Configurer le token HF comme secret GitHub
- [ ] Tester un premier déploiement bout-en-bout (même avec une API minimale)
- [ ] Vérifier que le Space est accessible publiquement

### 6. Standards / documentation
- [ ] Créer un README ou section décrivant :
  - [ ] Les standards de code adoptés
  - [ ] Les standards d'expérimentation ML
  - [ ] Le workflow de contribution

## Résultats attendus
- [ ] Pipeline CI/CD automatisé fonctionnel
- [ ] Fichier YAML configurant au moins une GitHub Action
- [ ] Tests automatiques exécutés à chaque push/PR
- [ ] Validation avant fusion de branche
- [ ] Gestion des environnements en place
- [ ] Secrets correctement gérés

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

## Statut global étape : **À FAIRE**
