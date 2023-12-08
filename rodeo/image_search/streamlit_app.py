import streamlit as st
from dotenv import load_dotenv
from image_search.views.search_page import search_page
from image_search.views.upload_page import upload_page

load_dotenv()

# Set Streamlit page configuration
st.set_page_config(page_title="Image Search", page_icon="🔍")

st.title("Image Search Engine 🤖")

# Sidebar for page selection
page = st.sidebar.selectbox(
    "Select a Page",
    [
        "Search Images",
        "Upload Images",
    ],
)


if page == "Upload Images":
    upload_page()
else:
    search_page()
