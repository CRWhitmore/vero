"""
components/property_hero.py
============================
Renders a clean, high-end hero section with a clickable image gallery.

Uses streamlit-image-select for the thumbnail strip so that clicking
directly on an image (no separate button) updates the main viewer.
"""

from typing import Dict, Any
import streamlit as st
import base64
import os

from streamlit_image_select import image_select
from utils.navigation import go_to_deal_room

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
        return None


def get_property_image_paths(property_type: str, listing_name: str = "") -> list:
    """Return list of 5 absolute image paths for the property type."""
    thumbnail_maps = {
        "Office":     ["officetower.jpg", "officetower1.jpg", "officetower2.jpg", "officetower3.jpg", "officetower4.jpg"],
        "Retail":     ["highstreetretail.jfif", "boutiquehotel.jpg", "officetower.jpg", "image(4).jpg", "image(5).jpg"],
        "Industrial": ["warehouse.jpg", "industrialland.jfif", "techpark.jfif", "image(4).jpg", "image(5).jpg"],
        "Hotel":      ["boutiquehotel.jpg", "highstreetretail.jfif", "officetower.jpg", "image(4).jpg", "image(5).jpg"],
        "Land":       ["industrialland.jfif", "warehouse.jpg", "techpark.jfif", "image(4).jpg", "image(5).jpg"],
    }
    if listing_name == "Tech Park Mixed-Use":
        filenames = ["techpark.jfif", "image(4).jpg", "image(5).jpg", "officetower.jpg", "warehouse.jpg"]
    else:
        filenames = thumbnail_maps.get(property_type, thumbnail_maps["Office"])

    paths = []
    for fn in filenames:
        p = os.path.join(_IMAGES_DIR, fn)
        if os.path.exists(p):
            paths.append(p)
    return paths


def render_property_hero(listing: Dict[str, Any]) -> None:
    """
    Renders the property hero with a clickable thumbnail gallery.

    streamlit-image-select renders each thumbnail as a clickable image —
    no separate buttons. Clicking a thumbnail immediately updates the
    main large image above.
    """
    listing_id = listing["listing_id"]
    state_key = f"selected_photo_idx_{listing_id}"

    if state_key not in st.session_state:
        st.session_state[state_key] = 0

    # Title & Location
    st.markdown(
        f'<h2 style="font-size: 34px; font-weight: 700; color: #1a1a1a; margin-bottom: 2px;">'
        f'{listing["name"]}</h2>'
        f'<p style="font-size: 17px; color: #666; margin-bottom: 25px;">'
        f'📍 {listing["location"]["address"]}</p>',
        unsafe_allow_html=True,
    )

    left, right = st.columns([2.2, 1], gap="large")

    with left:
        image_paths = get_property_image_paths(
            listing["property_type"], listing["name"]
        )

        selected_idx = st.session_state[state_key]

        # ── Main Feature Image ──────────────────────────────────────────────
        if image_paths:
            main_src = get_image_base64_helper(
                os.path.basename(image_paths[selected_idx])
            )
            if main_src:
                st.markdown(
                    f'<div style="height: 450px; border-radius: 12px; overflow: hidden; '
                    f'box-shadow: 0 10px 30px rgba(0,0,0,0.1); margin-bottom: 12px;">'
                    f'<img src="{main_src}" style="width: 100%; height: 100%; object-fit: cover;">'
                    f'</div>',
                    unsafe_allow_html=True,
                )
        else:
            st.markdown(
                '<div style="height: 450px; border-radius: 12px; background: #f0f0f0; '
                'margin-bottom: 12px;"></div>',
                unsafe_allow_html=True,
            )

        # ── Thumbnail Strip via streamlit-image-select ──────────────────────
        if image_paths:
            chosen_path = image_select(
                label="",
                images=image_paths,
                index=selected_idx,
                use_container_width=True,
                return_value="index",
                key=f"img_select_{listing_id}",
            )
            if chosen_path != selected_idx:
                st.session_state[state_key] = chosen_path
                st.rerun()

    with right:
        # Price Info Box
        st.markdown(
            f'<div style="background: #ffffff; border: 1px solid #e1e4e8; border-radius: 12px; '
            f'padding: 25px; box-shadow: 0 4px 20px rgba(0,0,0,0.06); text-align: center;">'
            f'<p style="color: #6a737d; font-size: 13px; text-transform: uppercase; '
            f'letter-spacing: 0.5px; margin-bottom: 8px;">List Price</p>'
            f'<p style="font-size: 34px; font-weight: 800; color: #28a745; margin-bottom: 24px;">'
            f'{listing["price"]["display"]}</p>'
            f'<div style="text-align: left; font-size: 15px; color: #24292e; line-height: 1.8; '
            f'border-top: 1px solid #f6f8fa; padding-top: 15px;">'
            f'<p><strong>🏢 Type:</strong> {listing["property_type"]}</p>'
            f'<p><strong>📐 Size:</strong> {listing["size"]["sqft"]:,} Sq Ft</p>'
            f'<p><strong>👤 Broker:</strong> {listing.get("broker", "N/A")}</p>'
            f'</div></div>'
            f'<div style="margin-top: 20px;"></div>',
            unsafe_allow_html=True,
        )

        if st.button(
            "💼  BUY NOW  💼",
            key=f"buy_now_{listing_id}",
            use_container_width=True,
            type="primary",
        ):
            go_to_deal_room(listing_id)

        st.button("📞 Contact Broker", use_container_width=True, key=f"contact_{listing_id}")
        st.button("🗓️ Schedule Tour", use_container_width=True, key=f"tour_{listing_id}")
