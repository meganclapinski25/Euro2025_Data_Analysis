# Euro2025_Data_Analysis

A data analysis project examining team compactness metrics from the Women's Euro 2025 tournament using StatsBomb event data. This project analyzes how teams organize their formations during different phases of play (in possession vs. defending) by computing compactness metrics based on player positional data.

## Overview

This project calculates team compactness by analyzing the spatial distribution of players during match events. Compactness is measured as the radius derived from the standard deviation of player x/y coordinates, providing insights into how teams structure their formations and transition between attacking and defensive phases.

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

**Compactness Radius**: Calculated as √(x_std² + y_std²), where x_std and y_std are the standard deviations of player positions. A smaller radius indicates a more compact, tighter team formation, while a larger radius suggests a more spread-out, expansive shape.