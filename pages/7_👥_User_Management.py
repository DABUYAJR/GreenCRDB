"""User Management — CSO only. View team roles, portfolios, and permissions."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st

from auth import require_login, sidebar_user_card, can_manage_users, USERS, ROLES

st.set_page_config(page_title="User Management | GreenCRDB", page_icon="👥", layout="wide")

# ── Auth ──────────────────────────────────────────────────────────────────────
user = require_login()
sidebar_user_card()

if not can_manage_users():
    st.markdown(
        '<div style="text-align:center;padding:60px;background:#fef2f2;border-radius:12px;margin:40px auto;max-width:500px;">'
        '<div style="font-size:48px;">🔒</div>'
        '<h2 style="color:#D85A30;margin:16px 0 8px 0;">Access Restricted</h2>'
        '<p style="color:#888;font-size:14px;">User Management is only available to the <b>Chief Sustainability Officer</b>.</p>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.stop()

st.markdown(
    '<div style="background:#7C3AED;padding:14px 24px;border-radius:8px;margin-bottom:12px;">'
    '<h2 style="color:white;margin:0;font-size:22px;">👥 User Management</h2>'
    '<p style="color:#e9d5ff;margin:2px 0 0 0;font-size:13px;">'
    "View and manage platform users · Sustainable Finance Unit · GreenCRDB"
    "</p></div>",
    unsafe_allow_html=True,
)

st.info(f"Logged in as: **{user['name']}** · {user['title']} · Full management access")

# ── Summary KPIs ───────────────────────────────────────────────────────────────
total_users = len(USERS)
roles_count = len(set(u["role"] for u in USERS.values()))

c1, c2, c3 = st.columns(3)
c1.metric("Total Users", total_users)
c2.metric("Roles Defined", roles_count)
c3.metric("Departments", len(set(u["department"] for u in USERS.values())))

st.markdown("---")

# ── User Cards ─────────────────────────────────────────────────────────────────
st.markdown("### Platform Users")

for username, udata in USERS.items():
    role_cfg = ROLES.get(udata["role"], {})
    colour = role_cfg.get("colour", "#888")
    badge = role_cfg.get("badge_text", udata["role"])
    sectors = udata["sectors"]
    regions = udata["regions"]
    sector_display = "All Sectors" if sectors == "all" else ", ".join(sectors)
    region_display = "All Regions" if regions == "all" else ", ".join(regions)

    with st.expander(f"{udata['avatar']}  {udata['name']}  ·  {udata['title']}", expanded=False):
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            st.markdown(
                f'<div style="background:{colour};color:white;padding:12px;border-radius:8px;">'
                f'<b style="font-size:16px;">{udata["name"]}</b><br>'
                f'<span style="font-size:12px;">{udata["title"]}</span><br>'
                f'<span style="font-size:11px;opacity:0.85;">{udata["department"]}</span><br><br>'
                f'<span style="background:rgba(255,255,255,0.2);padding:3px 8px;border-radius:10px;font-size:11px;">'
                f'🔑 {badge}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )
        with col2:
            st.markdown("**Contact**")
            st.markdown(f"📧 {udata['email']}")
            st.markdown(f"👤 Username: `{username}`")
            st.markdown("**Portfolio Scope**")
            st.markdown(f"📊 Sectors: {sector_display}")
            st.markdown(f"📍 Regions: {region_display}")
        with col3:
            st.markdown("**Module Permissions**")
            module_labels = {
                "sector_risk": "Module 1: Sector Risk",
                "borrower_esg": "Module 2: Borrower ESG",
                "finance_decisions": "Module 3: Finance Decisions",
                "regulatory": "Module 4: Regulatory",
                "ai_copilot": "AI Copilot",
                "data_upload": "Data Upload",
            }
            access_icons = {"full": "🟢", "read": "🔵", "limited": "🟡", "none": "🔴"}
            for mod_key, mod_label in module_labels.items():
                level = role_cfg.get("module_access", {}).get(mod_key, "none")
                icon = access_icons.get(level, "⚪")
                st.markdown(f"{icon} {mod_label}: **{level}**")

st.markdown("---")

# ── Role Permissions Matrix ────────────────────────────────────────────────────
st.markdown("### Role Permissions Matrix")

import pandas as pd

module_keys = ["sector_risk", "borrower_esg", "finance_decisions", "regulatory", "ai_copilot", "data_upload"]
module_names = ["Sector Risk", "Borrower ESG", "Finance Decisions", "Regulatory", "AI Copilot", "Data Upload"]

rows = []
for role_key, role_cfg in ROLES.items():
    row = {"Role": role_cfg["label"]}
    for mk, mn in zip(module_keys, module_names):
        row[mn] = role_cfg.get("module_access", {}).get(mk, "none").capitalize()
    row["Enter Data"] = ", ".join(role_cfg.get("can_enter_data", [])) or "None"
    row["Reports"] = "✓" if role_cfg.get("can_generate_reports") else "✗"
    row["Upload"] = "✓" if role_cfg.get("can_upload_files") else "✗"
    row["Export"] = "✓" if role_cfg.get("can_export") else "✗"
    row["Manage Users"] = "✓" if role_cfg.get("can_manage_users") else "✗"
    rows.append(row)

matrix_df = pd.DataFrame(rows)
st.dataframe(matrix_df, use_container_width=True, hide_index=True)

st.markdown("---")
st.markdown("### Legend")
st.markdown(
    "🟢 **Full** — read + write + data entry &nbsp;|&nbsp; "
    "🔵 **Read** — view only &nbsp;|&nbsp; "
    "🟡 **Limited** — restricted feature set &nbsp;|&nbsp; "
    "🔴 **None** — page hidden / access denied"
)
st.caption("GreenCRDB v1.0 · User management is view-only in this prototype. Contact IT to add or modify users.")
