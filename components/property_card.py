"""
components/property_card.py
============================
Renders a single commercial property listing card used in the listings grid.
"""

from typing import Dict, Any
import streamlit as st
import base64
import os

from utils.navigation import go_to_property_details

_IMAGES_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "images"
)

_MIME_MAP = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".jfif": "image/jpeg",
    ".png": "image/png",
    ".gif": "image/gif",
    ".webp": "image/webp",
    ".svg": "image/svg+xml",
}

_IMAGE_MAP = {
    "Office":     "officetower.jpg",
    "Retail":     "highstreetretail.jfif",
    "Industrial": "warehouse.jpg",
    "Hotel":      "boutiquehotel.jpg",
    "Land":       "industrialland.jfif",
}

_OVERRIDE_MAP = {
    "Tech Park Mixed-Use": "techpark.jfif",
}


@st.cache_data(show_spinner=False)
def _get_image_base64(filename: str) -> str | None:
    """Return a base64 data URI for the given image filename."""
    path = os.path.join(_IMAGES_DIR, filename)
    ext = os.path.splitext(filename)[1].lower()
    mime = _MIME_MAP.get(ext, "image/jpeg")
    try:
        with open(path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
        return f"data:{mime};base64,{encoded}"
    except FileNotFoundError:
        return None


def _card_image_src(property_type: str, listing_name: str) -> str | None:
    filename = _OVERRIDE_MAP.get(listing_name) or _IMAGE_MAP.get(property_type, "officetower.jpg")
    return _get_image_base64(filename)


def render_property_card(listing: Dict[str, Any]) -> None:
    """
    Render a single property listing card.

    The card image has a hover zoom effect. Clicking the image or the
    "View Details →" button both navigate to the property details page.
    The image click is handled by a Streamlit button styled to be
    invisible and positioned over the image via CSS.
    """
    listing_id = listing["listing_id"]
    image_src = _card_image_src(listing["property_type"], listing["name"])

    description = listing["short_description"]
    if len(description) > 120:
        description = description[:117] + "..."

    # ── Image section ────────────────────────────────────────────────────────
    # The image uses an onclick that calls Streamlit's internal navigation via
    # window.parent to navigate within the same Streamlit session.
    # We use a JS onclick on the image div that sets the URL using
    # window.parent.location so it stays in the same tab and Streamlit picks
    # up the query param on the next render.
    nav_js = (
        f"window.parent.location.href='/Property_Details?listing_id={listing_id}';"
    )

    detail_href = f"/Property_Details?listing_id={listing_id}"

    if image_src:
        image_html = (
            f'<a href="{detail_href}" target="_self" onclick="{nav_js} return false;" '
            f'style="display:block; overflow:hidden; height:200px; text-decoration:none; cursor:pointer;">'
            f'<img src="{image_src}" alt="{listing["property_type"]} Property" '
            f'style="width:100%; height:200px; object-fit:cover; display:block; '
            f'filter: contrast(1.1) brightness(1.05) saturate(1.1); '
            f'transition: transform 0.25s;" '
            f'onmouseover="this.style.transform=\'scale(1.04)\'" '
            f'onmouseout="this.style.transform=\'scale(1)\'">'
            f'</a>'
        )
    else:
        image_html = (
            f'<a href="{detail_href}" target="_self" onclick="{nav_js} return false;" '
            f'style="display:block; text-decoration:none; cursor:pointer;">'
            f'<div style="background: linear-gradient(135deg, #007bff, #2c3e50); '
            f'height:200px; display:flex; align-items:center; justify-content:center; '
            f'color:white; font-size:22px; font-weight:bold; text-align:center; '
            f'padding:20px;">🏢<br>{listing["property_type"]}</div>'
            f'</a>'
        )

    # ── Full card HTML ───────────────────────────────────────────────────────
    card_html = f"""
    <div style="
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        overflow: hidden;
        display: flex;
        flex-direction: column;
        height: 100%;
        margin-bottom: 20px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.08);
        background: white;
    ">
        <div style="overflow: hidden; height: 200px; cursor: pointer;">
            {image_html}
        </div>
        <div style="padding: 16px; flex: 1; display: flex; flex-direction: column;">
            <h4 style="margin: 0 0 6px 0; font-size: 16px; color: #1a1a1a; min-height: 44px;">
                {listing['name']}
            </h4>
            <p style="margin: 0 0 4px 0; font-size: 13px; color: #666;">
                📍 {listing['location']['city']}, {listing['location']['country']}
            </p>
            <p style="margin: 0 0 8px 0; font-size: 15px; font-weight: bold; color: #1a1a1a;">
                {listing['price']['display']}
            </p>
            <p style="margin: 0 0 10px 0; font-size: 13px; color: #444; flex: 1;">
                {description}
            </p>
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

    # ── "View Details" button ────────────────────────────────────────────────
    if st.button(
        "View Details →",
        key=f"view_{listing_id}",
        use_container_width=True,
        type="primary",
    ):
        go_to_property_details(listing_id)
