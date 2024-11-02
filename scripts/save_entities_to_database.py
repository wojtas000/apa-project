import pandas as pd
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = "http://localhost:8000/etl"

headers = {
    "api-key": os.getenv('API_KEY')
}

ENDPOINTS = {
    "ACTOR": f"{API_URL}/entity",
    "TOPIC": f"{API_URL}/topic",
    "EVALTYPEVAL": f"{API_URL}/sentiment"
}

SENTIMENT_MAPPING = {
    "positiv": "positive",
    "negativ": "negative",
    "neutral": "neutral",
    "ambivalent": "ambivalent"
}

ENTITY_TYPE_MAPPING = {
    "PERSONS": "person",
    "ORGS": "organization",
    "PRODUCTS": "product"
}

def insert_data(row):
    entity_type = row.get("ENTITYTYPE")
    endpoint = ENDPOINTS.get(entity_type)

    data = None
    if entity_type == "ACTOR":
        type = ENTITY_TYPE_MAPPING.get(row.get("TYPE"))
        data = {
            "apa_id": str(row.get("ID")),
            "name": row.get("NAME"),
            "type": type,
            "source": 'APA'
        }
    elif entity_type == "TOPIC":
        data = {
            "apa_id": str(row.get("ID")),
            "name": row.get("NAME"),
            "type": row.get("TYPE").lower(),
        }
    elif entity_type == "EVALTYPEVAL":
        if row.get("TYPE") == "3er Tonalität":
            type = "low"
        elif row.get("TYPE") == "4er Tonalität":
            type = "high"
        else:
            return {"error": f"TYPE '{row.get('TYPE')}' not supported"}
        data = {
            "apa_id": str(row.get("ID")),
            "name": SENTIMENT_MAPPING.get(row.get("NAME")),
            "type": type,
        }
    else:
        return {"error": f"Unknown ENTITYTYPE '{entity_type}'"}

    if endpoint and data:
        try:
            response = requests.post(endpoint, json=data, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to insert data: {e}"}
    else:
        return {"error": "Invalid data or endpoint"}

def process_csv(file_path):
    df = pd.read_csv(file_path, sep=';', encoding='iso-8859-1')

    results = []
    for _, row in df.iterrows():
        result = insert_data(row)

if __name__ == "__main__":
    csv_file_path = "./entities.csv"
    process_csv(csv_file_path)
