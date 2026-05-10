"""
services/document_service.py
=============================
Mock document repository service.
"""

from typing import List, Dict, Any
import json
import os

_DATA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data",
    "documents.json",
)


def list_documents(deal_id: str) -> List[Dict[str, Any]]:
    """
    List all documents associated with a deal.

    Args:
        deal_id: The deal ID.
    """
    with open(_DATA_PATH, "r", encoding="utf-8") as f:
        all_docs = json.load(f)
    # Return all documents for the prototype (deal-agnostic)
    return [d for d in all_docs if d.get("deal_id") in (deal_id, "*", None)] or all_docs
