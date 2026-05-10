"""
components/property_card.py
============================
Renders a single commercial property listing card used in the listings grid.
"""

from typing import Dict, Any
import streamlit as st

from utils.navigation import go_to_property_details


def render_property_card(listing: Dict[str, Any]) -> None:
    """
    Render a single property listing card.

    The card shows: hero image (placeholder), name, location, price,
    short description, and a "View Details" button that navigates to
    the property details page using session_state.

    Args:
        listing: A listing dict (see data/listings.json schema).
    """
    badges_html = ""
    for badge in listing.get("badges", []):
        badges_html += (
            f'<span style="background-color: #28a745; color: white; '
            f'padding: 3px 8px; border-radius: 4px; font-size: 11px; '
            f'margin-right: 5px;">🔒 {badge}</span>'
        )

    # Card container with shadow + border
    st.markdown(
        f"""
        <div style="border: 1px solid #ddd; border-radius: 8px;
                    overflow: hidden; background-color: white;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                    margin-bottom: 20px; min-height: 420px;">
            <div style="background: linear-gradient(135deg, {listing.get('card_color', '#007bff')}, #2c3e50);
                        height: 200px; display: flex; align-items: center;
                        justify-content: center; color: white;
                        font-size: 22px; font-weight: bold;
                        text-align: center; padding: 20px;">
                {listing.get('icon', '🏢')}<br>{listing['property_type']}
            </div>
            <div style="padding: 20px;">
                <h4 style="margin: 0 0 8px 0; font-size: 20px; color: #333;">
                    {listing['name']}
                </h4>
                <p style="color: #666; font-size: 14px; margin: 0 0 8px 0;">
                    📍 {listing['location']['city']}, {listing['location']['country']}
                </p>
                <p style="font-size: 22px; font-weight: bold;
                          color: #28a745; margin: 0 0 10px 0;">
                    {listing['price']['display']}
                </p>
                <p style="font-size: 13px; color: #555; line-height: 1.5;
                          height: 60px; overflow: hidden;">
                    {listing['short_description']}
                </p>
                <div style="margin-top: 10px;">{badges_html}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Streamlit button under the card to trigger navigation
    if st.button(
        "View Details →",
        key=f"view_{listing['listing_id']}",
        use_container_width=True,
        type="primary",
    ):
        go_to_property_details(listing["listing_id"])
