from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

# Create app
app = FastAPI()

# Allow frontend to access this API
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Load CSV
df = pd.read_csv('All_Diets.csv')


@app.get("/")
def home():
    return {"message": "API is working!"}


@app.get("/api/data")
def get_data():
    # Calculate averages by diet type
    result = df.groupby('Diet_type')[['Protein(g)', 'Carbs(g)', 'Fat(g)']].mean()
    return result.reset_index().to_dict(orient='records')


@app.get("/api/recipes")
def get_recipes():
    # Get first 50 recipes
    recipes = df.head(50)[['Diet_type', 'Recipe_name', 'Cuisine_type', 'Protein(g)', 'Carbs(g)', 'Fat(g)']]
    return recipes.to_dict(orient='records')


@app.get("/api/diet-types")
def get_diet_types():
    # Get unique diet types for the dropdown filter
    return df['Diet_type'].unique().tolist()


# Run the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

