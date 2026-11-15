# Changelog

Toutes les modifications importantes du projet **SentimentLab** sont documentées dans ce fichier.

## [1.0.0] - 15/11/2026

### Added

- ### Fixed

- **Text Cleaning** : suppression des tweets qui deviennent vides après le nettoyage afin d'éviter de conserver des données inutilisables.
- **Tokenizer** : amélioration de la gestion des nombres décimaux, des émoticônes et des émoticônes accolées aux mots.
- **Sentiment Scoring** : adaptation des tests pour permettre leur exécution sans disposer du dataset complet Sentiment140.
- **Hashtag Statistics** : validation du paramètre `n` de la fonction `top_hashtags`, avec gestion des valeurs négatives et des types non autorisés.
- **Time Series** : correction du traitement des fichiers CSV vides afin d'éviter les erreurs lors de l'agrégation des résultats.
- **Sentiment Score Histogram** : amélioration de la gestion des valeurs manquantes et non finies (`NaN`, `+Inf`, `-Inf`), avec contrôle des cas où aucun score valide n'est disponible.

### Fixed

- Correction du traitement des fichiers CSV vides dans l'analyse des séries temporelles.
- Amélioration de la gestion des valeurs manquantes et non finies (`NaN`, `+Inf`, `-Inf`) lors de la génération de l'histogramme des scores de sentiment.
- Ajout de contrôles pour éviter la génération d'un histogramme lorsqu'aucun score valide n'est disponible.