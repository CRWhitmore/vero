"""
services/deal_service.py
=========================
Mock service layer for deals managed by the Vero transaction engine.
"""

from typing import Dict, Any, Optional, List
import json
import os
import streamlit as st

_DATA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data",
    "deals.json",
)
_PARTICIPANTS_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data",
    "participants.json",
)


@st.cache_data(show_spinner=False)
def _load_deals() -> List[Dict[str, Any]]:
    """Load deals from JSON file (cached)."""
    with open(_DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@st.cache_data(show_spinner=False)
def _load_participants() -> List[Dict[str, Any]]:
    """Load participants from JSON file (cached)."""
    with open(_PARTICIPANTS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def get_or_create_deal(listing_id: str) -> Dict[str, Any]:
    """
    Return an existing deal for the listing, or create a new one in
    session state if none exists. This simulates the moment a user
    clicks "Buy Now" on a listing.

    Args:
        listing_id: The listing the deal is for.

    Returns:
        The deal dict (mutable; lives in session_state once created).
    """
    # Use session_state as our "database" for stage advancement
    deals_state = st.session_state.setdefault("deals", {})

    if listing_id in deals_state:
        return deals_state[listing_id]

    # Try to find a pre-seeded deal in the JSON
    for deal in _load_deals():
        if deal["listing_id"] == listing_id:
            deals_state[listing_id] = dict(deal)  # clone
            return deals_state[listing_id]

    # Otherwise, create a new default deal
    new_deal = {
        "deal_id": f"VERO-2024-{listing_id}",
        "listing_id": listing_id,
        "current_stage_index": 0,
        "stages": [
            "Offer Submitted",
            "KYC/AML Verification",
            "Due Diligence",
            "Escrow Management",
            "Contract Negotiation",
            "Closing",
        ],
        "status_label": "Offer Submitted - Awaiting Seller Review",
        "participant_ids": ["P-BUYER-01", "P-SELLER-01",
                            "P-BROKER-01", "P-LEGAL-01"],
        "escrow_id": "ESC-001",
        "kyc_summary_id": "KYC-001",
    }
    deals_state[listing_id] = new_deal
    return new_deal


def advance_stage(listing_id: str) -> Dict[str, Any]:
    """
    Advance the deal to the next stage (capped at the last stage).

    Args:
        listing_id: The listing whose deal should advance.

    Returns:
        The updated deal dict.
    """
    deal = get_or_create_deal(listing_id)
    if deal["current_stage_index"] < len(deal["stages"]) - 1:
        deal["current_stage_index"] += 1
        new_stage = deal["stages"][deal["current_stage_index"]]
        deal["status_label"] = f"{new_stage} — In Progress"
    return deal


def get_participants(participant_ids: List[str]) -> List[Dict[str, Any]]:
    """
    Resolve participant IDs to participant dicts.

    Args:
        participant_ids: List of participant IDs to load.
    """
    all_participants = _load_participants()
    by_id = {p["participant_id"]: p for p in all_participants}
    return [by_id[pid] for pid in participant_ids if pid in by_id]
