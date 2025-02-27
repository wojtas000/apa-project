import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# Actor Oriented Sentiment Analysis")

st.markdown(
    """
    App features
    - View the APA article dataset
    - Train a custom model
    - Infer sentiment for actor in an article
"""
)