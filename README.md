# SentimentLab


# Fonctionnalités :
- text-cleaning : nettoyage des tweets (URLs, mentions, hashtags, ponctuation) — RHOFRANE Ishak

- sentiment-scoring : classification des tweets en positif ou négatif (TF-IDF + régression logistique) avec un score entre -1 et +1 — FELLAH-IDRISSI Oumnia

- tokenizer : découpage des tweets en tokens (mots, URLs, mentions, hashtags, émoticônes, emojis, décimaux) — KAOUKAOU Ayoub

- hashtag-stats : extraction des hashtags, calcul de leur fréquence, identification des hashtags les plus populaires et statistiques par date — BITY Hiba

- time-series : analyse de l'évolution quotidienne des sentiments (nombre de tweets positifs et négatifs, pourcentages et statistiques par date) — MOUJRI Malika 

## Dataset

La fonctionnalité sentiment-scoring utilise le dataset Sentiment140, composé de 1,6 million de tweets étiquetés :
- `0` : sentiment négatif.
- `4` : sentiment positif.

Le jeu complet n'est pas versionné. Pour l'utiliser, télécharger « Sentiment140 dataset with 1.6 million tweets » (Kaggle) puis placer `training.1600000.processed.noemoticon.csv` dans `data/raw/` (dossier ignoré par git). Le modèle s'entraîne alors sur un échantillon équilibré de 20 000 tweets : 10 000 négatifs et 10 000 positifs.

Sans ce fichier, les tests fonctionnent quand même : ils utilisent un mini jeu étiqueté, et seul le test sur les 20 000 tweets est ignoré (skipped).

## Installation

```bash
python -m pip install -r requirements.txt
```

## Exécution des tests

```bash
pytest
```

ou, sans pytest : `python -m unittest discover -s tests -v`



