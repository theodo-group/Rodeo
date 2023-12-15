import streamlit as st
from components.image_displayer import display_image
from utils.get_nearest_images import get_nearest_images


def search_page():
    st.title("Search 🔍")
    grid = st.columns(2)

    text_query = st.text_input("Which image are you looking for ?")

    with st.spinner("Training ongoing"):
        if text_query:
            images = get_nearest_images(text_query=text_query)
            for i in range(len(images)):
                image = images[i]
                with grid[i % 2]:
                    display_image(image)
