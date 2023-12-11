import streamlit as st
from image_search.utils.convert_image_to_base64 import convert_image_to_base64
from image_search.utils.generate_embedding import generate_embedding
from image_search.utils.save_doc_and_embed import save_doc_and_embed


def render_image_uploader():
    uploaded_file = st.file_uploader(
        "Choose an image to upload",
        type=["png", "jpg", "jpeg"],
    )
    if uploaded_file is not None:
        # To read file as bytes:
        image_bytes_data = uploaded_file.getvalue()
        embedding = generate_embedding(image_bytes_data)
        save_doc_and_embed(
            content=convert_image_to_base64(image_bytes_data), embedding=embedding
        )
        st.toast("Your image was successfully uploaded!", icon="✅")
