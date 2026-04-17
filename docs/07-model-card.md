# Fiche technique du modèle — Attrition TechNova Partners

## Identité

| Champ | Valeur |
|---|---|
| Nom | CatBoost Attrition Classifier |
| Version | `1.0.0` |
| Fichier | `models/catboost_attrition.cbm` (~1 Mo) |
| Algorithme | `catboost.CatBoostClassifier` (gradient boosting sur arbres) |
| Tâche | Classification binaire (départ Oui/Non) |
| Origine | Sélectionné et tuné dans le **Projet 4** (« Classifiez automatiquement des informations »), réentraîné ici via `scripts/train_model.py` |
| Cible métier | Identifier les employés à risque de départ pour prioriser les actions RH |

## Données d'entraînement

- **Source** : dataset RH synthétique de TechNova Partners (fictif, Projet 4), fourni dans `data/` en 3 CSV fusionnés sur `id_employee` :
  - `extrait_sirh.csv` (SIRH — données administratives)
  - `extrait_eval.csv` (évaluations)
  - `extrait_sondage.csv` (sondages de satisfaction)
- **Volumétrie** : 1 470 lignes, 40 features après feature engineering.
- **Répartition de la cible** : 1 233 « Non » / 237 « Oui » — classe positive minoritaire (**16,1 %**).
- **Split** : 80/20 stratifié, seed `42`.

## Features d'entrée (API)

L'API attend **24 champs bruts** (types et bornes validés par Pydantic — voir `app/schemas/prediction.py`). Le préprocessing applicatif (`app/preprocessing.py::preprocess_single`) produit ensuite les **40 features** attendues par le modèle entraîné (one-hot + features dérivées).

| Groupe | Champs |
|---|---|
| Identité / profil | `age`, `genre`, `statut_marital`, `niveau_education`, `domaine_etude` |
| Carrière | `poste`, `departement`, `nombre_experiences_precedentes`, `annee_experience_totale`, `annees_dans_l_entreprise`, `annees_depuis_la_derniere_promotion` |
| Rémunération | `revenu_mensuel`, `augementation_salaire_precedente`, `nombre_participation_pee` |
| Satisfaction | `satisfaction_employee_environnement`, `_nature_travail`, `_equipe`, `_equilibre_pro_perso` |
| Évaluation | `note_evaluation_actuelle`, `note_evaluation_precedente` |
| Conditions | `heure_supplementaires`, `frequence_deplacement`, `distance_domicile_travail`, `nb_formations_suivies` |

**Features dérivées** (calculées côté serveur, pas attendues en entrée) : `ratio_anciennete_experience`, `satisfaction_moyenne`, `ecart_evaluation`, `anciennete_sans_promotion`.

## Sortie

```json
{
  "prediction_id": 123,
  "prediction": "Oui",
  "probability": 0.7421,
  "risk_level": "élevé",
  "threshold": 0.5,
  "model_version": "1.0.0",
  "timestamp": "2026-04-17T10:42:00Z"
}
```

- `prediction` : `"Oui"` si `probability >= threshold` (0.5), sinon `"Non"`.
- `risk_level` : bucket qualitatif — `faible` (< 0.3), `modéré` (0.3–0.6), `élevé` (≥ 0.6).

## Hyperparamètres retenus

| Paramètre | Valeur |
|---|---|
| `iterations` | 300 |
| `depth` | 4 |
| `learning_rate` | 0.01 |
| `l2_leaf_reg` | 10 |
| `border_count` | 32 |
| `auto_class_weights` | `"Balanced"` (compense le déséquilibre 83/17) |
| `random_seed` | 42 |

Valeurs issues du tuning effectué en Projet 4 (voir `scripts/train_model.py`).

## Performances sur jeu de test (20 %, stratifié)

| Métrique | Valeur |
|---|---|
| Accuracy | 0.789 |
| Precision (classe `Oui`) | 0.405 |
| **Recall (classe `Oui`)** | **0.681** |
| F1 (classe `Oui`) | 0.508 |
| ROC AUC | 0.811 |

**Matrice de confusion** (vraie → prédite) :

|  | Prédit `Non` | Prédit `Oui` |
|---|---|---|
| Vrai `Non` (247) | 200 | 47 |
| Vrai `Oui` (47) | 15 | 32 |

**Lecture métier** : le modèle identifie correctement **~68 % des employés qui partent réellement** (recall). En contrepartie, sur 100 employés signalés à risque, environ 40 quitteraient effectivement (precision). L'arbitrage est **volontairement orienté recall** — en contexte RH, rater un départ coûte plus cher que lever une fausse alerte : la DRH peut toujours filtrer, mais ne peut pas agir sur un profil qu'on n'a pas signalé.

## Limites connues

1. **Dataset synthétique et petit** (1 470 lignes). Les performances réelles chez un client ne sont pas garanties sans réentraînement.
2. **Précision limitée sur la classe positive** (~40 %). À utiliser comme outil de priorisation, pas comme décision automatisée.
3. **Pas de feature drift monitoring** en place.
4. **Pas d'explicabilité embarquée** (SHAP non exposé par l'API) — prévisible mais non interprétable côté utilisateur.
5. **Biais potentiels** : le modèle utilise `genre`, `statut_marital`, `age` — acceptable pour un POC, à auditer avant tout usage opérationnel (risque de discrimination indirecte).
6. **Pas d'authentification** sur l'API : toute personne ayant l'URL peut appeler `/predict` (cf. section sécurité du README).

## Protocole de mise à jour

### Réentraînement
1. Mettre à jour les CSV dans `data/` (fusion sur `id_employee`).
2. Lancer `python scripts/train_model.py` → régénère `models/catboost_attrition.cbm`.
3. Incrémenter `MODEL_VERSION` dans `app/services/prediction.py` (convention SemVer : PATCH pour réentraînement iso-features, MINOR pour nouvelles features, MAJOR pour rupture de schéma).
4. Mettre à jour cette fiche (métriques, dataset).

### Redéploiement
1. Commit + tag `vX.Y.Z` → push sur `main`.
2. Le workflow `ci-cd.yml` lance lint → tests → push HF Spaces.
3. Le `Dockerfile` réexécute `scripts/train_model.py` au build (le modèle n'est pas versionné), puis lance l'API.
4. Le champ `model_version` retourné par `/predict` permet de tracer quelle version a produit chaque prédiction (table `predictions`).

### Rollback
Redéployer un tag antérieur : `git push --force hf <old-tag>:main` (ou revert du commit et re-push). Toutes les prédictions précédemment persistées conservent leur `model_version` d'origine.

### Monitoring suggéré (hors scope POC)
- Suivre la distribution de `probability` dans la table `predictions` (signal de drift).
- Comparer la proportion de prédictions `Oui` à celle observée à l'entraînement (16 %).
- Collecter les retours terrain pour mesurer la precision réelle en production.
