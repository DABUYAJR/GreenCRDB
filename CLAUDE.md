# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

TZ-CRIP (Tanzania Climate-Finance Risk Intelligence Platform) is a three-module prototype built for a CRDB Bank engagement. It was developed as an MSc Finance & Investment academic prototype. All portfolio values and climate risk scores are **simulated/illustrative**.

## Running the pipeline

Scripts must be run in order from the project root (Python adds `scripts/` to `sys.path` automatically when a script in that directory is executed):

```bash
python3 scripts/01_TZCRIP_Module1_Sector_Climate_Risk.py
python3 scripts/02_TZCRIP_Module2_Borrower_ESG_Scoring_Engine.py
python3 scripts/03_TZCRIP_Module3_Climate_Finance_Decision_Engine.py
```

Or interactively in Jupyter:
```bash
jupyter notebook notebooks/
```

Install dependencies:
```bash
pip install -r requirements.txt
```

## Module architecture and data flow

The three modules form a sequential pipeline — each feeds into the next:

### Module 1: Sector Climate Risk Engine
- **Input:** `data/raw/crdb_sector_data.csv`, `data/raw/climate_risk_scores.csv`, `data/raw/regional_exposure_data.csv`
- **Processing:** Weighted composite climate risk scoring across 5 hazards (drought, flood, temperature, transition, water stress); rule-based risk-tier classification; percentile-rank clustering (no sklearn — uses `pd.cut` on rank percentiles)
- **Key outputs:**
  - `data/processed/module1/TZCRIP_Module1_Merged_Sector_Climate_Data.csv` — `composite_climate_risk` on **0–10 scale**
  - `data/processed/module1/TZCRIP_Module1_Sector_Risk_Ranking.csv` — the file Module 2 and 3 consume
- **Config:** `config/risk_thresholds.yaml` (module1 thresholds: medium=4.5, high=6.0, critical=7.5)

### Module 2: Borrower ESG Scoring Engine
- **Input:** `data/processed/module1/TZCRIP_Module1_Sector_Risk_Ranking.csv`
- **Processing:** Simulates ~60 borrowers per sector using `SECTOR_ESG_BASELINE` constants in the script; E/S/G pillar scoring blended with sector climate risk; borrower classification into Green Eligible / Standard / Watch List / High Risk
- **Key output:** `data/processed/module2/module2_borrower_esg_scores.csv` (lowercase — this is the file Module 3 reads)
- **Config:** `config/scoring_weights.yaml` (E=0.40, S=0.30, G=0.30; ESG_WEIGHT=0.55, CLIMATE_WEIGHT=0.45)

### Module 3: Climate Finance Decision Engine
- **Input:** `data/processed/module1/TZCRIP_Module1_Sector_Risk_Ranking.csv` and `data/processed/module2/module2_borrower_esg_scores.csv`
- **Processing:** Generates financing decisions, TCFD metrics, IFC Performance Standards alignment, green finance pipeline, scenario analysis (3 climate pathways)
- **Output:** `data/processed/module3/TZCRIP_Module3_Climate_Finance_Decisions.csv`
- **Config:** `config/scoring_weights.yaml` (ESG_WEIGHT=0.55, SECTOR_RISK_WEIGHT=0.45); `config/risk_thresholds.yaml` (approve≥65, conditional≥52, review≥40, decline<40)

## Critical scale conversion — Module 3

`composite_climate_risk` from Module 1 is on a **0–10 scale** (higher = more risky). Module 3 decision scores use a **0–100 scale** where higher = more creditworthy. The conversion **inverts** risk to readiness:

```python
# From scoring_helpers.py — compute_module3_decision_score()
esg_100 = esg_score * 10                          # 0–10 → 0–100
sector_readiness_100 = (10 - sector_risk_score) * 10  # invert: high risk → low readiness
composite_decision_score = 0.55 * esg_100 + 0.45 * sector_readiness_100
```

Do **not** pass `composite_climate_risk` directly — inversion is required, not just scaling.

## Helper modules (`scripts/`)

All three pipeline scripts import from these co-located helpers:

- **`utils.py`** — `get_project_root()`, `get_path()`, `ensure_module_dirs()`, `safe_read_csv()`, `export_csv()`, `export_figure()`, `load_yaml_config()`
- **`scoring_helpers.py`** — `compute_weighted_series()`, `compute_exposure_normalised()`, `compute_financial_climate_risk()`, `classify_risk()`, `assign_risk_clusters()`, `compute_esg_score()`, `classify_borrower()`, `compute_module3_decision_score()`, `classify_decision()`, `concentration_index()`, `safe_gap()`
- **`data_validation.py`** — `validate_module1_inputs()`, `validate_module2_input()`, `validate_module3_input()`

`load_yaml_config()` uses a custom YAML parser (no PyYAML dependency). It handles the simple key-value and nested-mapping structures used in `config/`; it does **not** support anchors, multi-line strings, or inline lists beyond `- item` syntax.

## Output destinations

Each module writes to three mirrored locations:
- `data/processed/moduleN/` — canonical CSV files for downstream consumption
- `outputs/figures/moduleN/` and `outputs/dashboards/moduleN/` — PNG/PDF dashboard exports
- `outputs/tables/moduleN/` — CSV tables for reporting

Reports (executive briefs, technical notes, presentation outlines) live under `reports/`.

## Config files

- `config/risk_thresholds.yaml` — risk tier cut-offs for all three modules
- `config/scoring_weights.yaml` — ESG pillar weights and module blend weights
- `config/sector_definitions.yaml` — canonical list of 12 sectors; used as the reference for sector names across the pipeline

Note: the Module 3 script and notebook have intentionally different names:
- script: `03_TZCRIP_Module3_Climate_Finance_Decision_Engine.py`
- notebook: `03_TZCRIP_Module3_Climate_Finance_Reporting.ipynb`
