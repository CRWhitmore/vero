# Final Answer — Realopedia × Vero Streamlit Clickable Prototype

A complete, modular Streamlit prototype has been delivered to the `output/` directory. Below is the full content of every source file produced.

## 📁 Final Directory Structure

```
output/
├── app.py                          # Entry — Realopedia Homepage
├── requirements.txt
├── README.md                       # Documentation
│
├── pages/
│   ├── __init__.py
│   ├── 1_Listings.py
│   ├── 2_Property_Details.py
│   └── 3_Deal_Room.py
│
├── components/
│   ├── __init__.py
│   ├── realopedia_header.py
│   ├── vero_header.py
│   ├── footer.py
│   ├── property_card.py
│   ├── property_hero.py
│   ├── progress_tracker.py
│   ├── participants_panel.py
│   ├── kyc_aml_panel.py
│   ├── escrow_panel.py
│   ├── document_list.py
│   ├── chat_panel.py
│   └── deal_summary.py
│
├── services/
│   ├── __init__.py
│   ├── listing_service.py
│   ├── deal_service.py
│   ├── kyc_service.py
│   ├── escrow_service.py
│   ├── document_service.py
│   └── messaging_service.py
│
├── utils/
│   ├── __init__.py
│   ├── state.py
│   └── navigation.py
│
└── data/
    ├── listings.json
    ├── deals.json
    ├── participants.json
    ├── kyc.json
    ├── escrow.json
    ├── documents.json
    ├── messages.json
    └── stages.json
```

---

## 📄 Source Files

### `output/requirements.txt`
```
streamlit>=1.28.0
pandas>=2.0.0
pillow>=10.0.0
```

### `output/app.py`
```python
"""
app.py
======
Main entry point for the Realopedia × Vero Streamlit Clickable Prototype.

This file serves as the Realopedia homepage. It renders the Realopedia
branded header, a hero / search section, a featured commercial property
listings grid, and the shared footer.

Navigation Flow:
    app.py (Homepage)
        -> pages/1_Listings.py (full listings)
        -> pages/2_Property_Details.py (single property)
            -> pages/3_Deal_Room.py (Vero deal room)

Run with:
    streamlit run app.py
"""

import streamlit as st

from components.realopedia_header import render_realopedia_header
from components.footer import render_realopedia_footer
from components.property_card import render_property_card
from services.listing_service import get_listings
from utils.state import init_session_state


st.set_page_config(
    page_title="Realopedia - Commercial Real Estate Listings",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def render_hero_search() -> None:
    """Render the hero / search section with AI-powered matching cue."""
    st.markdown(
        """
        <div style="background-color: #f8f8f8; padding: 40px 20px;
                    text-align: center; border-radius: 8px; margin-bottom: 30px;">
            <h2 style="color: #333; font-size: 32px; margin-bottom: 20px;">
                Find Your Next Commercial Property
            </h2>
            <p style="font-size: 14px; color: #777; margin-top: 10px;">
                ✨ Leveraging AI for smarter property matching &nbsp;|&nbsp;
                🔗 Blockchain-secured listings
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([5, 1])
    with col1:
        st.text_input("Search", placeholder="Search by location, property type, or keyword...",
                      label_visibility="collapsed", key="home_search_input")
    with col2:
        st.button("🔍 Search", use_container_width=True, key="home_search_btn")

    chip_cols = st.columns(4)
    for col, label in zip(chip_cols, ["Office", "Retail", "Industrial", "Land"]):
        with col:
            st.button(label, use_container_width=True, key=f"chip_{label}")


def render_listings_grid() -> None:
    """Render the featured listings grid (3 columns)."""
    st.markdown("<h3 style='color: #333; text-align: center; margin: 30px 0;'>"
                "Featured Commercial Properties</h3>", unsafe_allow_html=True)
    listings = get_listings()
    cols_per_row = 3
    for i in range(0, len(listings), cols_per_row):
        row = st.columns(cols_per_row)
        for j, listing in enumerate(listings[i: i + cols_per_row]):
            with row[j]:
                render_property_card(listing)


def main() -> None:
    init_session_state()
    render_realopedia_header(active="Buy")
    render_hero_search()
    render_listings_grid()
    st.info("💡 Click **View Details** on any property above, or use the sidebar to "
            "navigate to **Listings**, **Property Details**, or the **Deal Room**.", icon="ℹ️")
    render_realopedia_footer()


if __name__ == "__main__":
    main()
```

### `output/pages/1_Listings.py`
```python
"""
pages/1_Listings.py
====================
Realopedia Listings page — shows the full grid of commercial properties.
"""

import streamlit as st

from components.realopedia_header import render_realopedia_header
from components.footer import render_realopedia_footer
from components.property_card import render_property_card
from services.listing_service import get_listings
from utils.state import init_session_state


st.set_page_config(page_title="Realopedia - All Listings", page_icon="🏢",
                   layout="wide", initial_sidebar_state="collapsed")


def render_filter_bar() -> None:
    st.markdown(
        """
        <div style="background-color: #f8f8f8; padding: 20px;
                    border-radius: 8px; margin-bottom: 25px;">
            <h3 style="margin: 0 0 12px 0; color: #333;">🔎 Browse Commercial Properties</h3>
            <p style="margin: 0; color: #777; font-size: 14px;">
                ✨ AI-powered search & matching across global markets
            </p>
        </div>
        """, unsafe_allow_html=True)

    cols = st.columns([2, 2, 2, 2, 1])
    with cols[0]: st.selectbox("Property Type", ["All", "Office", "Retail", "Industrial", "Hotel", "Land"])
    with cols[1]: st.selectbox("Region", ["All", "North America", "Europe", "Middle East", "Asia"])
    with cols[2]: st.selectbox("Price Range", ["All", "Under $10M", "$10M - $50M", "$50M - $100M", "$100M+"])
    with cols[3]: st.text_input("Keyword", placeholder="e.g. logistics, Grade A...")
    with cols[4]:
        st.markdown("<br>", unsafe_allow_html=True)
        st.button("Filter", use_container_width=True)


def render_grid() -> None:
    listings = get_listings()
    cols_per_row = 3
    for i in range(0, len(listings), cols_per_row):
        row = st.columns(cols_per_row)
        for j, listing in enumerate(listings[i: i + cols_per_row]):
            with row[j]:
                render_property_card(listing)


def main() -> None:
    init_session_state()
    render_realopedia_header(active="Buy")
    render_filter_bar()
    render_grid()
    render_realopedia_footer()


if __name__ == "__main__":
    main()
```

### `output/pages/2_Property_Details.py`
```python
"""
pages/2_Property_Details.py
============================
Realopedia Property Details page — shows a single property and the
prominent "BUY NOW" CTA that launches the Vero deal room.
"""

import streamlit as st

from components.realopedia_header import render_realopedia_header
from components.footer import render_realopedia_footer
from components.property_hero import render_property_hero
from services.listing_service import get_listing, get_listings
from utils.state import init_session_state


st.set_page_config(page_title="Realopedia - Property Details", page_icon="🏢",
                   layout="wide", initial_sidebar_state="collapsed")


def render_description_block(listing: dict) -> None:
    st.markdown(f"""
        <div style="background-color: white; border: 1px solid #ddd; border-radius: 8px;
                    padding: 30px; margin-top: 30px; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
            <h3 style="font-size: 22px; color: #333; margin: 0 0 15px 0;
                       padding-bottom: 8px; border-bottom: 1px solid #eee;">📝 Property Description</h3>
            <p style="font-size: 15px; color: #555; line-height: 1.7;">
                {listing.get('long_description', listing['short_description'])}
            </p>
        </div>
    """, unsafe_allow_html=True)

    features_html = "".join(
        f'<li style="font-size: 14px; color: #555; padding: 6px 0;">'
        f'<span style="color: #28a745; margin-right: 8px;">✓</span>{f}</li>'
        for f in listing.get("key_features", [])
    )
    st.markdown(f"""
        <div style="background-color: white; border: 1px solid #ddd; border-radius: 8px;
                    padding: 30px; margin-top: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
            <h3 style="font-size: 22px; color: #333; margin: 0 0 15px 0;
                       padding-bottom: 8px; border-bottom: 1px solid #eee;">⭐ Key Features</h3>
            <ul style="list-style-type: none; padding: 0; margin: 0; columns: 2;">{features_html}</ul>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div style="background-color: white; border: 1px solid #ddd; border-radius: 8px;
                    padding: 30px; margin-top: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
            <h3 style="font-size: 22px; color: #333; margin: 0 0 15px 0;
                       padding-bottom: 8px; border-bottom: 1px solid #eee;">💼 Financials & Documents</h3>
            <p style="font-size: 15px; color: #555; line-height: 1.7;">
                Detailed financial proformas, tenant rosters, and due-diligence documents are
                available in the secure Vero Deal Room upon expressing interest. Our AI Valuation
                tools provide comprehensive market analysis to support your decision.
            </p>
        </div>
    """, unsafe_allow_html=True)

    cols = st.columns(2)
    with cols[0]: st.button("🎥 View Virtual Tour (Placeholder)", use_container_width=True, disabled=True)
    with cols[1]: st.button("📊 AI Valuation Report (Placeholder)", use_container_width=True, disabled=True)


def main() -> None:
    init_session_state()
    render_realopedia_header(active="Buy")

    listing_id = st.session_state.get("selected_property_id")
    listing = get_listing(listing_id) if listing_id else None
    if not listing:
        listings = get_listings()
        listing = listings[0] if listings else None
        if listing:
            st.session_state["selected_property_id"] = listing["listing_id"]

    if not listing:
        st.error("No property selected. Please return to the listings page.")
        render_realopedia_footer()