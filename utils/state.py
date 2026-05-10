"""
utils/state.py
===============
Helpers for initializing and reading Streamlit's session_state.

This is the single source of truth for cross-page state in the prototype:
  - selected_property_id: which listing the user clicked into
  - active_tab: which Deal Room tab is selected
  - deals: a dict of {listing_id: deal} so stage advancement persists
  - viewed_document: the most recently clicked document
"""

import streamlit as st


_DEFAULTS = {
    "selected_property_id": None,
    "active_tab": "Overview",
    "deals": {},
    "viewed_document": None,
    "navigate_to": None,
}


def init_session_state() -> None:
    """Ensure all expected session_state keys exist with sensible defaults."""
    for key, default in _DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = default


def get(key: str, default=None):
    """Convenience getter that falls back to a default."""
    return st.session_state.get(key, default)


def set_value(key: str, value) -> None:
    """Convenience setter."""
    st.session_state[key] = value
