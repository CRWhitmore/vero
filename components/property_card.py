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


# Resolve the images directory relative to this module so it works regardless
# of the working directory Streamlit is launched from.
_IMAGES_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "images"
)

# MIME type map for correct Content-Type in data URIs
_MIME_MAP = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".jfif": "image/jpeg",
    ".png": "image/png",
    ".gif": "image/gif",
    ".webp": "image/webp",
    ".svg": "image/svg+xml",
}


@st.cache_data(show_spinner=False)
def get_image_base64_helper(image_name: str) -> str:
    """Helper to convert image file to base64 (cached per filename)."""
    image_path = os.path.join(_IMAGES_DIR, image_name)
    ext = os.path.splitext(image_name)[1].lower()
    mime = _MIME_MAP.get(ext, "image/jpeg")
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        return f"data:{mime};base64,{encoded_string}"
    except FileNotFoundError:
        # Fallback to icon if image not found
        return None


def get_property_image_base64(property_type: str, listing_name: str = "") -> str:
    """Get base64 encoded image for property type, with specific overrides."""
    # Check for specific property overrides first
    if listing_name == "Tech Park Mixed-Use":
        return get_image_base64_helper("techpark.jfif")
    
    image_map = {
        "Office": "officetower.jpg",
        "Retail": "highstreetretail.jfif",
        "Industrial": "warehouse.jpg",
        "Hotel": "boutiquehotel.jpg",
        "Land": "industrialland.jfif"
    }
    
    image_name = image_map.get(property_type, "officetower.jpg")  # Default fallback
    return get_image_base64_helper(image_name)


def render_property_card(listing: Dict[str, Any]) -> None:
    """
    Render a single property listing card.

    The card shows: hero image (placeholder), name, location, price,
    short description, and a "View Details" button that navigates to
    the property details page using session_state.

    The card uses a fixed-height content area so that "View Details"
    buttons always align at the same vertical position across all cards
    in a row, regardless of how long the title or description is.

    Args:
        listing: A listing dict (see data/listings.json schema).
    """
    # Get property image
    image_src = get_property_image_base64(listing['property_type'], listing['name'])

    # Build the image HTML — wrapped in a button-like div so clicking navigates
    # to property details. We use a unique id and inject a tiny <script> that
    # adds an onclick to the div after render.
    card_img_id = f"card_img_{listing['listing_id']}"

    if image_src:
        image_html = (
            f'<div id="{card_img_id}" style="cursor: pointer; overflow: hidden; height: 200px;">'
            f'<img src="{image_src}" alt="{listing["property_type"]} Property" '
            f'style="width:100%; height:200px; object-fit:cover; display:block; '
            f'filter: contrast(1.1) brightness(1.05) saturate(1.1); '
            f'image-rendering: -webkit-optimize-contrast; '
            f'transition: transform 0.2s;" '
            f'onmouseover="this.style.transform=\'scale(1.04)\'" '
            f'onmouseout="this.style.transform=\'scale(1)\'">'
            f'</div>'
        )
    else:
        image_html = (
            f'<div id="{card_img_id}" style="cursor: pointer; '
            f'background: linear-gradient(135deg, '
            f'{listing.get("card_color", "#007bff")}, #2c3e50); '
            f'height:200px; display:flex; align-items:center; '
            f'justify-content:center; color:white; font-size:22px; '
            f'font-weight:bold; text-align:center; padding:20px;">'
            f'{listing.get("icon", "🏢")}<br>{listing["property_type"]}</div>'
        )

    # Truncate description to keep card heights consistent
    description = listing['short_description']
    if len(description) > 120:
        description = description[:117] + "..."

    # Render the entire card as a single HTML block so the button row
    # is always pushed to the bottom via flexbox, keeping all "View
    # Details" buttons aligned across cards in the same row.
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
        {image_html}
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

    # Streamlit button (rendered outside the HTML block so it stays interactive)
    if st.button(
        "View Details →",
        key=f"view_{listing['listing_id']}",
        use_container_width=True,
        type="primary",
    ):
        go_to_property_details(listing["listing_id"])
