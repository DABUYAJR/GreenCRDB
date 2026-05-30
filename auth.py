"""GreenCRDB — Authentication and Role-Based Access Control."""
from __future__ import annotations

import hashlib
from typing import Any

import streamlit as st

CRDB_GREEN = "#006B3C"


def _hash(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()


# ── User Database ─────────────────────────────────────────────────────────────
# Single shared demonstrator account.
USERS: dict[str, dict[str, Any]] = {
    "democrdb": {
        "name": "DemoCRDB",
        "title": "Chief Sustainability Officer",
        "department": "Demonstrator",
        "role": "cso",
        "password_hash": hashlib.sha256(b"GreenCRDB@2025").hexdigest(),
        "sectors": "all",
        "regions": "all",
        "email": "demo@greencrdb.local",
        "avatar": "DC",
    },
}

# ── Role Definitions & Permissions ────────────────────────────────────────────
ROLES: dict[str, dict[str, Any]] = {
    "cso": {
        "label": "Chief Sustainability Officer",
        "colour": "#7C3AED",
        "badge_text": "CSO · Full Access",
        "module_access": {
            "sector_risk": "full",
            "borrower_esg": "full",
            "finance_decisions": "full",
            "regulatory": "full",
            "ai_copilot": "full",
            "data_upload": "full",
        },
        "can_enter_data": ["sector_risk", "borrower_esg", "finance_decisions"],
        "can_generate_reports": True,
        "can_upload_files": True,
        "can_manage_users": True,
        "can_export": True,
        "description": "Full platform access. Can enter and approve data in all modules. User management.",
    },
    "climate_risk_manager": {
        "label": "Climate Risk Manager",
        "colour": "#D97706",
        "badge_text": "Climate Risk · Module 1",
        "module_access": {
            "sector_risk": "full",
            "borrower_esg": "read",
            "finance_decisions": "read",
            "regulatory": "full",
            "ai_copilot": "full",
            "data_upload": "full",
        },
        "can_enter_data": ["sector_risk"],
        "can_generate_reports": True,
        "can_upload_files": True,
        "can_manage_users": False,
        "can_export": True,
        "description": "Manages sector climate risk data. Full Module 1 & Regulatory access. Read-only Module 2 & 3.",
    },
    "esg_officer": {
        "label": "ESG Assessment Officer",
        "colour": "#1D9E75",
        "badge_text": "ESG Officer · Module 2",
        "module_access": {
            "sector_risk": "read",
            "borrower_esg": "full",
            "finance_decisions": "read",
            "regulatory": "read",
            "ai_copilot": "limited",
            "data_upload": "full",
        },
        "can_enter_data": ["borrower_esg"],
        "can_generate_reports": True,
        "can_upload_files": True,
        "can_manage_users": False,
        "can_export": True,
        "description": "Assesses borrower ESG scores for assigned sectors and regions. Full Module 2 access.",
    },
    "green_finance_officer": {
        "label": "Green Finance Officer",
        "colour": "#2563EB",
        "badge_text": "Green Finance · Module 3",
        "module_access": {
            "sector_risk": "read",
            "borrower_esg": "read",
            "finance_decisions": "full",
            "regulatory": "read",
            "ai_copilot": "full",
            "data_upload": "read",
        },
        "can_enter_data": ["finance_decisions"],
        "can_generate_reports": True,
        "can_upload_files": False,
        "can_manage_users": False,
        "can_export": True,
        "description": "Manages green finance pipeline and lending decisions. Full Module 3 access.",
    },
    "compliance_officer": {
        "label": "Compliance & Reporting Officer",
        "colour": "#0F766E",
        "badge_text": "Compliance · Read + Reports",
        "module_access": {
            "sector_risk": "read",
            "borrower_esg": "read",
            "finance_decisions": "read",
            "regulatory": "full",
            "ai_copilot": "full",
            "data_upload": "read",
        },
        "can_enter_data": [],
        "can_generate_reports": True,
        "can_upload_files": True,
        "can_manage_users": False,
        "can_export": True,
        "description": "Full read access to all modules. Can generate all regulatory reports. No data entry.",
    },
    "data_analyst": {
        "label": "Data Analyst",
        "colour": "#6B7280",
        "badge_text": "Analyst · Read Only",
        "module_access": {
            "sector_risk": "read",
            "borrower_esg": "read",
            "finance_decisions": "read",
            "regulatory": "none",
            "ai_copilot": "none",
            "data_upload": "none",
        },
        "can_enter_data": [],
        "can_generate_reports": False,
        "can_upload_files": False,
        "can_manage_users": False,
        "can_export": False,
        "description": "View-only access to Modules 1–3 dashboards. No data entry or AI access.",
    },
}

# ── Convenience helpers ────────────────────────────────────────────────────────
DEMO_CREDENTIALS = [
    ("DemoCRDB", "GreenCRDB@2025", "Chief Sustainability Officer", "#7C3AED"),
]


def authenticate(username: str, password: str) -> dict | None:
    user = USERS.get(username.strip().lower())
    if user and user["password_hash"] == _hash(password):
        return user
    return None


def get_user() -> dict | None:
    return st.session_state.get("current_user")


def get_role() -> str:
    user = get_user()
    return user["role"] if user else "guest"


def get_role_config() -> dict:
    return ROLES.get(get_role(), {})


def can_access_module(module_key: str) -> str:
    """Returns 'full', 'read', 'limited', or 'none'."""
    cfg = get_role_config()
    return cfg.get("module_access", {}).get(module_key, "none")


def can_enter_data(module_key: str) -> bool:
    cfg = get_role_config()
    allowed = cfg.get("can_enter_data", [])
    return allowed == "all" or module_key in allowed


def can_generate_reports() -> bool:
    return get_role_config().get("can_generate_reports", False)


def can_export() -> bool:
    return get_role_config().get("can_export", False)


def can_upload_files() -> bool:
    return get_role_config().get("can_upload_files", False)


def can_manage_users() -> bool:
    return get_role_config().get("can_manage_users", False)


def user_sectors() -> list[str] | str:
    user = get_user()
    return user["sectors"] if user else []


def user_regions() -> list[str] | str:
    user = get_user()
    return user["regions"] if user else []


def filter_by_user(df, sector_col: str = "sector", region_col: str = "region"):
    """Filter a DataFrame to only include rows the current user can access."""
    import pandas as pd
    sectors = user_sectors()
    regions = user_regions()
    if sectors != "all" and sector_col in df.columns:
        df = df[df[sector_col].isin(sectors)]
    if regions != "all" and region_col in df.columns:
        df = df[df[region_col].isin(regions)]
    return df


def is_role(role_key: str) -> bool:
    return get_role() == role_key


def access_level_banner(module_key: str) -> None:
    """Show a contextual banner telling the user their access level for this module."""
    level = can_access_module(module_key)
    role_cfg = get_role_config()
    label = role_cfg.get("label", "")
    if level == "read":
        st.markdown(
            f'<div style="background:#EFF6FF;border-left:4px solid #3B82F6;padding:10px 16px;'
            f'border-radius:0 6px 6px 0;margin-bottom:12px;font-size:13px;">'
            f'👁️ <b>Read-only access</b> — Your role (<b>{label}</b>) can view this module but cannot enter or modify data. '
            f'Contact the Chief Sustainability Officer to request elevated access.'
            f'</div>',
            unsafe_allow_html=True,
        )
    elif level == "limited":
        st.markdown(
            f'<div style="background:#FFFBEB;border-left:4px solid #F59E0B;padding:10px 16px;'
            f'border-radius:0 6px 6px 0;margin-bottom:12px;font-size:13px;">'
            f'⚠️ <b>Limited access</b> — Your role (<b>{label}</b>) has restricted access to some features on this page.'
            f'</div>',
            unsafe_allow_html=True,
        )


def mask_sensitive_data(df, name_col: str = "borrower_name", id_col: str = None):
    """For roles without full access, mask individual borrower names with anonymised IDs."""
    import pandas as pd
    level_esg = can_access_module("borrower_esg")
    level_dec = can_access_module("finance_decisions")
    # Only mask when role has read-only access to both modules (data_analyst pattern)
    if level_esg == "read" and level_dec == "read" and not can_enter_data("borrower_esg"):
        df = df.copy()
        if name_col in df.columns:
            # Preserve first letter of company name, mask rest
            df[name_col] = df[name_col].apply(
                lambda n: n[0] + "*" * (len(str(n)) - 2) + str(n)[-1] if isinstance(n, str) and len(n) > 2 else n
            )
        if id_col and id_col in df.columns:
            df[id_col] = df[id_col].apply(lambda x: f"BW-****")
    return df


def require_login() -> dict:
    """Call at top of every page. Shows login if not authenticated; returns user dict if ok."""
    if "current_user" not in st.session_state or not st.session_state["current_user"]:
        _show_login_page()
        st.stop()
    return st.session_state["current_user"]


def require_module_access(module_key: str) -> None:
    """Stops the page with an access denied message if user cannot access this module."""
    level = can_access_module(module_key)
    if level == "none":
        user = get_user()
        role_cfg = get_role_config()
        st.markdown(
            f'<div style="text-align:center;padding:60px;background:#fef2f2;border-radius:12px;margin:40px auto;max-width:500px;">'
            f'<div style="font-size:48px;">🔒</div>'
            f'<h2 style="color:#D85A30;margin:16px 0 8px 0;">Access Restricted</h2>'
            f'<p style="color:#888;font-size:14px;">Your role (<b>{role_cfg.get("label", "")}</b>) does not have permission to view this module.</p>'
            f'<p style="color:#888;font-size:13px;">Contact your Chief Sustainability Officer to request access.</p>'
            f'</div>',
            unsafe_allow_html=True,
        )
        st.stop()


def sidebar_user_card() -> None:
    """Render the user card and logout button in the sidebar."""
    user = get_user()
    if not user:
        return
    role_cfg = ROLES.get(user["role"], {})
    colour = role_cfg.get("colour", "#888")
    badge = role_cfg.get("badge_text", user["role"])
    sectors = user["sectors"]
    regions = user["regions"]
    sector_display = "All Sectors" if sectors == "all" else ", ".join(sectors)
    region_display = "All Regions" if regions == "all" else ", ".join(regions)

    with st.sidebar:
        st.markdown(
            f'<div style="background:{colour};color:white;padding:14px;border-radius:10px;margin-bottom:12px;">'
            f'<div style="display:flex;align-items:center;gap:10px;">'
            f'<div style="background:rgba(255,255,255,0.25);border-radius:50%;width:38px;height:38px;'
            f'display:flex;align-items:center;justify-content:center;font-weight:bold;font-size:14px;">'
            f'{user["avatar"]}</div>'
            f'<div>'
            f'<div style="font-weight:bold;font-size:14px;">{user["name"]}</div>'
            f'<div style="font-size:11px;opacity:0.85;">{user["title"]}</div>'
            f'</div></div>'
            f'<div style="margin-top:10px;font-size:11px;opacity:0.85;">'
            f'<div>📧 {user["email"]}</div>'
            f'<div>🏢 {user["department"]}</div>'
            f'</div>'
            f'<div style="margin-top:8px;background:rgba(255,255,255,0.2);padding:5px 10px;'
            f'border-radius:6px;font-size:11px;font-weight:bold;">'
            f'🔑 {badge}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
        if sectors != "all":
            st.caption(f"📊 Sectors: {sector_display}")
        if regions != "all":
            st.caption(f"📍 Regions: {region_display}")
        if st.button("🚪 Logout", use_container_width=True, type="secondary"):
            st.session_state.clear()
            st.rerun()
        st.markdown("---")


def _show_login_page() -> None:
    """Full-screen login page."""
    st.markdown(
        f"""
        <style>
        .main .block-container {{padding-top: 2rem;}}
        </style>
        <div style="max-width:480px;margin:0 auto;padding:40px 0;">
            <div style="background:{CRDB_GREEN};padding:28px;border-radius:12px 12px 0 0;text-align:center;">
                <h1 style="color:white;margin:0;font-size:28px;">🌍 GreenCRDB</h1>
                <p style="color:#c8e6c9;margin:6px 0 0 0;font-size:13px;">
                    Tanzania Climate-Finance Risk Intelligence Platform
                </p>
                <p style="color:#a5d6a7;margin:4px 0 0 0;font-size:12px;">CRDB Bank — Sustainable Finance Unit</p>
            </div>
            <div style="background:#f9fafb;border:1px solid #e5e7eb;border-top:none;
                padding:28px;border-radius:0 0 12px 12px;">
                <h3 style="margin:0 0 20px 0;color:#1a1a1a;text-align:center;">Sign In to Your Portal</h3>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_l, col_form, col_r = st.columns([1, 2, 1])
    with col_form:
        with st.form("login_form", clear_on_submit=False):
            username = st.text_input("Username", placeholder="DemoCRDB")
            password = st.text_input("Password", type="password", placeholder="Your portal password")
            submitted = st.form_submit_button("Sign In →", use_container_width=True, type="primary")

            if submitted:
                user = authenticate(username, password)
                if user:
                    st.session_state["current_user"] = user
                    st.session_state["authenticated"] = True
                    st.rerun()
                else:
                    st.error("Invalid username or password. Please try again.")

        st.markdown("---")
        with st.expander("🔑 Demo credentials (for presentation)"):
            for uname, pw, title, colour in DEMO_CREDENTIALS:
                st.markdown(
                    f'<div style="display:flex;justify-content:space-between;align-items:center;'
                    f'padding:6px 10px;background:#f0f4f0;border-left:3px solid {colour};'
                    f'border-radius:0 4px 4px 0;margin:4px 0;">'
                    f'<div>'
                    f'<span style="font-family:monospace;font-size:12px;font-weight:bold;">{uname}</span>'
                    f'<span style="font-size:11px;color:#888;margin-left:8px;">/ {pw}</span>'
                    f'</div>'
                    f'<span style="background:{colour};color:white;font-size:10px;padding:2px 7px;border-radius:8px;">'
                    f'{title.split()[0]}</span>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

        st.markdown(
            '<p style="text-align:center;color:#aaa;font-size:11px;margin-top:12px;">'
            'GreenCRDB v1.0 · Prototype · All data is simulated/illustrative'
            '</p>',
            unsafe_allow_html=True,
        )
