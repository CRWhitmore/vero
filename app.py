import streamlit as st
import pandas as pd

# Set page config for a professional "Dark Mode" real estate look
st.set_page_config(page_title="CRE DealRoom", layout="wide")

# Sidebar for Navigation
st.sidebar.title("🏢 Asset: 123 Main St")
menu = st.sidebar.radio("Navigate", ["Summary", "Financials", "Due Diligence", "Agent Chat"])

if menu == "Summary":
    st.header("Property Executive Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("Purchase Price", "$12.5M")
    col2.metric("Cap Rate", "5.8%", "+0.2%")
    col3.metric("Occupancy", "94%")
    
    st.subheader("Property Location")
    # Placeholder for map/image
    st.image("https://placeholder.com")

elif menu == "Financials":
    st.header("Interactive Pro-Forma")
    st.write("Adjust assumptions to see updated returns:")
    rent_growth = st.slider("Annual Rent Growth (%)", 0.0, 5.0, 3.0)
    # Your agent would insert logic here to update a dataframe
    st.dataframe(pd.DataFrame({"Year": [1,2,3], "NOI": [725000, 746750, 769152]}))
