import numpy as np
import pandas as pd


def compute_compactness(
    df: pd.DataFrame,
    group_cols: list[str] | None = None,
) -> pd.DataFrame:
    """
    Compute compactness metrics grouped by the given columns.

    This mirrors your notebook logic:

        compactness_base = df.dropna(subset=['player'])
        compactness = (
            compactness_base.groupby(['team','phase','possession'], as_index=False)
            .agg(
                x_mean =('x','mean'),
                y_mean = ('y','mean'),
                x_std  = ('x','std'),
                y_std  = ('y','std'),
                players_involved = ('player','nunique'),
                event_count = ('x','size')
            )
        )
        compactness['compactness_radius'] = sqrt(x_std^2 + y_std^2)
    """
    if group_cols is None:
        group_cols = ["team", "phase", "possession"]

    compactness_base = df.dropna(subset=["player"]).copy()

    compactness = (
        compactness_base.groupby(group_cols, as_index=False)
        .agg(
            x_mean=("x", "mean"),
            y_mean=("y", "mean"),
            x_std=("x", "std"),
            y_std=("y", "std"),
            players_involved=("player", "nunique"),
            event_count=("x", "size"),
        )
    )

    compactness["compactness_radius"] = np.sqrt(
        compactness["x_std"] ** 2 + compactness["y_std"] ** 2
    )

    return compactness


def clean_compactness(
    compactness: pd.DataFrame,
    min_players: int = 3,
) -> pd.DataFrame:
    """
    Clean compactness DataFrame:

    - Drop rows where compactness_radius is NaN
    - Keep only rows with players_involved >= min_players
    """
    compactness_clean = compactness.dropna(subset=["compactness_radius"]).copy()
    compactness_clean = compactness_clean[
        compactness_clean["players_involved"] >= min_players
    ]
    return compactness_clean
