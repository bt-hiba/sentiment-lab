"""Tests de src/sentiment_scoring.py.

Les tests tournent sans le jeu complet Sentiment140 : le modèle est entraîné
sur un mini jeu étiqueté écrit ici. Le test des 20 000 tweets n'est lancé que
si le fichier data/raw/training.1600000.processed.noemoticon.csv existe.
"""

import csv
import tempfile
import unittest
from pathlib import Path

from src.sentiment_scoring import (
    DATASET_PATH,
    load_dataset,
    predict_sentiment,
    train_model,
)

SAMPLE_PATH = (
    Path(__file__).resolve().parent.parent / "data" / "sample" / "tweets_sample.csv"
)

# Mini jeu étiqueté, même codage que Sentiment140 : 0 = négatif, 4 = positif.
TRAIN_DATA = [
    ("love this phone amazing quality", 4),
    ("great service love it", 4),
    ("amazing product so happy", 4),
    ("happy with this great purchase", 4),
    ("best day ever love it", 4),
    ("wonderful experience great staff", 4),
    ("I love it so much", 4),
    ("amazing and wonderful", 4),
    ("great price amazing quality", 4),
    ("so happy love this", 4),
    ("excellent service great product", 4),
    ("love love love this", 4),
    ("terrible service hate it", 0),
    ("this is terrible awful quality", 0),
    ("hate this product so bad", 0),
    ("awful experience terrible staff", 0),
    ("worst purchase ever hate it", 0),
    ("so bad awful and terrible", 0),
    ("I hate it so much", 0),
    ("terrible quality bad price", 0),
    ("worst service ever terrible", 0),
    ("hate this awful phone", 0),
    ("bad product so sad", 0),
    ("sad and disappointed terrible", 0),
]


class TestSentimentScoring(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        texts = [text for text, _ in TRAIN_DATA]
        labels = [label for _, label in TRAIN_DATA]
        cls.model = train_model(texts, labels)

    def test_positive_sentiment(self):
        result = predict_sentiment(
            self.model,
            "I love this product, it is amazing!"
        )
        self.assertEqual(result["sentiment"], "positive")
        self.assertGreater(result["score"], 0)

    def test_negative_sentiment(self):
        result = predict_sentiment(
            self.model,
            "This is terrible, I hate it!"
        )
        self.assertEqual(result["sentiment"], "negative")
        self.assertLess(result["score"], 0)

    def test_score_is_between_minus_one_and_one(self):
        result = predict_sentiment(
            self.model,
            "The product arrived today."
        )
        self.assertGreaterEqual(result["score"], -1)
        self.assertLessEqual(result["score"], 1)

    def test_empty_text_raises_error(self):
        with self.assertRaises(ValueError):
            predict_sentiment(self.model, "")

    def test_team_sample_csv(self):
        with open(SAMPLE_PATH, mode="r", encoding="utf-8", newline="") as file:
            rows = list(csv.DictReader(file))

        self.assertEqual(len(rows), 20)

        analyzed_count = 0

        for row in rows:
            text = row["text"].strip()

            if not text:
                continue

            result = predict_sentiment(self.model, text)

            self.assertIn(result["sentiment"], ["positive", "negative"])
            self.assertGreaterEqual(result["score"], -1)
            self.assertLessEqual(result["score"], 1)

            analyzed_count += 1

        self.assertEqual(analyzed_count, 19)


class TestLoadDataset(unittest.TestCase):

    def test_load_dataset_balances_classes_on_a_small_file(self):
        rows = [["0", str(i), "date", "NO_QUERY", "user", f"neg {i}"] for i in range(5)]
        rows += [["4", str(i), "date", "NO_QUERY", "user", f"pos {i}"] for i in range(5)]

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "mini.csv"
            with open(path, mode="w", encoding="latin-1", newline="") as file:
                csv.writer(file).writerows(rows)

            texts, labels = load_dataset(path, max_samples_per_class=3)

        self.assertEqual(len(texts), 6)
        self.assertEqual(labels.count(0), 3)
        self.assertEqual(labels.count(4), 3)

    def test_load_dataset_rejects_a_file_with_one_class(self):
        rows = [["0", str(i), "date", "NO_QUERY", "user", f"neg {i}"] for i in range(3)]

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "one_class.csv"
            with open(path, mode="w", encoding="latin-1", newline="") as file:
                csv.writer(file).writerows(rows)

            with self.assertRaises(ValueError):
                load_dataset(path, max_samples_per_class=3)

    @unittest.skipUnless(
        DATASET_PATH.exists(),
        "Sentiment140 absent (le placer dans data/raw/, voir le README)",
    )
    def test_full_dataset_is_balanced(self):
        texts, labels = load_dataset()

        self.assertEqual(len(texts), 20000)
        self.assertEqual(labels.count(0), 10000)
        self.assertEqual(labels.count(4), 10000)


if __name__ == "__main__":
    unittest.main()