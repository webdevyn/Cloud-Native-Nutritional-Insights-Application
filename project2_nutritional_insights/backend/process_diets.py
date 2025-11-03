from azure.storage.blob import BlobServiceClient
import pandas as pd
import io
import json
import os

# Azurite connection string
connect_str = (
    "DefaultEndpointsProtocol=http;"
    "AccountName=devstoreaccount1;"
    "AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;"
    "BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"
)

blob_service_client = BlobServiceClient.from_connection_string(connect_str)
container_name = 'diet-data'
blob_name = 'All_Diets.csv'

# Ensure container exists
try:
    blob_service_client.create_container(container_name)
    print(f"Container '{container_name}' created.")
except Exception as e:
    print("Container might already exist:", e)

container_client = blob_service_client.get_container_client(container_name)
blob_client = container_client.get_blob_client(blob_name)

# Upload CSV if it doesn't exist
try:
    blob_client.get_blob_properties()
    print(f"Blob '{blob_name}' already exists in container.")
except Exception:
    if not os.path.exists(blob_name):
        raise FileNotFoundError(f"CSV file '{blob_name}' not found in the current directory.")
    with open(blob_name, "rb") as data:
        blob_client.upload_blob(data)
    print(f"Uploaded '{blob_name}' to container '{container_name}'.")

# Download CSV content
stream = blob_client.download_blob().readall()
df = pd.read_csv(io.BytesIO(stream))

# Calculate averages
avg_macros = df.groupby('Diet_type')[['Protein(g)', 'Carbs(g)', 'Fat(g)']].mean()

# Save results as JSON
os.makedirs('simulated_nosql', exist_ok=True)
result = avg_macros.reset_index().to_dict(orient='records')
with open('simulated_nosql/results.json', 'w') as f:
    json.dump(result, f, indent=4)

print("Data processed and stored successfully.")

