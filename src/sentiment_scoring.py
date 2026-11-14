
import csv
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


DATASET_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "raw"
    / "training.1600000.processed.noemoticon.csv"
)


def load_dataset(dataset_path=DATASET_PATH, max_samples_per_class=10000):
    """Load a balanced sample of negative and positive tweets."""

    texts = []
    labels = []
    class_counts = {0: 0, 4: 0}

    with open(dataset_path, mode="r", encoding="latin-1", newline="") as file:
        reader = csv.reader(file)

        for row in reader:
            if len(row) != 6:
                continue

            target = int(row[0])

            if target not in class_counts:
                continue

            if class_counts[target] >= max_samples_per_class:
                if all(
                    count >= max_samples_per_class
                    for count in class_counts.values()
                ):
                    break
                continue

            texts.append(row[5])
            labels.append(target)
            class_counts[target] += 1

    if not texts or len(set(labels)) < 2:
        raise ValueError("The dataset must contain both negative and positive tweets.")

    return texts, labels

def train_model(texts, labels):
    """Train a TF-IDF and Logistic Regression sentiment model."""

    model = Pipeline([
        (
            "tfidf",
            TfidfVectorizer(
                max_features=30000,
                ngram_range=(1, 2),
                min_df=2
            )
        ),
        (
            "classifier",
            LogisticRegression(max_iter=1000)
        )
    ])

    model.fit(texts, labels)

    return model


def predict_sentiment(model, text):
    """Predict the sentiment and return a score between -1 and +1."""

    if not isinstance(text, str) or not text.strip():
        raise ValueError("Text must be a non-empty string.")

    probabilities = model.predict_proba([text])[0]
    classes = model.classes_

    negative_probability = probabilities[list(classes).index(0)]
    positive_probability = probabilities[list(classes).index(4)]

    score = positive_probability - negative_probability

    sentiment = "positive" if score >= 0 else "negative"

    return {
        "sentiment": sentiment,
        "score": round(float(score), 4)
    }
