import pandas as pd

from src.time_series import (
    parse_dates,
    aggregate_daily_sentiment,
    export_daily_stats
)


def test_parse_dates():
    df = pd.DataFrame({
        "date": ["Mon Apr 06 22:19:45 PDT 2009"]
    })

    result = parse_dates(df)

    assert pd.api.types.is_datetime64_any_dtype(result["date"])
    assert str(result["date"].dt.tz) == "UTC"


def test_aggregate_daily_sentiment():
    df = pd.DataFrame({
        "target": [4, 0, 4, 0],
        "date": pd.to_datetime([
            "2024-01-01",
            "2024-01-01",
            "2024-01-01",
            "2024-01-02"
        ], utc=True)
    })

    result = aggregate_daily_sentiment(df)

    first_day = result[result["day"] == "2024-01-01"].iloc[0]

    assert first_day["total_tweets"] == 3
    assert first_day["positive_tweets"] == 2
    assert first_day["negative_tweets"] == 1
    assert first_day["positive_rate"] == 66.67
    assert first_day["negative_rate"] == 33.33


def test_export_daily_stats(tmp_path):
    df = pd.DataFrame({
        "day": ["2024-01-01"],
        "total_tweets": [2],
        "positive_tweets": [1],
        "negative_tweets": [1],
        "positive_rate": [50.0],
        "negative_rate": [50.0]
    })

    output_file = tmp_path / "daily_sentiment.csv"

    export_daily_stats(df, output_file)

    result = pd.read_csv(output_file)

    assert len(result) == 1
    assert result.iloc[0]["total_tweets"] == 2