"""GreenCRDB Data Upload Studio — Excel, CSV, and PDF ingestion with AI review."""
from __future__ import annotations

import io
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

import web_data as wd
from auth import require_login, sidebar_user_card, can_upload_files, require_module_access

st.set_page_config(page_title="Data Upload | GreenCRDB", page_icon="📂", layout="wide")

# ── Auth ──────────────────────────────────────────────────────────────────────
require_login()
sidebar_user_card()
require_module_access("data_upload")

# Block upload for roles without file upload permission
if not can_upload_files():
    st.warning("Your role does not have permission to upload files. Contact the Chief Sustainability Officer to request access.")
    st.stop()

st.markdown(
    f'<div style="background:#0F766E;padding:14px 24px;border-radius:8px;margin-bottom:12px;">'
    '<h2 style="color:white;margin:0;font-size:22px;">📂 Data Upload Studio</h2>'
    '<p style="color:#ccfbf1;margin:2px 0 0 0;font-size:13px;">'
    "Upload your own Excel · CSV · PDF files → automatic validation, transformation, "
    "visualization, and AI-powered data review"
    "</p></div>",
    unsafe_allow_html=True,
)

# ── Sidebar controls ──────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 📂 Upload Settings")
    upload_mode = st.selectbox(
        "What are you uploading?",
        [
            "Borrower / Loan Portfolio",
            "Sector Climate Risk Scores",
            "ESG Assessment Scores",
            "Custom Report Data",
            "Auto-Detect",
        ],
    )
    st.markdown("---")
    st.markdown("**Accepted formats:**")
    st.markdown("- Excel (.xlsx, .xls)\n- CSV (.csv)\n- PDF (text extraction)\n- All sheets in multi-sheet Excel")
    st.markdown("---")
    st.markdown("**Need a template?**")

    # Template downloads
    borrower_template = pd.DataFrame({
        "borrower_id": ["BRW-001", "BRW-002"],
        "borrower_name": ["Example Company Ltd", "Sample Farm Coop"],
        "sector": ["Trade & Commerce", "Agriculture"],
        "region": ["Dar es Salaam", "Arusha"],
        "loan_size_tzs_mn": [500.0, 250.0],
        "env_management": [6.5, 5.0],
        "pollution_control": [5.5, 4.5],
        "climate_adaptation": [7.0, 6.0],
        "renewable_energy": [6.0, 4.0],
        "labour_practices": [6.5, 5.5],
        "community_impact": [7.0, 6.0],
        "gender_inclusion": [6.0, 5.0],
        "board_oversight": [7.0, 5.5],
        "transparency": [5.5, 4.5],
        "compliance_record": [7.0, 6.0],
    })
    sector_template = pd.DataFrame({
        "sector": ["Agriculture", "Energy", "Transport"],
        "loan_book_pct": [28.0, 5.0, 7.0],
        "loan_book_tzs_bn": [1960, 350, 490],
        "num_borrowers": [45000, 500, 3000],
        "drought_risk": [9.2, 3.5, 2.8],
        "flood_risk": [7.8, 4.0, 5.5],
        "temperature_risk": [8.5, 3.0, 3.2],
        "transition_risk": [6.5, 7.5, 6.8],
        "water_stress_risk": [8.8, 3.5, 3.0],
    })

    buf1 = io.BytesIO()
    borrower_template.to_excel(buf1, index=False, engine="openpyxl")
    buf1.seek(0)
    st.download_button("📥 Borrower Template (.xlsx)", buf1, "GreenCRDB_Borrower_Template.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    buf2 = io.BytesIO()
    sector_template.to_excel(buf2, index=False, engine="openpyxl")
    buf2.seek(0)
    st.download_button("📥 Sector Risk Template (.xlsx)", buf2, "GreenCRDB_Sector_Template.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    st.download_button("📥 Borrower Template (.csv)", borrower_template.to_csv(index=False),
                        "GreenCRDB_Borrower_Template.csv", mime="text/csv")


# ── File reader ────────────────────────────────────────────────────────────────
def read_uploaded(file) -> dict[str, pd.DataFrame]:
    """Return dict of sheet_name → DataFrame for any supported format."""
    name = file.name.lower()
    results: dict[str, pd.DataFrame] = {}
    try:
        if name.endswith(".csv"):
            df = pd.read_csv(file)
            results["Sheet1"] = df
        elif name.endswith((".xlsx", ".xls")):
            xf = pd.ExcelFile(file, engine="openpyxl")
            for sheet in xf.sheet_names:
                df = pd.read_excel(xf, sheet_name=sheet)
                if not df.empty:
                    results[sheet] = df
        elif name.endswith(".pdf"):
            try:
                import pdfplumber
                text_pages: list[str] = []
                with pdfplumber.open(file) as pdf:
                    for page in pdf.pages:
                        t = page.extract_text()
                        if t:
                            text_pages.append(t)
                        tbl = page.extract_table()
                        if tbl and len(tbl) > 1:
                            headers = [str(h) if h else f"Col{i}" for i, h in enumerate(tbl[0])]
                            rows = tbl[1:]
                            results[f"PDF Table (p{pdf.pages.index(page)+1})"] = pd.DataFrame(rows, columns=headers)
                if text_pages:
                    results["PDF Text"] = pd.DataFrame({"Extracted Text": text_pages})
            except ImportError:
                st.error("pdfplumber not installed. Run: pip install pdfplumber")
    except Exception as exc:
        st.error(f"Error reading file: {exc}")
    return results


# ── Schema definitions ────────────────────────────────────────────────────────
SCHEMAS = {
    "Borrower / Loan Portfolio": {
        "required": ["borrower_name", "sector", "loan_size_tzs_mn"],
        "optional": ["borrower_id", "region", "env_management", "pollution_control",
                     "climate_adaptation", "renewable_energy", "labour_practices",
                     "community_impact", "gender_inclusion", "board_oversight",
                     "transparency", "compliance_record"],
        "numeric": ["loan_size_tzs_mn", "env_management", "pollution_control",
                    "climate_adaptation", "renewable_energy", "labour_practices",
                    "community_impact", "gender_inclusion", "board_oversight",
                    "transparency", "compliance_record"],
    },
    "Sector Climate Risk Scores": {
        "required": ["sector", "drought_risk", "flood_risk", "temperature_risk",
                     "transition_risk", "water_stress_risk"],
        "optional": ["loan_book_pct", "loan_book_tzs_bn", "num_borrowers"],
        "numeric": ["drought_risk", "flood_risk", "temperature_risk",
                    "transition_risk", "water_stress_risk",
                    "loan_book_pct", "loan_book_tzs_bn", "num_borrowers"],
    },
    "ESG Assessment Scores": {
        "required": ["borrower_name", "E_score", "S_score", "G_score"],
        "optional": ["sector", "region", "loan_size_tzs_mn", "sector_climate_risk"],
        "numeric": ["E_score", "S_score", "G_score", "loan_size_tzs_mn", "sector_climate_risk"],
    },
    "Custom Report Data": {"required": [], "optional": [], "numeric": []},
    "Auto-Detect": {"required": [], "optional": [], "numeric": []},
}

VALID_SECTORS = [
    "Agriculture", "Trade & Commerce", "Real Estate", "Manufacturing",
    "Transport", "Energy", "Tourism & Hotels", "Personal Loans",
    "Construction", "Mining", "Microfinance", "Health & Education",
]
VALID_REGIONS = [
    "Dar es Salaam", "Arusha", "Mwanza", "Dodoma", "Mbeya",
    "Tanga", "Kilimanjaro", "Morogoro", "Iringa", "Tabora",
]


def auto_detect_mode(df: pd.DataFrame) -> str:
    cols = set(c.lower() for c in df.columns)
    if any(c in cols for c in ["drought_risk", "flood_risk", "water_stress_risk"]):
        return "Sector Climate Risk Scores"
    if any(c in cols for c in ["e_score", "s_score", "g_score", "esg_score"]):
        return "ESG Assessment Scores"
    if any(c in cols for c in ["borrower_name", "loan_size_tzs_mn", "borrower_id"]):
        return "Borrower / Loan Portfolio"
    return "Custom Report Data"


def fuzzy_map_columns(df_cols: list[str], expected: list[str]) -> dict[str, str]:
    """Return mapping: expected_col → best matching df_col."""
    from difflib import get_close_matches
    mapping: dict[str, str] = {}
    df_lower = {c.lower(): c for c in df_cols}
    for exp in expected:
        if exp in df_cols:
            mapping[exp] = exp
            continue
        matches = get_close_matches(exp.lower(), df_lower.keys(), n=1, cutoff=0.6)
        if matches:
            mapping[exp] = df_lower[matches[0]]
    return mapping


def validate_dataframe(df: pd.DataFrame, mode: str) -> dict:
    schema = SCHEMAS.get(mode, SCHEMAS["Custom Report Data"])
    issues: list[str] = []
    warnings: list[str] = []
    fixes: list[str] = []

    # Missing required columns
    missing_req = [c for c in schema["required"] if c not in df.columns]
    if missing_req:
        issues.append(f"Missing required columns: {', '.join(missing_req)}")

    # Null values
    for col in df.columns:
        null_pct = df[col].isna().mean() * 100
        if null_pct > 0:
            warnings.append(f"'{col}' has {null_pct:.1f}% missing values")

    # Numeric range validation (0–10 for risk/ESG scores)
    for col in schema["numeric"]:
        if col in df.columns:
            try:
                series = pd.to_numeric(df[col], errors="coerce")
                if series.isna().any():
                    issues.append(f"'{col}' contains non-numeric values")
                if col.endswith("_risk") or col.endswith("_score"):
                    out_of_range = ((series < 0) | (series > 10)).sum()
                    if out_of_range > 0:
                        issues.append(f"'{col}': {out_of_range} values outside 0–10 range")
            except Exception:
                pass

    # Sector validation
    if "sector" in df.columns:
        unknown = set(df["sector"].dropna().unique()) - set(VALID_SECTORS)
        if unknown:
            warnings.append(f"Unknown sectors (will be processed as-is): {', '.join(unknown)}")

    # Region validation
    if "region" in df.columns:
        unknown_reg = set(df["region"].dropna().unique()) - set(VALID_REGIONS)
        if unknown_reg:
            warnings.append(f"Unknown regions: {', '.join(unknown_reg)}")

    if not issues:
        fixes.append("Data passed all validation checks.")

    return {"issues": issues, "warnings": warnings, "fixes": fixes}


def compute_esg_scores(df: pd.DataFrame) -> pd.DataFrame:
    """Compute ESG scores if the detailed sub-scores are present."""
    E_COLS = ["env_management", "pollution_control", "climate_adaptation", "renewable_energy"]
    S_COLS = ["labour_practices", "community_impact", "gender_inclusion"]
    G_COLS = ["board_oversight", "transparency", "compliance_record"]

    out = df.copy()
    has_e = all(c in df.columns for c in E_COLS)
    has_s = all(c in df.columns for c in S_COLS)
    has_g = all(c in df.columns for c in G_COLS)

    if has_e:
        out["E_score"] = df[E_COLS].mean(axis=1).round(2)
    if has_s:
        out["S_score"] = df[S_COLS].mean(axis=1).round(2)
    if has_g:
        out["G_score"] = df[G_COLS].mean(axis=1).round(2)

    if has_e and has_s and has_g:
        out["esg_composite"] = (out["E_score"] * 0.40 + out["S_score"] * 0.30 + out["G_score"] * 0.30).round(2)

    return out


def classify_esg(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    if "esg_composite" not in out.columns:
        return out

    def _classify(row):
        esg = row.get("esg_composite", 0)
        clim = row.get("sector_climate_risk", 5.0)
        if esg >= 5.5 and clim <= 6.5:
            return "Green Eligible"
        if esg >= 4.5 and clim <= 7.0:
            return "Standard"
        if esg < 3.8 or clim >= 8.0:
            return "High Risk"
        return "Watch List"

    out["classification"] = out.apply(_classify, axis=1)
    return out


def compute_sector_scores(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    risk_cols = ["drought_risk", "flood_risk", "temperature_risk", "transition_risk", "water_stress_risk"]
    weights = [0.25, 0.25, 0.20, 0.20, 0.10]
    if all(c in df.columns for c in risk_cols):
        out["composite_climate_risk"] = sum(
            df[c] * w for c, w in zip(risk_cols, weights)
        ).round(2)
        out["risk_tier"] = out["composite_climate_risk"].apply(
            lambda x: "Critical" if x >= 7.5 else "High" if x >= 6.0 else "Medium" if x >= 4.5 else "Low"
        )
    return out


# ── Main upload area ──────────────────────────────────────────────────────────
uploaded = st.file_uploader(
    "Drop your file here or click to browse",
    type=["xlsx", "xls", "csv", "pdf"],
    help="Supported: Excel (.xlsx, .xls), CSV (.csv), PDF (.pdf). Max 50MB.",
    label_visibility="collapsed",
)

if not uploaded:
    # Show a welcoming info state
    st.markdown(
        f"""
        <div style="border:2px dashed #ccc;border-radius:12px;padding:40px;text-align:center;background:#fafafa;">
            <h3 style="color:#888;margin:0;">📂 Upload Your Data</h3>
            <p style="color:#aaa;margin:10px 0 0 0;">
                Drop any Excel, CSV, or PDF file here.<br>
                Download a template from the sidebar if you need the right column format.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("---")
    st.markdown("### How It Works")
    step1, step2, step3, step4 = st.columns(4)
    steps = [
        ("1️⃣", "Download Template", "Get the Excel template for your data type from the sidebar"),
        ("2️⃣", "Fill in Your Data", "Enter your borrower portfolio, sector risk scores, or ESG data"),
        ("3️⃣", "Upload the File", "Drop the file above — Excel, CSV, or PDF all accepted"),
        ("4️⃣", "Review & Analyse", "Instant validation, charts, ESG scoring, and AI-powered review"),
    ]
    for col, (num, title, desc) in zip([step1, step2, step3, step4], steps):
        with col:
            st.markdown(
                f'<div style="text-align:center;padding:16px;background:#f8f9fa;border-radius:8px;">'
                f'<div style="font-size:28px;">{num}</div>'
                f'<b style="font-size:13px;">{title}</b>'
                f'<p style="font-size:12px;color:#666;margin:6px 0 0 0;">{desc}</p>'
                f'</div>',
                unsafe_allow_html=True,
            )
    st.stop()

# ── File loaded: read and parse ───────────────────────────────────────────────
with st.spinner("Reading file..."):
    sheets = read_uploaded(uploaded)

if not sheets:
    st.error("Could not parse this file. Please check the format and try again.")
    st.stop()

st.success(f"File loaded: **{uploaded.name}** · {uploaded.size / 1024:.1f} KB · {len(sheets)} sheet(s) found")

# Sheet selector
if len(sheets) > 1:
    selected_sheet = st.selectbox("Select sheet to analyse:", list(sheets.keys()))
else:
    selected_sheet = list(sheets.keys())[0]

raw_df = sheets[selected_sheet]

# Auto-detect mode if selected
effective_mode = upload_mode
if upload_mode == "Auto-Detect":
    effective_mode = auto_detect_mode(raw_df)
    st.info(f"Auto-detected as: **{effective_mode}**")

# ── Tabs for the uploaded data ────────────────────────────────────────────────
tab_preview, tab_validate, tab_transform, tab_visual, tab_ai = st.tabs([
    "👁 Preview", "✅ Validate", "⚙ Transform & Score", "📊 Visualize", "🤖 AI Review",
])

# ── TAB 1: Preview ────────────────────────────────────────────────────────────
with tab_preview:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Rows", f"{len(raw_df):,}")
    c2.metric("Columns", len(raw_df.columns))
    c3.metric("Missing Values", f"{raw_df.isna().sum().sum():,}")
    c4.metric("File Size", f"{uploaded.size / 1024:.1f} KB")

    st.markdown("#### Raw Data Preview")
    st.dataframe(raw_df.head(50), use_container_width=True, hide_index=True)

    st.markdown("#### Column Summary")
    col_info = pd.DataFrame({
        "Column": raw_df.columns,
        "Type": raw_df.dtypes.values,
        "Non-Null": raw_df.count().values,
        "Null %": (raw_df.isna().mean() * 100).round(1).values,
        "Sample Values": [str(raw_df[c].dropna().iloc[0]) if not raw_df[c].dropna().empty else "—" for c in raw_df.columns],
    })
    st.dataframe(col_info, use_container_width=True, hide_index=True)

# ── TAB 2: Validate ───────────────────────────────────────────────────────────
with tab_validate:
    st.markdown("#### Data Validation Report")

    # Column mapping
    schema = SCHEMAS.get(effective_mode, SCHEMAS["Custom Report Data"])
    col_map = fuzzy_map_columns(raw_df.columns.tolist(), schema["required"] + schema["optional"])

    if schema["required"]:
        st.markdown("**Column Mapping (auto-detected):**")
        map_data = []
        for exp in schema["required"] + schema["optional"]:
            found = col_map.get(exp)
            status = "✅ Matched" if found == exp else ("🔄 Mapped" if found else "❌ Missing")
            map_data.append({"Expected Column": exp, "Found In File": found or "—", "Status": status})
        map_df = pd.DataFrame(map_data)
        st.dataframe(map_df, use_container_width=True, hide_index=True)
        st.markdown("---")

    # Apply fuzzy column rename
    if col_map:
        rename_map = {v: k for k, v in col_map.items() if v != k and v in raw_df.columns}
        if rename_map:
            st.markdown(f"**Applying {len(rename_map)} column rename(s):** {rename_map}")
            raw_df = raw_df.rename(columns=rename_map)

    # Run validation
    result = validate_dataframe(raw_df, effective_mode)

    if result["issues"]:
        for issue in result["issues"]:
            st.error(f"🚫 {issue}")
    else:
        st.success("No critical issues found — data passes schema validation.")

    for warning in result["warnings"]:
        st.warning(f"⚠ {warning}")

    for fix in result["fixes"]:
        st.info(f"ℹ {fix}")

    st.markdown("---")
    st.markdown("#### Data Quality Summary")
    null_summary = raw_df.isna().sum().reset_index()
    null_summary.columns = ["Column", "Null Count"]
    null_summary["Null %"] = (null_summary["Null Count"] / len(raw_df) * 100).round(1)
    null_summary["Quality"] = null_summary["Null %"].apply(
        lambda x: "✅ Complete" if x == 0 else "⚠ Partial" if x < 20 else "❌ Poor"
    )
    st.dataframe(null_summary, use_container_width=True, hide_index=True)

# ── TAB 3: Transform ──────────────────────────────────────────────────────────
with tab_transform:
    st.markdown("#### Transformation & Scoring Engine")

    transformed = raw_df.copy()

    if effective_mode == "Borrower / Loan Portfolio":
        st.markdown("**Running ESG scoring pipeline on uploaded borrower data...**")
        transformed = compute_esg_scores(transformed)

        # Join sector climate risk from existing Module 1 output if available
        sr = wd.sector_risk()
        if not sr.empty and "sector" in transformed.columns:
            risk_map = sr.set_index("sector")["composite_climate_risk"].to_dict()
            transformed["sector_climate_risk"] = transformed["sector"].map(risk_map).fillna(5.0)
            st.info("Sector climate risk scores joined from Module 1 data.")

        transformed = classify_esg(transformed)
        st.success("ESG scoring and classification complete!")

        new_cols = [c for c in transformed.columns if c not in raw_df.columns]
        if new_cols:
            st.markdown(f"**New columns added:** {', '.join(new_cols)}")

    elif effective_mode == "Sector Climate Risk Scores":
        st.markdown("**Computing composite climate risk scores...**")
        transformed = compute_sector_scores(transformed)
        new_cols = [c for c in transformed.columns if c not in raw_df.columns]
        if new_cols:
            st.markdown(f"**New columns added:** {', '.join(new_cols)}")
        st.success("Sector risk scoring complete!")

    elif effective_mode == "ESG Assessment Scores":
        transformed = classify_esg(transformed)
        new_cols = [c for c in transformed.columns if c not in raw_df.columns]
        if new_cols:
            st.markdown(f"**New columns added:** {', '.join(new_cols)}")
        st.success("ESG classification complete!")

    else:
        st.info("Custom data mode: no automated transformation applied. Use the AI Review tab for analysis.")

    st.markdown("#### Transformed Data Preview")
    st.dataframe(transformed, use_container_width=True, hide_index=True)

    buf = io.BytesIO()
    transformed.to_excel(buf, index=False, engine="openpyxl")
    buf.seek(0)
    col_dl1, col_dl2 = st.columns(2)
    col_dl1.download_button(
        "⬇ Download Transformed Data (.xlsx)",
        buf,
        file_name="GreenCRDB_Transformed_Data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    col_dl2.download_button(
        "⬇ Download Transformed Data (.csv)",
        transformed.to_csv(index=False),
        file_name="GreenCRDB_Transformed_Data.csv",
        mime="text/csv",
    )
    st.session_state["uploaded_transformed"] = transformed
    st.session_state["uploaded_mode"] = effective_mode

# ── TAB 4: Visualize ──────────────────────────────────────────────────────────
with tab_visual:
    if "uploaded_transformed" not in st.session_state:
        st.info("Go to the Transform tab first to process your data, then return here for charts.")
        st.stop()

    viz_df = st.session_state["uploaded_transformed"]
    mode = st.session_state["uploaded_mode"]

    st.markdown("#### Interactive Visualizations — Your Uploaded Data")

    if mode == "Borrower / Loan Portfolio" and "esg_composite" in viz_df.columns:
        col_a, col_b = st.columns([1, 1])
        with col_a:
            if "classification" in viz_df.columns:
                class_counts = viz_df["classification"].value_counts().reset_index()
                class_counts.columns = ["Classification", "Count"]
                fig = px.pie(class_counts, names="Classification", values="Count",
                             color="Classification", color_discrete_map=wd.ESG_COLOURS, hole=0.45,
                             title="Your Borrower Classifications")
                fig.update_traces(textinfo="percent+label", textposition="outside")
                fig.update_layout(height=360, showlegend=False, margin=dict(l=10, r=10, t=40, b=10))
                st.plotly_chart(fig, use_container_width=True)

        with col_b:
            if "sector" in viz_df.columns and "esg_composite" in viz_df.columns:
                sector_esg = viz_df.groupby("sector")["esg_composite"].mean().reset_index().sort_values("esg_composite")
                fig2 = px.bar(sector_esg, x="esg_composite", y="sector", orientation="h",
                              text="esg_composite", color="esg_composite",
                              color_continuous_scale=[[0, "#D85A30"], [0.5, "#EF9F27"], [1, "#1D9E75"]],
                              range_color=[0, 10],
                              title="Average ESG Score by Sector (Your Data)")
                fig2.update_traces(texttemplate="%{text:.2f}", textposition="outside")
                fig2.update_layout(height=360, plot_bgcolor="white", paper_bgcolor="white",
                                   coloraxis_showscale=False, margin=dict(l=10, r=50, t=40, b=10))
                st.plotly_chart(fig2, use_container_width=True)

        if "sector_climate_risk" in viz_df.columns and "esg_composite" in viz_df.columns:
            size_col = "loan_size_tzs_mn" if "loan_size_tzs_mn" in viz_df.columns else None
            fig3 = px.scatter(viz_df, x="sector_climate_risk", y="esg_composite",
                              color="classification" if "classification" in viz_df.columns else None,
                              color_discrete_map=wd.ESG_COLOURS,
                              size=size_col, size_max=30,
                              hover_data=["borrower_name"] if "borrower_name" in viz_df.columns else None,
                              title="Your Portfolio: ESG Score vs Sector Climate Risk",
                              labels={"sector_climate_risk": "Sector Climate Risk (0–10)", "esg_composite": "ESG Score (0–10)"})
            fig3.update_layout(height=400, plot_bgcolor="white", paper_bgcolor="white")
            st.plotly_chart(fig3, use_container_width=True)

    elif mode == "Sector Climate Risk Scores" and "composite_climate_risk" in viz_df.columns:
        colour_map = wd.RISK_COLOURS
        fig = px.bar(viz_df.sort_values("composite_climate_risk", ascending=True),
                     x="composite_climate_risk", y="sector", color="risk_tier",
                     color_discrete_map=colour_map, orientation="h",
                     text="composite_climate_risk",
                     title="Your Sector Climate Risk Scores",
                     labels={"composite_climate_risk": "Composite Risk (0–10)", "sector": ""})
        fig.update_traces(texttemplate="%{text:.2f}", textposition="outside")
        fig.update_layout(height=400, plot_bgcolor="white", paper_bgcolor="white",
                          margin=dict(l=10, r=50, t=40, b=10))
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.markdown("#### Data Overview")
        numeric_cols = viz_df.select_dtypes(include=[np.number]).columns.tolist()
        cat_cols = viz_df.select_dtypes(include=["object"]).columns.tolist()

        if numeric_cols:
            x_axis = st.selectbox("X axis", numeric_cols, key="viz_x")
            y_axis = st.selectbox("Y axis", [c for c in numeric_cols if c != x_axis], key="viz_y")
            color_col = st.selectbox("Colour by", ["None"] + cat_cols, key="viz_color")
            fig = px.scatter(viz_df, x=x_axis, y=y_axis,
                             color=color_col if color_col != "None" else None,
                             title=f"{x_axis} vs {y_axis}")
            fig.update_layout(height=400, plot_bgcolor="white", paper_bgcolor="white")
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("#### Numeric Summary Statistics")
        if numeric_cols:
            st.dataframe(viz_df[numeric_cols].describe().round(2), use_container_width=True)

# ── TAB 5: AI Review ──────────────────────────────────────────────────────────
with tab_ai:
    st.markdown("#### AI-Powered Data Review")

    with st.sidebar:
        _secret_key = st.secrets.get("GEMINI_API_KEY", "") if hasattr(st, "secrets") else ""
        ai_api_key = st.text_input("Gemini API Key (for AI review)", value=_secret_key,
                                    type="password", key="upload_gemini_key", placeholder="AIza...")
        ai_claude_key = st.text_input("Claude API Key (optional)", type="password",
                                       key="upload_claude_key", placeholder="sk-ant-...")

    use_ai = bool(ai_api_key or ai_claude_key)

    if not use_ai:
        st.warning("Enter a Gemini API key in the sidebar to enable AI-powered data review.")
    else:
        viz_df2 = st.session_state.get("uploaded_transformed", raw_df)
        mode2 = st.session_state.get("uploaded_mode", effective_mode)

        data_summary = f"""
UPLOADED DATA SUMMARY FOR AI REVIEW
File: {uploaded.name}
Mode: {mode2}
Rows: {len(viz_df2)}
Columns: {list(viz_df2.columns)}
Numeric Summary:
{viz_df2.describe().to_string()}

Sample Data (first 5 rows):
{viz_df2.head(5).to_string()}
"""

        system_prompt_upload = (
            "You are GreenCRDB Data Analyst — an expert in ESG reporting, climate risk analysis, "
            "and sustainable banking for Sub-Saharan Africa. "
            "You have been given uploaded portfolio data to review. "
            "Provide specific, professional analysis of the data quality and content."
        )

        review_prompts = {
            "Full Data Quality Review": (
                "Review this uploaded dataset for data quality. "
                "Cover: completeness, value ranges, outliers, potential errors, "
                "and recommendations for improving data quality before ESG scoring."
            ),
            "ESG Risk Summary": (
                "Based on this uploaded data, provide a concise ESG risk summary. "
                "Which borrowers or sectors have the highest ESG risk? "
                "Which are green finance eligible? What are the key patterns?"
            ),
            "Compare to CRDB Portfolio": (
                "Compare this uploaded data to the GreenCRDB simulated benchmark portfolio. "
                "How does the ESG performance, sector mix, and risk profile compare? "
                "What are the key differences and similarities?"
            ),
            "Identify Missing Data": (
                "Identify what critical data is missing from this upload that would be needed "
                "for a full PCAF financed emissions calculation, TCFD disclosure, or IFC PS compliance report."
            ),
        }

        r1, r2 = st.columns(2)
        for i, (name, prompt) in enumerate(review_prompts.items()):
            col = r1 if i % 2 == 0 else r2
            with col:
                if st.button(name, key=f"ai_review_{i}", use_container_width=True):
                    full_prompt = f"{data_summary}\n\nTask: {prompt}"
                    try:
                        if ai_claude_key:
                            from anthropic import Anthropic
                            client = Anthropic(api_key=ai_claude_key)
                            msg = client.messages.create(
                                model="claude-sonnet-4-6",
                                max_tokens=2048,
                                system=system_prompt_upload,
                                messages=[{"role": "user", "content": full_prompt}],
                            )
                            result = msg.content[0].text
                        else:
                            import google.generativeai as genai
                            genai.configure(api_key=ai_api_key)
                            m = genai.GenerativeModel("gemini-1.5-flash", system_instruction=system_prompt_upload)
                            result = m.generate_content(full_prompt).text
                        st.session_state[f"ai_upload_result_{i}"] = result
                    except Exception as exc:
                        st.error(f"API error: {exc}")

                if f"ai_upload_result_{i}" in st.session_state:
                    st.markdown(st.session_state[f"ai_upload_result_{i}"])
                    st.download_button(f"⬇ Download review", st.session_state[f"ai_upload_result_{i}"],
                                       f"GreenCRDB_DataReview_{name.replace(' ', '_')}.txt",
                                       mime="text/plain", key=f"dl_review_{i}")

        st.markdown("---")
        st.markdown("**Ask anything about your uploaded data:**")
        custom_q = st.text_area("Your question", placeholder="What are the main risk areas in this data?", height=80)
        if st.button("Ask AI about this data", use_container_width=True) and custom_q:
            full_prompt = f"{data_summary}\n\nQuestion: {custom_q}"
            try:
                if ai_claude_key:
                    from anthropic import Anthropic
                    client = Anthropic(api_key=ai_claude_key)
                    msg = client.messages.create(
                        model="claude-sonnet-4-6", max_tokens=2048,
                        system=system_prompt_upload,
                        messages=[{"role": "user", "content": full_prompt}],
                    )
                    st.markdown(msg.content[0].text)
                else:
                    import google.generativeai as genai
                    genai.configure(api_key=ai_api_key)
                    m = genai.GenerativeModel("gemini-1.5-flash", system_instruction=system_prompt_upload)
                    st.markdown(m.generate_content(full_prompt).text)
            except Exception as exc:
                st.error(f"API error: {exc}")
