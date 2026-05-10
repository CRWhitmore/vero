"""
components/escrow_panel.py
===========================
Renders the digital escrow management panel.
"""

from typing import Dict, Any
import streamlit as st


def render_escrow_panel(escrow: Dict[str, Any]) -> None:
    """
    Render the escrow status panel.

    Args:
        escrow: Escrow dict (see data/escrow.json schema).
    """
    status = escrow.get("status", "Not Started")
    status_colors = {
        "Initiated": "#17a2b8",
        "Funds Deposited": "#007bff",
        "Conditions Met": "#ffc107",
        "Funds Released": "#28a745",
        "Not Started": "#6c757d",
    }
    color = status_colors.get(status, "#6c757d")

    conditions_html = "".join(
        f'<li style="margin-bottom: 6px; font-size: 14px; color: #555;">'
        f'<span style="color: #28a745; margin-right: 8px;">✓</span>{cond}</li>'
        for cond in escrow.get("release_conditions", [])
    )

    amount = escrow.get("amount", 0)
    currency = escrow.get("currency", "USD")

    st.markdown(
        f"""
        <div style="background-color: white; border: 1px solid #eee;
                    border-radius: 8px; padding: 20px; height: 100%;">
            <h4 style="font-size: 18px; color: #333; margin: 0 0 15px 0;
                       padding-bottom: 8px; border-bottom: 2px solid #004a8f;">
                💰 Escrow Management
            </h4>
            <div style="background-color: #fafafa; padding: 12px;
                        border-radius: 6px; margin-bottom: 12px;
                        border-left: 4px solid {color};">
                <p style="margin: 4px 0; font-size: 14px;">
                    <strong>Status:</strong>
                    <span style="color: {color}; font-weight: bold;">
                        {status}
                    </span>
                </p>
                <p style="margin: 4px 0; font-size: 14px;">
                    <strong>Amount:</strong>
                    {currency} {amount:,}
                </p>
                <p style="margin: 4px 0; font-size: 14px;">
                    <strong>Escrow Agent:</strong>
                    {escrow.get('agent', 'N/A')}
                </p>
            </div>
            <p style="font-size: 13px; color: #666; margin: 10px 0 6px 0;">
                <strong>Release Conditions:</strong>
            </p>
            <ul style="list-style-type: none; padding-left: 0; margin: 0;">
                {conditions_html}
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
