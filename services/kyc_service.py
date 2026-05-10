"""
services/kyc_service.py
========================
Mock KYC/AML service. In production this would integrate with vendors
such as Onfido, Trulioo, ComplyAdvantage, etc.
"""

from typing import Dict, Any, Optional
import json
import os

_DATA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data",
    "kyc.json",
)


def get_kyc_summary(kyc_summary_id: str) -> Optional[Dict[str, Any]]:
    """
    Fetch the KYC/AML summary for a given deal.

    Args:
        kyc_summary_id: ID of the summary record.

    Returns:
        KYC summary dict, or None if not found.
    """
    with open(_DATA_PATH, "r", encoding="utf-8") as f:
        summaries = json.load(f)
    for s in summaries:
        if s["kyc_summary_id"] == kyc_summary_id:
            return s
    return summaries[0] if summaries else None
