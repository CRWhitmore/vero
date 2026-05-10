"""
components/property_hero.py
============================
Renders the hero section on the individual property details page,
including the prominent "Buy Now" CTA that launches the Vero deal room.
"""

from typing import Dict, Any
import streamlit as st
import base64
import os

from utils.navigation import go_to_deal_room


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


def get_property_thumbnail_images(property_type: str, listing_name: str = "") -> list:
    """Get list of 5 thumbnail images for property type."""
    # Check for specific property overrides first
    if listing_name == "Tech Park Mixed-Use":
        thumbnail_images = [
            "techpark.jfif",         # Main tech park image
            "image(4).jpg",          # Generic tech image
            "image(5).jpg",          # Generic tech image
            "officetower.jpg",       # Could be office in tech park
            "warehouse.jpg"          # Could be warehouse in tech park
        ]
        return get_thumbnails_base64(thumbnail_images)
    
    # Define related images for each property type
    thumbnail_maps = {
        "Office": [
            "officetower.jpg",      # Main image
            "officetower1.jpg",     # Office tower variant 1
            "officetower2.jpg",     # Office tower variant 2
            "officetower3.jpg",     # Office tower variant 3
            "officetower4.jpg"      # Office tower variant 4
        ],
        "Retail": [
            "highstreetretail.jfif",  # Main image
            "boutiquehotel.jpg",      # Could be retail hotel
            "officetower.jpg",        # Urban retail
            "image(4).jpg",          # Generic retail
            "image(5).jpg"           # Generic retail
        ],
        "Industrial": [
            "warehouse.jpg",         # Main image
            "industrialland.jfif",   # Related industrial land
            "techpark.jfif",         # Tech industrial
            "image(4).jpg",          # Generic industrial
            "image(5).jpg"           # Generic industrial
        ],
        "Hotel": [
            "boutiquehotel.jpg",     # Main image
            "highstreetretail.jfif", # Hotel retail
            "officetower.jpg",       # Urban hotel
            "image(4).jpg",          # Generic hotel
            "image(5).jpg"           # Generic hotel
        ],
        "Land": [
            "industrialland.jfif",   # Main image
            "warehouse.jpg",         # Land for warehouse
            "techpark.jfif",         # Land for tech
            "image(4).jpg",          # Generic land
            "image(5).jpg"           # Generic land
        ]
    }
    
    thumbnails = thumbnail_maps.get(property_type, thumbnail_maps["Office"])
    return get_thumbnails_base64(thumbnails)


def get_thumbnails_base64(thumbnail_images: list) -> list:
    """Convert list of image names to base64 encoded data URIs."""
    result = []
    
    for image_name in thumbnail_images:
        image_path = os.path.join("images", image_name)
        try:
            with open(image_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode()
            result.append(f"data:image/jpeg;base64,{encoded_string}")
        except FileNotFoundError:
            # Create a simple colored placeholder if image not found
            colors = ["#007bff", "#28a745", "#ffc107", "#dc3545", "#6f42c1"]
            color_index = len(result) % len(colors)
            result.append(f"data:image/svg+xml;base64,{base64.b64encode(f'<svg width=\"80\" height=\"80\" xmlns=\"http://www.w3.org/2000/svg\"><rect width=\"80\" height=\"80\" fill=\"{colors[color_index]}\"/><text x=\"40\" y=\"45\" font-family=\"Arial\" font-size=\"10\" fill=\"white\" text-anchor=\"middle\">IMG</text></svg>'.encode()).decode()}")
    
    return result


def render_property_hero(listing: Dict[str, Any]) -> None:
    """
    Render the property hero block: title + main image + price sidebar
    + Buy Now CTA.

    Args:
        listing: The property listing dictionary.
    """
    # Title with Blockchain Secure badge
    st.markdown(
        f"""
        <h2 style="font-size: 34px; color: #333; margin-bottom: 5px;">
            {listing['name']}
            <span style="background-color: #28a745; color: white;
                         padding: 5px 12px; border-radius: 5px;
                         font-size: 14px; margin-left: 15px;
                         vertical-align: middle;">
                🛡️ Blockchain Secure
            </span>
            <span style="background-color: #6f42c1; color: white;
                         padding: 5px 12px; border-radius: 5px;
                         font-size: 14px; margin-left: 5px;
                         vertical-align: middle;">
                ✨ AI Valuation
            </span>
        </h2>
        <p style="font-size: 17px; color: #666; margin-bottom: 25px;">
            📍 {listing['location']['address']}
        </p>
        """,
        unsafe_allow_html=True,
    )

    # Two-column layout: gallery (left, 2x) | price + CTA sidebar (right, 1x)
    left, right = st.columns([2, 1])

    with left:
        # Initialize session state for selected image
        session_key = f"selected_image_{listing['listing_id']}"
        if session_key not in st.session_state:
            st.session_state[session_key] = 0
        
        # Get all thumbnail images
        thumbnail_images = get_property_thumbnail_images(listing['property_type'], listing['name'])
        
        # Display selected image
        if thumbnail_images:
            selected_image = thumbnail_images[st.session_state[session_key]]
            st.markdown(
                f"""
                <div style="height: 400px; border-radius: 8px; overflow: hidden;
                            box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
                    <img src="{selected_image}" alt="{listing['property_type']} Property" 
                         style="width: 100%; height: 100%; object-fit: cover;
                                filter: contrast(1.1) brightness(1.05) saturate(1.1) 
                                        sharpen(0.5); image-rendering: -webkit-optimize-contrast;">
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            # Fallback to gradient with icon
            image_src = get_property_image_base64(listing['property_type'], listing['name'])
            
            if image_src:
                # Use actual property image with quality enhancements
                st.markdown(
                    f"""
                    <div style="height: 400px; border-radius: 8px; overflow: hidden;
                                box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
                        <img src="{image_src}" alt="{listing['property_type']} Property" 
                             style="width: 100%; height: 100%; object-fit: cover;
                                    filter: contrast(1.1) brightness(1.05) saturate(1.1) 
                                            sharpen(0.5); image-rendering: -webkit-optimize-contrast;">
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                # Fallback to gradient with icon
                st.markdown(
                    f"""
                    <div style="background: linear-gradient(135deg,
                                {listing.get('card_color', '#007bff')}, #2c3e50);
                                height: 400px; border-radius: 8px;
                                display: flex; align-items: center;
                                justify-content: center; color: white;
                                font-size: 48px; font-weight: bold;
                                box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
                        {listing.get('icon', '🏢')} {listing['property_type']}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        
        # Gallery thumbnails - clickable images
        thumbnail_images = get_property_thumbnail_images(listing['property_type'], listing['name'])
        
        st.markdown("<p style='font-size: 14px; color: #666; margin: 0 0 10px 0;'><strong>Gallery:</strong></p>", unsafe_allow_html=True)
        
        thumb_img_cols = st.columns(5, gap="small")
        for i in range(5):
            if i < len(thumbnail_images):
                with thumb_img_cols[i]:
                    border_color = "#007bff" if i == st.session_state[session_key] else "#ddd"
                    border_width = "3px" if i == st.session_state[session_key] else "2px"
                    
                    # Use a form to avoid button widget spacing
                    with st.form(key=f"img_form_{listing['listing_id']}_{i}", clear_on_submit=False):
                        st.markdown(
                            f"""
                            <div style="height: 80px; border-radius: 5px; overflow: hidden;
                                        cursor: pointer; border: {border_width} solid {border_color};
                                        box-shadow: {'0 0 8px rgba(0,123,255,0.5)' if i == st.session_state[session_key] else 'none'};
                                        margin-bottom: 5px;">
                                <img src="{thumbnail_images[i]}" alt="Property image {i+1}" 
                                     style="width: 100%; height: 100%; object-fit: cover; cursor: pointer; display: block;">
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                        
                        # Submit button - hidden but clickable
                        submitted = st.form_submit_button(
                            "Select",
                            use_container_width=True,
                            key=f"select_{listing['listing_id']}_{i}"
                        )
                        
                        if submitted:
                            st.session_state[session_key] = i
                            st.rerun()
            else:
                with thumb_img_cols[i]:
                    st.markdown(
                        f"""
                        <div style="background: linear-gradient(135deg, #e0e0e0, #d0d0d0);
                                    height: 80px; border-radius: 5px;
                                    display: flex; align-items: center;
                                    justify-content: center; color: #999;
                                    font-size: 12px;">
                            —
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

    with right:
        st.markdown(
            f"""
            <div style="background-color: #f9f9f9;
                        border: 1px solid #eee;
                        border-radius: 8px; padding: 25px;
                        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
                        text-align: center;">
                <p style="font-size: 30px; font-weight: bold;
                          color: #28a745; margin: 0 0 20px 0;">
                    {listing['price']['display']}
                </p>
                <p style="font-size: 15px; color: #555; margin: 5px 0;">
                    <strong>Property Type:</strong> {listing['property_type']}
                </p>
                <p style="font-size: 15px; color: #555; margin: 5px 0;">
                    <strong>Size:</strong>
                    {listing['size']['sqft']:,} Sq Ft
                    ({listing['size']['sqm']:,} Sq M)
                </p>
                <p style="font-size: 15px; color: #555; margin: 5px 0 20px 0;">
                    <strong>Broker:</strong> {listing.get('broker', 'N/A')}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Prominent BUY NOW button -> launches Vero deal room
        if st.button(
            "💼  BUY NOW  💼",
            key=f"buy_now_{listing['listing_id']}",
            use_container_width=True,
            type="primary",
        ):
            go_to_deal_room(listing["listing_id"])

        st.markdown(
            "<p style='text-align: center; font-size: 12px; color: #777; "
            "margin-top: 5px;'>🔒 Secure transaction powered by Vero</p>",
            unsafe_allow_html=True,
        )

        # Placeholder secondary CTAs (non-functional)
        st.button("📞 Contact Broker", use_container_width=True,
                  key=f"contact_{listing['listing_id']}")
        st.button("🗓️ Schedule Tour", use_container_width=True,
                  key=f"tour_{listing['listing_id']}")
