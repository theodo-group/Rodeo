import streamlit as st
from image_search.components.image_uploader import render_image_uploader


def upload_page():
    st.title("Upload 📤")
    render_image_uploader()
