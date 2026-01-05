# TournamentAnalysis
Dash application and data processing scripts to analyze penspinning tournaments.

## Overview
- Interactive dashboard built with Dash + Plotly + Dash Ag Grid.
- Data preparation and manipulation scripts in `scripts/`.
- Data files live under `data/` (ignored by git).

## Project Structure
- `ui/StatApp.py`: main Dash app (filters, AgGrid, violin plots).
- `ui/assets/`: CSS assets loaded by Dash.
- `scripts/`: data preparation and manipulation helpers.
- `data/source/`, `data/intermediate/`, `data/result/`: input/output data folders.

## Setup
Create a virtual environment and install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run the App
```bash
python ui/StatApp.py
```

## Data Inputs
The app currently reads:
```
data/intermediate/WT25_notes_long.xlsx
```
Make sure the file exists before running the app.

## Notes
- `data/` contents are ignored via `.gitignore`.
- CSS is managed in `ui/assets/header.css`.
