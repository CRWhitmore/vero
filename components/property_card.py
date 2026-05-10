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


def get_image_base64_helper(image_name: str) -> str:
    """Helper to convert image file to base64."""
    image_path = os.path.join("images", image_name)
    
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        return f"data:image/jpeg;base64,{encoded_string}"
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

    Args:
        listing: A listing dict (see data/listings.json schema).
    """
    badges_html = ""
    for badge in listing.get("badges", []):
        badges_html += (
            f'<span style="background-color: #28a745; color: white; '
            f'padding: 3px 8px; border-radius: 4px; font-size: 11px; '
            f'margin-right: 5px;">🔒 {badge}</span>'
        )

    # Get property image
    image_src = get_property_image_base64(listing['property_type'], listing['name'])
    
    # Use Streamlit container for the card
    with st.container():
        # Card styling
        st.markdown(
            """
            <style>
            .property-card {
                border: 1px solid #ddd;
                border-radius: 8px;
                overflow: hidden;
                background-color: white;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                margin-bottom: 20px;
                min-height: 420px;
            }
            .card-image {
                height: 200px;
                overflow: hidden;
                position: relative;
            }
            .card-image img {
                width: 100%;
                height: 100%;
                object-fit: cover;
            }
            .card-content {
                padding: 20px;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        
        # Image section
        if image_src:
            st.markdown(
                f'<div class="card-image"><img src="{image_src}" alt="{listing["property_type"]} Property" style="filter: contrast(1.1) brightness(1.05) saturate(1.1); image-rendering: -webkit-optimize-contrast;"></div>',
                unsafe_allow_html=True
            )
        else:
            # Fallback gradient
            st.markdown(
                f"""
                <div style="background: linear-gradient(135deg, {listing.get('card_color', '#007bff')}, #2c3e50);
                            height: 200px; display: flex; align-items: center;
                            justify-content: center; color: white;
                            font-size: 22px; font-weight: bold;
                            text-align: center; padding: 20px;">
                    {listing.get('icon', '🏢')}<br>{listing['property_type']}
                </div>
                """,
                unsafe_allow_html=True
            )
        
        # Content section
        st.markdown("### " + listing['name'])
        st.markdown(f"📍 {listing['location']['city']}, {listing['location']['country']}")
        st.markdown(f"**{listing['price']['display']}**")
        st.markdown(listing['short_description'])
        
        # Badges
        if badges_html:
            st.markdown(badges_html, unsafe_allow_html=True)
        
        # Button
        if st.button(
            "View Details →",
            key=f"view_{listing['listing_id']}",
            use_container_width=True,
            type="primary",
        ):
            go_to_property_details(listing["listing_id"])
