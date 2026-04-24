# Script de soutenance — Projet 5

> Texte de présentation commenté slide par slide.
> Durée cible : **~18 minutes** + questions.
> Conseils de lecture : les **blocs en gras** sont les points à ne pas oublier ; les
> paragraphes en italique sont des transitions à prononcer en changeant de slide.

---

## Slide 1 — Couverture
**Durée : 20 secondes**

Bonjour. Je suis Lamine Camara, en formation AI Engineer, et je vous présente aujourd'hui
mon Projet 5 : le **déploiement en production d'un modèle de machine learning** pour le
client Futurisys, sur un cas concret de prédiction d'attrition chez TechNova Partners.

*Passons rapidement sur le déroulé.*

---

## Slide 2 — Agenda
**Durée : 30 secondes**

Je vais couvrir six points :
- d'abord le **contexte métier** — pourquoi ce projet et pour qui,
- ensuite le **modèle retenu** et ses performances,
- puis l'**architecture** de la solution,
- la **mise en œuvre** — l'API et la base de données,
- la **qualité** — tests, CI/CD et déploiement,
- et pour finir, la **sécurité** et les perspectives d'évolution.

*Commençons par le contexte.*

---

## Slide 3 — Contexte & enjeu métier
**Durée : 1 min 30**

Le client **Futurisys** m'a confié une mission autour d'un cas fictif : sa filiale
TechNova Partners fait face à un **turnover élevé**. Pour la DRH, chaque départ
non-anticipé coûte cher — en recrutement, en formation, en perte de savoir-faire.

La mission est claire : **opérationnaliser un modèle ML** déjà développé lors du
Projet 4, et le rendre exploitable au quotidien par les équipes RH à travers une
API fiable, testée et déployée.

Côté chiffres, le dataset compte **1 470 employés**, avec un taux d'attrition
observé de **16 %** — une classe minoritaire, ce qui a eu des conséquences sur
le choix du modèle, j'y reviens. L'API expose **24 champs bruts** à l'utilisateur,
que le preprocessing transforme ensuite en **40 features** pour le modèle.

**Le résultat attendu** : une API déployée publiquement, capable de prendre en
entrée le profil d'un employé et de renvoyer une probabilité de départ, avec
chaque prédiction tracée en base de données.

*Parlons du modèle lui-même.*

---

## Slide 4 — Le modèle retenu
**Durée : 1 min 30**

J'ai retenu un **CatBoostClassifier**, c'est-à-dire du gradient boosting sur arbres
de décision. Ce choix vient du Projet 4, où j'avais comparé cinq approches
— DummyClassifier, régression logistique, RandomForest, XGBoost, CatBoost —
et **CatBoost est sorti en tête sur le F1 de la classe minoritaire**.

**Précision importante sur la version retenue** : j'ai aussi testé un tuning
par `RandomizedSearchCV` (100 combinaisons, 5 folds stratifiés, score = F1).
Résultat contre-intuitif : le tuning faisait monter le recall (0,55 → 0,68)
mais chutait la precision (0,58 → 0,41), donc le F1 global baissait
(0,57 → 0,51). **J'ai donc gardé la version non tunée** — les hyperparamètres
par défaut de CatBoost avec simplement `auto_class_weights="Balanced"`. C'est
un cas typique où « plus complexe » n'est pas « meilleur ».

Deux autres points techniques :

**Premièrement**, `auto_class_weights="Balanced"` est ce qui permet à CatBoost
de compenser tout seul le déséquilibre 84/16 en donnant plus de poids aux
exemples « Oui ». Sans ça, le modèle aurait appris à tout prédire « Non » et
aurait eu une excellente accuracy mais serait totalement inutile en pratique.

**Deuxièmement**, le preprocessing est **partagé entre l'entraînement et le
serving**. Concrètement, la même fonction `preprocess_single` est utilisée par
le script d'entraînement et par l'API. Ça garantit qu'il n'y a pas de dérive de
features entre les deux — un piège classique du ML en production.

**Le modèle lui-même n'est pas versionné dans Git** : il est régénéré à chaque
build Docker. C'est volontaire : le code d'entraînement est la source de vérité,
l'artefact `.cbm` est juste une compilation.

*Voyons ce que donne ce modèle en conditions de test.*

---

## Slide 5 — Performances sur jeu de test
**Durée : 2 min**

Sur 20 % du dataset mis de côté de manière stratifiée, voici les résultats.

L'**accuracy** est à 86 %. C'est correct — mais l'accuracy seule n'a **aucun
sens ici** : je pourrais atteindre 84 % en prédisant toujours « Non » sans
aucune valeur métier. Je ne m'en sers que comme repère.

Les métriques qui m'intéressent vraiment sont sur la **classe minoritaire**.

Le **recall** est à 49 % : le modèle détecte environ un départ sur deux.

La **precision** est à 56 % : sur dix employés signalés « à risque »,
cinq à six vont effectivement partir.

Le **F1** est à 0,52 — le meilleur F1 parmi tous les modèles comparés en P4,
y compris la version tunée.

**Un mot sur la PR AUC à 0,52** : c'est la métrique la plus parlante face au
déséquilibre 84/16. J'ai volontairement écarté la ROC AUC ici — avec une
classe positive aussi minoritaire, la ROC AUC est trompeusement élevée
(la grande masse des vrais négatifs suffit à gonfler le score). La PR AUC,
elle, ne mesure que le compromis precision/recall sur la classe « Oui » —
c'est bien ce qu'on veut évaluer.

**La matrice de confusion** le montre très clairement : sur les 47 départs
réels du jeu de test, **23 sont correctement identifiés** et 24 sont manqués.
Côté faux positifs, 18 employés sont signalés à tort.

**Ce qu'il faut retenir** : l'arbitrage est **équilibré** (precision ≈ recall),
ce qui maximise le F1. En RH, rater un départ coûte plus cher que lever une
fausse alerte ; la DRH peut toujours filtrer une liste de suspects, mais ne
peut pas agir sur un profil qu'on n'a pas signalé. Le modèle est donc
positionné comme un **outil d'aide à la décision**, pas comme une
automatisation — et c'est un message qu'il faut porter clairement aux
utilisateurs.

*Voyons maintenant comment ce modèle est servi.*

---

## Slide 6 — Architecture de la solution
**Durée : 1 min 30**

L'architecture est volontairement **simple** : un client HTTP qui appelle une
API FastAPI, laquelle s'appuie sur deux ressources — le modèle CatBoost chargé
en mémoire, et une base PostgreSQL pour la persistance.

Un détail important : le modèle est chargé **une seule fois au démarrage** de
l'API, via un singleton. Chaque requête le réutilise directement, sans
ré-instancier. Sur un modèle CatBoost, le chargement prend environ une seconde ;
le faire à chaque requête multiplierait la latence par cent.

La **stack technique** est volontairement mainstream :
- **FastAPI** pour l'API — typage fort, validation automatique, Swagger UI gratuit.
- **Pydantic v2** pour les schémas — l'API refuse automatiquement tout payload
  mal formé, avec un message d'erreur précis.
- **SQLAlchemy 2** + **PostgreSQL 16** pour la persistance.
- **pytest** et **Ruff** côté qualité.
- **Docker** et **GitHub Actions** pour la livraison, **Hugging Face Spaces**
  comme cible de déploiement.

*Entrons dans le détail de l'API.*

---

## Slide 7 — API FastAPI
**Durée : 1 min 30**

L'API expose **six endpoints**, regroupés en deux familles.

D'abord les endpoints de prédiction :
- **POST /predict** prend en entrée un payload RH de 24 champs et renvoie la
  prédiction, la probabilité, un niveau de risque qualitatif — faible, modéré,
  élevé —, ainsi que l'ID de la prédiction en base.
- **POST /predict/employee/{id}** est un raccourci : on passe un identifiant
  d'employé, l'API va chercher ses caractéristiques en base, lance la prédiction
  et enregistre le résultat. C'est utile pour scorer un employé déjà connu
  sans avoir à ressaisir ses données.

Ensuite les endpoints d'interrogation :
- **GET /predictions** renvoie l'historique paginé.
- **GET /predictions/{id}** renvoie le détail d'une prédiction passée.
- **GET /model/info** donne les métadonnées du modèle — version, algorithme,
  nombre de features.
- **GET /health** est le health-check standard.

**Un point à souligner** : la validation Pydantic est stricte. Si un utilisateur
envoie un âge à 200 ou un genre inconnu, il reçoit une **422** avec un message
qui liste précisément les champs invalides. Je n'ai pas une seule ligne de code
de validation manuelle — c'est entièrement déclaratif dans les schémas.

*Passons à la base de données.*

---

## Slide 8 — Base PostgreSQL
**Durée : 1 min 15**

Deux tables suffisent pour ce POC.

La table **dataset** est le référentiel RH source — les 1 470 employés fusionnés
depuis les trois CSV d'origine : SIRH, évaluations, sondages de satisfaction.
C'est cette table que consulte l'endpoint `/predict/employee/{id}`.

La table **predictions** est le **journal opérationnel** : à chaque appel à
`/predict`, une ligne est insérée avec l'input complet, l'output, la version
du modèle utilisée, et l'horodatage.

**J'ai volontairement mis input et output dans une seule table**. Séparer en
deux tables avec une clé étrangère aurait été plus « propre » d'un point de vue
théorique, mais pour un POC c'est de la complexité sans valeur : une ligne =
une requête = une prédiction complète, traçabilité immédiate.

Pas de clé étrangère entre les deux tables — elles vivent indépendamment.
Le lien applicatif se fait uniquement via l'endpoint qui lit `dataset` et écrit
`predictions`. Si demain on supprime un employé du référentiel, son historique
de prédictions reste consultable.

*Parlons qualité — comment on garantit que tout ça marche.*

---

## Slide 9 — Tests & qualité
**Durée : 1 min 30**

J'ai écrit **51 tests**, qui s'exécutent en moins de deux secondes et couvrent
**88 %** du code applicatif.

La suite est séparée en deux dossiers :
- **tests unitaires** pour chaque brique isolée : validation des schémas,
  pipeline de preprocessing, service de prédiction, modèles ORM.
- **tests fonctionnels** pour chaque endpoint via le TestClient FastAPI :
  cas nominaux, erreurs 422, erreurs 404, pagination.

**Un choix que je défends** : les tests utilisent **SQLite en fichier temporaire**,
pas PostgreSQL. Avantage énorme — aucun prérequis pour lancer `pytest`, la CI
n'a pas besoin de provisionner une base, les tests sont isolés les uns des
autres grâce à un nettoyage automatique entre chaque test.

Côté qualité de code, j'utilise **Ruff** pour le linting et le formatage,
intégré à la CI. Aucun warning de dépréciation ne traîne — j'ai migré les
`Field(example=...)` de Pydantic v1 vers `examples=[...]` en v2, et remplacé
`@app.on_event("startup")` par le nouveau gestionnaire `lifespan` de FastAPI.

*Voyons comment tout ça s'enchaîne en CI/CD.*

---

## Slide 10 — Pipeline CI/CD
**Durée : 1 min 30**

Le pipeline est unifié dans un seul fichier GitHub Actions, avec **quatre
étapes séquentielles** :
- **Lint** — Ruff vérifie le style et le formatage.
- **Test** — pytest avec couverture.
- **Train** — le modèle est réentraîné, parce que l'artefact `.cbm` n'est pas
  versionné.
- **Deploy** — push vers Hugging Face Spaces, qui rebuild l'image Docker côté
  HF et redémarre l'API.

Les étapes sont **dépendantes** : si le lint casse, les tests ne tournent pas ;
si un test échoue, rien n'est déployé. C'est ce qu'on appelle un **fail fast**.

**Chaque environnement a ses déclencheurs** :
- Sur **dev**, uniquement lint et test — j'ai du feedback rapide pendant que
  je développe.
- Sur une **pull request vers main**, lint et test servent de **gate bloquante** :
  la branche `main` est protégée, le merge est impossible sans une CI verte.
- Sur un **push vers main ou un tag v-quelque-chose**, le pipeline complet
  tourne et pousse en prod.

Les secrets — token Hugging Face, ID du Space — vivent dans GitHub Secrets
et sont injectés à l'exécution, jamais dans les logs, jamais dans le code.

*Un mot sur le déploiement lui-même et la sécurité.*

---

## Slide 11 — Déploiement & sécurité
**Durée : 1 min 30**

Côté **déploiement**, le Space Hugging Face est configuré en mode Docker.
L'image est construite à partir du `Dockerfile` à la racine du repo — le même
que celui qu'on utilise en local. Au build, le script d'entraînement tourne
et produit un modèle frais à chaque déploiement. L'API écoute sur le port
**7860**, qui est la convention Hugging Face.

**Le rollback est simple** : je retag une version antérieure et je push.
Le pipeline redéploie. Pas de base de données en prod pour ce POC — on reste
sur du stateless.

Côté **sécurité**, je veux être transparent sur l'état actuel.

**Ce qui est en place** : la validation Pydantic bloque les payloads malformés ;
les secrets ne touchent jamais Git ; la branche `main` est protégée ; les
dépendances sont figées avec des bornes min et max.

**Ce qui manque pour un passage en production réel** : il **n'y a pas
d'authentification** sur l'API. N'importe qui avec l'URL peut appeler les
endpoints. Pour passer en prod, je préconiserais une clé d'API en header,
un rate limiting, et — sur ce cas RH particulier — un vrai **audit RGPD**
parce que le modèle utilise des variables sensibles comme le genre, le
statut marital et l'âge.

*Parlons des retours d'expérience et des évolutions possibles.*

---

## Slide 12 — Retours & améliorations
**Durée : 1 min 30**

**Trois choses m'ont bien servi** sur ce projet :

D'abord, le **preprocessing partagé** entre entraînement et inférence. C'est
la clé pour éviter le feature skew — un bug silencieux classique où le
modèle voit en prod des features légèrement différentes de celles qu'il a
vues à l'entraînement.

Ensuite, la **traçabilité systématique** via la table predictions. Chaque
appel laisse une trace complète, avec la version du modèle. C'est la base
pour faire du monitoring plus tard.

Enfin, les **conventions strictes** : Conventional Commits pour l'historique,
SemVer pour les releases, protection de `main` avec gate CI bloquante. Ça
force la discipline même sur un projet solo.

**Si je devais pousser le projet plus loin**, je ferais quatre choses dans cet
ordre :
1. **Authentification et rate-limiting** de l'API — c'est le blocage numéro un
   pour un vrai passage en production.
2. **Monitoring de dérive** sur la distribution des probabilités et la
   proportion de « Oui » — une simple requête SQL agrégée sur la table
   predictions suffit pour commencer.
3. **Explicabilité** via SHAP, exposée côté API — pour chaque prédiction,
   renvoyer les 3 features qui ont le plus pesé. C'est non seulement de la
   valeur métier, c'est aussi une exigence RGPD quand on score des personnes.
4. **Tracking d'expérimentation** avec MLflow quand on entrera dans un cycle
   de réentraînements réguliers.

*Je termine.*

---

## Slide 13 — Merci / Questions
**Durée : 20 secondes**

Voilà pour cette présentation. **En deux mots, ce qui a été livré** : une API
de prédiction déployée, testée à 88 %, avec un pipeline CI/CD complet et une
traçabilité intégrale en base.

Je vous remercie pour votre attention, et je suis à votre disposition pour
toutes vos questions.

---

## Annexe — Questions probables & éléments de réponse

**Pourquoi CatBoost plutôt qu'un XGBoost ou un LightGBM ?**
→ Dans le Projet 4, j'ai comparé les trois. CatBoost gère nativement les
catégorielles sans encodage manuel, ce qui simplifie le pipeline. Sur mes
métriques F1 minoritaire, il sortait le mieux positionné — marginalement,
mais reproductiblement sur plusieurs seeds.

**Pourquoi pas un modèle plus simple, type régression logistique ?**
→ Testé aussi en P4. Sur le F1 de la classe minoritaire, CatBoost sort
devant ; la régression logistique reste interprétable mais plafonne plus
tôt. Le gain de F1 justifie la complexité supplémentaire, d'autant que
CatBoost gère nativement les catégorielles (pas de pipeline d'encodage
manuel à maintenir).

**Pourquoi ne pas avoir gardé la version tunée du modèle ?**
→ Le `RandomizedSearchCV` (100 combinaisons, 5 folds) a déplacé le
compromis : +13 points de recall mais −17 points de precision, pour un
F1 qui passait de 0,57 à 0,51. Le score d'optimisation était pourtant
le F1 lui-même — signe que l'espace d'hyperparamètres exploré poussait
vers des arbres plus profonds et un learning rate plus lent, qui
déséquilibrent la frontière de décision en faveur du rappel pur. La
version baseline reste supérieure sur le compromis métier.

**Pourquoi PR AUC et pas ROC AUC ?**
→ Avec une classe positive à 16 %, la ROC AUC est trompeusement élevée :
la grande masse des vrais négatifs suffit à la gonfler. La PR AUC
(*average precision*) ne regarde que le compromis precision/recall sur
la classe « Oui » — c'est exactement ce qu'on veut mesurer quand on
cherche à détecter des cas rares.

**Pourquoi SQLite pour les tests et PostgreSQL en prod ?**
→ Les tests doivent être hermétiques et rapides : pas de prérequis, pas de
serveur à démarrer, pas d'état persistant. SQLAlchemy abstrait le dialecte,
donc le code métier est identique. J'ai vérifié que les deux comportements
sont équivalents sur les cas que je teste (contraintes uniques, timestamps,
etc.).

**Et si le modèle devient moins précis avec le temps ?**
→ C'est prévu. La table `predictions` stocke la distribution des probabilités
dans le temps. Une alerte peut se déclencher si la moyenne dérive de plus
de X % par rapport à la baseline. Le réentraînement passe par le script
`train_model.py` et un nouveau tag — le déploiement suit automatiquement.

**Combien de temps pour un prédiction ?**
→ En local, environ 15 à 30 millisecondes par appel (preprocessing +
inférence + insert). Le goulot d'étranglement est plutôt le réseau dans
la pratique.

**Pourquoi pas un MLflow dès maintenant ?**
→ Je ne fais qu'un seul entraînement, reproductible depuis le seed 42.
MLflow a du sens quand on a une vraie cadence d'expérimentations. Pour un
POC, c'est un outil qui ajoute du ritual sans valeur immédiate.
