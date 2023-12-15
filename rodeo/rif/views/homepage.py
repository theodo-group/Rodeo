import streamlit as st


def home_page():
    st.markdown(
        """
        This is a demo of an image search engine built with VertexAI, Streamlit and Supabase.

        ### It allows you to upload images and search for similar images using text
        """
    )
    st.markdown(
        """
        ## How it works
        1. Go to Upload Images page and upload images
        2. Go to Search Images page and search for images
        """
    )
