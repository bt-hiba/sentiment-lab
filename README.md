# SentimentLab


## Fonctionnalités

- **Sentiment Scoring (Analyse de sentiment) :** Classification des tweets en sentiments positifs ou négatifs à l'aide de TF-IDF et de la régression logistique (Logistic Regression). La fonctionnalité retourne également un score compris entre -1 et +1.

## Dataset

La fonctionnalité utilise le dataset Sentiment140, composé de 1,6 million de tweets étiquetés :
- `0` : sentiment négatif.
- `4` : sentiment positif.

Pour le développement et les tests initiaux, le modèle utilise un échantillon équilibré de 20 000 tweets : 10 000 négatifs et 10 000 positifs.

## Installation

```bash
python -m pip install -r requirements.txt
```

## Exécution des tests

```bash
python -m unittest discover -s tests -v
```