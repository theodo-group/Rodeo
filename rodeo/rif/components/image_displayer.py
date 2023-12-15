import streamlit as st
from utils.convert_base64_to_image import convert_base64_to_image


def display_image(image):
    try:
        st.image(convert_base64_to_image(image["content"]), width=300)
        st.write("Similarity", round(image["similarity"], 2))
    except:
        st.write("Error", image["id"])
