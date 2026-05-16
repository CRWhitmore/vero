"""
services/messaging_service.py
==============================
Mock messaging service for the deal-room chat panel.
"""

from typing import List, Dict, Any
import json
import os
import streamlit as st

_DATA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data",
    "messages.json",
)


@st.cache_data(show_spinner=False)
def _load_messages() -> List[Dict[str, Any]]:
    """Load all messages from the static JSON file (cached)."""
    with open(_DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def get_messages(deal_id: str) -> List[Dict[str, Any]]:
    """
    Return all chat messages for a deal.

    Args:
        deal_id: The deal ID.
    """
    all_messages = _load_messages()
    return [m for m in all_messages if m.get("deal_id") in (deal_id, "*", None)] or all_messages
