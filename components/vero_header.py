"""
components/vero_header.py
==========================
Renders the Vero Deal Room branded top header (distinct from Realopedia).
"""

import streamlit as st


def render_vero_header(investor_name: str = "Investor Name") -> None:
    """
    Render the Vero Deal Room header.

    Args:
        investor_name: Display name shown in the welcome message.
    """
    st.markdown(
        f"""
        <div style="background-color: #004a8f; padding: 18px 30px;
                    color: white; border-bottom: 2px solid #003a70;
                    border-radius: 6px; margin-bottom: 20px;
                    display: flex; justify-content: space-between;
                    align-items: center;">
            <h1 style="margin: 0; font-size: 28px; font-weight: bold;
                       color: white;">
                🔐 Vero Deal Room
            </h1>
            <div style="font-size: 16px;">
                Welcome, <strong>{investor_name}</strong>!
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
