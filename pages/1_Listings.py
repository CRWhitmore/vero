"""
pages/1_Listings.py
====================
Realopedia Listings page — shows the full grid of commercial properties.
"""

import streamlit as st
import base64
import os

from components.realopedia_header import render_realopedia_header, get_image_base64
from components.footer import render_realopedia_footer
from components.partner_banner import render_partner_banner
from components.property_card import render_property_card
from services.listing_service import get_listings
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


st.set_page_config(
    page_title="Realopedia - All Listings",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def render_hero_header(active: str = "Buy") -> None:
    """
    Render a full-width hero section that combines the nav bar and banner image
    into a single seamless block covering roughly the top quarter of the page.
    The nav bar is transparent so the banner image shows through.
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
        + "Browse Commercial Properties"
        + "</h1>"
        + '<p style="margin: 0; font-size: 17px; color: rgba(255,255,255,0.88); text-shadow: 0 1px 6px rgba(0,0,0,0.5);">'
        + "AI-powered search &amp; matching &nbsp;|&nbsp; Verified global listings"
        + "</p>"
        + "</div>"
        + "</div>"
    )

    st.markdown(hero_html, unsafe_allow_html=True)


def render_filter_bar() -> None:
    """Render the filter controls row."""
    cols = st.columns([2, 2, 2, 2, 1])
    with cols[0]:
        st.selectbox("Property Type",
                     ["All", "Office", "Retail", "Industrial", "Hotel", "Land"],
                     key="filter_property_type")
    with cols[1]:
        st.selectbox("Region",
                     ["All", "North America", "Europe", "Middle East", "Asia"],
                     key="filter_region")
    with cols[2]:
        st.selectbox("Price Range",
                     ["All", "Under $10M", "$10M - $50M",
                      "$50M - $100M", "$100M+"],
                     key="filter_price_range")
    with cols[3]:
        st.text_input("Keyword", placeholder="e.g. logistics, Grade A...",
                      key="filter_keyword")
    with cols[4]:
        st.markdown("<br>", unsafe_allow_html=True)
        st.button("Filter", use_container_width=True, key="filter_apply_btn")


def render_grid() -> None:
    """Render the full property grid (3 columns)."""
    listings = get_listings()
    cols_per_row = 3
    for i in range(0, len(listings), cols_per_row):
        row = st.columns(cols_per_row)
        for j, listing in enumerate(listings[i : i + cols_per_row]):
            with row[j]:
                render_property_card(listing)


def main() -> None:
    """Page entry."""
    init_session_state()
    render_hero_header(active="Buy")   # replaces separate header + filter banner
    render_filter_bar()
    render_grid()
    render_partner_banner()
    render_realopedia_footer()


if __name__ == "__main__":
    main()
