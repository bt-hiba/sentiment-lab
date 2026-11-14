
import unittest
import csv
from pathlib import Path

from src.sentiment_scoring import (
    load_dataset,
    train_model,
    predict_sentiment,
)


class TestSentimentScoring(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.texts, cls.labels = load_dataset()
        cls.model = train_model(cls.texts, cls.labels)

    def test_dataset_is_balanced(self):
        self.assertEqual(len(self.texts), 20000)
        self.assertEqual(self.labels.count(0), 10000)
        self.assertEqual(self.labels.count(4), 10000)

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
        sample_path = (
            Path(__file__).resolve().parent.parent
            / "data"
            / "sample"
            / "tweets_sample.csv"
        )

        with open(sample_path, mode="r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)
            rows = list(reader)

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
  


if __name__ == "__main__":
    unittest.main()
