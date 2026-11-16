# Changelog

Toutes les modifications importantes du projet **SentimentLab** sont documentées dans ce fichier.

## [1.0.0] - 15/11/2026

### Added

- **Text Cleaning** : nettoyage des tweets avec suppression des URLs, mentions, ponctuations et espaces superflus, tout en conservant les mots des hashtags, les accents et les apostrophes.
- **Sentiment Scoring** : classification des tweets en sentiments positifs ou négatifs à l'aide de TF-IDF et d'un modèle de régression logistique. La fonctionnalité fournit également un score de sentiment compris entre -1 et +1.
- **Tokenizer** : découpage des tweets en tokens, avec prise en charge des mots, URLs, mentions, hashtags, émoticônes, emojis et nombres décimaux.
- **Hashtag Statistics** : extraction des hashtags, calcul de leur fréquence, identification des hashtags les plus populaires et génération de statistiques par date.
- **Time Series Analysis** : analyse quotidienne de l'évolution des sentiments, avec calcul du nombre de tweets positifs et négatifs, des pourcentages et des statistiques journalières.
- **CSV Export** : export des résultats d'analyse au format CSV, avec possibilité de sélectionner les colonnes à exporter.
- **Sentiment Score Histogram** : visualisation de la distribution des scores de sentiment sous forme d'histogramme, avec configuration du nombre de classes et du titre, ainsi que la possibilité d'enregistrer le graphique.

### Fixed

- **Text Cleaning** : suppression des tweets qui deviennent vides après le nettoyage afin d'éviter de conserver des données inutilisables.
- **Tokenizer** : amélioration de la gestion des nombres décimaux, des émoticônes et des émoticônes accolées aux mots.
- **Sentiment Scoring** : adaptation des tests pour permettre leur exécution sans disposer du dataset complet Sentiment140.
- **Hashtag Statistics** : validation du paramètre `n` de la fonction `top_hashtags`, avec gestion des valeurs négatives et des types non autorisés.
- **Time Series** : correction du traitement des fichiers CSV vides afin d'éviter les erreurs lors de l'agrégation des résultats.
- **Sentiment Score Histogram** : amélioration de la gestion des valeurs manquantes et non finies (`NaN`, `+Inf`, `-Inf`), avec contrôle des cas où aucun score valide n'est disponible.

## [1.0.1]
### Fixed
- clean_csv() crée le dossier de sortie s'il n'existe pas (#23, signalé par l'équipe E3)
