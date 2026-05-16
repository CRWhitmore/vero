"""
pages/2_Property_Details.py
============================
Realopedia Property Details page — shows a single property and the
prominent "BUY NOW" CTA that launches the Vero deal room.
"""

import streamlit as st

from components.realopedia_header import render_realopedia_header
from components.footer import render_realopedia_footer
from components.property_hero import render_property_hero
from services.listing_service import get_listing, get_listings
from utils.state import init_session_state


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
    """Render property details for the property in session_state or query params."""
    init_session_state()
    render_realopedia_header(active="Buy")

    # Support navigation via URL query param (e.g. from image href links)
    params = st.query_params
    if "listing_id" in params:
        qp_id = params["listing_id"]
        if qp_id != st.session_state.get("selected_property_id"):
            st.session_state["selected_property_id"] = qp_id

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
