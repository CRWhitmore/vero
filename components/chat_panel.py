"""
components/chat_panel.py
=========================
Renders the deal room communication / chat panel.
"""

from typing import List, Dict, Any
import streamlit as st


def render_chat_panel(messages: List[Dict[str, Any]]) -> None:
    """
    Render a simple chat interface with sample messages and a (placeholder)
    input box for sending new messages.

    Args:
        messages: List of message dicts (see data/messages.json).
    """
    st.markdown(
        "<h3 style='font-size: 22px; color: #333; "
        "margin: 0 0 20px 0;'>💬 Deal Communication</h3>",
        unsafe_allow_html=True,
    )

    # Build the chat HTML (scrollable container)
    chat_html = (
        '<div style="height: 450px; overflow-y: auto; '
        'border: 1px solid #eee; border-radius: 8px; '
        'padding: 20px; background-color: #f9f9f9; '
        'margin-bottom: 15px;">'
    )

    for msg in messages:
        is_self = msg.get("is_self", False)
        is_system = msg.get("role", "").lower() == "system"

        # Choose styling
        if is_system:
            avatar_bg = "#004a8f"
            bubble_bg = "#e2f0fe"
            border = "1px solid #004a8f"
        elif is_self:
            avatar_bg = "#007bff"
            bubble_bg = "#d4edda"
            border = "none"
        else:
            avatar_bg = msg.get("avatar_color", "#ffc107")
            bubble_bg = "#ffffff"
            border = "1px solid #e0e0e0"

        align = "flex-end" if is_self else "flex-start"
        flex_direction = "row-reverse" if is_self else "row"
        margin_side = "margin-right: 12px;" if is_self else "margin-left: 12px;"

        chat_html += f"""
        <div style="display: flex; flex-direction: {flex_direction};
                    justify-content: {align}; margin-bottom: 18px;
                    align-items: flex-start;">
            <div style="width: 40px; height: 40px; border-radius: 50%;
                        background-color: {avatar_bg}; color: white;
                        display: flex; align-items: center;
                        justify-content: center; font-weight: bold;
                        font-size: 14px; flex-shrink: 0;">
                {msg.get('avatar_initials', '??')}
            </div>
            <div style="{margin_side} max-width: 70%;">
                <p style="margin: 0 0 4px 0; font-weight: bold;
                          color: #333; font-size: 13px;">
                    {msg['sender']}
                    <span style="font-size: 11px; color: #999;
                                 font-weight: normal; margin-left: 8px;">
                        {msg.get('timestamp', '')}
                    </span>
                </p>
                <div style="background-color: {bubble_bg};
                            padding: 10px 14px; border-radius: 12px;
                            border: {border};
                            box-shadow: 0 1px 2px rgba(0,0,0,0.05);">
                    <p style="margin: 0; font-size: 14px; color: #333;
                              line-height: 1.5;">{msg['text']}</p>
                </div>
            </div>
        </div>
        """

    chat_html += "</div>"
    st.markdown(chat_html, unsafe_allow_html=True)

    # Message composer (placeholder — non-functional)
    composer_col1, composer_col2 = st.columns([5, 1])
    with composer_col1:
        st.text_input(
            "Message",
            placeholder="Type your message here...",
            label_visibility="collapsed",
            key="chat_input",
        )
    with composer_col2:
        st.button("📤 Send", use_container_width=True, key="chat_send_btn")
