from __future__ import annotations

from typing import Iterable

import pandas as pd


def validate_required_columns(df: pd.DataFrame, required_columns: Iterable[str], dataset_name: str) -> None:
    missing = [column for column in required_columns if column not in df.columns]
    if missing:
        raise ValueError(f"{dataset_name} is missing required columns: {missing}")


def validate_numeric_range(
    df: pd.DataFrame,
    columns: Iterable[str],
    minimum: float,
    maximum: float,
    dataset_name: str,
) -> None:
    for column in columns:
        if ((df[column] < minimum) | (df[column] > maximum)).any():
            raise ValueError(
                f"{dataset_name}.{column} contains values outside the expected range {minimum} to {maximum}."
            )


def validate_non_negative(df: pd.DataFrame, columns: Iterable[str], dataset_name: str) -> None:
    for column in columns:
        if (df[column] < 0).any():
            raise ValueError(f"{dataset_name}.{column} contains negative values.")


def validate_module1_inputs(
    portfolio_df: pd.DataFrame,
    climate_df: pd.DataFrame,
    regional_df: pd.DataFrame,
) -> None:
    validate_required_columns(
        portfolio_df,
        ["sector", "loan_book_pct", "loan_book_tzs_bn", "num_borrowers"],
        "module1 portfolio input",
    )
    validate_required_columns(
        climate_df,
        [
            "sector",
            "drought_risk",
            "flood_risk",
            "temperature_risk",
            "transition_risk",
            "water_stress_risk",
        ],
        "module1 climate input",
    )
    validate_required_columns(
        regional_df,
        [
            "region",
            "portfolio_pct",
            "exposure_tzs_bn",
            "flood_hazard",
            "drought_hazard",
            "overall_climate_risk",
        ],
        "module1 regional input",
    )
    validate_numeric_range(
        climate_df,
        ["drought_risk", "flood_risk", "temperature_risk", "transition_risk", "water_stress_risk"],
        0.0,
        10.0,
        "module1 climate input",
    )
    validate_numeric_range(
        regional_df,
        ["flood_hazard", "drought_hazard", "overall_climate_risk"],
        0.0,
        10.0,
        "module1 regional input",
    )
    validate_non_negative(
        portfolio_df,
        ["loan_book_pct", "loan_book_tzs_bn", "num_borrowers"],
        "module1 portfolio input",
    )


def validate_module2_input(df: pd.DataFrame) -> None:
    validate_required_columns(
        df,
        [
            "sector",
            "loan_book_tzs_bn",
            "composite_climate_risk",
            "financial_climate_risk",
            "risk_tier",
        ],
        "module2 sector feed",
    )
    validate_numeric_range(
        df,
        ["composite_climate_risk", "financial_climate_risk"],
        0.0,
        10.0,
        "module2 sector feed",
    )


def validate_module3_input(module1_df: pd.DataFrame, module2_df: pd.DataFrame) -> None:
    validate_required_columns(
        module1_df,
        ["sector", "loan_book_tzs_bn", "composite_climate_risk", "risk_tier"],
        "module3 module1 feed",
    )
    validate_required_columns(
        module2_df,
        [
            "borrower_id",
            "borrower_name",
            "sector",
            "region",
            "loan_size_tzs_mn",
            "esg_composite",
            "sector_climate_risk",
            "final_score",
            "classification",
        ],
        "module3 module2 feed",
    )
    validate_numeric_range(
        module2_df,
        ["esg_composite", "sector_climate_risk", "final_score"],
        0.0,
        10.0,
        "module3 module2 feed",
    )
