# Nutritional Insights API - Backend

A simple FastAPI backend that processes nutritional data from the All_Diets.csv dataset.

## 🚀 Quick Start

### 1. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 2. Run the API Server

```powershell
python app.py
```

You should see:
```
INFO:     Started server process [12345]
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Keep this running while using the frontend!**

---

## 📋 API Endpoints

| Endpoint | Method | Description | Example Response |
|----------|--------|-------------|------------------|
| `/` | GET | Health check | `{"message": "API is working!"}` |
| `/api/data` | GET | Average macros by diet type | Array of objects with diet stats |
| `/api/recipes` | GET | First 50 recipes | Array of recipe objects |
| `/api/diet-types` | GET | List of diet types | Array of strings |

---

## 🧪 Testing Your API

### Option 1: Browser
Open these URLs in your browser:
- http://localhost:8000/
- http://localhost:8000/api/data
- http://localhost:8000/api/recipes
- http://localhost:8000/api/diet-types

### Option 2: Interactive Docs (Recommended!)
- Go to: **http://localhost:8000/docs**
- Click on any endpoint
- Click "Try it out"
- Click "Execute"
- See the response!

### Option 3: PowerShell
```powershell
Invoke-RestMethod -Uri http://localhost:8000/api/data
```

---

## 📦 Dependencies

- **fastapi** - Web framework for building APIs
- **uvicorn** - ASGI web server
- **pandas** - Data processing
- **python-multipart** - Form data handling

---

## 🗂️ Files

- `app.py` - Main API application (45 lines)
- `All_Diets.csv` - Dataset (7,808 recipes)
- `requirements.txt` - Python dependencies
- `data_analysis.py` - (From Project 1, for reference)
- `process_diets.py` - (From Project 1, for reference)

---

## 🔍 How It Works

1. **Loads CSV** when the server starts
2. **Defines endpoints** using FastAPI decorators (`@app.get()`)
3. **Processes data** using Pandas (groupby, filtering, etc.)
4. **Returns JSON** automatically (FastAPI magic!)
5. **CORS enabled** so frontend can access it

---

## 🛑 Stopping the Server

Press `CTRL+C` in the terminal where it's running

Or find and kill the process:
```powershell
netstat -ano | findstr :8000
taskkill /F /PID <process_id>
```

---

## ⚠️ Troubleshooting

**Port 8000 already in use?**
```powershell
# Find what's using port 8000
netstat -ano | findstr :8000
# Kill that process
taskkill /F /PID <process_id>
```

**Module not found errors?**
```powershell
pip install -r requirements.txt
```

**CSV file not found?**
Make sure `All_Diets.csv` is in the same folder as `app.py`
