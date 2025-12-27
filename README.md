# Spatial Structure and Tactical Style in the UEFA Women’s Euro 2025

This project analyzes team spatial organization during the UEFA Women’s Euro 2025 using
event-level StatsBomb data. The goal is to understand how teams structure themselves on the
pitch across different phases of play and what those spatial patterns reveal about tactical
style.

Rather than focusing on traditional event counts (passes, shots, duels), this analysis
introduces spatial metrics that quantify **team shape**, **compactness**, and **space usage**
during attacking and defensive phases.

---

## Key Questions

- How does team compactness change between defending and attacking phases?
- Do teams differ meaningfully in how they expand or contract their shape?
- What tactical information is captured by spatial structure that box-score metrics miss?

---

## Key Findings

- Teams consistently adopt tighter spatial structures when defending and expand modestly
  when in possession.
- Differences in compactness are driven more by phase of play than by fixed team identity.
- Teams vary in how aggressively they expand in possession, reflecting stylistic and tactical
  choices rather than a single dominant approach.
- Compactness and space control describe **how teams play** more reliably than **how often
  they win**, showing weak direct relationships with match outcomes.

---

## Why This Matters

Spatial metrics provide structural context that complements traditional performance statistics.
Analyses like this can support tactical profiling, opponent scouting, and style-based team
comparison by quantifying how teams organize themselves beyond on-ball events.

---

## Project Contents

- `notebooks/data_load.ipynb` – Main analysis notebook with visualizations and interpretations
- `src/` – Helper functions for data loading, compactness calculation, and visualization
- `visuals/` – Generated figures used in the analysis

---

## Tools Used

- Python (pandas, numpy, matplotlib)
- statsbombpy
- mplsoccer

