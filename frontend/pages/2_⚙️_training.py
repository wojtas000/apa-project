import streamlit as st
import requests

from settings import BASE_URL, HEADERS
from apc_models_list import MODELS

def train(
    dataset_name: str = "dataset",
    from_checkpoint: str = "english",
    checkpoint_save_mode: str = "SAVE_FULL_MODEL",
    config: dict = {
        "num_epoch": 1,
        "model": "FAST_LSA_T_V2"
    }
):
    response = requests.post(
        f"{BASE_URL}/train",
        headers=HEADERS,
        json={
            "dataset_name": dataset_name,
            "from_checkpoint": from_checkpoint,
            "checkpoint_save_mode": checkpoint_save_mode,
            "config": config
        }
    )
    return response.json()

def get_datasets():
    response = requests.get(f"{BASE_URL}/dataset", headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch datasets")
        return {"datasets": []}


st.title("Train Model")

st.subheader("Available Datasets")
datasets = st.selectbox("Select Dataset", get_datasets()["datasets"])

st.subheader("Model Configuration")
num_epoch = st.number_input("Number of Epochs", min_value=1, value=1)
model = st.selectbox("Model", MODELS)
from_checkpoint = st.selectbox("From Checkpoint", ["english", "None"])

st.subheader("Run Training")
if st.button("Train"):
    st.success("Training started successfully")
    train(
        dataset_name=datasets,
        from_checkpoint=from_checkpoint,
        checkpoint_save_mode="SAVE_FULL_MODEL",
        config={
            "num_epoch": num_epoch,
            "model": model
        }
    )
