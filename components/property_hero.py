"""
components/property_hero.py
============================
Renders the hero section on the individual property details page,
including the prominent "Buy Now" CTA that launches the Vero deal room.
"""

from typing import Dict, Any
import streamlit as st

from utils.navigation import go_to_deal_room


def render_property_hero(listing: Dict[str, Any]) -> None:
    """
    Render the property hero block: title + main image + price sidebar
    + Buy Now CTA.

    Args:
        listing: The property listing dictionary.
    """
    # Title with Blockchain Secure badge
    st.markdown(
        f"""
        <h2 style="font-size: 34px; color: #333; margin-bottom: 5px;">
            {listing['name']}
            <span style="background-color: #28a745; color: white;
                         padding: 5px 12px; border-radius: 5px;
                         font-size: 14px; margin-left: 15px;
                         vertical-align: middle;">
                🛡️ Blockchain Secure
            </span>
            <span style="background-color: #6f42c1; color: white;
                         padding: 5px 12px; border-radius: 5px;
                         font-size: 14px; margin-left: 5px;
                         vertical-align: middle;">
                ✨ AI Valuation
            </span>
        </h2>
        <p style="font-size: 17px; color: #666; margin-bottom: 25px;">
            📍 {listing['location']['address']}
        </p>
        """,
        unsafe_allow_html=True,
    )

    # Two-column layout: gallery (left, 2x) | price + CTA sidebar (right, 1x)
    left, right = st.columns([2, 1])

    with left:
        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg,
                        {listing.get('card_color', '#007bff')}, #2c3e50);
                        height: 400px; border-radius: 8px;
                        display: flex; align-items: center;
                        justify-content: center; color: white;
                        font-size: 48px; font-weight: bold;
                        box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
                {listing.get('icon', '🏢')} {listing['property_type']}
            </div>
            """,
            unsafe_allow_html=True,
        )
        # Gallery thumbnails
        thumbs = st.columns(5)
        for i, thumb_col in enumerate(thumbs, start=1):
            with thumb_col:
                st.markdown(
                    f"""
                    <div style="background: linear-gradient(135deg, #6c757d, #343a40);
                                height: 80px; border-radius: 5px;
                                display: flex; align-items: center;
                                justify-content: center; color: white;
                                font-size: 12px; margin-top: 10px;
                                cursor: pointer;">
                        Image {i}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    with right:
        st.markdown(
            f"""
            <div style="background-color: #f9f9f9;
                        border: 1px solid #eee;
                        border-radius: 8px; padding: 25px;
                        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
                        text-align: center;">
                <p style="font-size: 30px; font-weight: bold;
                          color: #28a745; margin: 0 0 20px 0;">
                    {listing['price']['display']}
                </p>
                <p style="font-size: 15px; color: #555; margin: 5px 0;">
                    <strong>Property Type:</strong> {listing['property_type']}
                </p>
                <p style="font-size: 15px; color: #555; margin: 5px 0;">
                    <strong>Size:</strong>
                    {listing['size']['sqft']:,} Sq Ft
                    ({listing['size']['sqm']:,} Sq M)
                </p>
                <p style="font-size: 15px; color: #555; margin: 5px 0 20px 0;">
                    <strong>Broker:</strong> {listing.get('broker', 'N/A')}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Prominent BUY NOW button -> launches Vero deal room
        if st.button(
            "💼  BUY NOW  💼",
            key=f"buy_now_{listing['listing_id']}",
            use_container_width=True,
            type="primary",
        ):
            go_to_deal_room(listing["listing_id"])

        st.markdown(
            "<p style='text-align: center; font-size: 12px; color: #777; "
            "margin-top: 5px;'>🔒 Secure transaction powered by Vero</p>",
            unsafe_allow_html=True,
        )

        # Placeholder secondary CTAs (non-functional)
        st.button("📞 Contact Broker", use_container_width=True,
                  key=f"contact_{listing['listing_id']}")
        st.button("🗓️ Schedule Tour", use_container_width=True,
                  key=f"tour_{listing['listing_id']}")
