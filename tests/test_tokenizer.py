"""Tests de src/tokenizer.py.

Lancer depuis la racine du dépôt : python -m pytest tests/test_tokenizer.py
"""

import csv
from pathlib import Path

import pytest

from src.tokenizer import tokenize

SAMPLE = Path(__file__).resolve().parents[1] / "data" / "sample" / "tweets_sample.csv"


@pytest.mark.parametrize("value", ["", "   ", "\n\t", None, float("nan"), 42])
def test_empty_or_non_text_returns_empty_list(value):
    assert tokenize(value) == []


def test_words_are_split_and_simple_punctuation_is_dropped():
    assert tokenize("Not bad, but the battery could be better.") == [
        "Not",
        "bad",
        "but",
        "the",
        "battery",
        "could",
        "be",
        "better",
    ]


def test_case_is_preserved():
    assert tokenize("Hello WORLD") == ["Hello", "WORLD"]


def test_url_mention_and_hashtag_are_kept_whole():
    assert tokenize("Love this product! http://t.co/abc #happy") == [
        "Love",
        "this",
        "product",
        "http://t.co/abc",
        "#happy",
    ]
    assert tokenize("@support terrible service... waiting for 3 days!!!") == [
        "@support",
        "terrible",
        "service",
        "waiting",
        "for",
        "3",
        "days",
    ]


def test_retweet_line():
    assert tokenize("RT @john: Best phone ever #Apple https://apple.com") == [
        "RT",
        "@john",
        "Best",
        "phone",
        "ever",
        "#Apple",
        "https://apple.com",
    ]


def test_url_without_scheme_and_trailing_punctuation():
    assert (
        tokenize("Amazing quality #deal www.shop.com/deal")[-1] == "www.shop.com/deal"
    )
    assert tokenize("Voir https://example.org/page, puis (www.test.com).") == [
        "Voir",
        "https://example.org/page",
        "puis",
        "www.test.com",
    ]


@pytest.mark.parametrize("emoticon", [":)", ":-)", ":(", ";D", ":P", "=)", ":/"])
def test_emoticons_are_single_tokens(emoticon):
    assert tokenize(f"ok {emoticon} ok") == ["ok", emoticon, "ok"]


def test_emoticon_is_not_detected_inside_words_or_times():
    assert tokenize("Note:data at 3:30") == ["Note", "data", "at", "3", "30"]


def test_each_emoji_is_a_token():
    assert tokenize("WORST experience of my life 😡😡 #fail") == [
        "WORST",
        "experience",
        "of",
        "my",
        "life",
        "😡",
        "😡",
        "#fail",
    ]


def test_accents_apostrophes_and_percent():
    assert tokenize("C'est génial, je recommande à 100% !") == [
        "C'est",
        "génial",
        "je",
        "recommande",
        "à",
        "100%",
    ]
    assert tokenize("I can't believe how good this is!!!") == [
        "I",
        "can't",
        "believe",
        "how",
        "good",
        "this",
        "is",
    ]
    assert tokenize("Très déçu, le produit est arrivé cassé...") == [
        "Très",
        "déçu",
        "le",
        "produit",
        "est",
        "arrivé",
        "cassé",
    ]


def test_lone_hash_is_ignored():
    assert tokenize("# not a tag") == ["not", "a", "tag"]


def test_sample_file_never_crashes_and_tokens_are_clean():
    with open(SAMPLE, encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))

    assert len(rows) == 20
    for row in rows:
        tokens = tokenize(row["text"])
        assert isinstance(tokens, list)
        assert all(token and not token.isspace() for token in tokens)
        if row["text"].strip():
            assert tokens, f"row {row['id']} produced no token"
        else:
            assert tokens == [], f"row {row['id']} is empty"
