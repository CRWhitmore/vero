"""
pages/2_Property_Details.py
============================
Realopedia Property Details page — shows a single property and the
prominent "BUY NOW" CTA that launches the Vero deal room.
"""

import streamlit as st
import base64
import os

from components.realopedia_header import get_image_base64
from components.footer import render_realopedia_footer
from components.property_hero import render_property_hero
from services.listing_service import get_listing, get_listings
from utils.state import init_session_state

_IMAGES_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "images"
)
# Logo-relaopedia.png is RGBA (transparent background) — correct for dark/image headers
_LOGO_PATH = os.path.join(_IMAGES_DIR, "Logo-relaopedia.png")


@st.cache_data(show_spinner=False)
def _get_banner_base64() -> str | None:
    """Load banner.jpg as a base64 data URI (cached)."""
    banner_path = os.path.join(_IMAGES_DIR, "banner.jpg")
    try:
        with open(banner_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
        return f"data:image/jpeg;base64,{encoded}"
    except FileNotFoundError:
        return None


def render_hero_header(active: str = "Buy") -> None:
    """
    Render the same full-width hero header as the Listings page.
    """
    banner_src = _get_banner_base64()
    logo_src = get_image_base64(_LOGO_PATH)

    nav_items = ["Buy", "Sell", "About Us", "Login"]
    nav_html = ""
    for item in nav_items:
        weight = "bold" if item == active else "normal"
        underline = "border-bottom: 2px solid white;" if item == active else ""
        nav_html += (
            f'<a href="#" style="color: white; text-decoration: none; '
            f'margin-left: 28px; font-size: 16px; font-weight: {weight}; '
            f'opacity: 0.95; padding-bottom: 2px; {underline}">{item}</a>'
        )

    if logo_src:
        logo_html = (
            f'<img src="{logo_src}" alt="Realopedia Logo" '
            f'style="height: 64px; width: auto; filter: drop-shadow(0 2px 6px rgba(0,0,0,0.4));">'
        )
    else:
        logo_html = (
            '<span style="font-size: 38px; line-height: 64px; '
            'text-shadow: 0 2px 8px rgba(0,0,0,0.5);" '
            'aria-label="Realopedia Logo">🏢</span>'
        )

    if banner_src:
        hero_bg = (
            f"background-image: linear-gradient(to bottom, rgba(0,0,0,0.55) 0%, rgba(0,0,0,0.25) 60%, rgba(0,0,0,0.55) 100%), "
            f"url('{banner_src}');"
        )
    else:
        hero_bg = "background: linear-gradient(135deg, #1a2a3a 0%, #2c3e50 100%);"

    hero_html = (
        '<div style="'
        + hero_bg
        + 'background-size: cover; background-position: center; border-radius: 10px; margin-bottom: 28px; overflow: hidden;">'
        + '<div style="padding: 20px 36px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.15);">'
        + logo_html
        + "<nav>" + nav_html + "</nav>"
        + "</div>"
        + '<div style="padding: 32px 36px 36px 36px; text-align: center;">'
        + '<h1 style="margin: 0 0 8px 0; font-size: 36px; font-weight: 800; color: #ffffff; text-shadow: 0 2px 12px rgba(0,0,0,0.6); letter-spacing: -0.5px;">'
        + "Property Details"
        + "</h1>"
        + '<p style="margin: 0; font-size: 16px; color: rgba(255,255,255,0.88); text-shadow: 0 1px 6px rgba(0,0,0,0.5);">'
        + "AI-powered search &amp; matching &nbsp;|&nbsp; Verified global listings"
        + "</p>"
        + "</div>"
        + "</div>"
    )

    st.markdown(hero_html, unsafe_allow_html=True)


st.set_page_config(
    page_title="Realopedia - Property Details",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def render_description_block(listing: dict) -> None:
    """Render long-form description, key features, and financial CTAs."""
    st.markdown(
        f"""
        <div style="background-color: white; border: 1px solid #ddd;
                    border-radius: 8px; padding: 30px; margin-top: 30px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
            <h3 style="font-size: 22px; color: #333;
                       margin: 0 0 15px 0; padding-bottom: 8px;
                       border-bottom: 1px solid #eee;">
                📝 Property Description
            </h3>
            <p style="font-size: 15px; color: #555; line-height: 1.7;">
                {listing.get('long_description', listing['short_description'])}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Key features
    features_html = "".join(
        f'<li style="font-size: 14px; color: #555; padding: 6px 0;">'
        f'<span style="color: #28a745; margin-right: 8px;">✓</span>{f}</li>'
        for f in listing.get("key_features", [])
    )

    st.markdown(
        f"""
        <div style="background-color: white; border: 1px solid #ddd;
                    border-radius: 8px; padding: 30px; margin-top: 20px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
            <h3 style="font-size: 22px; color: #333;
                       margin: 0 0 15px 0; padding-bottom: 8px;
                       border-bottom: 1px solid #eee;">
                ⭐ Key Features
            </h3>
            <ul style="list-style-type: none; padding: 0; margin: 0;
                       columns: 2;">
                {features_html}
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Financials & Documents (placeholder buttons)
    st.markdown(
        """
        <div style="background-color: white; border: 1px solid #ddd;
                    border-radius: 8px; padding: 30px; margin-top: 20px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
            <h3 style="font-size: 22px; color: #333;
                       margin: 0 0 15px 0; padding-bottom: 8px;
                       border-bottom: 1px solid #eee;">
                💼 Financials & Documents
            </h3>
            <p style="font-size: 15px; color: #555; line-height: 1.7;">
                Detailed financial proformas, tenant rosters, and due-diligence
                documents are available in the secure Vero Deal Room upon
                expressing interest. Our AI Valuation tools provide
                comprehensive market analysis to support your decision.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    cols = st.columns(2)
    with cols[0]:
        st.button("🎥 View Virtual Tour (Placeholder)",
                  use_container_width=True, disabled=True)
    with cols[1]:
        st.button("📊 AI Valuation Report (Placeholder)",
                  use_container_width=True, disabled=True)


def main() -> None:
    """Render property details for the property in session_state."""
    init_session_state()
    render_hero_header(active="Buy")

    listing_id = st.session_state.get("selected_property_id")
    listing = get_listing(listing_id) if listing_id else None

    if not listing:
        # Default to first listing if none selected
        listings = get_listings()
        listing = listings[0] if listings else None
        if listing:
            st.session_state["selected_property_id"] = listing["listing_id"]

    if not listing:
        st.error("No property selected. Please return to the listings page.")
        render_realopedia_footer()
        return

    # Back link
    if st.button("← Back to Listings"):
        from utils.navigation import go_to_listings
        go_to_listings()

    render_property_hero(listing)
    render_description_block(listing)
    render_realopedia_footer()


if __name__ == "__main__":
    main()
