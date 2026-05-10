"""
components/document_list.py
============================
Renders the document repository for the deal room: a list on the left,
a placeholder document viewer on the right.
"""

from typing import List, Dict, Any
import streamlit as st


def _file_icon(filename: str) -> str:
    """Return an emoji icon based on file extension."""
    if filename.lower().endswith(".pdf"):
        return "📕"
    if filename.lower().endswith((".xlsx", ".xls", ".csv")):
        return "📊"
    if filename.lower().endswith((".doc", ".docx")):
        return "📘"
    return "📄"


def render_document_list(documents: List[Dict[str, Any]]) -> None:
    """
    Render a clickable document list with a simulated viewer.

    Args:
        documents: List of document dicts (see data/documents.json schema).
    """
    st.markdown(
        "<h3 style='font-size: 22px; color: #333; "
        "margin: 0 0 20px 0;'>📁 Deal Documents</h3>",
        unsafe_allow_html=True,
    )

    list_col, viewer_col = st.columns([1, 2])

    with list_col:
        st.markdown("**Document Repository**")
        for doc in documents:
            icon = _file_icon(doc["name"])
            label = f"{icon}  {doc['name']}"
            # Each doc is a button — click sets it as the viewed doc
            if st.button(
                label,
                key=f"doc_{doc['document_id']}",
                use_container_width=True,
            ):
                st.session_state["viewed_document"] = doc

            st.markdown(
                f"<p style='font-size: 11px; color: #999; "
                f"margin: -8px 0 8px 8px;'>"
                f"Uploaded: {doc.get('uploaded_at', '—')} &nbsp;|&nbsp; "
                f"Category: {doc.get('category', 'General')}</p>",
                unsafe_allow_html=True,
            )

        st.markdown("<br>", unsafe_allow_html=True)
        st.button("⬆️ Upload New Document", use_container_width=True,
                  disabled=True, help="Placeholder — not functional in prototype")

    with viewer_col:
        viewed = st.session_state.get("viewed_document")
        if viewed:
            st.markdown(
                f"""
                <div style="background-color: #f0f0f0;
                            border: 1px dashed #ccc;
                            border-radius: 8px; padding: 30px;
                            text-align: center; min-height: 400px;">
                    <h4 style="color: #333; margin-bottom: 10px;">
                        📄 Document Viewer
                    </h4>
                    <p style="font-size: 18px; color: #007bff;
                              font-weight: bold;">
                        Viewing: {viewed['name']}
                    </p>
                    <p style="color: #666; font-size: 13px;">
                        Category: {viewed.get('category', 'General')}
                    </p>
                    <hr>
                    <div style="background-color: white;
                                padding: 30px; border-radius: 6px;
                                margin-top: 20px;
                                box-shadow: 0 2px 6px rgba(0,0,0,0.1);
                                text-align: left;">
                        <p style="font-family: 'Times New Roman', serif;
                                  color: #333; line-height: 1.7;">
                            <em>{viewed.get('preview_text',
                            'This is a placeholder document preview. In production, '
                            'the secure PDF viewer would render the actual file '
                            'with watermarking and audit logging.')}</em>
                        </p>
                        <p style="text-align: right; color: #999;
                                  font-size: 12px; margin-top: 30px;">
                            🔐 Hash recorded on blockchain:
                            <code>0x{viewed['document_id'].lower()}...a4f2</code>
                        </p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                """
                <div style="background-color: #f0f0f0;
                            border: 1px dashed #ccc;
                            border-radius: 8px; padding: 60px 20px;
                            text-align: center; min-height: 400px;
                            display: flex; flex-direction: column;
                            align-items: center; justify-content: center;">
                    <div style="font-size: 64px; margin-bottom: 20px;">📄</div>
                    <p style="font-size: 18px; color: #666; font-weight: bold;">
                        Click on a document to view it here.
                    </p>
                    <p style="font-size: 13px; color: #999;">
                        All documents are encrypted at rest and audited on-chain.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )
