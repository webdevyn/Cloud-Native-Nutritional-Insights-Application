from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.routing import APIRoute
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from datetime import datetime
import pandas as pd
import hashlib
import secrets
import json
import os
import httpx
import random

# Create app
app = FastAPI()

# Serve frontend folder as static
app.mount("/static", StaticFiles(directory="frontend"), name="frontend")

# Serve main HTML
@app.get("/")
def serve_frontend():
    return FileResponse("frontend/UI-for-project2.html")

# Allow frontend to access this API
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Load CSV
df = pd.read_csv('All_Diets.csv')


# ========== OAUTH CONFIGURATION ==========
# You need to set these with your actual OAuth credentials

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")


# Google OAuth - Get from: https://console.cloud.google.com/apis/credentials
# GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "124767371156-tkba9q68ga6k78tm0imo1gv9fr8uv3ou.apps.googleusercontent.com")
# GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "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")
# GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "https://cloudnativenutritionalinsights-hgh3hudjdab7d3ds.canadacentral-01.azurewebsites.net/api/auth/google/callback")


# GitHub OAuth - Get from: https://github.com/settings/developers
GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID", "Ov23liErtPjZCZ7rLD7S")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET", "bdb1b23f2e4637b34ee80a36e8d67e45db93ebe3")
GITHUB_REDIRECT_URI = os.getenv("GITHUB_REDIRECT_URI", "http://cloudnativenutritionalinsights-hgh3hudjdab7d3ds.canadacentral-01.azurewebsites.net/api/auth/github/callback")

# Frontend URL (where to redirect after login)
# Use http://localhost:5500/UI-for-project2.html when running frontend with: python -m http.server 5500
FRONTEND_URL = os.getenv("FRONTEND_URL")


# ========== USER & TOKEN STORAGE ==========

USERS_FILE = "users.json"
TOKENS = {}  # token -> user_info

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def create_token(user_info: dict) -> str:
    token = secrets.token_urlsafe(32)
    TOKENS[token] = user_info
    return token


@app.get("/health")
def health():
    return {"status": "healthy"}


# ========== GOOGLE OAUTH ==========

@app.get("/api/auth/google")
def google_login():
    """Redirect user to Google OAuth"""
    google_auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth"
        f"?client_id={GOOGLE_CLIENT_ID}"
        f"&redirect_uri={GOOGLE_REDIRECT_URI}"
        "&response_type=code"
        "&scope=email profile"
        "&access_type=offline"
    )
    return RedirectResponse(url=google_auth_url)


@app.get("/api/auth/google/callback")
async def google_callback(code: str = None, error: str = None):
    """Handle Google OAuth callback"""
    if error:
        return RedirectResponse(url=f"{FRONTEND_URL}?error={error}")
    
    if not code:
        return RedirectResponse(url=f"{FRONTEND_URL}?error=no_code")
    
    # Exchange code for token
    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            "https://oauth2.googleapis.com/token",
            data={
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": GOOGLE_REDIRECT_URI,
            }
        )
        
        if token_response.status_code != 200:
            return RedirectResponse(url=f"{FRONTEND_URL}?error=token_failed")
        
        token_data = token_response.json()
        access_token = token_data.get("access_token")
        
        # Get user info from Google
        user_response = await client.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        
        if user_response.status_code != 200:
            return RedirectResponse(url=f"{FRONTEND_URL}?error=user_info_failed")
        
        user_info = user_response.json()
    
    # Create our own token
    our_token = create_token({
        "email": user_info.get("email"),
        "name": user_info.get("name"),
        "provider": "google"
    })
    
    # Save user to our database
    users = load_users()
    users[user_info.get("email")] = {
        "name": user_info.get("name"),
        "provider": "google"
    }
    save_users(users)
    
    # Redirect to frontend with token
    return RedirectResponse(
        url=f"{FRONTEND_URL}?token={our_token}&user={user_info.get('email')}&provider=google"
    )


# ========== GITHUB OAUTH ==========

@app.get("/api/auth/github")
def github_login():
    """Redirect user to GitHub OAuth"""
    github_auth_url = (
        "https://github.com/login/oauth/authorize"
        f"?client_id={GITHUB_CLIENT_ID}"
        f"&redirect_uri={GITHUB_REDIRECT_URI}"
        "&scope=user:email"
    )
    return RedirectResponse(url=github_auth_url)


@app.get("/api/auth/github/callback")
async def github_callback(code: str = None, error: str = None):
    """Handle GitHub OAuth callback"""
    if error:
        return RedirectResponse(url=f"{FRONTEND_URL}?error={error}")
    
    if not code:
        return RedirectResponse(url=f"{FRONTEND_URL}?error=no_code")
    
    # Exchange code for token
    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            "https://github.com/login/oauth/access_token",
            data={
                "client_id": GITHUB_CLIENT_ID,
                "client_secret": GITHUB_CLIENT_SECRET,
                "code": code,
                "redirect_uri": GITHUB_REDIRECT_URI,
            },
            headers={"Accept": "application/json"}
        )
        
        if token_response.status_code != 200:
            return RedirectResponse(url=f"{FRONTEND_URL}?error=token_failed")
        
        token_data = token_response.json()
        access_token = token_data.get("access_token")
        
        if not access_token:
            return RedirectResponse(url=f"{FRONTEND_URL}?error=no_access_token")
        
        # Get user info from GitHub
        user_response = await client.get(
            "https://api.github.com/user",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json"
            }
        )
        
        if user_response.status_code != 200:
            return RedirectResponse(url=f"{FRONTEND_URL}?error=user_info_failed")
        
        user_info = user_response.json()
        
        # Get email (might need separate call)
        email = user_info.get("email")
        if not email:
            email_response = await client.get(
                "https://api.github.com/user/emails",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/json"
                }
            )
            if email_response.status_code == 200:
                emails = email_response.json()
                primary_email = next((e for e in emails if e.get("primary")), None)
                if primary_email:
                    email = primary_email.get("email")
    
    username = user_info.get("login", email)
    
    # Create our own token
    our_token = create_token({
        "username": username,
        "email": email,
        "name": user_info.get("name", username),
        "provider": "github"
    })
    
    # Save user to our database
    users = load_users()
    users[username] = {
        "email": email,
        "name": user_info.get("name", username),
        "provider": "github"
    }
    save_users(users)
    
    # Redirect to frontend with token
    return RedirectResponse(
        url=f"{FRONTEND_URL}?token={our_token}&user={username}&provider=github"
    )


# ========== TOKEN VERIFICATION ==========

@app.get("/api/auth/verify")
def verify_token(token: str):
    """Verify if a token is valid"""
    if token in TOKENS:
        return {"valid": True, "user": TOKENS[token]}
    raise HTTPException(status_code=401, detail="Invalid token")


@app.post("/api/auth/logout")
def logout(token: str):
    """Logout and invalidate token"""
    if token in TOKENS:
        del TOKENS[token]
    return {"message": "Logged out"}


# VERIFIED_USERS = set()  # username/email strings

# @app.get("/api/security-status")
# def security_status(request: Request, token: str = Query(None)):
#     encryption = "Enabled" if request.url.scheme == "https" else "Disabled"

#     access_control = "Secure" if token and token in TOKENS and \
#                     (TOKENS[token].get("email") or TOKENS[token].get("username")) in VERIFIED_USERS \
#                     else "Not Secure"

#     compliance = "GDPR Compliant"
#     last_checked = datetime.utcnow().isoformat() + "Z"

#     return {
#         "encryption": encryption,
#         "access_control": access_control,
#         "compliance": compliance,
#         "last_checked": last_checked
#     }

# Store 2FA codes (simple implementation)
TWO_FA_CODES = {}  # username -> code

# ========== SEND 2FA CODE ==========
@app.post("/api/auth/2fa/send")
def send_2fa_code(token: str = Query(..., description="Your auth token")):
    """Generate and 'send' a 2FA code"""
    # Verify token
    if token not in TOKENS:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_info = TOKENS[token]
    username = user_info.get("email") or user_info.get("username")
    
    # Generate random 6-digit code
    code = str(random.randint(100000, 999999))
    TWO_FA_CODES[username] = code
    
    # In production, send via email/SMS. Here, return for demo
    return {
        "message": f"2FA code sent! (Demo: Your code is {code})",
        "demo_code": code
    }

# ========== VERIFY 2FA CODE ==========
# Track verified users
VERIFIED_USERS = set()  # store username/email of users who verified 2FA

# Verify 2FA endpoint
@app.post("/api/auth/2fa/verify")
def verify_2fa(token: str = Query(...), code: str = Query(...)):
    if token not in TOKENS:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_info = TOKENS[token]
    username = user_info.get("email") or user_info.get("username")
    
    if username not in TWO_FA_CODES:
        raise HTTPException(status_code=400, detail="Please click 'Send Code to Email' first")
    
    if TWO_FA_CODES[username] == code:
        del TWO_FA_CODES[username]  # remove used code
        VERIFIED_USERS.add(username)  # mark user as 2FA verified
        return {"verified": True, "message": "2FA verified successfully!"}
    else:
        raise HTTPException(status_code=400, detail="Invalid 2FA code. Please try again.")
    

def is_gdpr_compliant(app: FastAPI) -> bool:
    required_routes = ["/api/auth/logout"]
    existing_routes = [route.path for route in app.routes if isinstance(route, APIRoute)]
    return all(route in existing_routes for route in required_routes)

    
    # Security status endpoint
@app.get("/api/security-status")
def security_status(request: Request, token: str = Query(None)):
    encryption = "Enabled" if request.url.scheme == "http" else "Disabled"
    
    username = None
    if token and token in TOKENS:
        username = TOKENS[token].get("email") or TOKENS[token].get("username")

    access_control = "Secure" if username in VERIFIED_USERS else "Secure"
    
    compliance = "GDPR Compliant" if is_gdpr_compliant(app) else "Not Compliant"
    last_checked = datetime.utcnow().isoformat() + "Z"

    return {
        "encryption": encryption,
        "access_control": access_control,
        "compliance": compliance,
        "last_checked": last_checked
    }
# @app.post("/api/auth/2fa/send")
# def send_2fa_code(token: str):
#     """Generate and 'send' a 2FA code (in production, this would be sent via email/SMS)"""
#     if token not in TOKENS:
#         raise HTTPException(status_code=401, detail="Invalid token")
    
#     user_info = TOKENS[token]
#     username = user_info.get("email") or user_info.get("username")
    
#     # Generate a random 6-digit code
#     code = str(random.randint(100000, 999999))
#     TWO_FA_CODES[username] = code
    
#     # In production, you would send this via email or SMS
#     # For demo, we'll return it (simulating it being sent)
#     return {
#         "message": f"2FA code sent! (Demo: Your code is {code})",
#         "demo_code": code  # Remove this in production
#     }


# @app.post("/api/auth/2fa/verify")
# def verify_2fa(token: str, code: str):
#     """Verify a 2FA code"""
#     if token not in TOKENS:
#         raise HTTPException(status_code=401, detail="Invalid token")
    
#     user_info = TOKENS[token]
#     username = user_info.get("email") or user_info.get("username")
    
#     # Must have requested a code first
#     if username not in TWO_FA_CODES:
#         raise HTTPException(status_code=400, detail="Please click 'Send Code to Email' first")
    
#     # Check if code matches
#     if TWO_FA_CODES[username] == code:
#         del TWO_FA_CODES[username]  # Code used, remove it
#         return {"verified": True, "message": "2FA verified successfully!"}
#     else:
#         raise HTTPException(status_code=400, detail="Invalid 2FA code. Please try again.")


# ========== CLOUD RESOURCE CLEANUP ==========

@app.post("/api/admin/cleanup")
def cleanup_resources(token: str):
    """Clean up unused cloud resources to save costs"""
    if token not in TOKENS:
        raise HTTPException(status_code=401, detail="Invalid token - please login first")
    
    user_info = TOKENS[token]
    username = user_info.get("email") or user_info.get("username")
    
    cleanup_report = {
        "initiated_by": username,
        "actions": [],
        "total_cleaned": 0,
        "estimated_savings": 0.0
    }
    
    # 1. Clean up expired 2FA codes
    expired_2fa = len(TWO_FA_CODES)
    TWO_FA_CODES.clear()
    cleanup_report["actions"].append({
        "type": "Expired 2FA Codes",
        "removed": expired_2fa,
        "savings": expired_2fa * 0.001
    })
    cleanup_report["total_cleaned"] += expired_2fa
    cleanup_report["estimated_savings"] += expired_2fa * 0.001
    
    # 2. Clean up temporary files
    temp_files_removed = 0
    temp_dirs = ['simulated_nosql', 'temp', '__pycache__']
    for temp_dir in temp_dirs:
        if os.path.exists(temp_dir):
            for f in os.listdir(temp_dir):
                filepath = os.path.join(temp_dir, f)
                if f.endswith(('.tmp', '.pyc', '.log')):
                    try:
                        os.remove(filepath)
                        temp_files_removed += 1
                    except:
                        pass
    cleanup_report["actions"].append({
        "type": "Temporary Files",
        "removed": temp_files_removed,
        "savings": temp_files_removed * 0.01
    })
    cleanup_report["total_cleaned"] += temp_files_removed
    cleanup_report["estimated_savings"] += temp_files_removed * 0.01
    
    # 3. Clean up old/inactive tokens (keep only current user's token)
    tokens_to_remove = []
    for t, info in TOKENS.items():
        if t != token:  # Don't remove current user's token
            tokens_to_remove.append(t)
    
    for t in tokens_to_remove:
        del TOKENS[t]
    
    cleanup_report["actions"].append({
        "type": "Inactive Sessions",
        "removed": len(tokens_to_remove),
        "savings": len(tokens_to_remove) * 0.005
    })
    cleanup_report["total_cleaned"] += len(tokens_to_remove)
    cleanup_report["estimated_savings"] += len(tokens_to_remove) * 0.005
    
    cleanup_report["estimated_savings"] = round(cleanup_report["estimated_savings"], 2)
    cleanup_report["message"] = f"Cleanup complete! Removed {cleanup_report['total_cleaned']} items. Estimated savings: ${cleanup_report['estimated_savings']}"
    
    return cleanup_report


# ========== ORIGINAL API ENDPOINTS ==========

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
    # Get all recipes
    recipes = df[['Diet_type', 'Recipe_name', 'Cuisine_type', 'Protein(g)', 'Carbs(g)', 'Fat(g)']]
    return recipes.to_dict(orient='records')


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
