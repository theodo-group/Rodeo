import streamlit as st
from utils.convert_image_to_base64 import convert_image_to_base64
from utils.generate_embedding import generate_embedding
from utils.save_doc_and_embed import save_doc_and_embed


def render_image_uploader():
    dropped_files = st.file_uploader(
        "Choose an image to upload",
        type=["png", "jpg", "jpeg"],
        accept_multiple_files=True,
    )
    if dropped_files is not None:
        for file in dropped_files:
            # To read file as bytes:
            image_bytes_data = file.getvalue()
            embedding = generate_embedding(image_bytes_data)
            save_doc_and_embed(
                content=convert_image_to_base64(image_bytes_data), embedding=embedding
            )

    st.toast("Your images have been uploaded 🎉")
