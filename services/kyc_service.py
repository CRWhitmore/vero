"""
services/kyc_service.py
========================
Mock KYC/AML service. In production this would integrate with vendors
such as Onfido, Trulioo, ComplyAdvantage, etc.
"""

from typing import Dict, Any, List, Optional
import json
import os
import streamlit as st

_DATA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data",
    "kyc.json",
)


@st.cache_data(show_spinner=False)
def _load_kyc_summaries() -> List[Dict[str, Any]]:
    """Load all KYC summaries from the static JSON file (cached)."""
    with open(_DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def get_kyc_summary(kyc_summary_id: str) -> Optional[Dict[str, Any]]:
    """
    Fetch the KYC/AML summary for a given deal.

    Args:
        kyc_summary_id: ID of the summary record.

    Returns:
        KYC summary dict, or None if not found.
    """
    summaries = _load_kyc_summaries()
    for s in summaries:
        if s["kyc_summary_id"] == kyc_summary_id:
            return s
    return summaries[0] if summaries else None
