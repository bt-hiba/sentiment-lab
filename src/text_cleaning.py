"""Nettoyage de tweets : URLs, mentions, hashtags, ponctuation, casse.

Utilisable sur une chaîne (clean_text), une colonne pandas (clean_series)
ou directement sur un fichier CSV (clean_csv, Sentiment140 inclus).

Exemple en ligne de commande (depuis la racine du dépôt) :
    python -m src.text_cleaning data/sample/tweets_sample.csv data/processed/sample_clean.csv
    python -m src.text_cleaning data/raw/training.1600000.processed.noemoticon.csv \
        data/processed/sent140_clean.csv --sentiment140 --nrows 10000
"""
import argparse
import html
import re

import pandas as pd

URL_PATTERN = re.compile(r"(https?://|www\.)\S+")
MENTION_PATTERN = re.compile(r"@\w+")
HASHTAG_PATTERN = re.compile(r"#(\w+)")
RETWEET_PATTERN = re.compile(r"^rt\s+")
# tout sauf lettres, chiffres, espaces et apostrophes
PUNCTUATION_PATTERN = re.compile(r"[^\w\s'’]")
SPACES_PATTERN = re.compile(r"\s+")

# Sentiment140 : fichier sans en-tête, encodé en latin-1
SENTIMENT140_COLUMNS = ["target", "id", "date", "flag", "user", "text"]


def clean_text(text):
    """Nettoie un tweet et retourne une chaîne propre.

    Étapes : entités HTML (&amp; ...), minuscules, préfixe RT, URLs,
    mentions, symbole # (le mot est conservé), ponctuation, espaces.

    Une valeur vide ou non textuelle (None, NaN, nombre) retourne "".
    """
    if not isinstance(text, str):
        return ""

    text = html.unescape(text).lower().strip()
    text = RETWEET_PATTERN.sub("", text)
    text = URL_PATTERN.sub(" ", text)
    text = MENTION_PATTERN.sub(" ", text)
    text = HASHTAG_PATTERN.sub(r"\1", text)
    text = PUNCTUATION_PATTERN.sub(" ", text)
    text = SPACES_PATTERN.sub(" ", text)
    return text.strip()


def clean_series(series):
    """Applique clean_text à une colonne pandas (pd.Series) de tweets."""
    return series.apply(clean_text)


def load_sentiment140(path, nrows=None):
    """Charge le fichier Sentiment140 (sans en-tête, encodage latin-1).

    target vaut 0 (négatif) ou 4 (positif).
    """
    return pd.read_csv(
        path,
        names=SENTIMENT140_COLUMNS,
        encoding="latin-1",
        nrows=nrows,
    )


def clean_csv(input_path, output_path, text_column="text",
              sentiment140=False, nrows=None , drop_empty=True):
    """Lit un CSV de tweets, ajoute la colonne clean_text, écrit le résultat.

    Retourne le DataFrame nettoyé.
    """
    if sentiment140:
        df = load_sentiment140(input_path, nrows=nrows)
    else:
        df = pd.read_csv(input_path, nrows=nrows)

    if text_column not in df.columns:
        raise ValueError(f"Colonne '{text_column}' introuvable : {list(df.columns)}")

    df["clean_text"] = clean_series(df[text_column])
    if drop_empty:
        df = df[df["clean_text"] != ""].reset_index(drop=True)
    df.to_csv(output_path, index=False)
    return df


def main():
    parser = argparse.ArgumentParser(description="Nettoie un CSV de tweets.")
    parser.add_argument("input", help="CSV d'entrée (ex. data/raw/...)")
    parser.add_argument("output", help="CSV de sortie (ex. data/processed/...)")
    parser.add_argument("--sentiment140", action="store_true",
                        help="Le fichier est au format Sentiment140")
    parser.add_argument("--nrows", type=int, default=None,
                        help="Ne traiter que les N premières lignes")
    args = parser.parse_args()

    df = clean_csv(args.input, args.output,
                   sentiment140=args.sentiment140, nrows=args.nrows)
    print(f"{len(df)} tweets nettoyés -> {args.output}")


if __name__ == "__main__":
    main()