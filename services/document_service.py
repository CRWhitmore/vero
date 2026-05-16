"""
services/document_service.py
=============================
Mock document repository service.
"""

from typing import List, Dict, Any
import json
import os
import streamlit as st

_DATA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data",
    "documents.json",
)


@st.cache_data(show_spinner=False)
def _load_documents() -> List[Dict[str, Any]]:
    """Load all documents from the static JSON file (cached)."""
    with open(_DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def list_documents(deal_id: str) -> List[Dict[str, Any]]:
    """
    List all documents associated with a deal.

    Args:
        deal_id: The deal ID.
    """
    all_docs = _load_documents()
    # Return all documents for the prototype (deal-agnostic)
    return [d for d in all_docs if d.get("deal_id") in (deal_id, "*", None)] or all_docs
