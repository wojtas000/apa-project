import streamlit as st
import requests

from settings import BASE_URL, HEADERS

def inference(text: str):
    response = requests.post(
        f"{BASE_URL}/inference",
        headers=HEADERS,
        json={"text": text}
    )
    return response.json()

st.title("Inference")

text = st.text_area("Enter Text")
if st.button("Predict"):
    prediction = inference(text)
    st.json(prediction)