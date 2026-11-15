
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pytest

from src.sentiment_plot import plot_score_histogram


def test_returns_matplotlib_figure():
    scores = [-0.8, -0.4, 0.2, 0.5, 0.9]

    fig = plot_score_histogram(scores)

    try:
        assert isinstance(fig, matplotlib.figure.Figure)
    finally:
        plt.close(fig)


def test_histogram_bins_and_total():
    scores = [-0.8, -0.4, 0.2, 0.5, 0.9]
    bins = 5

    fig = plot_score_histogram(scores, bins=bins)

    try:
        ax = fig.axes[0]

        assert len(ax.patches) == bins

        total = sum(patch.get_height() for patch in ax.patches)
        assert total == len(scores)
    finally:
        plt.close(fig)


def test_missing_values_are_ignored():
    scores = [-0.8, None, 0.2, np.nan, 0.9]

    fig = plot_score_histogram(scores, bins=5)

    try:
        ax = fig.axes[0]

        total = sum(patch.get_height() for patch in ax.patches)
        assert total == 3
    finally:
        plt.close(fig)


def test_empty_scores_raise_value_error():
    with pytest.raises(ValueError, match="Aucun score"):
        plot_score_histogram([])


def test_all_missing_scores_raise_value_error():
    with pytest.raises(ValueError):
        plot_score_histogram([None, np.nan])


def test_output_image_is_created(tmp_path):
    scores = [-0.8, -0.4, 0.2, 0.5, 0.9]
    output_file = tmp_path / "sentiment_histogram.png"

    fig = plot_score_histogram(
        scores,
        output_path=output_file
    )

    try:
        assert output_file.exists()
        assert output_file.stat().st_size > 0
    finally:
        plt.close(fig)
