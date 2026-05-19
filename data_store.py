"""GreenCRDB — Session-based + CSV-persisted data store for web-entered records."""
from __future__ import annotations

from pathlib import Path
import pandas as pd
import streamlit as st

ENTERED_DIR = Path(__file__).parent / "data" / "entered"
ENTERED_DIR.mkdir(parents=True, exist_ok=True)

_FILES = {
    "borrowers": ENTERED_DIR / "entered_borrowers.csv",
    "sectors": ENTERED_DIR / "entered_sectors.csv",
    "decisions": ENTERED_DIR / "entered_decisions.csv",
}

_SESSION_KEYS = {
    "borrowers": "_entered_borrowers",
    "sectors": "_entered_sectors",
    "decisions": "_entered_decisions",
}

# ── Column schemas ─────────────────────────────────────────────────────────────
BORROWER_COLS = [
    "borrower_id", "borrower_name", "sector", "region", "loan_amount_tzs_mn",
    "env_score", "social_score", "governance_score", "esg_composite",
    "classification", "entered_by", "entered_at",
]

SECTOR_COLS = [
    "sector", "drought_score", "flood_score", "temperature_score",
    "transition_score", "water_stress_score", "composite_climate_risk",
    "risk_tier", "entered_by", "entered_at",
]

DECISION_COLS = [
    "borrower_id", "borrower_name", "sector", "region", "loan_amount_tzs_mn",
    "esg_composite", "composite_decision_score", "decision",
    "green_eligible", "product_type", "officer_notes",
    "entered_by", "entered_at",
]

_SCHEMAS = {"borrowers": BORROWER_COLS, "sectors": SECTOR_COLS, "decisions": DECISION_COLS}


def _load_csv(store: str) -> pd.DataFrame:
    path = _FILES[store]
    if path.exists():
        try:
            return pd.read_csv(path)
        except Exception:
            pass
    return pd.DataFrame(columns=_SCHEMAS[store])


def _get(store: str) -> pd.DataFrame:
    key = _SESSION_KEYS[store]
    if key not in st.session_state:
        st.session_state[key] = _load_csv(store)
    return st.session_state[key]


def _save(store: str, df: pd.DataFrame) -> None:
    st.session_state[_SESSION_KEYS[store]] = df
    df.to_csv(_FILES[store], index=False)


# ── Public API ─────────────────────────────────────────────────────────────────

def get_entered_borrowers() -> pd.DataFrame:
    return _get("borrowers")


def get_entered_sectors() -> pd.DataFrame:
    return _get("sectors")


def get_entered_decisions() -> pd.DataFrame:
    return _get("decisions")


def append_borrower(record: dict) -> None:
    df = _get("borrowers")
    new_row = pd.DataFrame([record])
    df = pd.concat([df, new_row], ignore_index=True)
    _save("borrowers", df)


def append_sector(record: dict) -> None:
    df = _get("sectors")
    # Replace existing entry for the same sector (upsert)
    if "sector" in df.columns and record.get("sector") in df["sector"].values:
        df = df[df["sector"] != record["sector"]]
    new_row = pd.DataFrame([record])
    df = pd.concat([df, new_row], ignore_index=True)
    _save("sectors", df)


def append_decision(record: dict) -> None:
    df = _get("decisions")
    new_row = pd.DataFrame([record])
    df = pd.concat([df, new_row], ignore_index=True)
    _save("decisions", df)


def delete_borrower(borrower_id: str) -> None:
    df = _get("borrowers")
    df = df[df["borrower_id"].astype(str) != str(borrower_id)]
    _save("borrowers", df)


def delete_sector(sector: str) -> None:
    df = _get("sectors")
    df = df[df["sector"] != sector]
    _save("sectors", df)


def delete_decision(borrower_id: str) -> None:
    df = _get("decisions")
    df = df[df["borrower_id"].astype(str) != str(borrower_id)]
    _save("decisions", df)


def merge_with_processed(processed_df: pd.DataFrame, store: str,
                          join_col: str = "sector") -> pd.DataFrame:
    """Merge entered records on top of processed CSV data (entered records take priority)."""
    entered = _get(store)
    if entered.empty:
        return processed_df
    shared_cols = [c for c in processed_df.columns if c in entered.columns]
    if not shared_cols:
        return processed_df
    entered_sub = entered[shared_cols].copy()
    # Remove rows from processed that are overridden by entered data
    if join_col in processed_df.columns and join_col in entered_sub.columns:
        mask = ~processed_df[join_col].isin(entered_sub[join_col])
        return pd.concat([processed_df[mask], entered_sub], ignore_index=True)
    return pd.concat([processed_df, entered_sub], ignore_index=True)
