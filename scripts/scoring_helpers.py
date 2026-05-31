from __future__ import annotations

import math
from typing import Iterable

import pandas as pd


def weighted_score(row: pd.Series, weights: dict[str, float]) -> float:
    return float(sum(row[column] * weight for column, weight in weights.items()))


def compute_weighted_series(df: pd.DataFrame, weights: dict[str, float]) -> pd.Series:
    return df.apply(lambda row: weighted_score(row, weights), axis=1)


def compute_exposure_normalised(series: pd.Series) -> pd.Series:
    minimum = float(series.min())
    maximum = float(series.max())
    if math.isclose(minimum, maximum):
        return pd.Series(0.0, index=series.index)
    return (series - minimum) / (maximum - minimum)


def compute_financial_climate_risk(
    composite_risk: pd.Series,
    exposure_normalised: pd.Series,
    climate_weight: float = 0.60,
    exposure_weight: float = 0.40,
) -> pd.Series:
    return composite_risk * climate_weight + exposure_normalised * 10 * exposure_weight


def classify_risk(score: float, thresholds: dict[str, float]) -> str:
    if score >= thresholds["critical"]:
        return "Critical"
    if score >= thresholds["high"]:
        return "High"
    if score >= thresholds["medium"]:
        return "Medium"
    return "Low"


def assign_risk_clusters(df: pd.DataFrame, feature_columns: Iterable[str]) -> pd.DataFrame:
    cluster_df = df.copy()
    cluster_df["_cluster_rank"] = cluster_df["financial_climate_risk"].rank(method="first", pct=True)
    cluster_df["risk_cluster"] = pd.cut(
        cluster_df["_cluster_rank"],
        bins=[0.0, 0.25, 0.50, 0.75, 1.0],
        labels=[0, 1, 2, 3],
        include_lowest=True,
    ).astype(int)
    cluster_df["cluster_label"] = cluster_df["risk_cluster"].map(
        {0: "Low Risk", 1: "Medium Risk", 2: "High Risk", 3: "Critical Risk"}
    )
    cluster_df = cluster_df.drop(columns="_cluster_rank")
    return cluster_df


def compute_esg_score(e_score: float, s_score: float, g_score: float, weights: dict[str, float]) -> float:
    return e_score * weights["E_WEIGHT"] + s_score * weights["S_WEIGHT"] + g_score * weights["G_WEIGHT"]


def compute_composite_score(esg_score: float, second_score: float, weights: dict[str, float]) -> float:
    return esg_score * weights["ESG_WEIGHT"] + second_score * weights["SECOND_WEIGHT"]


def classify_borrower(esg_score: float, climate_risk: float, thresholds: dict[str, float]) -> str:
    if esg_score >= thresholds["green_esg_min"] and climate_risk <= thresholds["green_climate_max"]:
        return "Green Eligible"
    if esg_score >= thresholds["standard_esg_min"] and climate_risk <= thresholds["standard_climate_max"]:
        return "Standard"
    if esg_score < thresholds["high_risk_esg_max"] or climate_risk >= thresholds["high_risk_climate_min"]:
        return "High Risk"
    return "Watch List"


def compute_module3_decision_score(esg_score: float, sector_risk_score: float, weights: dict[str, float]) -> float:
    esg_100 = esg_score * 10
    sector_readiness_100 = (10 - sector_risk_score) * 10
    return esg_100 * weights["ESG_WEIGHT"] + sector_readiness_100 * weights["SECTOR_RISK_WEIGHT"]


def classify_decision(score: float, thresholds: dict[str, float]) -> str:
    if score >= thresholds["approve_min"]:
        return "Approve"
    if score >= thresholds["conditional_approval_min"]:
        return "Conditional Approval"
    if score >= thresholds["review_required_min"]:
        return "Review Required"
    return "Decline"


def safe_gap(target: float, current: float) -> float:
    return max(0.0, round(target - current, 1))


def concentration_index(exposures: pd.Series) -> float:
    total = float(exposures.sum())
    if total == 0:
        return 0.0
    weights = exposures / total
    return float(math.sqrt((weights.pow(2)).sum()))
