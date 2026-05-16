"""
components/realopedia_header.py
================================
Renders the Realopedia branded top header with logo, navigation, and a
full-width banner image background.

The header bleeds to the edges of the Streamlit page container using the
same negative-margin technique as the Vero header.
"""

import os
import streamlit as st
import base64

# Resolve paths relative to this module file
_IMAGES_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "images"
)
_LOGO_PATH = os.path.join(_IMAGES_DIR, "Logo-relaopedia.png")
_BANNER_PATH = os.path.join(_IMAGES_DIR, "banner.jpg")


@st.cache_data(show_spinner=False)
def get_image_base64(image_path: str) -> str | None:
    """Convert image to base64 for embedding in HTML (cached)."""
    ext = os.path.splitext(image_path)[1].lower()
    mime_map = {
        ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
        ".png": "image/png", ".gif": "image/gif",
        ".webp": "image/webp", ".svg": "image/svg+xml",
        ".jfif": "image/jpeg",
    }
    mime = mime_map.get(ext, "image/jpeg")
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        return f"data:{mime};base64,{encoded_string}"
    except FileNotFoundError:
        return None


def render_realopedia_header(active: str = "Buy", subtitle: str = "") -> None:
    """
    Render the Realopedia full-width hero header.

    The banner image bleeds to the page edges using negative side margins
    (the standard Streamlit full-bleed technique, same as the Vero header).
    Logo is top-left, nav links top-right, optional subtitle centred below.

    Args:
        active:   Which nav link should be highlighted (e.g. "Buy", "Sell").
        subtitle: Optional subtitle text shown below the nav bar.
    """
    logo_src = get_image_base64(_LOGO_PATH)
    banner_src = get_image_base64(_BANNER_PATH)

    nav_items = ["Buy", "Sell", "About Us", "Login"]
    nav_html = ""
    for item in nav_items:
        weight = "bold" if item == active else "normal"
        underline = "border-bottom: 2px solid white;" if item == active else ""
        nav_html += (
            f'<a href="#" style="color: white; text-decoration: none; '
            f'margin-left: 28px; font-size: 16px; font-weight: {weight}; '
            f'opacity: 0.95; padding-bottom: 2px; {underline}">{item}</a>'
        )

    if logo_src:
        logo_html = (
            f'<img src="{logo_src}" alt="Realopedia Logo" '
            f'style="height: 64px; width: auto; filter: drop-shadow(0 2px 6px rgba(0,0,0,0.4));">'
        )
    else:
        logo_html = (
            '<span style="font-size: 38px; line-height: 64px; '
            'text-shadow: 0 2px 8px rgba(0,0,0,0.5);" '
            'aria-label="Realopedia Logo">🏢</span>'
        )

    if banner_src:
        bg_css = (
            f"background-image: linear-gradient(to bottom, rgba(0,0,0,0.55) 0%, rgba(0,0,0,0.25) 60%, rgba(0,0,0,0.55) 100%), "
            f"url('{banner_src}'); background-size: cover; background-position: center;"
        )
    else:
        bg_css = "background: linear-gradient(135deg, #1a2a3a 0%, #2c3e50 100%);"

    subtitle_html = ""
    if subtitle:
        subtitle_html = (
            f'<div style="padding: 20px 4rem 24px 4rem; text-align: center;">'
            f'<p style="margin: 0; font-size: 17px; color: rgba(255,255,255,0.88); '
            f'text-shadow: 0 1px 6px rgba(0,0,0,0.5);">{subtitle}</p>'
            f'</div>'
        )

    # Full-width bleed: pull the div outside Streamlit's padded container
    st.markdown(
        f'<div style="'
        f'{bg_css} '
        f'margin-left: -4rem; margin-right: -4rem; '
        f'margin-top: -1rem; '
        f'margin-bottom: 28px; '
        f'overflow: hidden;">'
        f'<div style="padding: 20px 4rem; display: flex; justify-content: space-between; '
        f'align-items: center; border-bottom: 1px solid rgba(255,255,255,0.15);">'
        f'{logo_html}'
        f'<nav>{nav_html}</nav>'
        f'</div>'
        f'{subtitle_html}'
        f'</div>',
        unsafe_allow_html=True,
    )
