"""
utils/navigation.py
====================
Page navigation helpers. We use Streamlit's `st.switch_page` API where
available; if not, we fall back to setting session_state and prompting
the user to click the relevant entry in the sidebar.
"""

import streamlit as st


def _safe_switch(target: str) -> None:
    """Try to switch to the target Streamlit page (if API is available)."""
    try:
        st.switch_page(target)
    except Exception:
        # Older Streamlit fallback — write a hint and rerun
        st.session_state["navigate_to"] = target
        st.rerun()


def go_to_listings() -> None:
    """Navigate to the Listings page."""
    _safe_switch("pages/1_Listings.py")


def go_to_property_details(listing_id: str) -> None:
    """
    Set the selected property and navigate to the property details page.

    Args:
        listing_id: ID of the listing to view.
    """
    st.session_state["selected_property_id"] = listing_id
    _safe_switch("pages/2_Property_Details.py")


def go_to_deal_room(listing_id: str) -> None:
    """
    Set the selected property and navigate to the Vero Deal Room.

    Args:
        listing_id: ID of the listing whose deal we're entering.
    """
    st.session_state["selected_property_id"] = listing_id
    st.session_state["active_tab"] = "Overview"
    _safe_switch("pages/3_Deal_Room.py")
