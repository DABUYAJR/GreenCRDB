from __future__ import annotations

import warnings
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from data_validation import validate_module3_input
from scoring_helpers import classify_decision, compute_module3_decision_score, concentration_index, safe_gap
from utils import ensure_module_dirs, export_csv, export_figure, get_project_root, load_yaml_config, safe_read_csv

warnings.filterwarnings("ignore")

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 220)
pd.set_option("display.float_format", lambda x: f"{x:,.2f}")

CRDB_GREEN = "#006B3C"
DECISION_COLOURS = {
    "Approve": "#1D9E75",
    "Conditional Approval": "#3B82F6",
    "Review Required": "#F59E0B",
    "Decline": "#D85A30",
}


def load_inputs(root: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    module1_df = safe_read_csv(
        root / "data" / "processed" / "module1" / "TZCRIP_Module1_Sector_Risk_Ranking.csv",
        required_columns=["sector", "loan_book_tzs_bn", "loan_book_pct", "composite_climate_risk", "risk_tier", "exposure_normalised"],
    )
    module2_df = safe_read_csv(
        root / "data" / "processed" / "module2" / "module2_borrower_esg_scores.csv",
        required_columns=["borrower_id", "borrower_name", "sector", "region", "loan_size_tzs_mn", "esg_composite", "sector_climate_risk", "final_score", "classification"],
    )
    validate_module3_input(module1_df, module2_df)
    return module1_df, module2_df


def product_recommendation(row: pd.Series) -> str:
    if row["decision"] == "Approve":
        if row["sector"] in {"Energy", "Tourism & Hotels"}:
            return "Green Project Loan"
        if row["sector"] in {"Trade & Commerce", "Manufacturing", "Transport"}:
            return "Green SME Facility"
        return "Green Business Loan"
    if row["decision"] == "Conditional Approval":
        return "Sustainability-Linked Loan"
    if row["decision"] == "Review Required":
        return "Transition Support Facility"
    return "Decline / Remediation Plan"


def build_decisions(module1_df: pd.DataFrame, module2_df: pd.DataFrame, weights_cfg: dict[str, float], thresholds_cfg: dict[str, float]) -> pd.DataFrame:
    decisions_df = module2_df.copy()
    decision_weights = {
        "ESG_WEIGHT": weights_cfg["ESG_WEIGHT"],
        "SECTOR_RISK_WEIGHT": weights_cfg["SECTOR_RISK_WEIGHT"],
    }
    decisions_df["application_id"] = [f"APP-{index:03d}" for index in range(1, len(decisions_df) + 1)]
    decisions_df["esg_score"] = (decisions_df["esg_composite"] * 10).round(1)
    decisions_df["sector_risk_score"] = (decisions_df["sector_climate_risk"] * 10).round(1)
    decisions_df["composite_decision_score"] = decisions_df.apply(
        lambda row: round(compute_module3_decision_score(row["esg_composite"], row["sector_climate_risk"], decision_weights), 1),
        axis=1,
    )
    decisions_df["decision"] = decisions_df["composite_decision_score"].apply(lambda value: classify_decision(value, thresholds_cfg))
    decisions_df["product_recommendation"] = decisions_df.apply(product_recommendation, axis=1)

    sector_overlay = module1_df[["sector", "loan_book_tzs_bn", "loan_book_pct", "risk_tier"]].rename(
        columns={"risk_tier": "sector_risk_tier"}
    )
    decisions_df = decisions_df.merge(sector_overlay, on="sector", how="left")
    return decisions_df.sort_values(["composite_decision_score", "loan_size_tzs_mn"], ascending=[False, False]).reset_index(drop=True)


def build_green_pipeline(decisions_df: pd.DataFrame) -> pd.DataFrame:
    pipeline = decisions_df[decisions_df["decision"].isin(["Approve", "Conditional Approval"])].copy()
    return pipeline[
        [
            "borrower_name",
            "sector",
            "region",
            "loan_size_tzs_mn",
            "esg_composite",
            "sector_climate_risk",
            "final_score",
            "product_recommendation",
        ]
    ]


def build_sll_candidates(decisions_df: pd.DataFrame) -> pd.DataFrame:
    candidates = decisions_df[decisions_df["classification"] == "Standard"].copy()
    candidates = candidates.assign(
        sll_kpi_trigger=candidates["esg_composite"].apply(
            lambda score: f"ESG target: {score:.1f} -> 5.5 (gap: {safe_gap(5.5, score):.1f})"
        )
    )
    return candidates.sort_values("composite_decision_score", ascending=False)


def build_sector_materiality(module1_df: pd.DataFrame) -> pd.DataFrame:
    materiality_df = module1_df.copy()
    materiality_df["materiality_score"] = (
        materiality_df["composite_climate_risk"] * 0.65 + materiality_df["exposure_normalised"] * 10 * 0.35
    ).round(2)
    materiality_df["materiality_tier"] = pd.cut(
        materiality_df["materiality_score"],
        bins=[-np.inf, 4.0, 6.0, np.inf],
        labels=["Low Materiality", "Medium Materiality", "High Materiality"],
    )
    return materiality_df[
        [
            "sector",
            "composite_climate_risk",
            "loan_book_tzs_bn",
            "loan_book_pct",
            "risk_tier",
            "materiality_score",
            "materiality_tier",
        ]
    ].rename(columns={"composite_climate_risk": "climate_risk_score"})


def build_tcfd_metrics(module1_df: pd.DataFrame, decisions_df: pd.DataFrame) -> pd.DataFrame:
    high_risk_sector_exposure = module1_df[module1_df["risk_tier"].isin(["High", "Critical"])]["loan_book_tzs_bn"].sum()
    total_sector_exposure = module1_df["loan_book_tzs_bn"].sum()
    green_candidates = decisions_df[decisions_df["classification"] == "Green Eligible"]
    high_risk_borrowers = decisions_df[decisions_df["classification"] == "High Risk"]

    metrics = [
        ("Weighted average climate risk score", f"{module1_df['composite_climate_risk'].mean():.2f} / 10"),
        (
            "High/Critical risk sector exposure",
            f"TZS {high_risk_sector_exposure:,.0f}Bn ({high_risk_sector_exposure / total_sector_exposure * 100:.1f}%)",
        ),
        ("Portfolio climate concentration index", f"{concentration_index(module1_df['loan_book_tzs_bn']):.3f}"),
        (
            "Green-eligible borrower share",
            f"{len(green_candidates) / len(decisions_df) * 100:.1f}% ({len(green_candidates)} borrowers)",
        ),
        (
            "Green-eligible exposure",
            f"TZS {green_candidates['loan_size_tzs_mn'].sum():,.1f}Mn ({green_candidates['loan_size_tzs_mn'].sum() / decisions_df['loan_size_tzs_mn'].sum() * 100:.1f}%)",
        ),
        ("Weighted average ESG composite", f"{decisions_df['esg_composite'].mean():.2f} / 10"),
        ("Environmental pillar average (E)", f"{decisions_df['E_score'].mean():.2f} / 10"),
        ("Social pillar average (S)", f"{decisions_df['S_score'].mean():.2f} / 10"),
        ("Governance pillar average (G)", f"{decisions_df['G_score'].mean():.2f} / 10"),
        (
            "High-risk borrower exposure",
            f"TZS {high_risk_borrowers['loan_size_tzs_mn'].sum():,.1f}Mn ({high_risk_borrowers['loan_size_tzs_mn'].sum() / decisions_df['loan_size_tzs_mn'].sum() * 100:.1f}%)",
        ),
        (
            "Agriculture sector climate risk",
            f"{module1_df.loc[module1_df['sector'] == 'Agriculture', 'composite_climate_risk'].iloc[0]:.2f} / 10 -- "
            f"{module1_df.loc[module1_df['sector'] == 'Agriculture', 'risk_tier'].iloc[0]}",
        ),
        (
            "Sectors above climate risk threshold (6.0)",
            f"{int((module1_df['composite_climate_risk'] >= 6.0).sum())} of {len(module1_df)}",
        ),
    ]
    return pd.DataFrame(metrics, columns=["TCFD Metric", "Portfolio Value"])


def build_scenarios(module1_df: pd.DataFrame) -> pd.DataFrame:
    total_exposure = module1_df["loan_book_tzs_bn"].sum()
    agriculture_risk = module1_df.loc[module1_df["sector"] == "Agriculture", "composite_climate_risk"].iloc[0]
    energy_risk = module1_df.loc[module1_df["sector"] == "Energy", "composite_climate_risk"].iloc[0]
    flood_exposed = module1_df["loan_book_tzs_bn"].sum() * 0.035

    scenarios = [
        {
            "Scenario": "Base case",
            "Description": "Moderate warming (2.5C by 2100). Current NDC trajectory.",
            "Agriculture loss (%)": round(agriculture_risk, 1),
            "Energy transition impact (%)": round(energy_risk * 0.8, 1),
            "Flood-exposed portfolio (%)": 3.5,
            "Est. portfolio impact (%)": 4.2,
        },
        {
            "Scenario": "Accelerated transition",
            "Description": "Policy acceleration (1.5C pathway). Carbon pricing introduced.",
            "Agriculture loss (%)": round(agriculture_risk * 0.6, 1),
            "Energy transition impact (%)": round(energy_risk * 2.9, 1),
            "Flood-exposed portfolio (%)": 2.5,
            "Est. portfolio impact (%)": 6.8,
        },
        {
            "Scenario": "Severe physical shock",
            "Description": "Severe drought and flood event. 1-in-20-year climate scenario.",
            "Agriculture loss (%)": round(agriculture_risk * 2.7, 1),
            "Energy transition impact (%)": round(energy_risk * 0.5, 1),
            "Flood-exposed portfolio (%)": 14.0,
            "Est. portfolio impact (%)": 11.5,
        },
    ]
    scenario_df = pd.DataFrame(scenarios)
    scenario_df["Est. credit loss TZS Bn"] = (scenario_df["Est. portfolio impact (%)"] / 100 * total_exposure).round(1)
    return scenario_df


def build_ifc_ps_alignment(decisions_df: pd.DataFrame) -> pd.DataFrame:
    sector_groups = {
        "PS1": ("Assessment and Management of E&S Risks", ["Agriculture", "Construction", "Mining"]),
        "PS2": ("Labour and Working Conditions", ["Microfinance", "Agriculture", "Construction"]),
        "PS3": ("Resource Efficiency and Pollution Prevention", ["Mining", "Manufacturing", "Construction"]),
        "PS4": ("Community Health, Safety and Security", ["Mining", "Energy", "Construction"]),
        "PS6": ("Biodiversity Conservation and Natural Resources", ["Agriculture", "Microfinance", "Tourism & Hotels"]),
        "PS7": ("Indigenous Peoples", ["Agriculture", "Microfinance"]),
    }
    rows = []
    for standard, (title, sectors) in sector_groups.items():
        subset = decisions_df[decisions_df["sector"].isin(sectors)]
        portfolio_score = round(subset["esg_composite"].mean() if len(subset) else 0.0, 2)
        alignment_tier = "Adequate" if portfolio_score >= 5.2 else "Partial"
        rows.append(
            {
                "standard": standard,
                "title": title,
                "portfolio_score": portfolio_score,
                "key_gap": f"{', '.join(sectors[:2])} require stronger monitoring or disclosure controls",
                "sectors_at_risk": ", ".join(sectors),
                "alignment_tier": alignment_tier,
            }
        )
    return pd.DataFrame(rows)


def build_recommendations(decisions_df: pd.DataFrame) -> pd.DataFrame:
    recommendations = [
        {
            "priority": 1,
            "recommendation": "Prioritise approved green transactions for quick pipeline conversion.",
            "rationale": f"{int((decisions_df['decision'] == 'Approve').sum())} borrowers clear the approval threshold on current data.",
        },
        {
            "priority": 2,
            "recommendation": "Use sustainability-linked structures for conditional approvals.",
            "rationale": f"{int((decisions_df['decision'] == 'Conditional Approval').sum())} borrowers are financeable with KPI-linked covenants.",
        },
        {
            "priority": 3,
            "recommendation": "Escalate decline and review-required names into remediation workflows.",
            "rationale": f"{int(decisions_df['decision'].isin(['Review Required', 'Decline']).sum())} borrowers need tighter risk action plans before new lending.",
        },
    ]
    return pd.DataFrame(recommendations)


def create_dashboard(
    decisions_df: pd.DataFrame,
    pipeline_df: pd.DataFrame,
    materiality_df: pd.DataFrame,
    scenario_df: pd.DataFrame,
):
    fig = plt.figure(figsize=(22, 24))
    fig.patch.set_facecolor("#f8f9fa")

    ax_title = fig.add_axes([0, 0.955, 1, 0.045])
    ax_title.set_facecolor(CRDB_GREEN)
    ax_title.text(0.5, 0.65, "TZ-CRIP: Tanzania Climate-Finance Risk Intelligence Platform", ha="center", va="center", fontsize=20, fontweight="bold", color="white")
    ax_title.text(
        0.5,
        0.18,
        "Module 3: Climate Finance Decision Engine | Cross-module portfolio decisions | Prototype v2.0",
        ha="center",
        va="center",
        fontsize=10.5,
        color="#d4e6d4",
    )
    ax_title.axis("off")

    gs = fig.add_gridspec(3, 2, left=0.06, right=0.97, top=0.94, bottom=0.04, hspace=0.35, wspace=0.25)

    ax1 = fig.add_subplot(gs[0, 0])
    decision_counts = decisions_df["decision"].value_counts().reindex(DECISION_COLOURS.keys()).fillna(0)
    ax1.bar(decision_counts.index, decision_counts.values, color=[DECISION_COLOURS[key] for key in decision_counts.index], edgecolor="white")
    ax1.set_title("Decision distribution", fontsize=12, fontweight="bold")
    ax1.set_ylabel("Borrowers")
    ax1.tick_params(axis="x", rotation=12)
    ax1.grid(axis="y", alpha=0.3)

    ax2 = fig.add_subplot(gs[0, 1])
    for decision, group in decisions_df.groupby("decision"):
        ax2.scatter(
            group["sector_risk_score"],
            group["esg_score"],
            s=group["loan_size_tzs_mn"] / 3,
            alpha=0.75,
            c=DECISION_COLOURS[decision],
            edgecolors="white",
            linewidth=0.8,
            label=decision,
        )
    ax2.set_xlabel("Sector climate risk score (0-100)")
    ax2.set_ylabel("ESG score (0-100)")
    ax2.set_title("Decision drivers", fontsize=12, fontweight="bold")
    ax2.grid(alpha=0.3)
    ax2.legend(fontsize=8)

    ax3 = fig.add_subplot(gs[1, 0])
    top_pipeline = pipeline_df.nlargest(min(10, len(pipeline_df)), "loan_size_tzs_mn")
    ax3.barh(top_pipeline["borrower_name"], top_pipeline["loan_size_tzs_mn"], color="#1D9E75", edgecolor="white")
    ax3.set_title("Largest green pipeline candidates", fontsize=12, fontweight="bold")
    ax3.set_xlabel("Exposure (TZS Mn)")
    ax3.grid(axis="x", alpha=0.3)

    ax4 = fig.add_subplot(gs[1, 1])
    sns.barplot(
        data=materiality_df.sort_values("materiality_score", ascending=False).head(8),
        x="materiality_score",
        y="sector",
        hue="risk_tier",
        dodge=False,
        palette={"Critical": "#7b241c", "High": "#e74c3c", "Medium": "#f39c12", "Low": "#2ecc71"},
        ax=ax4,
    )
    ax4.set_title("Sector materiality", fontsize=12, fontweight="bold")
    ax4.set_xlabel("Materiality score")
    ax4.set_ylabel("")
    ax4.grid(axis="x", alpha=0.3)
    ax4.legend(fontsize=8, title="Risk tier")

    ax5 = fig.add_subplot(gs[2, 0])
    ax5.bar(scenario_df["Scenario"], scenario_df["Est. credit loss TZS Bn"], color=["#60A5FA", "#F59E0B", "#D85A30"], edgecolor="white")
    ax5.set_title("Scenario credit-loss estimates", fontsize=12, fontweight="bold")
    ax5.set_ylabel("Estimated credit loss (TZS Bn)")
    ax5.tick_params(axis="x", rotation=10)
    ax5.grid(axis="y", alpha=0.3)

    ax6 = fig.add_subplot(gs[2, 1])
    product_mix = pipeline_df["product_recommendation"].value_counts()
    ax6.pie(product_mix.values, labels=product_mix.index, autopct="%1.0f%%", startangle=90, colors=["#1D9E75", "#3B82F6", "#06B6D4"])
    ax6.set_title("Recommended product mix", fontsize=12, fontweight="bold")

    fig.text(0.5, 0.012, "TZ-CRIP Module 3 | Integrated decision and reporting layer", ha="center", fontsize=8, color="gray", style="italic")
    return fig


def export_outputs(
    root: Path,
    decisions_df: pd.DataFrame,
    pipeline_df: pd.DataFrame,
    sll_candidates_df: pd.DataFrame,
    materiality_df: pd.DataFrame,
    tcfd_df: pd.DataFrame,
    scenario_df: pd.DataFrame,
    ifc_df: pd.DataFrame,
    recommendations_df: pd.DataFrame,
    fig,
) -> None:
    paths = ensure_module_dirs("module3", root=root)
    export_csv(
        decisions_df[
            [
                "application_id",
                "borrower_id",
                "sector_risk_score",
                "esg_score",
                "composite_decision_score",
                "decision",
                "product_recommendation",
            ]
        ],
        paths["processed"] / "TZCRIP_Module3_Climate_Finance_Decisions.csv",
        paths["tables"] / "TZCRIP_Module3_Climate_Finance_Decisions.csv",
    )
    export_csv(pipeline_df, paths["processed"] / "module3_green_loan_pipeline.csv", paths["tables"] / "module3_green_loan_pipeline.csv")
    export_csv(sll_candidates_df, paths["tables"] / "module3_sll_candidates.csv")
    export_csv(materiality_df, paths["tables"] / "module3_sector_materiality.csv")
    export_csv(tcfd_df, paths["processed"] / "module3_tcfd_metrics.csv", paths["tables"] / "module3_tcfd_metrics.csv")
    export_csv(scenario_df, paths["processed"] / "module3_climate_scenarios.csv", paths["tables"] / "module3_climate_scenarios.csv")
    export_csv(ifc_df, paths["processed"] / "module3_ifc_ps_alignment.csv", paths["tables"] / "module3_ifc_ps_alignment.csv")
    export_csv(recommendations_df, paths["processed"] / "TZCRIP_Module3_Portfolio_Recommendations.csv")
    export_figure(
        fig,
        paths["figures"] / "TZCRIP_Module3_Reporting_Dashboard.png",
        paths["dashboards"] / "TZCRIP_Module3_Reporting_Dashboard.pdf",
    )


def main() -> None:
    root = get_project_root(Path(__file__))
    weights_cfg = load_yaml_config("scoring_weights.yaml")["module3"]
    thresholds_cfg = load_yaml_config("risk_thresholds.yaml")["module3"]
    module1_df, module2_df = load_inputs(root)

    decisions_df = build_decisions(module1_df, module2_df, weights_cfg, thresholds_cfg)
    pipeline_df = build_green_pipeline(decisions_df)
    sll_candidates_df = build_sll_candidates(decisions_df)
    materiality_df = build_sector_materiality(module1_df)
    tcfd_df = build_tcfd_metrics(module1_df, decisions_df)
    scenario_df = build_scenarios(module1_df)
    ifc_df = build_ifc_ps_alignment(decisions_df)
    recommendations_df = build_recommendations(decisions_df)
    fig = create_dashboard(decisions_df, pipeline_df, materiality_df, scenario_df)
    export_outputs(
        root,
        decisions_df,
        pipeline_df,
        sll_candidates_df,
        materiality_df,
        tcfd_df,
        scenario_df,
        ifc_df,
        recommendations_df,
        fig,
    )

    print(decisions_df[["application_id", "borrower_id", "composite_decision_score", "decision", "product_recommendation"]].head(10).to_string(index=False))
    plt.close(fig)


if __name__ == "__main__":
    main()
