# CONTRIBUTING.md

## 1. Présentation

Ce document décrit les règles de contribution au projet **SentimentLab**, réalisé dans le cadre du module Versioning & Collaboration (Git et GitFlow).

Il définit l'organisation de l'équipe, les conventions de développement, la gestion des branches, les commits, les Pull Requests et le processus de relecture.

Tous les membres de l'équipe doivent respecter ces règles afin de garantir un travail collaboratif, organisé et traçable.

## 2. Organisation de l'équipe

L'équipe est composée de six membres.

- Release Manager : BITY Hiba
- Integrateur : RHOFRANE Ishak
- Documentaliste : FELLAH-IDRISSI Oumnia
- Developpeurs : tous les membres

Tous les membres restent développeurs, indépendamment de leur rôle principal.

### Membres de l'équipe

- RHOFRANE Ishak (s-7a9)
- FELLAH-IDRISSI Oumnia
- KAOUKAOU Ayoub
- MOUJRI Malika
- LKHLIFI Hiba
- BITY Hiba (bt-hiba)

## 3. Organisation des branches

Le projet utilise une organisation inspirée de GitFlow, appliquée manuellement, sans l'extension git-flow.

Les branches principales sont :

| Branche | Utilisation |
|---|---|
| `main` | Contient les versions stables du projet destinées à la production. |
| `develop` | Branche d'intégration des fonctionnalités développées et validées. |
| `feature/<nom>` | Branche dédiée au développement d'une fonctionnalité. |
| `release/<version>` | Branche de préparation d'une nouvelle version. |
| `hotfix/<version>` | Branche destinée à corriger rapidement une version publiée. |
| `docs/<nom>` | Branche dédiée à une modification documentaire. |

### Règles de création et de fusion

- Une branche `feature/*` doit toujours être créée à partir de `develop`.
- Une branche `release/*` est créée à partir de `develop`.
- Une branche `hotfix/*` est créée à partir de `main`.
- Toute intégration dans `develop` ou `main` doit passer par une Pull Request.
- Les branches `main` et `develop` sont protégées : aucun push direct n'est autorisé.
- Chaque branche de fonctionnalité est supprimée après sa fusion.

## 4. Convention des commits

Les messages de commit doivent suivre une convention commune afin de faciliter la compréhension de l'historique du projet.

Les préfixes autorisés sont :

| Préfixe | Utilisation |
|---|---|
| `feat:` | Ajout d'une nouvelle fonctionnalité. |
| `fix:` | Correction d'un problème ou d'un bug. |
| `docs:` | Modification de la documentation. |
| `test:` | Ajout ou modification de tests. |
| `refactor:` | Réorganisation du code sans changement fonctionnel. |
| `chore:` | Tâches techniques et maintenance du projet. |

Les messages doivent être explicites et rédigés à l'impératif.



## 5. Gestion des Issues

Chaque fonctionnalité doit posséder une Issue GitHub.

Les règles à respecter sont :

- Une Issue est créée pour chaque fonctionnalité.
- Elle est assignée au membre responsable de cette fonctionnalité.
- Elle reçoit le label `feature`.
- Elle est associée au milestone `v1.0.0`.
- Elle doit être liée à la Pull Request correspondante.

La description de la Pull Request doit contenir la référence :

```
Closes #<numero-issue>
```

Cette référence permet de fermer automatiquement l'Issue lorsque la Pull Request est fusionnée.

## 6. Développement des fonctionnalités

Chaque développeur travaille sur sa propre branche `feature/<nom>`.

Chaque fonctionnalité doit obligatoirement comporter :

- Le code source correspondant dans le dossier `src/`.
- Au moins un test unitaire dans le dossier `tests/`.
- Une description de la fonctionnalité dans le fichier `README.md`.

Les tests doivent être exécutables sur un environnement de développement et utiliser les données d'échantillon disponibles dans `data/sample/`.

Les jeux de données complets ne doivent jamais être ajoutés au dépôt.

Les dossiers suivants doivent rester ignorés par Git :

```text
data/raw/
data/processed/
```

Seul un petit échantillon de données inférieur à 1 Mo peut être versionné dans `data/sample/`.

## 7. Pull Requests et processus de relecture

Toute fonctionnalité doit être intégrée dans `develop` à travers une Pull Request.

### Ordre de relecture de l'équipe

L'équipe a organisé les relectures selon la répartition suivante :
Chaque membre est responsable de la relecture et de la fusion de la Pull Request qui lui est attribuée.

**1. RHOFRANE Ishak**
- Fonctionnalité : `text-cleaning`
- Branche : `feature/text-cleaning`
- Relecteur et responsable de la fusion : LKHLIFI Hiba
- Méthode de fusion : **Merge commit**

**2. KAOUKAOU Ayoub**
- Fonctionnalité : `tokenizer`
- Branche : `feature/tokenizer`
- Relecteur et responsable de la fusion : RHOFRANE Ishak
- Méthode de fusion : **Rebase and merge**

**3. FELLAH-IDRISSI Oumnia**
- Fonctionnalité : `sentiment-scoring`
- Branche : `feature/sentiment-scoring`
- Relecteur et responsable de la fusion : KAOUKAOU Ayoub
- Méthode de fusion : **Merge commit**

**4. BITY Hiba**
- Fonctionnalité : `hashtag-stats`
- Branche : `feature/hashtag-stats`
- Relecteur et responsable de la fusion : FELLAH-IDRISSI Oumnia
- Méthode de fusion : **Rebase and merge**

**5. MOUJRI Malika**
- Fonctionnalité : `time-series`
- Branche : `feature/time-series`
- Relecteur et responsable de la fusion : BITY Hiba
- Méthode de fusion : **Merge commit**

**6. LKHLIFI Hiba**
- Fonctionnalité : `csv-export`
- Branche : `feature/csv-export`
- Relecteur et responsable de la fusion : MOUJRI Malika
- Méthode de fusion : **Rebase and merge**

Deux méthodes de fusion sont utilisées :

- **Merge** : conserve un commit de fusion dans l'historique.
- **Rebase** : replace les commits de la branche sur la dernière version de la branche cible avant la fusion.

La répartition prévoit trois PR fusionnées avec Merge et trois avec Rebase.


