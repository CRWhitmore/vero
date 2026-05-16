"""
pages/3_Deal_Room.py
=====================
Vero Transaction Engine — Deal Room Dashboard.

Provides a tabbed interface:
  - Overview (participants, summary, KYC/AML, escrow)
  - Documents (clickable repository + viewer)
  - Communication (chat panel)
  - Tasks & Next Steps (placeholder list)

Plus a "Complete Current Stage / Next Stage" button that advances the
6-stage progress tracker, simulating workflow automation.
"""

import streamlit as st

from components.vero_header import render_vero_header
from components.footer import render_vero_footer
from components.progress_tracker import render_progress_tracker
from components.participants_panel import render_participants_panel
from components.kyc_aml_panel import render_kyc_aml_panel
from components.escrow_panel import render_escrow_panel
from components.document_list import render_document_list
from components.chat_panel import render_chat_panel
from components.deal_summary import render_deal_summary

from services.listing_service import get_listing, get_listings
from services.deal_service import (
    get_or_create_deal,
    advance_stage,
    get_participants,
)
from services.kyc_service import get_kyc_summary
from services.escrow_service import get_escrow
from services.document_service import list_documents
from services.messaging_service import get_messages

from utils.state import init_session_state
from utils.navigation import go_to_listings


st.set_page_config(
    page_title="Vero Deal Room",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def render_deal_header(deal: dict, listing: dict) -> None:
    """Render the deal title and ID."""
    st.markdown(
        f"""
        <div style="margin-bottom: 20px;">
            <h2 style="font-size: 30px; color: #333; margin-bottom: 5px;">
                Deal: {listing['name']}
            </h2>
            <p style="font-size: 15px; color: #666; margin: 0;">
                Deal ID: <code>{deal['deal_id']}</code> &nbsp;|&nbsp;
                🛡️ Blockchain-secured &nbsp;|&nbsp;
                ⚙️ Powered by Vero Transaction Engine
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_next_stage_button(deal: dict, listing: dict) -> None:
    """Render the 'Next Stage' button if not yet at final stage."""
    is_last = deal["current_stage_index"] >= len(deal["stages"]) - 1
    cur_stage = deal["stages"][deal["current_stage_index"]]

    cols = st.columns([3, 2])
    with cols[1]:
        if is_last:
            st.success("🎉 Deal Closed — All stages complete!", icon="✅")
        else:
            next_stage = deal["stages"][deal["current_stage_index"] + 1]
            if st.button(
                f"✅ Complete '{cur_stage}' → Advance to '{next_stage}'",
                use_container_width=True,
                type="primary",
                key="advance_stage_btn",
            ):
                advance_stage(listing["listing_id"])
                st.rerun()


def render_tabs(deal: dict, listing: dict) -> None:
    """Render the four-tab Deal Room interface."""
    participants = get_participants(deal["participant_ids"])
    kyc = get_kyc_summary(deal["kyc_summary_id"])
    escrow = get_escrow(deal["escrow_id"])
    documents = list_documents(deal["deal_id"])
    messages = get_messages(deal["deal_id"])

    overview_tab, docs_tab, comm_tab, tasks_tab = st.tabs(
        ["📊 Overview", "📁 Documents", "💬 Communication", "✅ Tasks & Next Steps"]
    )

    # --- OVERVIEW TAB --------------------------------------------------------
    with overview_tab:
        # Top row: Participants | Deal Summary
        c1, c2 = st.columns(2)
        with c1:
            render_participants_panel(participants)
        with c2:
            render_deal_summary(deal, listing)

        st.markdown("<br>", unsafe_allow_html=True)

        # Bottom row: KYC/AML | Escrow
        c3, c4 = st.columns(2)
        with c3:
            if kyc:
                render_kyc_aml_panel(kyc)
        with c4:
            if escrow:
                render_escrow_panel(escrow)

    # --- DOCUMENTS TAB -------------------------------------------------------
    with docs_tab:
        render_document_list(documents)

    # --- COMMUNICATION TAB ---------------------------------------------------
    with comm_tab:
        render_chat_panel(messages)

    # --- TASKS TAB -----------------------------------------------------------
    with tasks_tab:
        render_tasks_panel(deal)


def render_tasks_panel(deal: dict) -> None:
    """Render a simple tasks/next steps panel."""
    cur_stage = deal["stages"][deal["current_stage_index"]]

    tasks_by_stage = {
        "Offer Submitted": [
            ("Submit Letter of Intent (LOI)", True),
            ("Seller acknowledges receipt", True),
            ("Negotiate LOI terms", False),
        ],
        "KYC/AML Verification": [
            ("Buyer submits KYC documents", True),
            ("Seller submits AML documents", False),
            ("Compliance officer review", False),
            ("UBO declarations collected", False),
        ],
        "Due Diligence": [
            ("Receive due diligence checklist", True),
            ("Property condition report", False),
            ("Environmental assessment (Phase I ESA)", False),
            ("Title commitment review", False),
            ("Financial proforma analysis", False),
        ],
        "Escrow Management": [
            ("Open escrow account", False),
            ("Deposit earnest money", False),
            ("Verify release conditions", False),
            ("Lender funds wired", False),
        ],
        "Contract Negotiation": [
            ("Draft Sales & Purchase Agreement", False),
            ("Legal redlines exchanged", False),
            ("Final SPA executed (digital signature)", False),
            ("Smart contract terms recorded on-chain", False),
        ],
        "Closing": [
            ("Final walkthrough", False),
            ("Recordation of Deed", False),
            ("Funds released from escrow", False),
            ("Post-closing archival to blockchain", False),
        ],
    }

    tasks = tasks_by_stage.get(cur_stage, [("No tasks for this stage", False)])

    items_html = ""
    for task, done in tasks:
        if done:
            items_html += (
                f'<li style="padding: 10px; margin-bottom: 6px;'
                f' background-color: #d4edda; border-radius: 5px;'
                f' border-left: 4px solid #28a745;'
                f' text-decoration: line-through; color: #155724;">'
                f'✅ {task}</li>'
            )
        else:
            items_html += (
                f'<li style="padding: 10px; margin-bottom: 6px;'
                f' background-color: #fff3cd; border-radius: 5px;'
                f' border-left: 4px solid #ffc107; color: #856404;">'
                f'⏳ {task}</li>'
            )

    st.markdown(
        f'<h3 style="font-size: 22px; color: #333; margin: 0 0 15px 0;">'
        f'✅ Tasks for stage: <em>{cur_stage}</em></h3>'
        f'<ul style="list-style-type: none; padding: 0; margin: 0;">{items_html}</ul>',
        unsafe_allow_html=True,
    )


def main() -> None:
    """Page entry."""
    init_session_state()
    # Pull the buyer's name from participants if available; fall back gracefully
    deals_state = st.session_state.get("deals", {})
    listing_id_for_name = st.session_state.get("selected_property_id")
    investor_name = "Investor"
    if listing_id_for_name and listing_id_for_name in deals_state:
        deal_preview = deals_state[listing_id_for_name]
        from services.deal_service import get_participants as _gp
        participants_preview = _gp(deal_preview.get("participant_ids", []))
        buyer = next(
            (p for p in participants_preview if p.get("role", "").lower() == "buyer"),
            None,
        )
        if buyer:
            investor_name = buyer.get("name", "Investor")
    render_vero_header(investor_name=investor_name)

    listing_id = st.session_state.get("selected_property_id")
    listing = get_listing(listing_id) if listing_id else None

    if not listing:
        # Default to first listing
        listings = get_listings()
        listing = listings[0] if listings else None
        if listing:
            st.session_state["selected_property_id"] = listing["listing_id"]

    if not listing:
        st.error("No property selected. Please choose a listing first.")
        render_vero_footer()
        return

    # Get/Create the deal in session state
    deal = get_or_create_deal(listing["listing_id"])

    # Exit deal room link
    if st.button("← Exit Deal Room (back to Realopedia)"):
        go_to_listings()

    render_deal_header(deal, listing)

    # Progress tracker (always visible at top)
    render_progress_tracker(deal["stages"], deal["current_stage_index"])

    # Next stage button — always visible, directly below the progress bar
    render_next_stage_button(deal, listing)

    # Tabbed content
    render_tabs(deal, listing)

    render_vero_footer()


if __name__ == "__main__":
    main()
