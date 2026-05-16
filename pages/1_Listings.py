"""
pages/1_Listings.py
====================
Realopedia Listings page — shows the full grid of commercial properties.
"""

import streamlit as st

from components.realopedia_header import render_realopedia_header
from components.footer import render_realopedia_footer
from components.property_card import render_property_card
from components.partner_banner import render_partner_banner
from services.listing_service import get_listings
from utils.state import init_session_state


st.set_page_config(
    page_title="Realopedia - All Listings",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed",
)


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
                     ["All", "Under $10M", "$10M - $50M", "$50M - $200M", "Over $200M"],
                     key="filter_price")
    with cols[3]:
        st.text_input("Search", placeholder="Keyword...", key="filter_search")
    with cols[4]:
        st.button("🔍 Filter", use_container_width=True, key="filter_btn")


def render_listings_grid() -> None:
    """Render the full listings grid (3 columns)."""
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
    render_realopedia_header(
        active="Buy",
        subtitle="AI-powered search &amp; matching &nbsp;|&nbsp; Verified global listings",
    )
    render_filter_bar()

    st.markdown(
        "<h3 style='color: #333; margin: 20px 0 16px 0;'>All Commercial Properties</h3>",
        unsafe_allow_html=True,
    )
    render_listings_grid()
    render_partner_banner()
    render_realopedia_footer()


if __name__ == "__main__":
    main()
