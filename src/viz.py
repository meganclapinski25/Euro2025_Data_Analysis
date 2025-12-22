import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import Pitch


def plot_avg_team_compactness(
    compactness_clean: pd.DataFrame,
    save_path: str | None = "avgteamOverall.png",
):
    """
    Plot average compactness_radius per team as a horizontal bar chart.

    Oringial Code: 

        avg_team = compactness_clean.groupby('team')['compactness_radius'].mean().sort_values()
        fig, ax = plt.subplots(...)
        avg_team.plot(kind='barh', ...)

    Returns the (fig, ax, avg_team_series) so caller can inspect or reuse.
    """
    avg_team = (
        compactness_clean
        .groupby("team")["compactness_radius"]
        .mean()
        .sort_values()
    )

    fig, ax = plt.subplots(figsize=(8, 5))
    avg_team.plot(kind="barh", ax=ax, color="#2ecc71")
    ax.set_xlabel("Avg compactness radius (m)")
    ax.set_title("Average Team Compactness (overall)")
    plt.tight_layout()

    if save_path is not None:
        plt.savefig(save_path, dpi=300)

    return fig, ax, avg_team




def plot_team_compactness_maps(compactness_clean: pd.DataFrame):
    """
    Replaces your team_loop() function.

    For each team, and each phase ('in_possession', 'defending'):
      - takes top 10 possessions by event_count (with >= 3 players involved)
      - scales compactness_radius into a visualization radius
      - draws circles on a StatsBomb pitch around (x_mean, y_mean)
    """
    for team_name in compactness_clean["team"].dropna().unique():
        team_comp_all = compactness_clean[
            compactness_clean["team"] == team_name
        ].copy()

        # scale radius so largest ~ fits nicely on pitch
        max_r = team_comp_all["compactness_radius"].quantile(0.95)
        scale = 20.0 / max_r if pd.notna(max_r) and max_r > 0 else 1.0

        for phase in ["in_possession", "defending"]:
            rep = (
                team_comp_all[team_comp_all["phase"] == phase]
                [team_comp_all["players_involved"] >= 3]
                .sort_values("event_count", ascending=False)
                .head(10)
                .copy()
            )
            if rep.empty:
                continue

            rep["r_vis"] = rep["compactness_radius"] * scale

            pitch = Pitch(
                pitch_type="statsbomb",
                pitch_color="white",
                line_color="gray",
            )
            fig, ax = pitch.draw(figsize=(9, 6))

            color = "gold" if phase == "in_possession" else "red"

            # scatter centers
            ax.scatter(
                rep["x_mean"],
                rep["y_mean"],
                s=25,
                c=color,
                alpha=0.9,
                edgecolors="white",
                linewidth=0.5,
            )

            # circle outlines scaled by r_vis
            for _, r in rep.iterrows():
                circle = plt.Circle(
                    (r["x_mean"], r["y_mean"]),
                    r["r_vis"],
                    fill=False,
                    edgecolor=color,
                    lw=1.5,
                    alpha=0.8,
                )
                ax.add_patch(circle)

            title_phase = "In Possession" if phase == "in_possession" else "Defending"
            ax.set_title(f"{team_name} — {title_phase}", fontsize=13)
            plt.show()
