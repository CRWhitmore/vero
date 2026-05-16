"""
services/listing_service.py
============================
Mock service layer for property listings.

In production, these functions would proxy real REST calls to the
Realopedia listing API. The signatures are kept REST-like so they can
be swapped 1:1 for HTTP requests later.
"""

from typing import List, Dict, Any, Optional
import json
import os
import streamlit as st

# Resolve the path to the data file relative to this module
_DATA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data",
    "listings.json",
)


@st.cache_data(show_spinner=False)
def _load_listings() -> List[Dict[str, Any]]:
    """Load and return all listings from the static JSON file (cached)."""
    with open(_DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def get_listings() -> List[Dict[str, Any]]:
    """
    Return all available property listings.

    Returns:
        A list of listing dicts.
    """
    return _load_listings()


def get_listing(listing_id: str) -> Optional[Dict[str, Any]]:
    """
    Return a single listing by ID, or None if not found.

    Args:
        listing_id: The unique listing identifier.
    """
    for listing in _load_listings():
        if listing["listing_id"] == listing_id:
            return listing
    return None
