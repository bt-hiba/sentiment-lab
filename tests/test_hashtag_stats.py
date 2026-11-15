from pathlib import Path

import pandas as pd
import pytest

from src.hashtag_stats import (
    extract_hashtags,
    count_hashtags,
    top_hashtags,
    hashtag_stats_by_date,
)

SAMPLE = Path(__file__).resolve().parents[1] / "data" / "sample" / "tweets_sample.csv"


# ---------- extract_hashtags ----------

def test_extract_hashtags():
    assert extract_hashtags("Love #Python and #AI") == ["python", "ai"]


def test_extract_hashtags_case_insensitive():
    assert extract_hashtags("#Python #PYTHON #python") == [
        "python", "python", "python"
    ]


def test_extract_hashtags_without_hashtag():
    assert extract_hashtags("Hello world") == []


def test_extract_hashtags_non_string():
    assert extract_hashtags(None) == []
    assert extract_hashtags(42) == []


def test_extract_multiple_hashtags():
    assert extract_hashtags("#Data #BigData #Cloud") == [
        "data", "bigdata", "cloud"
    ]


# ---------- count_hashtags ----------

def test_count_hashtags():
    tweets = [
        "Love #Python",
        "Learn #Python and #AI",
        "Explore #AI",
    ]

    result = count_hashtags(tweets)

    assert result["python"] == 2
    assert result["ai"] == 2


def test_count_hashtags_empty():
    result = count_hashtags(["Hello world", "No hashtag"])

    assert result.empty


# ---------- top_hashtags ----------

def test_top_hashtags():
    tweets = [
        "#Python #AI",
        "#Python",
        "#Python #Data",
    ]

    result = top_hashtags(tweets, n=2)

    assert list(result.index) == ["python", "ai"]
    assert list(result.values) == [3, 1]


def test_top_hashtags_negative_n():
    with pytest.raises(ValueError):
        top_hashtags(["#Python"], n=-1)



def test_top_hashtags_rejects_non_integer_n():
    with pytest.raises(TypeError):
        top_hashtags(["#python #data"], n=5.5)

    with pytest.raises(TypeError):
        top_hashtags(["#python #data"], n="5")


def test_top_hashtags_rejects_negative_n():
    with pytest.raises(ValueError):
        top_hashtags(["#python #data"], n=-1)


def test_top_hashtags_accepts_zero():
    result = top_hashtags(["#python #data"], n=0)
    assert len(result) == 0
    

# ---------- hashtag_stats_by_date ----------

def test_hashtag_stats_by_date():
    df = pd.DataFrame({
        "date": ["2024-01-01", "2024-01-01", "2024-01-02"],
        "text": ["#Python #AI", "#Python", "#AI"],
    })

    result = hashtag_stats_by_date(df)

    python = result[result["hashtag"] == "python"]
    ai = result[result["hashtag"] == "ai"]

    assert python["count"].sum() == 2
    assert ai["count"].sum() == 2


def test_hashtag_stats_by_date_missing_column():
    df = pd.DataFrame({"date": ["2024-01-01"]})

    with pytest.raises(ValueError):
        hashtag_stats_by_date(df)


def test_hashtag_stats_by_date_empty_hashtags():
    df = pd.DataFrame({
        "date": ["2024-01-01"],
        "text": ["Hello world"],
    })

    result = hashtag_stats_by_date(df)

    assert result.empty


# ---------- sample dataset ----------

def test_sample_file_exists():
    assert SAMPLE.exists()


def test_hashtag_stats_on_sample():
    df = pd.read_csv(SAMPLE)

    result = count_hashtags(df["text"])

    assert result["happy"] == 1
    assert result["apple"] == 1
    assert result["fail"] == 1
    assert result["deal"] == 1