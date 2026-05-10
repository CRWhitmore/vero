"""
components/kyc_aml_panel.py
============================
Renders the dedicated KYC/AML compliance status panel.
"""

from typing import Dict, Any
import streamlit as st


def render_kyc_aml_panel(kyc_summary: Dict[str, Any]) -> None:
    """
    Render the KYC/AML status panel showing each party's verification state
    plus the list of required documents.

    Args:
        kyc_summary: KYC summary dict (see data/kyc.json schema).
    """
    color_map = {
        "Approved": "#28a745",
        "Pending": "#ffc107",
        "Pending Review": "#ffc107",
        "Rejected": "#dc3545",
        "Not Started": "#6c757d",
    }
    icon_map = {
        "Approved": "✅",
        "Pending": "⏳",
        "Pending Review": "⏳",
        "Rejected": "❌",
        "Not Started": "⚪",
    }

    entries_html = ""
    for entry in kyc_summary.get("entries", []):
        c = color_map.get(entry["status"], "#6c757d")
        ic = icon_map.get(entry["status"], "•")
        entries_html += f"""
        <li style="margin-bottom: 10px; font-size: 15px;
                   padding: 8px 12px; background-color: #fafafa;
                   border-left: 4px solid {c}; border-radius: 4px;">
            <strong>{entry['party']} {entry['type']}:</strong>
            <span style="color: {c}; font-weight: bold;
                         margin-left: 8px;">{ic} {entry['status']}</span>
            <span style="float: right; font-size: 12px; color: #999;">
                Updated: {entry.get('updated_at', '—')}
            </span>
        </li>
        """

    docs_html = "".join(
        f'<span style="display: inline-block; background-color: #e9ecef; '
        f'color: #495057; padding: 4px 10px; border-radius: 4px; '
        f'margin: 3px; font-size: 12px;">📄 {d}</span>'
        for d in kyc_summary.get("required_documents", [])
    )

    st.markdown(
        f"""
        <div style="background-color: white; border: 1px solid #eee;
                    border-radius: 8px; padding: 20px; height: 100%;">
            <h4 style="font-size: 18px; color: #333; margin: 0 0 15px 0;
                       padding-bottom: 8px; border-bottom: 2px solid #004a8f;">
                🛡️ KYC / AML Compliance
            </h4>
            <ul style="list-style-type: none; padding: 0; margin: 0 0 15px 0;">
                {entries_html}
            </ul>
            <div style="margin-top: 12px;">
                <p style="font-size: 13px; color: #666; margin-bottom: 6px;">
                    <strong>Required Documents:</strong>
                </p>
                {docs_html}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
