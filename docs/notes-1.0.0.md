# SentimentLab — Release 1.0.0

## Présentation

SentimentLab est un projet d'analyse de sentiments sur des tweets.

Cette version 1.0.0 regroupe les fonctionnalités suivantes :

## Fonctionnalités

- **Text Cleaning** : nettoyage des tweets (URLs, mentions, ponctuation et espaces superflus).
- **Tokenizer** : découpage des tweets en tokens, avec prise en charge des mots, URLs, mentions, hashtags, émoticônes, emojis et nombres décimaux.
- **Sentiment Scoring** : classification des tweets en sentiments positifs ou négatifs avec TF-IDF et régression logistique, ainsi que calcul d'un score entre -1 et +1.
- **Hashtag Statistics** : extraction des hashtags, calcul des fréquences et statistiques par date.
- **Time Series Analysis** : analyse quotidienne de l'évolution des sentiments.
- **CSV Export** : export des résultats d'analyse au format CSV avec sélection des colonnes.
- **Sentiment Score Histogram** : visualisation de la distribution des scores de sentiment avec possibilité d'enregistrer le graphique.

## Corrections et améliorations

- Suppression des tweets vides après nettoyage.
- Amélioration de la gestion des nombres décimaux et des émoticônes dans le tokenizer.
- Validation du paramètre `n` de la fonction `top_hashtags`.
- Gestion des fichiers CSV vides dans l'analyse temporelle.
- Gestion des valeurs manquantes et non finies dans l'histogramme (`NaN`, `+Inf`, `-Inf`).
- Adaptation des tests pour permettre leur exécution sans le dataset complet Sentiment140.

## Tests

Suite de tests exécutée avec succès : **106 tests passés**.

