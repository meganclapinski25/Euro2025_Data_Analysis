# Women's Euro 2025 Data Analysis

A data analysis project examining team compactness metrics from the Women's Euro 2025 tournament using StatsBomb event data. This project analyzes how teams organize their formations during different phases of play (in possession vs. defending) by computing compactness metrics based on player positional data.

## Overview

This project calculates team compactness by analyzing the spatial distribution of players during match events. Compactness is measured as the radius derived from the standard deviation of player x/y coordinates, providing insights into how teams structure their formations and transition between attacking and defensive phases.

The visualizations show each team's average positional shape during both attacking possessions and defensive moments out of possessions. Each dot represents the team's mean on-ball position during possession or out of possession. The circle visualizes the team's compactness radius, achieved by calculating the standard deviation of players' respective x/y locations. The smaller the circle, the more compact the team's shape.

### Analysis Insights

**Belgium's Example**: In possession, Belgium's shape is wider and more dispersed, covering almost the full width of the field, indicating a style of play that includes spreading the field and taking advantage of the wider spaces. While defending, the circles are tighter and concentrated towards the defensive half, showing that Belgium prioritizes a narrow defensive shape and organization.

**Germany's Example**: In possession, Germany is much of the opposite of Belgium—they stay compact and work their way up the field through the middle, favoring the central channels, which suggests shorter combinations between players. Defensively, Germany's compactness remains balanced, holding the defense up instead of collapsing deep into their defensive third. This reflects a very disciplined team that maintains control both in possession and out, controlling transitions and limiting open space instead of drastically shifting positionally when in transition moments.

## Features

- **Data Loading**: Automated loading of match events from StatsBomb API for Women's Euro 2025
- **Data Cleaning**: Removal of non-play events and null values, extraction of spatial coordinates
- **Compactness Analysis**: 
  - Computes compactness metrics grouped by team, phase (in_possession/defending), and possession
  - Calculates mean positions, standard deviations, and compactness radius
  - Filters for possessions with sufficient player involvement
- **Visualizations**:
  - Average team compactness comparisons
  - Phase-by-phase compactness analysis
  - Pitch maps showing team shapes during possession and defending moments

## Project Structure

- `src/data_io.py` - Functions for loading and cleaning StatsBomb event data
- `src/compactness.py` - Functions for computing compactness metrics and team summaries
- `src/viz.py` - Visualization functions for compactness analysis
- `notebooks/data_load.ipynb` - Interactive notebook demonstrating the analysis workflow
- `visuals/` - Generated visualization outputs

## Usage

See `notebooks/data_load.ipynb` for a complete workflow example demonstrating:
1. Loading Women's Euro 2025 match events
2. Cleaning and processing event data
3. Computing team compactness metrics
4. Generating visualizations

## Requirements

- pandas
- numpy
- statsbombpy
- matplotlib
- mplsoccer

## Key Metrics

The analysis computes several metrics to quantify team compactness and spatial organization:

### Per-Possession Metrics

- **x_mean, y_mean**: Mean positional coordinates of all players involved in a possession, representing the centroid of the team's shape
- **x_std, y_std**: Standard deviation of player positions along the x and y axes, measuring horizontal and vertical spread
- **Compactness Radius**: Calculated as √(x_std² + y_std²), combining both dimensions into a single measure of spatial spread. A smaller radius indicates a more compact, tighter team formation, while a larger radius suggests a more spread-out, expansive shape
- **players_involved**: Number of unique players participating in the possession/defensive moment
- **event_count**: Total number of events occurring during the possession, indicating possession length and activity

### Team-Level Summary Metrics

- **avg_radius**: Average compactness radius across all possessions for a team
- **std_radius**: Standard deviation of compactness radius, showing consistency of shape
- **avg_x_std**: Average horizontal spread, indicating typical width of formation
- **avg_y_std**: Average vertical spread, indicating typical length/depth of formation
- **avg_players**: Average number of players involved per possession

### Phase Analysis

Metrics are calculated separately for two distinct phases:
- **in_possession**: Team shape when the team has the ball
- **defending**: Team shape when the team is out of possession

This phase separation reveals how teams adapt their spatial organization between attacking and defensive situations, highlighting tactical discipline and transition behaviors.