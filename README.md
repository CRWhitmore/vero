# Realopedia × Vero — Streamlit Clickable Prototype

> A clickable Streamlit prototype demonstrating an end-to-end commercial
> real estate transaction: from property discovery on **Realopedia** to
> deal management in the **Vero Transaction Engine**-powered Deal Room,
> complete with **KYC/AML**, **digital escrow**, **smart contracts**, and
> **blockchain audit trails**.

---

## 🎯 Purpose

This prototype is built for **investor pitches**. It illustrates:

1. **Realopedia** — a global commercial real-estate listing portal.
2. The seamless **"Buy Now"** hand-off from listing to deal room.
3. **Vero Deal Room** — a unified workspace covering:
   - 6-stage progress tracker
   - Participants with KYC/AML status badges
   - Dedicated **KYC/AML** compliance panel
   - Dedicated **Escrow Management** panel
   - Document repository with simulated viewer
   - Multi-party communication / chat panel
   - Tasks per stage
   - **"Advance to Next Stage"** workflow automation

All data is **mocked** (static JSON). There is **no backend**. However, the
service layer mimics REST signatures so real APIs can be plugged in later.

---

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app
streamlit run app.py
```

Open the URL Streamlit prints (usually <http://localhost:8501>).

> **Tip:** Streamlit auto-discovers files in `pages/`. Use the sidebar
> page selector or click in-app buttons to navigate.

---

## 🗺️ User Journeys

### Journey 1: Discovery → Deal Room
1. Land on the **Homepage** (`app.py`).
2. Click **View Details** on a property card.
3. On the **Property Details** page, click the prominent **"BUY NOW"** button.
4. You are seamlessly redirected to the **Vero Deal Room** for that property.

### Journey 2: Deal Room Exploration
1. From the Deal Room **Overview**, review the **Progress Tracker**,
   **Participants** (with KYC badges), **KYC/AML Panel**, and **Escrow Panel**.
2. Switch to the **Documents** tab → click any document to preview it.
3. Switch to **Communication** → see sample messages including Vero system
   notifications about KYC approvals.
4. Switch to **Tasks & Next Steps** → see the actionable checklist for the
   current stage.
5. Click **"Complete Current Stage → Advance to ..."** to simulate the
   workflow advancing through all 6 stages, ending at **Closing**.

---

## 📁 Project Structure

```
output/
├── app.py                           # Entry point — Realopedia Homepage
├── requirements.txt
├── README.md
│
├── pages/
│   ├── 1_Listings.py                # All listings grid + filters
│   ├── 2_Property_Details.py        # Single property + BUY NOW
│   └── 3_Deal_Room.py               # Vero Deal Room (tabbed)
│
├── components/                      # Reusable UI widgets
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
├── services/                        # Mock API layer (REST-shaped)
│   ├── listing_service.py
│   ├── deal_service.py
│   ├── kyc_service.py
│   ├── escrow_service.py
│   ├── document_service.py
│   └── messaging_service.py
│
├── data/                            # Static JSON fixtures
│   ├── listings.json
│   ├── deals.json
│   ├── participants.json
│   ├── kyc.json
│   ├── escrow.json
│   ├── documents.json
│   ├── messages.json
│   └── stages.json
│
└── utils/
    ├── state.py                     # session_state initialisation/helpers
    └── navigation.py                # page-switch helpers
```

---

## 🏛️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  PRESENTATION  (pages/)                                     │
│    app.py → 1_Listings → 2_Property_Details → 3_Deal_Room   │
├─────────────────────────────────────────────────────────────┤
│  COMPONENTS    (components/)                                │
│    headers • cards • tracker • panels • chat • viewer       │
├─────────────────────────────────────────────────────────────┤
│  SERVICES      (services/)                                  │
│    listing_service • deal_service • kyc_service • ...       │
├─────────────────────────────────────────────────────────────┤
│  DATA          (data/*.json)                                │
│    listings • deals • participants • kyc • escrow • docs    │
├─────────────────────────────────────────────────────────────┤
│  STATE         (st.session_state via utils/state.py)        │
│    selected_property_id • deals{} • viewed_document         │
└─────────────────────────────────────────────────────────────┘
```

### Design Principles

| Principle | Implementation |
|---|---|
| **Separation of concerns** | UI ↔ Components ↔ Services ↔ Data are clean layers |
| **Stateful navigation** | `st.session_state` is the single source of truth |
| **Modularity** | Each Deal Room panel is an independent component |
| **Future-proof** | Service signatures mimic REST endpoints |

---

## 🔑 Key Features Demonstrated

| Pitch Deck Value | Where to See it in the Prototype |
|---|---|
| **Global access** | 6 listings spanning USA, UK, UAE, France, Singapore, Germany |
| **AI-powered search** | Banner cue on Homepage + AI Valuation badge |
| **Blockchain security** | "Blockchain Secure" badges on property hero & footer |
| **KYC / AML compliance** | Dedicated panel + per-participant badges |
| **Digital escrow** | Dedicated escrow panel with conditions list |
| **Smart contracts** | Smart Contract Terms doc + on-chain hash in viewer |
| **Workflow automation** | "Advance to Next Stage" button on Overview tab |
| **Transparency** | Centralised tabs for documents, comms, participants |
| **Reduced friction** | Single-click hand-off Realopedia → Deal Room |

---

## 🔧 Extending the Prototype

### Plugging in a real backend

The `services/*.py` modules are intentionally REST-shaped. To wire up
real APIs, replace the JSON file reads with `requests.get(...)` calls.
For example:

```python
# Before (mock)
def get_listing(listing_id: str):
    with open(_DATA_PATH) as f:
        ...

# After (real API)
def get_listing(listing_id: str):
    return requests.get(f"{API}/listings/{listing_id}").json()
```

The UI components and pages do **not** need to change.

### Adding a new property
1. Add an entry to `data/listings.json` (follow the existing schema).
2. The card and detail page will render automatically.

### Adding a new deal stage
1. Add the stage to `data/stages.json` and to the `stages` array in `deals.json`.
2. Add stage-specific tasks in `pages/3_Deal_Room.py` → `render_tasks_panel`.

---

## 📦 Tech Stack

- **Streamlit** ≥ 1.28 (for tabs and `st.switch_page`)
- **Python** ≥ 3.9
- **Pandas, Pillow** (declared but optional for future enhancements)

---

## 📝 Notes on Compatibility

- Uses `st.switch_page` for navigation (Streamlit ≥ 1.28). On older
  Streamlit versions, the `_safe_switch` helper falls back gracefully
  and instructs the user to use the sidebar.
- All inline styling is via Streamlit's `unsafe_allow_html=True` to
  achieve the design-spec look without a separate CSS build step.

---

## 📄 License

Prototype for demonstration purposes. © 2024 Realopedia.
