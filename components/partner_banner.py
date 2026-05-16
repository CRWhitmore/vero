"""
components/partner_banner.py
=============================
Renders a continuously scrolling partner / featured-member logo banner,
mirroring the old Realopedia homepage carousel.

Logos are displayed in greyscale and transition to colour on hover.
The animation is pure CSS (no JavaScript dependency).
"""

import base64
import os
from typing import Optional

import streamlit as st

_IMAGES_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "images"
)

# Partner logos in display order (filename, alt text, link)
_PARTNERS = [
    ("partner-dubai-properties.jpg", "Dubai Properties", "https://www.dubaiproperties.ae/"),
    ("partner-asteco.jpg", "Asteco Property Management", "https://www.asteco.com/"),
    ("partner-drei.jpg", "Dubai Real Estate Institute", "https://www.drei.ae/"),
    ("partner-jll.jpg", "JLL MENA", "https://www.jll-mena.com/"),
    ("partner-plus-properties.jpg", "Plus Properties", "https://www.plusproperties.com/"),
    ("partner-mecsc.jpg", "MECSC", "https://www.mecsc.org/"),
    ("partner-mipim.jpg", "MIPIM", "https://www.mipim.com/"),
    ("partner-miami.jpg", "Miami Association of Realtors", "https://www.miamire.com/"),
]


@st.cache_data(show_spinner=False)
def _load_logo(filename: str) -> Optional[str]:
    """Return a base64 data URI for a partner logo image, or None if missing."""
    path = os.path.join(_IMAGES_DIR, filename)
    try:
        ext = filename.rsplit(".", 1)[-1].lower()
        mime = "image/jpeg" if ext in ("jpg", "jpeg") else f"image/{ext}"
        with open(path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
        return f"data:{mime};base64,{encoded}"
    except FileNotFoundError:
        return None


def render_partner_banner() -> None:
    """
    Render the scrolling partner logo banner.
    Logos scroll continuously left using a CSS keyframe animation.
    """
    # Build logo img tags — duplicate the list so the scroll loops seamlessly
    logo_items = ""
    for filename, alt, href in _PARTNERS * 2:
        src = _load_logo(filename)
        if src:
            logo_items += (
                f'<a href="{href}" target="_blank" rel="noopener noreferrer" '
                f'style="display: inline-block; margin: 0 24px; flex-shrink: 0;">'
                f'<img src="{src}" alt="{alt}" '
                f'style="height: 56px; width: auto; max-width: 140px; '
                f'object-fit: contain; '
                f'filter: grayscale(100%) opacity(0.65); '
                f'transition: filter 0.3s ease;" '
                f'onmouseover="this.style.filter=\'grayscale(0%) opacity(1)\'" '
                f'onmouseout="this.style.filter=\'grayscale(100%) opacity(0.65)\'">'
                f'</a>'
            )

    # Total width of one set of logos (8 logos × ~188px each ≈ 1504px)
    # The animation shifts by exactly half the track width so it loops perfectly
    banner_html = (
        '<div style="background-color: #f8f9fa; border-top: 1px solid #e0e0e0; '
        'border-bottom: 1px solid #e0e0e0; padding: 18px 0; margin: 30px 0 0 0; '
        'overflow: hidden; position: relative;">'
        '<p style="text-align: center; font-size: 12px; color: #999; '
        'margin: 0 0 12px 0; letter-spacing: 1px; text-transform: uppercase; '
        'font-weight: 600;">Featured Partners &amp; Members</p>'
        '<div style="display: flex; align-items: center; '
        'animation: scroll-logos 28s linear infinite; '
        'width: max-content;">'
        + logo_items
        + '</div>'
        '</div>'
        '<style>'
        '@keyframes scroll-logos {'
        '  0%   { transform: translateX(0); }'
        '  100% { transform: translateX(-50%); }'
        '}'
        '</style>'
    )

    st.markdown(banner_html, unsafe_allow_html=True)
