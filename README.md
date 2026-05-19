# TZ-CRIP

TZ-CRIP is a three-module climate-finance risk intelligence prototype for a Tanzanian bank context. The repo is designed for VS Code and Jupyter work, but the current implementation is now script-driven as well.

## Modules
- **Module 1:** Sector Climate Risk Engine
- **Module 2:** Borrower ESG Scoring Engine
- **Module 3:** Climate Finance Decision and Reporting Engine

## Current State
- Module 1 is implemented and exports sector climate-risk tables plus dashboards.
- Module 2 is implemented and consumes the Module 1 processed sector feed instead of hardcoded scores.
- Module 3 is implemented and consumes Module 1 and Module 2 outputs to generate financing decisions, reporting tables, and dashboards.
- Shared helper logic now lives in `scripts/utils.py`, `scripts/data_validation.py`, and `scripts/scoring_helpers.py`.
- Configuration is read from `config/scoring_weights.yaml` and `config/risk_thresholds.yaml`.

## Canonical Workflow
1. Run Module 1 to generate the sector climate-risk feed.
2. Run Module 2 to generate borrower ESG outputs using the Module 1 feed.
3. Run Module 3 to generate decision, reporting, and portfolio recommendation outputs.

Example commands:

```bash
python3 scripts/01_TZCRIP_Module1_Sector_Climate_Risk.py
python3 scripts/02_TZCRIP_Module2_Borrower_ESG_Scoring_Engine.py
python3 scripts/03_TZCRIP_Module3_Climate_Finance_Decision_Engine.py
```

## Notebook Order
The notebooks are still present for exploratory work and presentation:
- `notebooks/01_TZCRIP_Module1_Sector_Climate_Risk.ipynb`
- `notebooks/02_TZCRIP_Module2_Borrower_ESG_Scoring_Engine.ipynb`
- `notebooks/03_TZCRIP_Module3_Climate_Finance_Reporting.ipynb`

The script and notebook names for Module 3 are intentionally different:
- script: `03_TZCRIP_Module3_Climate_Finance_Decision_Engine.py`
- notebook: `03_TZCRIP_Module3_Climate_Finance_Reporting.ipynb`

## Folder Structure
```text
TZ-CRIP/
├── config/
├── data/
│   ├── raw/
│   ├── interim/
│   └── processed/
│       ├── module1/
│       ├── module2/
│       └── module3/
├── notebooks/
├── outputs/
│   ├── dashboards/
│   ├── figures/
│   └── tables/
├── reports/
│   ├── executive_briefs/
│   ├── presentations/
│   └── technical_notes/
├── scripts/
├── README.md
└── requirements.txt
```

## Key Design Rules
- Module outputs are written to both `data/processed/<module>` and `outputs/.../<module>` where appropriate.
- Module 2 reads `data/processed/module1/TZCRIP_Module1_Sector_Risk_Ranking.csv`.
- Module 3 reads both the Module 1 sector output and the Module 2 borrower output.
- Module 3 decision scoring uses Module 2 ESG scores on a `0-100` scale and Module 1 climate risk converted from `0-10` to climate-readiness on a `0-100` scale inside the script logic.

## Environment
Core runtime dependencies:
- `pandas`
- `numpy`
- `matplotlib`
- `seaborn`

Jupyter dependencies remain listed in `requirements.txt` for notebook usage.
