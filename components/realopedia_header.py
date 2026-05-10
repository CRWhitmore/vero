"""
components/realopedia_header.py
================================
Renders the Realopedia branded top header with logo and navigation.
"""

import streamlit as st


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

    st.markdown(
        f"""
        <div style="background-color: #2c3e50; padding: 18px 30px;
                    color: white; border-bottom: 2px solid #34495e;
                    border-radius: 6px; margin-bottom: 20px;
                    display: flex; justify-content: space-between;
                    align-items: center;">
            <h1 style="margin: 0; font-size: 28px; font-weight: bold;
                       color: white;">
                🏢 Realopedia
            </h1>
            <nav>{nav_html}</nav>
        </div>
        """,
        unsafe_allow_html=True,
    )
