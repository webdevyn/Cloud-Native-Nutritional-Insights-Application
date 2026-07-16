# Cloud-Native Nutritional Insights Application

A full-stack cloud-native web application that analyzes and visualizes nutritional data from various diet types and cuisines. Built with FastAPI (Python), React, and containerized with Docker for cloud deployment on Azure.

**[Live Application](https://cloudnativenutritionalinsights-hgh3hudjdab7d3ds.canadacentral-01.azurewebsites.net)**

## 🎯 Project Overview

This is a comprehensive nutritional insights platform that processes a dataset of 7,808+ recipes across multiple diet types and cuisines. The application provides real-time analysis, secure OAuth authentication, 2FA verification, and data visualization capabilities. It demonstrates modern cloud-native application development practices including microservices architecture, containerization, security, and cost optimization.

## 📦 Tech Stack

### Backend
- **Python 3.9** - Core language
- **FastAPI** - Modern, async web framework with automatic API documentation
- **Uvicorn** - ASGI server for production deployment
- **Pandas** - Data processing and analysis
- **Httpx** - Async HTTP client for OAuth flows
- **Python-dotenv** - Environment variable management

### Frontend
- **HTML5** - Semantic markup
- **JavaScript (ES6+)** - Fetch API for async data retrieval
- **Tailwind CSS** - Utility-first styling framework
- **Chart.js** - Interactive data visualizations (bar charts, scatter plots, pie charts)

### Infrastructure & Deployment
- **Docker** - Containerization for consistency and portability
- **Azure App Service** - Cloud hosting and auto-scaling
- **GitHub** - Version control and source management

### Security & Authentication
- **Google OAuth 2.0** - Social login integration
- **GitHub OAuth 2.0** - Developer authentication
- **Two-Factor Authentication (2FA)** - Enhanced security with 6-digit codes
- **JWT Tokens** - Secure session management
- **CORS** - Cross-origin request handling

## 📁 Project Structure

```
Cloud-Native-Nutritional-Insights-Application/
├── project2_nutritional_insights/        # Main application directory
│   ├── backend/                          # Python FastAPI backend
│   │   ├── app.py                        # Main FastAPI application with all endpoints
│   │   ├── data_analysis.py              # Data processing and analysis functions
│   │   ├── process_diets.py              # Diet data processing utilities
│   │   ├── process_diets_improved.py     # Enhanced diet processing with optimization
│   │   ├── All_Diets.csv                 # Dataset (7,808 recipes)
│   │   ├── users.json                    # User profile storage
│   │   ├── requirements.txt              # Python dependencies
│   │   └── README.md                     # Backend-specific documentation
│   ├── frontend/                         # Web interface
│   │   └── UI-for-project2.html          # Single-page HTML application
│   └── README.md                         # Project documentation
├── simulated_nosql/                      # NoSQL database simulation
│   └── results.json                      # Cached query results
├── tests/                                # Test suite
│   ├── test_data_analysis.py             # Data analysis unit tests
│   └── test_process_diets.py             # Diet processing unit tests
├── Dockerfile                            # Multi-stage production container image
├── venv/                                 # Python virtual environment
└── README.md                             # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Docker (for containerized deployment)
- Git
- .env file with OAuth credentials (see configuration section)

### Local Development

#### 1. Clone and Setup

```bash
git clone https://github.com/webdevyn/Cloud-Native-Nutritional-Insights-Application.git
cd Cloud-Native-Nutritional-Insights-Application
cd project2_nutritional_insights/backend
```

#### 2. Create Virtual Environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

#### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 4. Configure Environment Variables

Create a `.env` file in the backend directory:

```env
# Google OAuth
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REDIRECT_URI=http://localhost:8000/api/auth/google/callback

# GitHub OAuth
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret
GITHUB_REDIRECT_URI=http://localhost:8000/api/auth/github/callback

# Frontend URL
FRONTEND_URL=http://localhost:8000/
```

#### 5. Run the Backend

```bash
python app.py
```

The API will be available at `http://localhost:8000`

#### 6. Access the Frontend

Open your browser and navigate to: `http://localhost:8000/`

The frontend will load automatically with all visualizations populated from the backend API.

## 🐳 Docker Deployment

### Build Docker Image

```bash
docker build -t nutritional-insights:latest .
```

### Run Docker Container

```bash
docker run -p 8000:8000 \
  -e GOOGLE_CLIENT_ID=your_google_client_id \
  -e GOOGLE_CLIENT_SECRET=your_google_client_secret \
  -e GITHUB_CLIENT_ID=your_github_client_id \
  -e GITHUB_CLIENT_SECRET=your_github_client_secret \
  nutritional-insights:latest
```

### Multi-Stage Build

The Dockerfile uses a multi-stage build process:

1. **Build Stage** - Maven/pip installs dependencies and packages the application
2. **Runtime Stage** - Minimal Alpine image with only runtime dependencies

This reduces the final image size significantly and improves security.

## 🔐 Authentication & Security

### OAuth Integration

The application supports two OAuth providers:

#### Google OAuth
1. Users click "Login with Google"
2. Redirected to Google's authorization endpoint
3. Upon approval, redirected back with authorization code
4. Backend exchanges code for access token
5. Backend fetches user information from Google
6. Custom JWT token created and stored
7. User session managed with token

#### GitHub OAuth
1. Similar flow to Google
2. GitHub-specific endpoint handling
3. Email retrieval requires separate API call if not in primary user response
4. Token validation includes username and email

### Two-Factor Authentication (2FA)

```
POST /api/auth/2fa/send
- Generates random 6-digit code
- Stores in memory (demo) or sends via email/SMS (production)
- Returns code for demo purposes

POST /api/auth/2fa/verify
- Verifies 2FA code
- Marks user as verified
- Maintains VERIFIED_USERS set
```

### Token Management

- Tokens stored in memory dictionary: `TOKENS = {token_string: user_info}`
- Each token linked to user information (email, name, provider)
- Tokens invalidated on logout
- Clean up mechanism removes inactive sessions

## 📊 API Endpoints

### Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/auth/google` | Initiate Google OAuth flow |
| `GET` | `/api/auth/google/callback` | Google OAuth callback handler |
| `GET` | `/api/auth/github` | Initiate GitHub OAuth flow |
| `GET` | `/api/auth/github/callback` | GitHub OAuth callback handler |
| `GET` | `/api/auth/verify` | Verify if token is valid |
| `POST` | `/api/auth/logout` | Invalidate user session |
| `POST` | `/api/auth/2fa/send` | Generate and send 2FA code |
| `POST` | `/api/auth/2fa/verify` | Verify 2FA code |

### Data Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Serve frontend HTML |
| `GET` | `/health` | Health check endpoint |
| `GET` | `/api/data` | Average macronutrients by diet type |
| `GET` | `/api/recipes` | All recipes from dataset |
| `GET` | `/api/diet-types` | List of unique diet types |
| `GET` | `/api/top-protein` | Top 5 protein-rich recipes per diet type |
| `GET` | `/api/recipe-counts` | Recipe count by diet type (for pie chart) |
| `GET` | `/api/security-status` | Security and compliance status |

### Admin Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/admin/cleanup` | Clean up unused resources and optimize costs |

### Interactive API Documentation

FastAPI automatically generates interactive API documentation:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 📈 Data Analysis Features

### Available Analyses

1. **Average Macronutrients by Diet Type**
   - Protein, carbohydrates, and fat averages
   - Visualized with bar charts

2. **Top Protein-Rich Recipes**
   - Top 5 recipes per diet type sorted by protein content
   - Scatter plot showing protein vs. carbs relationship

3. **Recipe Distribution**
   - Count of recipes per diet type
   - Pie chart visualization

4. **Nutritional Ratios**
   - Protein-to-Carbs ratio
   - Carbs-to-Fat ratio
   - Custom calculations for dietary analysis

5. **Most Common Cuisines**
   - Cuisine frequency by diet type
   - Trend analysis

### Dataset Details

- **File**: `All_Diets.csv`
- **Total Recipes**: 7,808+
- **Columns**:
  - `Diet_type` - Type of diet (Keto, Vegan, Paleo, etc.)
  - `Recipe_name` - Name of the recipe
  - `Cuisine_type` - Cuisine category
  - `Protein(g)` - Protein content in grams
  - `Carbs(g)` - Carbohydrate content in grams
  - `Fat(g)` - Fat content in grams

### Data Processing Pipeline

1. **Load** - CSV loaded into Pandas DataFrame
2. **Clean** - Missing values filled with mean (numeric columns only)
3. **Process** - Calculations performed on grouped data
4. **Serve** - Results converted to JSON and sent via API
5. **Visualize** - Frontend receives JSON and renders charts

## 🧪 Testing

### Unit Tests

Run the test suite:

```bash
python -m pytest tests/ -v
```

### Test Coverage

#### test_data_analysis.py
- Tests for data loading and cleaning
- Macro nutrient average calculations
- Top protein recipe filtering
- Highest protein diet identification
- Most common cuisine detection
- Ratio column calculations

#### test_process_diets.py
- Diet type processing
- Cuisine filtering
- Data transformation functions

### Running Tests Individually

```bash
python -m pytest tests/test_data_analysis.py -v
python -m pytest tests/test_process_diets.py -v
```

## ☁️ Cloud Deployment

### Azure App Service Deployment

#### Prerequisites
- Azure subscription
- Azure CLI installed
- Docker registry (Docker Hub or Azure Container Registry)

#### Steps

1. **Build and Push Docker Image**
```bash
docker build -t yourregistry.azurecr.io/nutritional-insights:latest .
docker push yourregistry.azurecr.io/nutritional-insights:latest
```

2. **Create App Service**
```bash
az appservice plan create \
  --name nutritional-insights-plan \
  --resource-group your-resource-group \
  --sku B1 --is-linux

az webapp create \
  --resource-group your-resource-group \
  --plan nutritional-insights-plan \
  --name nutritional-insights-app \
  --deployment-container-image-name yourregistry.azurecr.io/nutritional-insights:latest
```

3. **Configure Environment Variables**
```bash
az webapp config appsettings set \
  --resource-group your-resource-group \
  --name nutritional-insights-app \
  --settings GOOGLE_CLIENT_ID="..." GITHUB_CLIENT_ID="..." ...
```

4. **Access Application**
```
https://nutritional-insights-app.azurewebsites.net
```

## 💰 Cost Optimization

### Cloud Resource Cleanup

The application includes an automated cleanup endpoint to optimize cloud costs:

```
POST /api/admin/cleanup?token={auth_token}
```

**Cleanup Actions:**
1. **Expired 2FA Codes** - Remove unused 2FA tokens
2. **Temporary Files** - Delete .tmp, .pyc, .log files
3. **Inactive Sessions** - Remove old authentication tokens
4. **Estimated Savings** - Calculate potential cost reduction

**Example Response:**
```json
{
  "initiated_by": "user@example.com",
  "total_cleaned": 42,
  "estimated_savings": 0.15,
  "message": "Cleanup complete! Removed 42 items. Estimated savings: $0.15"
}
```

## 🔍 Features Implemented

✅ **Multi-provider OAuth Authentication** - Google and GitHub  
✅ **Two-Factor Authentication** - Enhanced security with 2FA codes  
✅ **RESTful API Design** - Consistent endpoints with proper HTTP methods  
✅ **Data Visualization** - Multiple chart types (bar, scatter, pie)  
✅ **CORS Support** - Frontend-backend communication across origins  
✅ **Responsive Design** - Works on desktop and mobile browsers  
✅ **Docker Containerization** - Multi-stage builds for production  
✅ **Cloud Deployment** - Azure App Service integration  
✅ **Unit Testing** - Comprehensive test coverage  
✅ **Cost Optimization** - Resource cleanup and monitoring  
✅ **Security Compliance** - GDPR compliance checks  
✅ **Interactive API Docs** - Swagger UI and ReDoc  

## 🎓 Learning Outcomes

This project demonstrates:

- **Cloud-Native Architecture** - Microservices, containerization, cloud deployment
- **Full-Stack Development** - Frontend and backend integration
- **Authentication & Security** - OAuth, 2FA, token management, CORS
- **Data Analysis** - Pandas data processing, statistical analysis
- **API Design** - RESTful principles, documentation, versioning
- **DevOps** - Docker, CI/CD pipeline setup, cloud deployment
- **Testing** - Unit tests, integration testing, test coverage
- **Performance Optimization** - Multi-stage builds, resource cleanup

## 🐛 Troubleshooting

### Port Already in Use

```bash
# Find process using port 8000
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill the process or use different port
python app.py --port 9000
```

### CORS Errors

The API has CORS enabled by default. If issues persist:
- Check browser console for specific error messages
- Verify frontend is making requests to correct backend URL
- Ensure OAuth redirect URIs match configuration

### OAuth Not Working

1. Verify OAuth credentials are correct in `.env`
2. Check redirect URIs match exactly (including protocol and port)
3. Test OAuth provider's API endpoints directly
4. Check browser console for detailed error messages

### Dataset Not Loading

```bash
# Verify CSV file exists
ls -la project2_nutritional_insights/backend/All_Diets.csv

# Check for missing or corrupted data
head project2_nutritional_insights/backend/All_Diets.csv
```

### Tests Failing

```bash
# Run with verbose output
python -m pytest tests/ -vv

# Run specific test
python -m pytest tests/test_data_analysis.py::TestDataAnalysis::test_compute_avg_macros -v
```

## 📚 Additional Resources

- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **Pandas Documentation**: https://pandas.pydata.org/docs/
- **Chart.js Documentation**: https://www.chartjs.org/docs/latest/
- **OAuth 2.0 Flow**: https://tools.ietf.org/html/rfc6749
- **Azure App Service**: https://docs.microsoft.com/en-us/azure/app-service/

## 🔄 CI/CD Integration

The project is set up for continuous integration and deployment:

- GitHub Actions workflows in `.github/workflows/`
- Automated testing on push and pull requests
- Automated Docker image building and pushing
- Deployment to Azure on main branch merge

## 📝 Configuration

### Environment Variables

```env
# OAuth Credentials (Required for Authentication)
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GOOGLE_REDIRECT_URI=

GITHUB_CLIENT_ID=
GITHUB_CLIENT_SECRET=
GITHUB_REDIRECT_URI=

# Frontend Configuration
FRONTEND_URL=http://localhost:8000/
```

### Port Configuration

Default port: **8000**

To change: Edit `app.py` line 531 or use environment variable

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the MIT License.

## 👤 Author

**Devyn Weir**
- GitHub: [@webdevyn](https://github.com/webdevyn)
- Portfolio: [webdevyn.github.io](https://webdevyn.github.io)

## 📞 Support

For issues, questions, or suggestions, please open a GitHub Issue or contact via the portfolio website.

---

**Last Updated**: July 16, 2026  
**Version**: 2.0  
**Status**: Production Ready ✅
