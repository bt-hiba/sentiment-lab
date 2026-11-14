from pathlib import Path
from typing import Optional, Sequence, Union

import pandas as pd


def export_to_csv(
    df: pd.DataFrame,
    path: Union[str, Path],
    columns: Optional[Sequence[str]] = None,
    index: bool = False,
    sep: str = ",",
) -> Path:

    if not isinstance(df, pd.DataFrame):
        raise TypeError("df doit être un pandas.DataFrame")
    if df.empty:
        raise ValueError("Le DataFrame à exporter est vide")

    if columns is not None:
        missing = [col for col in columns if col not in df.columns]
        if missing:
            raise ValueError(f"Colonnes introuvables : {missing}")
        df = df[list(columns)]

    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output, index=index, sep=sep, encoding="utf-8")
    return output