import numpy as np
import pandas as pd
from scipy.spatial import ConvexHull


def _convex_hull_area(points: np.ndarray) -> float:
    """
    Compute the convex hull area for a set of 2D points (x, y).

    """
    if len(points) < 3:
        return np.nan

    hull = ConvexHull(points)
    return float(hull.area)


def compute_space_control(
    df: pd.DataFrame,
    group_cols: list[str] | None = None,
) -> pd.DataFrame:
    """
    Compute team space control using convex hull area.

    Space control represents the total area occupied by a team's
    positional structure on the pitch.

    """

    # Decide grouping columns automatically if none provided
    if group_cols is None:
        candidate_cols = ["match_id", "team", "phase"]
        group_cols = [c for c in candidate_cols if c in df.columns]

    # Remove rows without valid spatial coordinates
    base = df.dropna(subset=["x", "y"]).copy()

    # Compute convex hull area per group
    space_control = (
        base
        .groupby(group_cols, as_index=False)
        .apply(
            lambda group: _convex_hull_area(
                group[["x", "y"]].to_numpy()
            ),
            include_groups=False
        )
        .rename(columns={None: "space_control"})
    )

    return space_control


def compute_compactness(
    df: pd.DataFrame,
    group_cols: list[str] | None = None,
) -> pd.DataFrame:
    """
    Compute compactness metrics grouped by the given columns.

    Oringial Code: 
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

def team_compactness_summary(compactness_clean: pd.DataFrame) -> pd.DataFrame:
    """
    Summarise compactness by team.

    Oringial Code: 

        team_summary = (
            compactness_clean
                .groupby('team')
                .agg(
                    avg_radius=('compactness_radius','mean'),
                    std_radius=('compactness_radius','std'),
                    avg_x_std=('x_std','mean'),
                    avg_y_std=('y_std','mean'),
                    avg_players=('players_involved','mean')
                )
                .round(2)
                .sort_values('avg_radius')
        )
    """
    team_summary = (
        compactness_clean
        .groupby("team")
        .agg(
            avg_radius=("compactness_radius", "mean"),
            std_radius=("compactness_radius", "std"),
            avg_x_std=("x_std", "mean"),
            avg_y_std=("y_std", "mean"),
            avg_players=("players_involved", "mean"),
        )
        .round(2)
        .sort_values("avg_radius")
    )
    return team_summary
