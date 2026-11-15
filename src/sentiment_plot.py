
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot_score_histogram(
    scores,
    bins=20,
    title="Distribution des scores de sentiment",
    output_path=None,
):
    """
    Generate a histogram of sentiment scores.

    Parameters
    ----------
    scores : pandas.Series, list or array
        Sentiment scores. Missing and non-finite values are ignored.
    bins : int
        Number of histogram bins.
    title : str
        Chart title.
    output_path : str or Path, optional
        Destination path for the PNG image.

    Returns
    -------
    matplotlib.figure.Figure
        The generated figure.

    Note
    ----
    The caller is responsible for closing the returned figure
    with plt.close(fig) after use.
    """
    valid_scores = pd.to_numeric(
        pd.Series(scores), errors="coerce"
    ).dropna()

    # Remove positive and negative infinity
    valid_scores = valid_scores[np.isfinite(valid_scores)]

    if valid_scores.empty:
        raise ValueError(
            "Aucun score de sentiment valide à afficher."
        )

    fig, ax = plt.subplots()

    ax.hist(valid_scores, bins=bins)
    ax.set_xlabel("Score")
    ax.set_ylabel("Nombre de tweets")
    ax.set_title(title)

    fig.tight_layout()

    if output_path is not None:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_path)

    return fig
