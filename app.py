"""
app.py
======
Main entry point for the Realopedia × Vero Streamlit Clickable Prototype.

This file serves as the Realopedia homepage. It renders the Realopedia
branded header, a hero / search section, a featured commercial property
listings grid, and the shared footer.

Navigation Flow:
    app.py (Homepage)
        -> pages/1_Listings.py (full listings)
        -> pages/2_Property_Details.py (single property)
            -> pages/3_Deal_Room.py (Vero deal room)

Run with:
    streamlit run app.py
"""

import streamlit as st

from components.realopedia_header import render_realopedia_header
from components.footer import render_realopedia_footer
from components.property_card import render_property_card
from services.listing_service import get_listings
from utils.state import init_session_state


# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Realopedia - Commercial Real Estate Listings",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def render_hero_search() -> None:
    """Render the hero / search section with AI-powered matching cue."""
    st.markdown(
        """
        <div style="background-color: #f8f8f8; padding: 40px 20px;
                    text-align: center; border-radius: 8px; margin-bottom: 30px;">
            <h2 style="color: #333; font-size: 32px; margin-bottom: 20px;">
                Find Your Next Commercial Property
            </h2>
            <p style="font-size: 14px; color: #777; margin-top: 10px;">
                ✨ Leveraging AI for smarter property matching &nbsp;|&nbsp;
                🔗 Blockchain-secured listings
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Search bar (visual only — non-functional placeholder)
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

    # Quick-filter chips
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
    # Render as a 3-column responsive grid
    cols_per_row = 3
    for i in range(0, len(listings), cols_per_row):
        row = st.columns(cols_per_row)
        for j, listing in enumerate(listings[i : i + cols_per_row]):
            with row[j]:
                render_property_card(listing)


def main() -> None:
    """Main entry: initialise state and render page sections in order."""
    init_session_state()
    render_realopedia_header(active="Buy")
    render_hero_search()
    render_listings_grid()

    # Visual hint to navigate
    st.info(
        "💡 Click **View Details** on any property above, or use the sidebar to "
        "navigate to **Listings**, **Property Details**, or the **Deal Room**.",
        icon="ℹ️",
    )

    render_realopedia_footer()


if __name__ == "__main__":
    main()
