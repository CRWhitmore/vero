"""
services/escrow_service.py
===========================
Mock escrow service.
"""

from typing import Dict, Any, List, Optional
import json
import os
import streamlit as st

_DATA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data",
    "escrow.json",
)


@st.cache_data(show_spinner=False)
def _load_escrows() -> List[Dict[str, Any]]:
    """Load all escrow records from the static JSON file (cached)."""
    with open(_DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def get_escrow(escrow_id: str) -> Optional[Dict[str, Any]]:
    """
    Fetch escrow details by ID.

    Args:
        escrow_id: ID of the escrow record.
    """
    escrows = _load_escrows()
    for e in escrows:
        if e["escrow_id"] == escrow_id:
            return e
    return escrows[0] if escrows else None
