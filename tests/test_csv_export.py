from pathlib import Path

import pandas as pd
import pytest

from src.csv_export import export_to_csv

SAMPLE = Path("data/sample/tweets_sample.csv")


@pytest.fixture
def results_df():
    return pd.DataFrame(
        {
            "tweet_id": [1, 2, 3],
            "text": ["I love it", "Not good", "Bof"],
            "sentiment": ["positive", "negative", "neutral"],
        }
    )


def test_export_creates_file(tmp_path, results_df):
    out = export_to_csv(results_df, tmp_path / "result.csv")
    assert out.exists()


def test_export_content_roundtrip(tmp_path, results_df):
    out = export_to_csv(results_df, tmp_path / "result.csv")
    reloaded = pd.read_csv(out)
    pd.testing.assert_frame_equal(reloaded, results_df)


def test_export_creates_missing_folder(tmp_path, results_df):
    out = export_to_csv(results_df, tmp_path / "a" / "b" / "result.csv")
    assert out.exists()


def test_export_selected_columns(tmp_path, results_df):
    out = export_to_csv(
        results_df, tmp_path / "result.csv", columns=["tweet_id", "sentiment"]
    )
    reloaded = pd.read_csv(out)
    assert list(reloaded.columns) == ["tweet_id", "sentiment"]


def test_export_unknown_column_raises(tmp_path, results_df):
    with pytest.raises(ValueError):
        export_to_csv(results_df, tmp_path / "result.csv", columns=["inconnue"])


def test_export_empty_dataframe_raises(tmp_path):
    with pytest.raises(ValueError):
        export_to_csv(pd.DataFrame(), tmp_path / "empty.csv")


def test_export_not_a_dataframe_raises(tmp_path):
    with pytest.raises(TypeError):
        export_to_csv([1, 2, 3], tmp_path / "bad.csv")


def test_export_keeps_special_characters(tmp_path):
    df = pd.DataFrame({"text": ['Il a dit "salut", puis é à ç 😀']})
    out = export_to_csv(df, tmp_path / "special.csv")
    reloaded = pd.read_csv(out, encoding="utf-8")
    assert reloaded.loc[0, "text"] == df.loc[0, "text"]


def test_export_sample_dataset(tmp_path):
    sample = pd.read_csv(SAMPLE, encoding="utf-8")
    out = export_to_csv(sample, tmp_path / "sample_out.csv")
    reloaded = pd.read_csv(out, encoding="utf-8")
    assert list(reloaded.columns) == ["id", "date", "text"]
    pd.testing.assert_frame_equal(reloaded, sample)