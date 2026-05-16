"""
app.py
======
Main entry point for the Realopedia × Vero Streamlit Clickable Prototype.

This file serves as the Realopedia homepage. It renders the same full-width
hero header used by the Listings and Property Details pages, a search section,
a featured commercial property listings grid, and the shared footer.

Navigation Flow:
    app.py (Homepage)
        -> pages/1_Listings.py (full listings)
        -> pages/2_Property_Details.py (single property)
            -> pages/3_Deal_Room.py (Vero deal room)

Run with:
    streamlit run app.py
"""

import streamlit as st
import base64
import os

from components.realopedia_header import get_image_base64
from components.footer import render_realopedia_footer
from components.property_card import render_property_card
from services.listing_service import get_listings
from utils.state import init_session_state

_IMAGES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")
_LOGO_PATH = os.path.join(_IMAGES_DIR, "Logo-relaopedia.png")


# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Realopedia - Commercial Real Estate Listings",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed",
)


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
    Render the same full-width hero header used by the Listings and
    Property Details pages — banner image background, logo top-left,
    nav links top-right, headline and subtitle centred.
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
        + '<div style="padding: 48px 36px 52px 36px; text-align: center;">'
        + '<h1 style="margin: 0 0 12px 0; font-size: 42px; font-weight: 800; color: #ffffff; text-shadow: 0 2px 12px rgba(0,0,0,0.6); letter-spacing: -0.5px;">'
        + "Global Commercial Real Estate"
        + "</h1>"
        + '<p style="margin: 0; font-size: 17px; color: rgba(255,255,255,0.88); text-shadow: 0 1px 6px rgba(0,0,0,0.5);">'
        + "AI-powered search &amp; matching &nbsp;|&nbsp; Verified global listings"
        + "</p>"
        + "</div>"
        + "</div>"
    )

    st.markdown(hero_html, unsafe_allow_html=True)


def render_search_bar() -> None:
    """Render the search bar and quick-filter chips."""
    col1, col2 = st.columns([5, 1])
    with col1:
        st.text_input(
            "Search",
            placeholder="Search by location, property type, or keyword...",
            label_visibility="collapsed",
            key="home_search_input",
        )
    with col2:
        st.button("🔍 Search", use_container_width=True, key="home_search_btn")

    chip_cols = st.columns(4)
    for col, label in zip(chip_cols, ["Office", "Retail", "Industrial", "Land"]):
        with col:
            st.button(label, use_container_width=True, key=f"chip_{label}")


def render_listings_grid() -> None:
    """Render the featured listings grid (3 columns)."""
    st.markdown(
        "<h3 style='color: #333; text-align: center; margin: 30px 0;'>"
        "Featured Commercial Properties</h3>",
        unsafe_allow_html=True,
    )

    listings = get_listings()
    cols_per_row = 3
    for i in range(0, len(listings), cols_per_row):
        row = st.columns(cols_per_row)
        for j, listing in enumerate(listings[i : i + cols_per_row]):
            with row[j]:
                render_property_card(listing)


def main() -> None:
    """Main entry: initialise state and render page sections in order."""
    init_session_state()
    render_hero_header(active="Buy")
    render_search_bar()
    render_listings_grid()

    st.info(
        "💡 Click **View Details** on any property above, or use the sidebar to "
        "navigate to **Listings**, **Property Details**, or the **Deal Room**.",
        icon="ℹ️",
    )

    render_realopedia_footer()


if __name__ == "__main__":
    main()
