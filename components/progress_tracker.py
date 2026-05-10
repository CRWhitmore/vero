"""
components/progress_tracker.py
===============================
Renders the 6-stage horizontal progress timeline for a deal.

Stages (in order):
    1. Offer Submitted
    2. KYC/AML Verification
    3. Due Diligence
    4. Escrow Management
    5. Contract Negotiation
    6. Closing
"""

from typing import List
import streamlit as st


def render_progress_tracker(stages: List[str], current_index: int) -> None:
    """
    Render a horizontal stepper / progress tracker.

    Args:
        stages: Ordered list of stage names.
        current_index: Zero-based index of the currently active stage.
    """
    st.markdown(
        "<h3 style='font-size: 22px; color: #333; margin: 10px 0 20px 0;'>"
        "Deal Progress</h3>",
        unsafe_allow_html=True,
    )

    # Build the stage HTML
    n = len(stages)
    pct = int(((current_index) / max(n - 1, 1)) * 100) if n > 1 else 0

    steps_html = ""
    for i, name in enumerate(stages):
        if i < current_index:
            # Completed
            bg, color, icon = "#28a745", "white", "✓"
            text_color = "#28a745"
            text_weight = "normal"
        elif i == current_index:
            # Current
            bg, color, icon = "#007bff", "white", str(i + 1)
            text_color = "#007bff"
            text_weight = "bold"
        else:
            # Future
            bg, color, icon = "#e0e0e0", "#666", str(i + 1)
            text_color = "#666"
            text_weight = "normal"

        steps_html += f"""
        <div style="flex: 1; text-align: center; position: relative; z-index: 1;">
            <div style="width: 36px; height: 36px; border-radius: 50%;
                        background-color: {bg}; color: {color};
                        display: flex; align-items: center; justify-content: center;
                        margin: 0 auto 8px auto; font-weight: bold;
                        font-size: 14px; border: 3px solid white;
                        box-shadow: 0 0 0 2px {bg};">{icon}</div>
            <p style="font-size: 12px; color: {text_color};
                      font-weight: {text_weight}; margin: 0;">
                {name}
            </p>
        </div>
        """

    st.markdown(
        f"""
        <div style="background-color: white; border: 1px solid #ddd;
                    border-radius: 8px; padding: 25px;
                    margin-bottom: 25px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
            <div style="display: flex; justify-content: space-between;
                        align-items: flex-start; position: relative;
                        padding: 0 10px;">
                <!-- Background track -->
                <div style="position: absolute; top: 18px; left: 5%;
                            right: 5%; height: 4px;
                            background-color: #e0e0e0; border-radius: 2px;
                            z-index: 0;"></div>
                <!-- Progress fill -->
                <div style="position: absolute; top: 18px; left: 5%;
                            width: calc({pct}% * 0.9); height: 4px;
                            background-color: #28a745; border-radius: 2px;
                            z-index: 0;"></div>
                {steps_html}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
