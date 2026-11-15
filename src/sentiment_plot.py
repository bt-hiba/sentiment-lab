
import pandas as pd
import matplotlib.pyplot as plt


def plot_score_histogram(
    scores,
    bins=20,
    title="Distribution des scores de sentiment",
    output_path=None
):
    """
    Génère un histogramme de distribution des scores de sentiment.

    Parameters
    ----------
    scores : pandas.Series, list or array
        Scores de sentiment des tweets.
    bins : int
        Nombre de classes de l'histogramme.
    title : str
        Titre du graphique.
    output_path : str or Path, optional
        Chemin où enregistrer l'image PNG.

    Returns
    -------
    matplotlib.figure.Figure
        Figure Matplotlib générée.

    Raises
    ------
    ValueError
        Si aucun score valide n'est disponible.
    """

    # Convertir les scores en valeurs numériques
    valid_scores = pd.to_numeric(
        pd.Series(scores),
        errors="coerce"
    ).dropna()

    # Vérifier qu'il reste des scores valides
    if valid_scores.empty:
        raise ValueError("Aucun score de sentiment valide à afficher.")

    # Créer la figure avec l'API objet
    fig, ax = plt.subplots()

    # Générer l'histogramme
    ax.hist(valid_scores, bins=bins)

    # Configurer les axes et le titre
    ax.set_xlabel("Score")
    ax.set_ylabel("Nombre de tweets")
    ax.set_title(title)

    # Ajuster la disposition
    fig.tight_layout()

    # Enregistrer l'image si un chemin est fourni
    if output_path is not None:
        fig.savefig(output_path)

    return fig
