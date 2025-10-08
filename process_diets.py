import pandas as pd
from azure.storage.blob import BlobServiceClient
import io
import json
import os

def get_blob_service(connect_str):
    return BlobServiceClient.from_connection_string(connect_str)

def ensure_container(blob_service_client, container_name):
    try:
        blob_service_client.create_container(container_name)
    except Exception:
        pass  # container already exists
    return blob_service_client.get_container_client(container_name)

def upload_csv_if_missing(container_client, blob_name, local_path):
    blob_client = container_client.get_blob_client(blob_name)
    try:
        blob_client.get_blob_properties()
    except Exception:
        if not os.path.exists(local_path):
            raise FileNotFoundError(f"CSV file '{local_path}' not found")
        with open(local_path, "rb") as data:
            blob_client.upload_blob(data)
    return blob_client

def download_csv_to_df(blob_client):
    stream = blob_client.download_blob().readall()
    return pd.read_csv(io.BytesIO(stream))

def compute_avg_macros(df):
    return df.groupby('Diet_type')[['Protein(g)', 'Carbs(g)', 'Fat(g)']].mean()

def save_results_json(avg_macros, output_dir='simulated_nosql'):
    os.makedirs(output_dir, exist_ok=True)
    result = avg_macros.reset_index().to_dict(orient='records')
    with open(os.path.join(output_dir, 'results.json'), 'w') as f:
        json.dump(result, f, indent=4)
