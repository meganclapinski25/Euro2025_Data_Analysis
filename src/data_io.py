import pandas as pd
import numpy as np
from pathlib import Path
from statsbombpy import sb


def load_euro_events(comp_id: int = 53, season_id: int = 315) -> pd.DataFrame:
    """
    Load all events for a given competition + season from StatsBomb.
    Defaults match your Women's Euro 2025 settings.
    """
    matches = sb.matches(competition_id=comp_id, season_id=season_id)

    events_list: list[pd.DataFrame] = []
    for _, row in matches.iterrows():
        match_id = int(row.match_id)
        try:
            e = sb.events(match_id=match_id)
            e["match_id"] = match_id
            events_list.append(e)
        except Exception:
            # For now just log and skip bad matches
            print(f"Error loading events for match_id={match_id}")

    if not events_list:
        raise ValueError("No events could be loaded for the given competition/season.")

    events = pd.concat(events_list, ignore_index=True)
    print("Loaded events shape:", events.shape)
    return events


def drop_mostly_null_columns(
    df: pd.DataFrame, threshold: float = 0.90
) -> tuple[pd.DataFrame, pd.Series]:
    """
    Drop columns where fraction of null values is >= threshold.
    Returns (clean_df, series_of_dropped_columns).
    """
    null_percent = df.isnull().mean()
    mostly_null = null_percent[null_percent >= threshold]

    cleaned = df.drop(columns=mostly_null.index)
    return cleaned, mostly_null


def extract_xy_from_location(
    df: pd.DataFrame, location_col: str = "location"
) -> pd.DataFrame:
    """
    From a StatsBomb-style 'location' column [x, y],
    create numeric 'x' and 'y' columns.
    """

    def _get_coords(loc):
        if isinstance(loc, list) and len(loc) >= 2:
            return loc[0], loc[1]
        return None, None

    df = df.copy()
    df["x"], df["y"] = zip(*df[location_col].apply(_get_coords))
    return df


OFF_FIELD_TYPES = [
    "Starting XI",
    "Half Start",
    "Half End",
    "Substitution",
    "Tactical Shift",
    "Referee Ball-Drop",
    "Injury Stoppage",
]


def filter_play_events(
    df: pd.DataFrame,
    type_col: str = "type",
    off_field_types: list[str] | None = None,
) -> pd.DataFrame:
    """
    Remove non-play events (starting XI, subs, etc.).
    """
    if off_field_types is None:
        off_field_types = OFF_FIELD_TYPES

    df = df.copy()
    return df[~df[type_col].isin(off_field_types)].copy()


def add_phase_column(
    df: pd.DataFrame,
    team_col: str = "team",
    poss_team_col: str = "possession_team",
    phase_col: str = "phase",
) -> pd.DataFrame:
    """
    Add a 'phase' column:
    - 'in_possession' if team == possession_team
    - 'defending' otherwise
    """
    df = df.copy()
    df[phase_col] = np.where(
        df[team_col] == df[poss_team_col],
        "in_possession",
        "defending",
    )
    return df
