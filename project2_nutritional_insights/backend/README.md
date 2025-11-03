# Nutritional Insights API - Simple Beginner Version

## 🚀 Quick Start Guide

### Step 1: Install What You Need

Open PowerShell in the `backend` folder and run:

```powershell
pip install -r requirements.txt
```

This installs FastAPI and Pandas.

### Step 2: Run Your API

```powershell
python app.py
```

You should see:
```
✅ CSV file loaded!
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 3: Test It!

**Easy way - Use your browser:**

1. Go to: **http://localhost:8000**
   - You'll see: `{"message": "Welcome to Nutritional Insights API!"}`

2. Go to: **http://localhost:8000/docs**
   - This shows interactive documentation where you can test your API!

3. Go to: **http://localhost:8000/api/data**
   - You'll see the average protein/carbs/fat for each diet type!

## 📋 What Does This API Do?

| URL | What it returns |
|-----|----------------|
| `http://localhost:8000/` | Welcome message |
| `http://localhost:8000/api/data` | Average protein, carbs, fat per diet |
| `http://localhost:8000/api/recipes` | First 50 recipes from the CSV |
| `http://localhost:8000/api/diet-types` | List of all diet types (for filters) |

## 🎯 Next Steps

Once this works, we'll:
1. Add more endpoints (more features!)
2. Connect HTML page to display this data
3. Add charts and visualizations