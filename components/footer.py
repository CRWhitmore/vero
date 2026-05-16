"""
components/footer.py
=====================
Shared footer components for both Realopedia and Vero pages.
"""

import base64
import os
from typing import Optional

import streamlit as st

_IMAGES_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "images"
)

_SOCIAL_LINKS = [
    ("social-facebook.png",  "Facebook",  "https://www.facebook.com/realopedia"),
    ("social-twitter.png",   "Twitter/X", "https://twitter.com/Realopedia"),
    ("social-linkedin.png",  "LinkedIn",  "https://www.linkedin.com/company/realopedia"),
    ("social-youtube.png",   "YouTube",   "https://www.youtube.com/channel/UC1dqDae3BdtULO5ChSlgmnA"),
    ("social-pinterest.png", "Pinterest", "https://www.pinterest.com/realopedia/"),
    ("social-instagram.png", "Instagram", "https://www.instagram.com/realopedia/"),
]


@st.cache_data(show_spinner=False)
def _load_social_icon(filename: str) -> Optional[str]:
    """Return a base64 data URI for a social icon, or None if missing."""
    path = os.path.join(_IMAGES_DIR, filename)
    try:
        with open(path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
        return f"data:image/png;base64,{encoded}"
    except FileNotFoundError:
        return None


def render_realopedia_footer() -> None:
    """Render the Realopedia branded footer with social media icons."""
    social_html = ""
    for filename, label, href in _SOCIAL_LINKS:
        src = _load_social_icon(filename)
        if src:
            social_html += (
                f'<a href="{href}" target="_blank" rel="noopener noreferrer" '
                f'title="{label}" style="display: inline-block; margin: 0 8px;">'
                f'<img src="{src}" alt="{label}" '
                f'style="width: 28px; height: 28px; object-fit: contain; '
                f'opacity: 0.85; transition: opacity 0.2s;" '
                f'onmouseover="this.style.opacity=\'1\'" '
                f'onmouseout="this.style.opacity=\'0.85\'">'
                f'</a>'
            )

    st.markdown(
        f'<div style="background-color: #2c3e50; color: white; '
        f'text-align: center; padding: 20px 0; margin-top: 50px; border-radius: 6px;">'
        f'<div style="margin-bottom: 12px;">{social_html}</div>'
        f'<p style="margin: 0; font-size: 14px;">'
        f'&copy; 2026 Realopedia. All rights reserved. &nbsp;|&nbsp; '
        f'Global Commercial Real Estate Marketplace'
        f'</p></div>',
        unsafe_allow_html=True,
    )


def render_vero_footer() -> None:
    """Render the Vero Deal Room footer."""
    st.markdown(
        """
        <div style="background-color: #004a8f; color: white;
                    text-align: center; padding: 20px 0;
                    margin-top: 50px; border-radius: 6px;">
            <p style="margin: 0; font-size: 14px;">
                Powered by <strong>Vero Transaction Engine</strong> &nbsp;|&nbsp;
                Secured by Blockchain &nbsp;|&nbsp;
                &copy; 2026 Realopedia
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
