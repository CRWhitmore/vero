"""
components/participants_panel.py
=================================
Renders the list of deal participants with their KYC/AML status badges.
"""

from typing import List, Dict, Any
import streamlit as st


def _status_badge(status: str) -> str:
    """Return an HTML badge string for a given KYC/AML status."""
    palette = {
        "Approved": ("#d4edda", "#155724", "✓"),
        "Pending": ("#fff3cd", "#856404", "⏳"),
        "Pending Review": ("#fff3cd", "#856404", "⏳"),
        "Rejected": ("#f8d7da", "#721c24", "✗"),
        "Not Started": ("#e2e3e5", "#41464b", "•"),
    }
    bg, fg, icon = palette.get(status, ("#e2e3e5", "#41464b", "•"))
    return (
        f'<span style="background-color: {bg}; color: {fg}; '
        f'padding: 3px 10px; border-radius: 12px; '
        f'font-size: 12px; font-weight: bold; '
        f'margin-left: 8px;">{icon} {status}</span>'
    )


def render_participants_panel(participants: List[Dict[str, Any]]) -> None:
    """
    Render the participants panel with KYC indicators.

    Args:
        participants: List of participant dicts (see participants.json schema).
    """
    items_html = ""
    for p in participants:
        org = f" ({p['organization']})" if p.get("organization") else ""
        avatar_color = p.get("avatar_color", "#007bff")
        avatar_initials = p.get("avatar_initials", "??")
        badge = _status_badge(p.get("kyc_status", "Not Started"))
        items_html += (
            f'<li style="margin-bottom: 12px; font-size: 15px; color: #555;'
            f' padding: 8px; border-bottom: 1px solid #f0f0f0;">'
            f'<span style="display: inline-block; width: 32px; height: 32px;'
            f' border-radius: 50%; background-color: {avatar_color};'
            f' color: white; text-align: center; line-height: 32px;'
            f' font-weight: bold; font-size: 12px;'
            f' margin-right: 10px; vertical-align: middle;">'
            f'{avatar_initials}</span>'
            f'<strong>{p["role"]}:</strong> {p["name"]}{org}'
            f'{badge}</li>'
        )

    st.markdown(
        f"""
        <div style="background-color: white; border: 1px solid #eee;
                    border-radius: 8px; padding: 20px; height: 100%;">
            <h4 style="font-size: 18px; color: #333; margin: 0 0 15px 0;
                       padding-bottom: 8px; border-bottom: 2px solid #004a8f;">
                👥 Participants
            </h4>
            <ul style="list-style-type: none; padding: 0; margin: 0;">
                {items_html}
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
