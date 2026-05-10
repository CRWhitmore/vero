"""
services/escrow_service.py
===========================
Mock escrow service.
"""

from typing import Dict, Any, Optional
import json
import os

_DATA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data",
    "escrow.json",
)


def get_escrow(escrow_id: str) -> Optional[Dict[str, Any]]:
    """
    Fetch escrow details by ID.

    Args:
        escrow_id: ID of the escrow record.
    """
    with open(_DATA_PATH, "r", encoding="utf-8") as f:
        escrows = json.load(f)
    for e in escrows:
        if e["escrow_id"] == escrow_id:
            return e
    return escrows[0] if escrows else None
