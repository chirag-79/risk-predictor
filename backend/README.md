# CLPP Risk Prediction Backend API

FastAPI-based backend server for the CLPP Risk Prediction System. This module handles machine learning model training and serves prediction endpoints.

## 📋 Features

- **Logistic Regression Model**: Pre-trained on 2,400 participant dataset
- **REST API**: FastAPI with automatic OpenAPI documentation
- **Model Training**: Complete pipeline for training on Patient_data.csv
- **CORS Support**: Ready for frontend communication
- **Production Ready**: Error handling, validation, and health checks

## 🛠️ Setup & Installation

### 1. Create Virtual Environment (if not done)
```bash
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate  # Linux/Mac
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

Or manually:
```bash
pip install fastapi uvicorn scikit-learn pandas numpy python-multipart joblib pydantic python-dotenv
```

## 📊 Model Training

### Train the Model
Before running the API, train the model on your dataset:

```bash
python model.py
```

This will:
1. Load `Patient_data.csv` from the parent directory
2. Extract 7 clinical features:
   - Hamstring Tightness
   - Lumbar Lordosis
   - Hip Flexibility
   - Foot Posture
   - Psychological Stress
   - Physical Activity
   - Core Performance
3. Split data (80% train, 20% test)
4. Train Logistic Regression model
5. Evaluate on test set
6. Save model to `trained_model.pkl`
7. Save scaler to `scaler.pkl`

**Output:**
```
Loading data from ../Patient_data.csv...
Dataset shape: (2400, 22)
Training Logistic Regression Model...
Model training completed!

Evaluating Model on Test Set...
Accuracy:  0.8234
Precision: 0.7891
Recall:    0.8456
F1-Score:  0.8168
ROC-AUC:   0.8945

Model saved successfully!
```

## 🚀 Running the API

### Start the Development Server
```bash
python app.py
```

Or using uvicorn directly:
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

**Server will start at:** `http://localhost:8000`

### Access API Documentation
- **Interactive Docs (Swagger):** http://localhost:8000/docs
- **Alternative Docs (ReDoc):** http://localhost:8000/redoc

## 📡 API Endpoints

### 1. Health Check
```
GET /health
```
Check API and model status.

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "message": "API is ready. Model is loaded and ready for predictions."
}
```

---

### 2. Predict CLPP Risk
```
POST /predict
```
Main prediction endpoint for patient risk assessment.

**Request Body:**
```json
{
  "hamstring_tightness": 45,
  "lumbar_lordosis": 60,
  "hip_flexibility": 55,
  "foot_posture": 50,
  "psychological_stress": 7,
  "physical_activity": 400,
  "core_performance": 2
}
```

**Response:**
```json
{
  "risk_probability": 0.7823,
  "risk_percentage": 78.23,
  "risk_classification": "HIGH RISK",
  "recommendation": "Patient is at HIGH RISK for CLPP. Schedule consultation with clinician for detailed assessment and intervention planning."
}
```

---

### 3. Sample Prediction
```
GET /sample-prediction
```
Get a prediction with pre-filled test data (no request body needed).

**Response:** Same as POST /predict

---

### 4. Model Information
```
GET /info
```
Get details about the trained model.

**Response:**
```json
{
  "model_type": "Logistic Regression",
  "features": [
    "hamstring_tightness",
    "lumbar_lordosis",
    "hip_flexibility",
    "foot_posture",
    "psychological_stress",
    "physical_activity",
    "core_performance"
  ],
  "feature_count": 7,
  "output": {
    "risk_probability": "0.0-1.0",
    "risk_threshold": 0.5,
    "high_risk": "> 0.5",
    "low_risk": "<= 0.5"
  }
}
```

---

### 5. Root Endpoint
```
GET /
```
Get API overview and available endpoints.

---

## 📁 Project Structure

```
backend/
├── venv/                      # Python virtual environment
├── app.py                     # FastAPI application
├── model.py                   # Model training & inference
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables
├── trained_model.pkl          # Trained ML model (created after training)
├── scaler.pkl                 # Feature scaler (created after training)
├── README.md                  # This file
└── __pycache__/              # Python cache (ignored)
```

## 🔧 Configuration

Edit `.env` file to customize:

```ini
# Server
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True

# CORS
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# Logging
LOG_LEVEL=INFO
```

## 📊 Clinical Parameters

### Input Features (7 parameters):

| Parameter | Type | Range | Description |
|-----------|------|-------|-------------|
| Hamstring Tightness | Numeric | 0-100 | Hamstring muscle tightness test score |
| Lumbar Lordosis | Numeric | 0-100° | Spine lordosis angle measurement |
| Hip Flexibility | Numeric | 0-100 cm | Hip range of motion |
| Foot Posture | Numeric | 0-100 | Foot Posture Index score |
| Psychological Stress | Numeric | 0-10 | Perceived Stress Scale |
| Physical Activity | Numeric | 0-10000 MET min/week | IPAQ physical activity level |
| Core Performance | Numeric | 0-10 | Core strength and stability test |

### Output:

| Field | Type | Description |
|-------|------|-------------|
| risk_probability | Float (0.0-1.0) | Likelihood of CLPP |
| risk_percentage | Float (0-100) | Probability as percentage |
| risk_classification | String | "HIGH RISK" (>0.5) or "LOW RISK" (≤0.5) |
| recommendation | String | Clinical recommendation |

## 🧪 Testing

### Using Python Requests
```python
import requests

# Test with sample data
patient_data = {
    "hamstring_tightness": 45,
    "lumbar_lordosis": 60,
    "hip_flexibility": 55,
    "foot_posture": 50,
    "psychological_stress": 7,
    "physical_activity": 400,
    "core_performance": 2
}

response = requests.post("http://localhost:8000/predict", json=patient_data)
print(response.json())
```

### Using cURL
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "hamstring_tightness": 45,
    "lumbar_lordosis": 60,
    "hip_flexibility": 55,
    "foot_posture": 50,
    "psychological_stress": 7,
    "physical_activity": 400,
    "core_performance": 2
  }'
```

### Using Swagger UI
1. Open http://localhost:8000/docs
2. Click on `/predict` endpoint
3. Click "Try it out"
4. Enter sample data
5. Execute

## 📚 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| fastapi | 0.135.1 | Web framework |
| uvicorn | 0.41.0 | ASGI server |
| scikit-learn | 1.8.0 | Machine learning |
| pandas | 3.0.1 | Data processing |
| numpy | 2.4.3 | Numerical computing |
| pydantic | 2.12.5 | Data validation |
| python-dotenv | 1.2.2 | Environment variables |
| joblib | 1.5.3 | Model serialization |

## 🚨 Troubleshooting

### Model Not Found
```
Error: Pre-trained model not found. Please train the model first.
```
**Solution:** Run `python model.py`

### Port Already in Use
```
Error: Address already in use
```
**Solution:** Kill existing process or use different port:
```bash
uvicorn app:app --port 8001
```

### CORS Issues
```
Error: CORS policy blocked request
```
**Solution:** Update CORS_ORIGINS in `.env`

## 🔐 Security Notes

- **Development Only**: Currently CORS allows all origins (`allow_origins=["*"]`)
- **Production**: Specify allowed origins in `.env`
- **API Key**: For production, add API authentication
- **HTTPS**: Use HTTPS in production

## 📈 Model Details

- **Algorithm**: Logistic Regression
- **Training Data**: 2,400 Indian women
- **Features**: 7 clinical parameters
- **Target**: CLPP (1 = High Risk, 0 = Low Risk)
- **Train-Test Split**: 80-20
- **Scaler**: StandardScaler (z-score normalization)

## 🎯 Next Steps

1. ✅ Train the model: `python model.py`
2. ✅ Start the API: `python app.py`
3. ➡️ Build React frontend (see ../frontend/README.md)
4. ➡️ Connect frontend to backend
5. ➡️ Deploy to Render/Vercel

## 📞 Support

For issues or questions:
1. Check `/docs` at http://localhost:8000/docs
2. Review model.py docstrings
3. Check error logs in terminal

## 📄 License
[Add your license]

---

**Status**: Ready for PHASE 2 Completion ✅  
**Backend**: Configured and Ready  
**Next**: PHASE 3 (Frontend Setup with React)
