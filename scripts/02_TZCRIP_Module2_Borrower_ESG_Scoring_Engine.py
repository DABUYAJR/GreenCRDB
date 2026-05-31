from __future__ import annotations

import warnings
from pathlib import Path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from data_validation import validate_module2_input
from scoring_helpers import classify_borrower, compute_esg_score
from utils import ensure_module_dirs, export_csv, export_figure, get_project_root, load_yaml_config, safe_read_csv

warnings.filterwarnings("ignore")

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 220)
pd.set_option("display.float_format", lambda x: f"{x:,.2f}")

CRDB_GREEN = "#006B3C"
ESG_COLOURS = {
    "Green Eligible": "#1D9E75",
    "Standard": "#378ADD",
    "Watch List": "#EF9F27",
    "High Risk": "#D85A30",
}
CLASS_ORDER = ["Green Eligible", "Standard", "Watch List", "High Risk"]

REGIONS = [
    "Dar es Salaam",
    "Arusha",
    "Mwanza",
    "Dodoma",
    "Mbeya",
    "Tanga",
    "Kilimanjaro",
    "Morogoro",
    "Iringa",
    "Tabora",
]

BORROWER_TYPES = {
    "Agriculture": ["Smallholder Coop", "Agribusiness Ltd", "Farm Inputs Co"],
    "Trade & Commerce": ["Import/Export Ltd", "Retail Chain Co", "Wholesale Dist"],
    "Real Estate": ["Property Dev Ltd", "Housing Trust", "Commercial REIT"],
    "Manufacturing": ["Food Processing", "Textile Mill", "Packaging Co"],
    "Transport": ["Logistics Ltd", "Bus Operator", "Freight Co"],
    "Energy": ["Solar Developer", "Hydro Plant Co", "Fuel Dist Ltd"],
    "Tourism & Hotels": ["Safari Lodge", "City Hotel", "Eco-Tourism Co"],
    "Personal Loans": ["Individual Borrower", "SME Owner", "Salaried Employee"],
    "Construction": ["Civil Works Ltd", "Roads Contractor", "Building Co"],
    "Mining": ["Minerals Ltd", "Artisanal Coop", "Quarry Co"],
    "Microfinance": ["Women's Group", "Youth Enterprise", "Rural SACCO"],
    "Health & Education": ["Private Clinic", "School Ltd", "Pharmacy Co"],
}

SECTOR_ESG_BASELINE = {
    "Agriculture": (4.5, 5.5, 4.0),
    "Trade & Commerce": (5.0, 5.8, 5.5),
    "Real Estate": (4.8, 4.5, 5.2),
    "Manufacturing": (4.2, 5.0, 5.8),
    "Transport": (4.0, 5.2, 5.5),
    "Energy": (6.5, 5.5, 6.0),
    "Tourism & Hotels": (6.0, 6.5, 5.8),
    "Personal Loans": (5.5, 6.0, 5.5),
    "Construction": (3.8, 4.8, 4.5),
    "Mining": (3.5, 4.2, 4.8),
    "Microfinance": (5.2, 7.0, 4.5),
    "Health & Education": (5.8, 7.5, 6.0),
}

E_DIMS = {
    "env_management": 0.30,
    "pollution_control": 0.25,
    "climate_adaptation": 0.30,
    "renewable_energy": 0.15,
}
S_DIMS = {
    "labour_practices": 0.35,
    "community_impact": 0.35,
    "gender_inclusion": 0.30,
}
G_DIMS = {
    "board_oversight": 0.35,
    "transparency": 0.35,
    "compliance_record": 0.30,
}


def score(rng: np.random.Generator, base: float, std: float = 1.5) -> float:
    return float(np.clip(rng.normal(base, std), 1.0, 10.0))


def load_module1_feed(root: Path) -> pd.DataFrame:
    module1_df = safe_read_csv(
        root / "data" / "processed" / "module1" / "TZCRIP_Module1_Sector_Risk_Ranking.csv",
        required_columns=["sector", "loan_book_pct", "composite_climate_risk", "risk_tier"],
    )
    validate_module2_input(module1_df)
    return module1_df


def simulate_borrowers(module1_df: pd.DataFrame, weights_cfg: dict[str, float], thresholds_cfg: dict[str, float]) -> pd.DataFrame:
    rng = np.random.default_rng(42)
    sectors = module1_df["sector"].tolist()
    sector_weights = (module1_df["loan_book_pct"] / module1_df["loan_book_pct"].sum()).tolist()
    n_borrowers = 60

    borrower_sectors = rng.choice(sectors, size=n_borrowers, p=sector_weights)
    borrower_regions = rng.choice(REGIONS, size=n_borrowers)
    loan_sizes_tzs_mn = np.clip(rng.lognormal(mean=4.5, sigma=1.2, size=n_borrowers), 5, 2000).round(1)

    climate_lookup = module1_df.set_index("sector")["composite_climate_risk"].to_dict()
    scoring_weights = {
        "E_WEIGHT": weights_cfg["E_WEIGHT"],
        "S_WEIGHT": weights_cfg["S_WEIGHT"],
        "G_WEIGHT": weights_cfg["G_WEIGHT"],
    }

    rows: list[dict[str, object]] = []
    for index, sector in enumerate(borrower_sectors):
        base_name = rng.choice(BORROWER_TYPES[sector])
        borrower_name = f"{base_name} {rng.integers(100, 999)}"
        e_base, s_base, g_base = SECTOR_ESG_BASELINE[sector]

        env_management = score(rng, e_base)
        pollution_control = score(rng, e_base - 0.3)
        climate_adaptation = score(rng, e_base + 0.2)
        renewable_energy = score(rng, e_base - 0.5)

        labour_practices = score(rng, s_base)
        community_impact = score(rng, s_base + 0.3)
        gender_inclusion = score(rng, s_base - 0.2)

        board_oversight = score(rng, g_base)
        transparency = score(rng, g_base - 0.3)
        compliance_record = score(rng, g_base + 0.4)

        e_score = (
            env_management * E_DIMS["env_management"]
            + pollution_control * E_DIMS["pollution_control"]
            + climate_adaptation * E_DIMS["climate_adaptation"]
            + renewable_energy * E_DIMS["renewable_energy"]
        )
        s_score = (
            labour_practices * S_DIMS["labour_practices"]
            + community_impact * S_DIMS["community_impact"]
            + gender_inclusion * S_DIMS["gender_inclusion"]
        )
        g_score = (
            board_oversight * G_DIMS["board_oversight"]
            + transparency * G_DIMS["transparency"]
            + compliance_record * G_DIMS["compliance_record"]
        )

        esg_composite = compute_esg_score(e_score, s_score, g_score, scoring_weights)
        climate_risk = float(climate_lookup[sector])
        climate_performance = 10 - climate_risk
        final_score = esg_composite * weights_cfg["ESG_WEIGHT"] + climate_performance * weights_cfg["CLIMATE_WEIGHT"]
        classification = classify_borrower(esg_composite, climate_risk, thresholds_cfg)

        rows.append(
            {
                "borrower_id": f"BRW-{index + 1:03d}",
                "borrower_name": borrower_name,
                "sector": sector,
                "region": borrower_regions[index],
                "loan_size_tzs_mn": round(float(loan_sizes_tzs_mn[index]), 1),
                "env_management": round(env_management, 2),
                "pollution_control": round(pollution_control, 2),
                "climate_adaptation": round(climate_adaptation, 2),
                "renewable_energy": round(renewable_energy, 2),
                "labour_practices": round(labour_practices, 2),
                "community_impact": round(community_impact, 2),
                "gender_inclusion": round(gender_inclusion, 2),
                "board_oversight": round(board_oversight, 2),
                "transparency": round(transparency, 2),
                "compliance_record": round(compliance_record, 2),
                "E_score": round(e_score, 2),
                "S_score": round(s_score, 2),
                "G_score": round(g_score, 2),
                "esg_composite": round(esg_composite, 2),
                "sector_climate_risk": round(climate_risk, 2),
                "climate_performance": round(climate_performance, 2),
                "final_score": round(final_score, 2),
                "classification": classification,
                "green_loan_eligible": classification == "Green Eligible",
            }
        )

    borrower_df = pd.DataFrame(rows).sort_values("final_score", ascending=False).reset_index(drop=True)
    borrower_df["rank"] = borrower_df.index + 1
    ordered_columns = ["rank"] + [column for column in borrower_df.columns if column != "rank"]
    return borrower_df[ordered_columns]


def build_summaries(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    class_summary = (
        df.groupby("classification")
        .agg(
            borrowers=("borrower_id", "count"),
            total_exposure_tzs_mn=("loan_size_tzs_mn", "sum"),
            avg_esg=("esg_composite", "mean"),
            avg_climate_risk=("sector_climate_risk", "mean"),
            avg_final=("final_score", "mean"),
        )
        .reindex(CLASS_ORDER)
        .reset_index()
    )
    sector_summary = (
        df.groupby("sector")
        .agg(
            borrowers=("borrower_id", "count"),
            avg_E=("E_score", "mean"),
            avg_S=("S_score", "mean"),
            avg_G=("G_score", "mean"),
            avg_esg=("esg_composite", "mean"),
            avg_climate_risk=("sector_climate_risk", "mean"),
            avg_final=("final_score", "mean"),
            green_count=("green_loan_eligible", "sum"),
        )
        .sort_values("avg_final", ascending=False)
        .reset_index()
    )
    return class_summary, sector_summary


def create_dashboard(df: pd.DataFrame, class_summary: pd.DataFrame):
    green_candidates = df[df["classification"] == "Green Eligible"]
    watchlist = df[df["classification"] == "Watch List"]
    high_risk = df[df["classification"] == "High Risk"]

    fig = plt.figure(figsize=(22, 26))
    fig.patch.set_facecolor("#f8f9fa")

    ax_title = fig.add_axes([0, 0.955, 1, 0.045])
    ax_title.set_facecolor(CRDB_GREEN)
    ax_title.text(0.5, 0.65, "TZ-CRIP: Tanzania Climate-Finance Risk Intelligence Platform", ha="center", va="center", fontsize=20, fontweight="bold", color="white")
    ax_title.text(
        0.5,
        0.18,
        f"Module 2: Borrower ESG Scoring Engine | {len(df)} Borrowers Assessed | Green Eligible: {len(green_candidates)} | High Risk: {len(high_risk)} | Prototype v2.0",
        ha="center",
        va="center",
        fontsize=10.5,
        color="#d4e6d4",
    )
    ax_title.axis("off")

    gs = fig.add_gridspec(4, 2, left=0.06, right=0.97, top=0.945, bottom=0.04, hspace=0.42, wspace=0.30)

    ax1 = fig.add_subplot(gs[0, 0])
    class_counts = df["classification"].value_counts().reindex(CLASS_ORDER).fillna(0)
    bars1 = ax1.bar(CLASS_ORDER, class_counts.values, color=[ESG_COLOURS[item] for item in CLASS_ORDER], edgecolor="white", linewidth=0.8, width=0.6)
    ax1.set_title("Borrower classification distribution", fontsize=12, fontweight="bold", pad=10)
    ax1.set_ylabel("Number of borrowers")
    ax1.set_facecolor("white")
    ax1.grid(axis="y", alpha=0.3)
    for bar, value in zip(bars1, class_counts.values):
        ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3, f"{int(value)}\nborrowers", ha="center", va="bottom", fontsize=9, fontweight="bold")

    ax2 = fig.add_subplot(gs[0, 1])
    for classification, group in df.groupby("classification"):
        ax2.scatter(
            group["sector_climate_risk"],
            group["esg_composite"],
            c=ESG_COLOURS[classification],
            s=group["loan_size_tzs_mn"] / 2,
            alpha=0.75,
            edgecolors="white",
            linewidth=0.8,
            label=classification,
        )
    ax2.set_xlabel("Sector climate risk (Module 1 score, 0-10)")
    ax2.set_ylabel("ESG composite score (0-10)")
    ax2.set_title("ESG performance vs sector climate risk", fontsize=12, fontweight="bold", pad=10)
    ax2.legend(fontsize=8, loc="upper right")
    ax2.set_facecolor("white")
    ax2.grid(alpha=0.3)

    ax3 = fig.add_subplot(gs[1, :])
    pillar_by_sector = df.groupby("sector")[["E_score", "S_score", "G_score"]].mean()
    pillar_by_sector.columns = ["Environmental (E)", "Social (S)", "Governance (G)"]
    pillar_by_sector = pillar_by_sector.sort_values("Environmental (E)", ascending=False)
    sns.heatmap(
        pillar_by_sector,
        ax=ax3,
        cmap="RdYlGn",
        vmin=2,
        vmax=8,
        annot=True,
        fmt=".1f",
        linewidths=0.5,
        cbar_kws={"label": "Average pillar score (0-10)"},
        annot_kws={"size": 9},
    )
    ax3.set_title("ESG pillar scores by sector", fontsize=12, fontweight="bold", pad=10)

    ax4 = fig.add_subplot(gs[2, 0])
    top_green = green_candidates.nlargest(min(10, len(green_candidates)), "final_score")
    if len(top_green) > 0:
        bars4 = ax4.barh(top_green["borrower_name"], top_green["final_score"], color=ESG_COLOURS["Green Eligible"], edgecolor="white", linewidth=0.5, height=0.65)
        ax4.set_xlabel("Final ESG-Climate score (0-10)")
        ax4.set_title("Top green-eligible borrowers", fontsize=12, fontweight="bold", pad=10)
        ax4.set_facecolor("white")
        ax4.grid(axis="x", alpha=0.3)
        ax4.set_xlim(0, 10)
        for bar, (_, row) in zip(bars4, top_green.iterrows()):
            ax4.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height() / 2, f"TZS {row['loan_size_tzs_mn']:,.0f}Mn [{row['sector'][:14]}]", va="center", fontsize=8)
    else:
        ax4.text(0.5, 0.5, "No green-eligible borrowers identified", ha="center", va="center", transform=ax4.transAxes)
        ax4.axis("off")

    ax5 = fig.add_subplot(gs[2, 1])
    concern_chart = pd.concat([high_risk, watchlist]).nlargest(min(10, len(high_risk) + len(watchlist)), "sector_climate_risk")
    if len(concern_chart) > 0:
        bars5 = ax5.barh(
            concern_chart["borrower_name"],
            concern_chart["sector_climate_risk"],
            color=[ESG_COLOURS[item] for item in concern_chart["classification"]],
            edgecolor="white",
            linewidth=0.5,
            height=0.65,
        )
        ax5.set_xlabel("Sector climate risk score (0-10)")
        ax5.set_title("High-risk and watch-list borrowers", fontsize=12, fontweight="bold", pad=10)
        ax5.set_facecolor("white")
        ax5.grid(axis="x", alpha=0.3)
        ax5.legend(
            handles=[
                mpatches.Patch(color=ESG_COLOURS["High Risk"], label="High Risk"),
                mpatches.Patch(color=ESG_COLOURS["Watch List"], label="Watch List"),
            ],
            fontsize=8,
        )
        for bar, (_, row) in zip(bars5, concern_chart.iterrows()):
            ax5.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height() / 2, f"ESG: {row['esg_composite']:.1f} [{row['sector'][:12]}]", va="center", fontsize=8)
    else:
        ax5.text(0.5, 0.5, "No concern borrowers identified", ha="center", va="center", transform=ax5.transAxes)
        ax5.axis("off")

    ax6 = fig.add_subplot(gs[3, 0])
    exposure_by_class = df.groupby("classification")["loan_size_tzs_mn"].sum().reindex(CLASS_ORDER).fillna(0)
    bars6 = ax6.bar(CLASS_ORDER, exposure_by_class.values, color=[ESG_COLOURS[item] for item in CLASS_ORDER], edgecolor="white", linewidth=0.8, width=0.6)
    ax6.set_ylabel("Total exposure (TZS Million)")
    ax6.set_title("Portfolio exposure by ESG classification", fontsize=12, fontweight="bold", pad=10)
    ax6.set_facecolor("white")
    ax6.grid(axis="y", alpha=0.3)
    for bar, value in zip(bars6, exposure_by_class.values):
        ax6.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 5, f"TZS\n{value:,.0f}Mn", ha="center", va="bottom", fontsize=8.5, fontweight="bold")

    ax7 = fig.add_subplot(gs[3, 1])
    for classification in CLASS_ORDER:
        subset = df[df["classification"] == classification]["final_score"]
        if len(subset) > 1:
            ax7.hist(subset, bins=8, alpha=0.7, color=ESG_COLOURS[classification], label=classification, edgecolor="white", linewidth=0.5)
    ax7.set_xlabel("Final ESG-Climate score (0-10)")
    ax7.set_ylabel("Number of borrowers")
    ax7.set_title("Distribution of final ESG-Climate scores", fontsize=12, fontweight="bold", pad=10)
    ax7.legend(fontsize=8)
    ax7.set_facecolor("white")
    ax7.grid(alpha=0.3)

    fig.text(0.5, 0.012, "TZ-CRIP Module 2 | Config-driven borrower ESG pipeline", ha="center", fontsize=8, color="gray", style="italic")
    return fig


def export_outputs(root: Path, df: pd.DataFrame, class_summary: pd.DataFrame, sector_summary: pd.DataFrame, fig) -> None:
    paths = ensure_module_dirs("module2", root=root)
    green_candidates = df[df["classification"] == "Green Eligible"].copy()
    risk_watchlist = df[df["classification"].isin(["High Risk", "Watch List"])].copy()

    export_csv(
        df,
        paths["processed"] / "module2_borrower_esg_scores.csv",
        paths["processed"] / "TZCRIP_Module2_Borrower_ESG_Scores.csv",
        paths["tables"] / "module2_borrower_esg_scores.csv",
        paths["tables"] / "TZCRIP_Module2_Borrower_ESG_Scores.csv",
    )
    export_csv(
        green_candidates,
        paths["processed"] / "module2_green_loan_candidates.csv",
        paths["tables"] / "module2_green_loan_candidates.csv",
    )
    export_csv(risk_watchlist, paths["tables"] / "module2_risk_watchlist.csv")
    export_csv(
        sector_summary,
        paths["processed"] / "module2_sector_esg_summary.csv",
        paths["tables"] / "module2_sector_esg_summary.csv",
    )
    export_csv(
        class_summary,
        paths["processed"] / "module2_classification_summary.csv",
        paths["tables"] / "module2_classification_summary.csv",
    )
    export_figure(
        fig,
        paths["figures"] / "TZCRIP_Module2_ESG_Dashboard.png",
        paths["dashboards"] / "TZCRIP_Module2_ESG_Dashboard.pdf",
    )


def main() -> None:
    root = get_project_root(Path(__file__))
    weights_cfg = load_yaml_config("scoring_weights.yaml")["module2"]
    thresholds_cfg = load_yaml_config("risk_thresholds.yaml")["module2"]
    module1_df = load_module1_feed(root)
    borrower_df = simulate_borrowers(module1_df, weights_cfg, thresholds_cfg)
    class_summary, sector_summary = build_summaries(borrower_df)
    fig = create_dashboard(borrower_df, class_summary)
    export_outputs(root, borrower_df, class_summary, sector_summary, fig)
    print(class_summary.round(2).to_string(index=False))
    plt.close(fig)


if __name__ == "__main__":
    main()
