"""
components/property_hero.py
============================
Renders a clean, high-end hero section with a static image gallery.
"""

from typing import Dict, Any
import streamlit as st
import base64
import os

from utils.navigation import go_to_deal_room

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
        return None


def get_property_thumbnail_images(property_type: str, listing_name: str = "") -> list:
    """Get list of 5 thumbnail images for property type."""
    thumbnail_maps = {
        "Office": ["officetower.jpg", "officetower1.jpg", "officetower2.jpg", "officetower3.jpg", "officetower4.jpg"],
        "Retail": ["highstreetretail.jfif", "boutiquehotel.jpg", "officetower.jpg", "image(4).jpg", "image(5).jpg"],
        "Industrial": ["warehouse.jpg", "industrialland.jfif", "techpark.jfif", "image(4).jpg", "image(5).jpg"],
        "Hotel": ["boutiquehotel.jpg", "highstreetretail.jfif", "officetower.jpg", "image(4).jpg", "image(5).jpg"],
        "Land": ["industrialland.jfif", "warehouse.jpg", "techpark.jfif", "image(4).jpg", "image(5).jpg"]
    }
    
    if listing_name == "Tech Park Mixed-Use":
        images = ["techpark.jfif", "image(4).jpg", "image(5).jpg", "officetower.jpg", "warehouse.jpg"]
    else:
        images = thumbnail_maps.get(property_type, thumbnail_maps["Office"])
    
    return [get_image_base64_helper(img) for img in images]


def render_property_hero(listing: Dict[str, Any]) -> None:
    """
    Renders the property hero with a clean Title, Main Image, and static Gallery row.
    """

    # Title & Location
    st.markdown(
        f"""
        <h2 style="font-size: 34px; font-weight: 700; color: #1a1a1a; margin-bottom: 2px;">
            {listing['name']}
            <span style="font-size: 14px; background: #e8f5e9; color: #2e7d32; padding: 4px 12px; border-radius: 4px; margin-left: 10px; vertical-align: middle; border: 1px solid #c8e6c9;">🛡️ Blockchain Secure</span>
        </h2>
        <p style="font-size: 17px; color: #666; margin-bottom: 25px;">📍 {listing['location']['address']}</p>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns([2.2, 1], gap="large")

    with left:
        thumbnail_images = get_property_thumbnail_images(listing['property_type'], listing['name'])
        
        # Main Feature Image (Always show the first image)
        if thumbnail_images and thumbnail_images[0]:
            st.markdown(
                f"""
                <div style="height: 450px; border-radius: 12px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.1); margin-bottom: 20px;">
                    <img src="{thumbnail_images[0]}" style="width: 100%; height: 100%; object-fit: cover;">
                </div>
                """,
                unsafe_allow_html=True,
            )
        
        # Static Gallery Row
        st.markdown("<p style='font-size: 14px; font-weight: 600; color: #333; margin-bottom: 12px;'>PROPERTY PHOTOS</p>", unsafe_allow_html=True)
        
        cols = st.columns(5, gap="small")
        for i in range(5):
            with cols[i]:
                if i < len(thumbnail_images) and thumbnail_images[i]:
                    st.markdown(
                        f"""
                        <div style="height: 100px; border-radius: 8px; overflow: hidden; border: 1px solid #eee; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
                            <img src="{thumbnail_images[i]}" style="width: 100%; height: 100%; object-fit: cover;">
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown('<div style="background: #f8f9fa; height: 100px; border-radius: 8px; border: 1px dashed #ddd;"></div>', unsafe_allow_html=True)

    with right:
        # Price Info Box
        st.markdown(
            f"""
            <div style="background: #ffffff; border: 1px solid #e1e4e8; border-radius: 12px; padding: 25px; box-shadow: 0 4px 20px rgba(0,0,0,0.06); text-align: center;">
                <p style="color: #6a737d; font-size: 13px; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px;">List Price</p>
                <p style="font-size: 34px; font-weight: 800; color: #28a745; margin-bottom: 24px;">{listing['price']['display']}</p>
                <div style="text-align: left; font-size: 15px; color: #24292e; line-height: 1.8; border-top: 1px solid #f6f8fa; padding-top: 15px;">
                    <p><strong>🏢 Type:</strong> {listing['property_type']}</p>
                    <p><strong>📐 Size:</strong> {listing['size']['sqft']:,} Sq Ft</p>
                    <p><strong>👤 Broker:</strong> {listing.get('broker', 'N/A')}</p>
                </div>
            </div>
            <div style="margin-top: 20px;"></div>
            """,
            unsafe_allow_html=True,
        )

        # Primary Action
        if st.button("💼  BUY NOW  💼", key=f"buy_now_{listing['listing_id']}", use_container_width=True, type="primary"):
            go_to_deal_room(listing["listing_id"])

        st.markdown("<p style='text-align: center; font-size: 11px; color: #959da5; margin-top: 10px;'>Secure transaction powered by Vero Blockchain</p>", unsafe_allow_html=True)
        
        # Secondary Actions
        st.button("📞 Contact Broker", use_container_width=True, key=f"contact_{listing['listing_id']}")
        st.button("🗓️ Schedule Tour", use_container_width=True, key=f"tour_{listing['listing_id']}")