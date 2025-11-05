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
def get_recipes(limit: int = 50, offset: int = 0):
    # Get recipes but use pagination
    total = len(df)
    recipes = df.iloc[offset:offset+limit][['Diet_type', 'Recipe_name', 'Cuisine_type', 'Protein(g)', 'Carbs(g)', 'Fat(g)']]
    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "recipes": recipes.to_dict(orient='records')
    }


@app.get("/api/diet-types")
def get_diet_types():
    # Get unique diet types for the dropdown filter
    return df['Diet_type'].unique().tolist()


@app.get("/api/top-protein")
def get_top_protein():
    # Get top 5 protein-rich recipes for each diet type (for scatter plot)
    top_protein = df.sort_values('Protein(g)', ascending=False).groupby('Diet_type').head(5)
    return top_protein[['Diet_type', 'Recipe_name', 'Cuisine_type', 'Protein(g)', 'Carbs(g)', 'Fat(g)']].to_dict(orient='records')


@app.get("/api/recipe-counts")
def get_recipe_counts():
    # Count recipes per diet type for pie chart
    counts = df['Diet_type'].value_counts().to_dict()
    return counts


# Run the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

