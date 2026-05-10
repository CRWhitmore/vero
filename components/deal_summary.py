"""
components/deal_summary.py
===========================
Renders a small "Deal Summary" card showing key transaction metadata.
"""

from typing import Dict, Any
import streamlit as st


def render_deal_summary(deal: Dict[str, Any], listing: Dict[str, Any]) -> None:
    """
    Render a quick-glance summary panel for the deal.

    Args:
        deal: Deal dict (see data/deals.json schema).
        listing: Associated listing dict.
    """
    current_stage = deal["stages"][deal["current_stage_index"]]

    st.markdown(
        f"""
        <div style="background-color: white; border: 1px solid #eee;
                    border-radius: 8px; padding: 20px; height: 100%;">
            <h4 style="font-size: 18px; color: #333; margin: 0 0 15px 0;
                       padding-bottom: 8px; border-bottom: 2px solid #004a8f;">
                📋 Deal Summary
            </h4>
            <table style="width: 100%; font-size: 14px; color: #555;">
                <tr><td style="padding: 6px 0;"><strong>Property:</strong></td>
                    <td>{listing['name']}</td></tr>
                <tr><td style="padding: 6px 0;"><strong>Location:</strong></td>
                    <td>{listing['location']['city']}, {listing['location']['country']}</td></tr>
                <tr><td style="padding: 6px 0;"><strong>Price:</strong></td>
                    <td style="color: #28a745; font-weight: bold;">
                        {listing['price']['display']}</td></tr>
                <tr><td style="padding: 6px 0;"><strong>Deal ID:</strong></td>
                    <td><code>{deal['deal_id']}</code></td></tr>
                <tr><td style="padding: 6px 0;"><strong>Current Stage:</strong></td>
                    <td><span style="background-color: #007bff; color: white;
                              padding: 3px 8px; border-radius: 4px;
                              font-size: 12px;">{current_stage}</span></td></tr>
                <tr><td style="padding: 6px 0;"><strong>Status:</strong></td>
                    <td>{deal.get('status_label', '—')}</td></tr>
            </table>
        </div>
        """,
        unsafe_allow_html=True,
    )
