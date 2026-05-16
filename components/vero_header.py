"""
components/vero_header.py
==========================
Renders the Vero Deal Room branded top header (distinct from Realopedia).

Uses VeroLogo.png whose background colour is #0E3149 (dark navy).
The header is stretched full-width using negative margins so it bleeds
to the edges of the Streamlit page container.
"""

import base64
import os
from typing import Optional

import streamlit as st

_IMAGES_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "images"
)
_LOGO_PATH = os.path.join(_IMAGES_DIR, "VeroLogo.png")

# Background colour sampled from VeroLogo.png corners (RGB 14, 49, 79)
_HEADER_BG = "#0E3149"


@st.cache_data(show_spinner=False)
def _get_vero_logo_base64() -> Optional[str]:
    """Load VeroLogo.png as a base64 data URI (cached)."""
    try:
        with open(_LOGO_PATH, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
        return f"data:image/png;base64,{encoded}"
    except FileNotFoundError:
        return None


def render_vero_header(investor_name: str = "Investor Name") -> None:
    """
    Render the Vero Deal Room header.

    The header uses VeroLogo.png and is stretched to 100% page width via
    negative side margins (the standard Streamlit full-bleed technique).

    Args:
        investor_name: Display name shown in the welcome message.
    """
    logo_src = _get_vero_logo_base64()

    if logo_src:
        logo_html = (
            f'<img src="{logo_src}" alt="Vero Transaction Engine" '
            f'style="height: 120px; width: auto; display: block;">'
        )
    else:
        logo_html = (
            '<span style="font-size: 28px; font-weight: bold; color: white;">'
            '🔐 Vero Deal Room</span>'
        )

    # Full-width bleed: pull the div outside Streamlit's padded container
    st.markdown(
        f'<div style="'
        f'background-color: {_HEADER_BG}; '
        f'margin-left: -4rem; margin-right: -4rem; '
        f'padding: 12px 4rem; '
        f'margin-top: -1rem; '
        f'margin-bottom: 24px; '
        f'display: flex; justify-content: space-between; align-items: center; '
        f'border-bottom: 3px solid rgba(255,255,255,0.12);">'
        f'{logo_html}'
        f'<div style="font-size: 16px; color: rgba(255,255,255,0.9);">'
        f'Welcome, <strong style="color: white;">{investor_name}</strong>'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True,
    )
