"""Extraction et analyse des hashtags dans les tweets."""

import re
from collections import Counter

import pandas as pd


HASHTAG_PATTERN = re.compile(r"#(\w+)")


def extract_hashtags(text):
    """Extrait les hashtags d'un tweet et les retourne en minuscules."""
    if not isinstance(text, str):
        return []

    return [
        match.group(1).lower()
        for match in HASHTAG_PATTERN.finditer(text)
    ]


def count_hashtags(texts):
    """Compte les occurrences de chaque hashtag dans une collection de tweets."""
    counter = Counter()

    for text in texts:
        counter.update(extract_hashtags(text))

    return pd.Series(
        dict(counter), dtype="int64", name="count"
    ).sort_values(ascending=False, kind="stable")


def top_hashtags(texts, n=10):
    """Retourne les n hashtags les plus fréquents."""
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("n doit être un entier")

    if n < 0:
        raise ValueError("n doit être positif ou nul")

    return count_hashtags(texts).head(n)


def hashtag_stats_by_date(df, date_column="date", text_column="text"):
    """Calcule le nombre d'occurrences de chaque hashtag par date."""
    if date_column not in df.columns:
        raise ValueError(f"Colonne '{date_column}' introuvable")

    if text_column not in df.columns:
        raise ValueError(f"Colonne '{text_column}' introuvable")

    data = df[[date_column, text_column]].copy()
    data["hashtag"] = data[text_column].apply(extract_hashtags)
    data = data.explode("hashtag").dropna(subset=["hashtag"])

    if data.empty:
        return pd.DataFrame(columns=["date", "hashtag", "count"])

    result = (
        data.groupby([date_column, "hashtag"])
        .size()
        .reset_index(name="count")
        .rename(columns={date_column: "date"})
    )

    return result.sort_values(
        ["date", "count", "hashtag"],
        ascending=[True, False, True]
    ).reset_index(drop=True)