"""
components/realopedia_header.py
================================
Renders the Realopedia branded top header with logo and navigation.
"""

import os
import streamlit as st
import base64


# Resolve logo path relative to this module file
# Logo-relaopedia.png is RGBA (transparent background) — correct for dark headers
_LOGO_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "images", "Logo-relaopedia.png"
)


@st.cache_data(show_spinner=False)
def get_image_base64(image_path: str) -> str | None:
    """Convert image to base64 for embedding in HTML (cached)."""
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        return f"data:image/png;base64,{encoded_string}"
    except FileNotFoundError:
        return None


def render_realopedia_header(active: str = "Buy") -> None:
    """
    Render the Realopedia top navigation header.

    Args:
        active: Which nav link should be highlighted (e.g. "Buy", "Sell").
    """
    nav_items = ["Buy", "Sell", "About Us", "Login"]

    nav_html = ""
    for item in nav_items:
        weight = "bold" if item == active else "normal"
        opacity = "1" if item == active else "0.85"
        nav_html += (
            f'<a href="#" style="color: white; text-decoration: none; '
            f'margin-left: 25px; font-size: 16px; font-weight: {weight}; '
            f'opacity: {opacity};">{item}</a>'
        )

    # Get base64 encoded image using the absolute path resolved at module load
    logo_src = get_image_base64(_LOGO_PATH)

    # Build the logo element: use <img> when we have a data URI, fall back to
    # a styled <span> with an emoji so the header HTML stays valid.
    if logo_src:
        logo_html = (
            f'<img src="{logo_src}" alt="Realopedia Logo" '
            f'style="height: 40px; width: auto;">'
        )
    else:
        logo_html = (
            '<span style="font-size: 28px; line-height: 40px;" '
            'aria-label="Realopedia Logo">🏢</span>'
        )

    st.markdown(
        f"""
        <div style="background-color: #2c3e50; padding: 18px 30px;
                    color: white; border-bottom: 2px solid #34495e;
                    border-radius: 6px; margin-bottom: 20px;
                    display: flex; justify-content: space-between;
                    align-items: center;">
            {logo_html}
            <nav>{nav_html}</nav>
        </div>
        """,
        unsafe_allow_html=True,
    )
