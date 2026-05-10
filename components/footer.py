"""
components/footer.py
=====================
Shared footer components for both Realopedia and Vero pages.
"""

import streamlit as st


def render_realopedia_footer() -> None:
    """Render the Realopedia branded footer."""
    st.markdown(
        """
        <div style="background-color: #2c3e50; color: white;
                    text-align: center; padding: 20px 0;
                    margin-top: 50px; border-radius: 6px;">
            <p style="margin: 0; font-size: 14px;">
                &copy; 2024 Realopedia. All rights reserved. &nbsp;|&nbsp;
                Global Commercial Real Estate Marketplace
            </p>
        </div>
        """,
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
                &copy; 2024 Realopedia
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
