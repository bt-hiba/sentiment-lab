from pathlib import Path

import pandas as pd
import pytest

from src.text_cleaning import (
    clean_csv,
    clean_series,
    clean_text,
    load_sentiment140,
)

SAMPLE = Path(__file__).resolve().parents[1] / "data" / "sample" / "tweets_sample.csv"


# ---------- clean_text ----------
def test_clean_text_removes_url():
    assert clean_text("Hello http://x.com") == "hello"
    assert clean_text("Look https://example.com/a?b=1 now") == "look now"
    assert clean_text("Visit www.example.com today") == "visit today"


def test_clean_text_removes_mentions():
    assert clean_text("@john thanks for the help") == "thanks for the help"


def test_clean_text_keeps_hashtag_word():
    assert clean_text("I love #Python") == "i love python"


def test_clean_text_lowercases():
    assert clean_text("GREAT Product") == "great product"


def test_clean_text_removes_punctuation():
    assert clean_text("Wow!!! Really?...") == "wow really"


def test_clean_text_keeps_apostrophes_and_accents():
    assert clean_text("C'est génial !") == "c'est génial"


def test_clean_text_removes_retweet_prefix():
    assert clean_text("RT @user: great news") == "great news"


def test_clean_text_decodes_html_entities():
    assert clean_text("Tom &amp; Jerry &quot;rock&quot;") == "tom jerry rock"


def test_clean_text_collapses_spaces():
    assert clean_text("  too    many   spaces  ") == "too many spaces"


def test_clean_text_empty_string():
    assert clean_text("") == ""


def test_clean_text_non_string_returns_empty():
    assert clean_text(None) == ""
    assert clean_text(float("nan")) == ""
    assert clean_text(42) == ""


def test_clean_text_only_noise_returns_empty():
    assert clean_text("@a http://x.com !!!") == ""


# ---------- clean_series ----------
def test_clean_series():
    series = pd.Series(["Hi @bob!", None, "#Fun http://t.co"])
    assert clean_series(series).tolist() == ["hi", "", "fun"]


# ---------- sur l'échantillon data/sample/ ----------
def test_sample_file_exists():
    assert SAMPLE.exists(), "data/sample/tweets_sample.csv est introuvable"


def test_clean_csv_on_sample(tmp_path):
    out = tmp_path / "sample_clean.csv"
    df = clean_csv(SAMPLE, out)

    assert out.exists()
    assert "clean_text" in df.columns
    assert len(df) == 20
    first = df.loc[0, "clean_text"]
    assert "http" not in first and "#" not in first and "!" not in first
    assert not df["clean_text"].str.contains(r"[@#]|http").any()


def test_clean_csv_missing_column_raises(tmp_path):
    with pytest.raises(ValueError):
        clean_csv(SAMPLE, tmp_path / "x.csv", text_column="nope")


# ---------- format Sentiment140 (sans en-tête, latin-1) ----------
def make_sent140(tmp_path):
    path = tmp_path / "sent140.csv"
    rows = (
        '"0","1","Mon Apr 06 22:19:45 PDT 2009","NO_QUERY","bob","@mary I\'m sad :( http://t.co/x"\n'
        '"4","2","Mon Apr 06 22:19:49 PDT 2009","NO_QUERY","amy","Caf\xe9 time!!! #happy"\n'
        '"4","3","Mon Apr 06 22:19:53 PDT 2009","NO_QUERY","joe","Tom &amp; Jerry"\n'
    )
    path.write_bytes(rows.encode("latin-1"))
    return path


def test_load_sentiment140(tmp_path):
    df = load_sentiment140(make_sent140(tmp_path))
    assert list(df.columns) == ["target", "id", "date", "flag", "user", "text"]
    assert len(df) == 3
    assert set(df["target"]) == {0, 4}


def test_load_sentiment140_nrows(tmp_path):
    df = load_sentiment140(make_sent140(tmp_path), nrows=2)
    assert len(df) == 2


def test_clean_csv_sentiment140(tmp_path):
    out = tmp_path / "out.csv"
    df = clean_csv(make_sent140(tmp_path), out, sentiment140=True)
    assert df["clean_text"].tolist() == ["i'm sad", "café time happy", "tom jerry"]
    assert out.exists()
