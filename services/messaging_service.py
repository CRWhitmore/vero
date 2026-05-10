"""
services/messaging_service.py
==============================
Mock messaging service for the deal-room chat panel.
"""

from typing import List, Dict, Any
import json
import os

_DATA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data",
    "messages.json",
)


def get_messages(deal_id: str) -> List[Dict[str, Any]]:
    """
    Return all chat messages for a deal.

    Args:
        deal_id: The deal ID.
    """
    with open(_DATA_PATH, "r", encoding="utf-8") as f:
        all_messages = json.load(f)
    return [m for m in all_messages if m.get("deal_id") in (deal_id, "*", None)] or all_messages
