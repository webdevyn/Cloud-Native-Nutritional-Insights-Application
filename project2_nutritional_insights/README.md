# Nutritional Insights Application - Project 2

A simple web application that processes and visualizes nutritional data from various diet types and cuisines.

## 📁 Project Structure

```
project2_nutritional_insights/
├── backend/              # API server (Python/FastAPI)
│   ├── app.py           # Main API application
│   ├── requirements.txt # Python dependencies
│   └── All_Diets.csv    # Dataset (7,808 recipes)
├── frontend/            # Web interface
│   └── UI-for-project2.html  # Main web page
└── README.md           # This file
```

## 🚀 How to Run the Application

### Step 1: Start the Backend API

Open PowerShell/Terminal and run:

```powershell
cd backend
pip install -r requirements.txt
python app.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Keep this running!**

### Step 2: Open the Frontend

1. Navigate to the `frontend` folder in File Explorer
2. Double-click `UI-for-project2.html`
3. It will open in your browser

### Step 3: Use the Application

**Charts load automatically when you open the page!**

Click the buttons to fetch data:
- **Get Nutritional Insights** - Shows average protein/carbs/fat by diet type
- **Get Recipes** - Shows first 50 recipes from the dataset
- **Get Diet Types** - Shows list of all available diet types

---

## 🛠️ Technology Stack

### Backend
- **Python 3.13**
- **FastAPI** - Modern web framework for building APIs
- **Uvicorn** - ASGI web server
- **Pandas** - Data processing and analysis

### Frontend
- **HTML5**
- **JavaScript (ES6+)** - Fetch API for data retrieval
- **Tailwind CSS** - Styling
- **Chart.js** - Data visualizations (bar charts, scatter plots)

---

## 📊 API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /` | Health check |
| `GET /api/data` | Average macronutrients by diet type |
| `GET /api/recipes` | List of recipes (first 50) |
| `GET /api/diet-types` | List of all diet types |
| `GET /api/top-protein` | Top 5 protein-rich recipes per diet type |
| `GET /api/recipe-counts` | Recipe count by diet type (for pie chart) |

**Interactive API Docs:** http://localhost:8000/docs

---

## 📝 Features

✅ RESTful API for nutritional data  
✅ Data fetched from backend and displayed in tables  
✅ Simple, beginner-friendly codebase  
✅ Responsive web design  

---

## 🔍 Dataset

**File:** `All_Diets.csv`  
**Size:** 7,808 recipes  
**Columns:** Diet_type, Recipe_name, Cuisine_type, Protein(g), Carbs(g), Fat(g)

---

## 📚 How It Works

1. **Backend API** (`app.py`) reads the CSV file using Pandas
2. **Processes data** (calculates averages, filters recipes, etc.)
3. **Serves data as JSON** via API endpoints
4. **Frontend** fetches data from the API using JavaScript
5. **Displays data** in HTML tables

---

## 🎯 Next Steps (Future Enhancements)

- [ ] Add charts and visualizations (Chart.js)
- [ ] Implement filtering and search functionality
- [ ] Add pagination for recipes
- [ ] Deploy to cloud (Azure)
- [ ] Set up CI/CD pipeline

---

## 📖 Project Context

This is **Project 2** for CPSY 301 - Cloud-Native Application Development.  
It builds upon Project 1 by creating a full-stack web application with:
- Backend data processing
- RESTful API design
- Frontend-backend integration

---

## ⚠️ Troubleshooting

**Problem: Can't access http://localhost:8000**
- Make sure the backend is running (`python app.py`)
- Check if port 8000 is already in use

**Problem: Buttons don't work**
- Open browser console (F12) to see errors
- Verify backend is running at http://localhost:8000

**Problem: CORS errors**
- CORS is already enabled in `app.py` - this shouldn't happen


