"""
pages/1_Listings.py
====================
Realopedia Listings page — shows the full grid of commercial properties.
"""

import streamlit as st

from components.realopedia_header import render_realopedia_header
from components.footer import render_realopedia_footer
from components.property_card import render_property_card
from services.listing_service import get_listings
from utils.state import init_session_state


st.set_page_config(
    page_title="Realopedia - All Listings",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def render_filter_bar() -> None:
    """Render a top filter bar (visual only)."""
    st.markdown(
        """
        <div style="background-color: #f8f8f8; padding: 20px;
                    border-radius: 8px; margin-bottom: 25px;">
            <h3 style="margin: 0 0 12px 0; color: #333;">
                🔎 Browse Commercial Properties
            </h3>
            <p style="margin: 0; color: #777; font-size: 14px;">
                ✨ AI-powered search & matching across global markets
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    cols = st.columns([2, 2, 2, 2, 1])
    with cols[0]:
        st.selectbox("Property Type",
                     ["All", "Office", "Retail", "Industrial", "Hotel", "Land"])
    with cols[1]:
        st.selectbox("Region",
                     ["All", "North America", "Europe", "Middle East", "Asia"])
    with cols[2]:
        st.selectbox("Price Range",
                     ["All", "Under $10M", "$10M - $50M",
                      "$50M - $100M", "$100M+"])
    with cols[3]:
        st.text_input("Keyword", placeholder="e.g. logistics, Grade A...")
    with cols[4]:
        st.markdown("<br>", unsafe_allow_html=True)
        st.button("Filter", use_container_width=True)


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
    render_realopedia_header(active="Buy")
    render_filter_bar()
    render_grid()
    render_realopedia_footer()


if __name__ == "__main__":
    main()
