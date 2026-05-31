from __future__ import annotations

import warnings
from pathlib import Path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from data_validation import validate_module1_inputs
from scoring_helpers import (
    assign_risk_clusters,
    classify_risk,
    compute_exposure_normalised,
    compute_financial_climate_risk,
    compute_weighted_series,
)
from utils import ensure_module_dirs, export_csv, export_figure, get_project_root, load_yaml_config, safe_read_csv

warnings.filterwarnings("ignore")

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)
pd.set_option("display.float_format", lambda x: f"{x:,.2f}")

CRDB_GREEN = "#006B3C"
RISK_COLOURS = {
    "Critical": "#7b241c",
    "High": "#e74c3c",
    "Medium": "#f39c12",
    "Low": "#2ecc71",
}
RISK_COLUMNS = [
    "drought_risk",
    "flood_risk",
    "temperature_risk",
    "transition_risk",
    "water_stress_risk",
]


def load_inputs(root: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    portfolio_df = safe_read_csv(root / "data" / "raw" / "crdb_sector_data.csv")
    climate_df = safe_read_csv(root / "data" / "raw" / "climate_risk_scores.csv")
    regional_df = safe_read_csv(root / "data" / "raw" / "regional_exposure_data.csv")
    validate_module1_inputs(portfolio_df, climate_df, regional_df)
    return portfolio_df, climate_df, regional_df


def build_sector_scores(root: Path) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, float]]:
    portfolio_df, climate_df, regional_df = load_inputs(root)
    thresholds = load_yaml_config("risk_thresholds.yaml")["module1"]

    hazard_weights = {
        "drought_risk": 0.25,
        "flood_risk": 0.25,
        "temperature_risk": 0.20,
        "transition_risk": 0.20,
        "water_stress_risk": 0.10,
    }

    sector_df = portfolio_df.merge(climate_df, on="sector", how="inner")
    sector_df["composite_climate_risk"] = compute_weighted_series(sector_df, hazard_weights)
    sector_df["exposure_normalised"] = compute_exposure_normalised(sector_df["loan_book_tzs_bn"])
    sector_df["financial_climate_risk"] = compute_financial_climate_risk(
        sector_df["composite_climate_risk"],
        sector_df["exposure_normalised"],
    )
    sector_df["risk_tier"] = sector_df["financial_climate_risk"].apply(lambda score: classify_risk(score, thresholds))
    sector_df = assign_risk_clusters(
        sector_df,
        ["composite_climate_risk", "exposure_normalised", "financial_climate_risk"],
    )
    sector_df = sector_df.sort_values("financial_climate_risk", ascending=False).reset_index(drop=True)
    return sector_df, regional_df, thresholds


def create_dashboard(sector_df: pd.DataFrame, regional_df: pd.DataFrame, thresholds: dict[str, float]):
    fig = plt.figure(figsize=(20, 24))
    fig.patch.set_facecolor("#f8f9fa")

    ax_title = fig.add_axes([0, 0.95, 1, 0.05])
    ax_title.set_facecolor(CRDB_GREEN)
    ax_title.text(
        0.5,
        0.65,
        "TZ-CRIP: Tanzania Climate-Finance Analytics Demonstrator",
        ha="center",
        va="center",
        fontsize=20,
        fontweight="bold",
        color="white",
    )
    ax_title.text(
        0.5,
        0.20,
        "CRDB Bank Portfolio Climate Risk Assessment | Module 1: Sector Risk Mapper | Prototype v2.0",
        ha="center",
        va="center",
        fontsize=11,
        color="#d4e6d4",
    )
    ax_title.axis("off")

    total_exposure = sector_df["loan_book_tzs_bn"].sum()
    high_risk_exp = sector_df[sector_df["risk_tier"].isin(["High", "Critical"])]["loan_book_tzs_bn"].sum()

    ax_sub = fig.add_axes([0, 0.92, 1, 0.03])
    ax_sub.set_facecolor("#f8f9fa")
    ax_sub.text(
        0.5,
        0.5,
        f"Total Portfolio Analysed: TZS {total_exposure:,.0f}Bn | High/Critical Risk Exposure: "
        f"TZS {high_risk_exp:,.0f}Bn ({high_risk_exp / total_exposure * 100:.1f}% of portfolio)",
        ha="center",
        va="center",
        fontsize=12,
        color="#2c3e50",
        fontweight="bold",
    )
    ax_sub.axis("off")

    gs = fig.add_gridspec(3, 2, left=0.06, right=0.97, top=0.90, bottom=0.04, hspace=0.38, wspace=0.30)

    ax1 = fig.add_subplot(gs[0, :])
    df_sorted = sector_df.sort_values("financial_climate_risk", ascending=True)
    bars = ax1.barh(
        df_sorted["sector"],
        df_sorted["financial_climate_risk"],
        color=[RISK_COLOURS[tier] for tier in df_sorted["risk_tier"]],
        edgecolor="white",
        linewidth=0.5,
        height=0.65,
    )
    ax1.set_xlabel("Financial Climate Risk Score (0-10)")
    ax1.set_title("Sector Financial Climate Risk Score", fontsize=13, fontweight="bold", pad=12)
    ax1.set_xlim(0, 11)
    ax1.axvline(x=thresholds["medium"], color="gray", linestyle="--", alpha=0.5, linewidth=1)
    ax1.axvline(x=thresholds["high"], color="orange", linestyle="--", alpha=0.5, linewidth=1)
    ax1.axvline(x=thresholds["critical"], color="red", linestyle="--", alpha=0.5, linewidth=1)
    for bar, (_, row) in zip(bars, df_sorted.iterrows()):
        ax1.text(
            bar.get_width() + 0.1,
            bar.get_y() + bar.get_height() / 2,
            f"TZS {row['loan_book_tzs_bn']:,.0f}Bn [{row['risk_tier']}]",
            va="center",
            fontsize=9,
        )
    ax1.legend(handles=[mpatches.Patch(color=value, label=key) for key, value in RISK_COLOURS.items()], fontsize=9)
    ax1.set_facecolor("white")
    ax1.grid(axis="x", alpha=0.3)

    ax2 = fig.add_subplot(gs[1, 0])
    heat_data = df_sorted.set_index("sector")[RISK_COLUMNS]
    heat_data.columns = ["Drought", "Flood", "Temperature", "Transition", "Water Stress"]
    sns.heatmap(
        heat_data,
        ax=ax2,
        cmap="RdYlGn_r",
        vmin=0,
        vmax=10,
        annot=True,
        fmt=".1f",
        linewidths=0.5,
        cbar_kws={"label": "Risk Score (0-10)"},
        annot_kws={"size": 8},
    )
    ax2.set_title("Climate Risk Breakdown by Sector", fontsize=12, fontweight="bold", pad=10)

    ax3 = fig.add_subplot(gs[1, 1])
    ax3.scatter(
        sector_df["composite_climate_risk"],
        sector_df["loan_book_tzs_bn"],
        s=sector_df["num_borrowers"] / 80,
        c=[RISK_COLOURS[tier] for tier in sector_df["risk_tier"]],
        alpha=0.8,
        edgecolors="white",
        linewidth=1.2,
    )
    for _, row in sector_df.iterrows():
        ax3.annotate(row["sector"], (row["composite_climate_risk"], row["loan_book_tzs_bn"]), xytext=(6, 4), textcoords="offset points", fontsize=8)
    ax3.set_xlabel("Composite Climate Risk Score")
    ax3.set_ylabel("Loan Book Exposure (TZS Bn)")
    ax3.set_title("Risk vs Exposure Bubble Chart", fontsize=12, fontweight="bold", pad=10)
    ax3.set_facecolor("white")
    ax3.grid(alpha=0.3)

    ax4 = fig.add_subplot(gs[2, 0])
    regional_sorted = regional_df.sort_values("overall_climate_risk", ascending=True)
    regional_colours = [RISK_COLOURS[classify_risk(score, thresholds)] for score in regional_sorted["overall_climate_risk"]]
    ax4.barh(
        regional_sorted["region"],
        regional_sorted["overall_climate_risk"],
        color=regional_colours,
        edgecolor="white",
        linewidth=0.5,
        height=0.65,
    )
    ax4.set_xlabel("Regional Climate Risk Score (0-10)")
    ax4.set_title("Regional Portfolio Climate Risk", fontsize=12, fontweight="bold", pad=10)
    ax4.set_facecolor("white")
    ax4.grid(axis="x", alpha=0.3)
    for index, (_, row) in enumerate(regional_sorted.iterrows()):
        ax4.text(row["overall_climate_risk"] + 0.1, index, f"TZS {row['exposure_tzs_bn']:,.0f}Bn", va="center", fontsize=8.5)

    ax5 = fig.add_subplot(gs[2, 1])
    risk_summary = (
        sector_df.groupby("risk_tier")
        .agg(sectors=("sector", "count"), total_exposure=("loan_book_tzs_bn", "sum"))
        .reset_index()
    )
    risk_summary["risk_tier"] = pd.Categorical(risk_summary["risk_tier"], categories=["Critical", "High", "Medium", "Low"], ordered=True)
    risk_summary = risk_summary.sort_values("risk_tier")
    x_positions = np.arange(len(risk_summary))
    bars2 = ax5.bar(
        x_positions,
        risk_summary["total_exposure"],
        color=[RISK_COLOURS[tier] for tier in risk_summary["risk_tier"]],
        width=0.5,
        edgecolor="white",
        linewidth=0.5,
    )
    ax5.set_xticks(x_positions)
    ax5.set_xticklabels(risk_summary["risk_tier"], fontsize=11)
    ax5.set_ylabel("Total Exposure (TZS Bn)")
    ax5.set_title("Portfolio Exposure by Risk Tier", fontsize=12, fontweight="bold", pad=10)
    ax5.set_facecolor("white")
    ax5.grid(axis="y", alpha=0.3)
    for bar, (_, row) in zip(bars2, risk_summary.iterrows()):
        ax5.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 15,
            f"{row['sectors']} sectors\nTZS {row['total_exposure']:,.0f}Bn",
            ha="center",
            va="bottom",
            fontsize=9,
            fontweight="bold",
        )

    fig.text(
        0.5,
        0.01,
        "TZ-CRIP Prototype | Config-driven Module 1 pipeline | For demonstration purposes",
        ha="center",
        fontsize=8,
        color="gray",
        style="italic",
    )
    return fig


def export_outputs(root: Path, sector_df: pd.DataFrame, regional_df: pd.DataFrame, fig) -> None:
    paths = ensure_module_dirs("module1", root=root)
    export_csv(
        sector_df,
        paths["processed"] / "TZCRIP_Module1_Sector_Risk_Ranking.csv",
        paths["tables"] / "TZCRIP_Module1_Sector_Risk_Ranking.csv",
        paths["tables"] / "sector_risk_ranking.csv",
    )
    export_csv(sector_df, paths["processed"] / "TZCRIP_Module1_Merged_Sector_Climate_Data.csv")
    export_csv(regional_df, paths["processed"] / "TZCRIP_Module1_Regional_Climate_Exposure_Data.csv")
    export_figure(
        fig,
        paths["figures"] / "TZCRIP_Module1_Sector_Climate_Risk_Dashboard.png",
        paths["dashboards"] / "TZCRIP_Module1_Sector_Climate_Risk_Dashboard.pdf",
        paths["figures"] / "TZCRIP_CRDB_Climate_Risk_Dashboard.png",
        paths["dashboards"] / "TZCRIP_CRDB_Climate_Risk_Dashboard.pdf",
    )


def print_summary(sector_df: pd.DataFrame) -> None:
    total_exposure = sector_df["loan_book_tzs_bn"].sum()
    high_risk_exp = sector_df[sector_df["risk_tier"].isin(["High", "Critical"])]["loan_book_tzs_bn"].sum()

    print("\n" + "=" * 70)
    print(" TZ-CRIP PORTFOLIO CLIMATE RISK SUMMARY — CRDB BANK")
    print("=" * 70)
    print(f"\n Total Portfolio Analysed : TZS {total_exposure:,.0f} Billion")
    print(f" Sectors Assessed         : {len(sector_df)}")
    print(f" High/Critical Exposure   : TZS {high_risk_exp:,.0f}Bn ({high_risk_exp / total_exposure * 100:.1f}%)")
    print("\n SECTOR RISK RANKING:")
    print(f" {'Sector':<22} {'Risk Score':>10} {'Tier':>10} {'Exposure (TZS Bn)':>18}")
    print(" " + "-" * 66)
    for _, row in sector_df.iterrows():
        print(f" {row['sector']:<22} {row['financial_climate_risk']:>10.2f} {row['risk_tier']:>10} {row['loan_book_tzs_bn']:>18,.0f}")


def main() -> None:
    root = get_project_root(Path(__file__))
    sector_df, regional_df, thresholds = build_sector_scores(root)
    fig = create_dashboard(sector_df, regional_df, thresholds)
    export_outputs(root, sector_df, regional_df, fig)
    print_summary(sector_df)
    plt.close(fig)


if __name__ == "__main__":
    main()
