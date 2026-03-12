# Quick Start Guide - Risk Predictor Project

## 🚀 Phase 1: Immediate Next Steps

### Step 1: Analyze Your Dataset
Open Jupyter Notebook and explore your Patient_data.csv:

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv('Patient_data.csv')

# Quick analysis
print(df.head())
print(df.info())
print(df.describe())
print(df.isnull().sum())

# Check if LPP Group exists (target variable)
print(df['LPP Group'].value_counts())
```

### Step 2: Create Project Folder Structure
Run these commands in PowerShell:

```powershell
# Navigate to your Risk Predictor folder
cd "C:\Users\Chirag\OneDrive\Desktop\Risk Predictor"

# Create folder structure
mkdir frontend, backend, data, models, notebooks

# Initialize git repository
git init

# Create Python virtual environment for backend
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1

# Create Node project for frontend (we'll do this next)
cd ../frontend
npm create vite@latest . -- --template react
```

### Step 3: Backend Setup Template
Create `backend/app.py`:

```python
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import numpy as np
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="CLPP Risk Prediction API",
    description="AI-Driven Risk Prediction System for Chronic Lumbopelvic Pain",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variable to store model (loaded once at startup)
model = None

# ==================== PYDANTIC MODELS ====================

class PatientInput(BaseModel):
    """Input model for patient data"""
    hamstring_tightness: float  # Range: 0-100
    lumbar_lordosis: float      # Range: 0-100
    hip_flexibility: float      # Range: 0-100
    foot_posture: float         # Range: 0-100
    psychological_stress: float # Range: 0-100
    physical_activity: float    # Range: 0-100
    core_performance: float     # Range: 0-100

    class Config:
        json_schema_extra = {
            "example": {
                "hamstring_tightness": 45.5,
                "lumbar_lordosis": 35.2,
                "hip_flexibility": 60.1,
                "foot_posture": 55.3,
                "psychological_stress": 70.2,
                "physical_activity": 40.5,
                "core_performance": 50.0
            }
        }


class PredictionResponse(BaseModel):
    """Output model for prediction results"""
    risk_score: float          # 0.0 to 1.0
    risk_level: str            # "HIGH RISK" or "LOW RISK"
    confidence: float          # Confidence percentage
    message: str               # User-friendly message
    recommendation: str        # Clinical recommendation


# ==================== ENDPOINTS ====================

@app.get("/")
def read_root():
    """Root endpoint"""
    return {
        "message": "CLPP Risk Prediction API",
        "version": "1.0.0",
        "documentation": "/docs"
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "model_loaded": model is not None}


@app.post("/predict", response_model=PredictionResponse)
def predict(patient: PatientInput):
    """
    Predict risk of CLPP based on patient parameters
    
    Returns:
        - risk_score: Probability (0.0-1.0)
        - risk_level: Classification (HIGH or LOW RISK)
        - confidence: Confidence level
        - message: Explanation
        - recommendation: Clinical recommendation
    """
    try:
        if model is None:
            raise HTTPException(status_code=500, detail="Model not loaded")
        
        # Prepare input data
        features = np.array([[
            patient.hamstring_tightness,
            patient.lumbar_lordosis,
            patient.hip_flexibility,
            patient.foot_posture,
            patient.psychological_stress,
            patient.physical_activity,
            patient.core_performance
        ]])
        
        # Get prediction probability
        risk_score = float(model.predict_proba(features)[0][1])
        
        # Determine risk level
        risk_level = "HIGH RISK" if risk_score > 0.5 else "LOW RISK"
        confidence = max(risk_score, 1 - risk_score) * 100
        
        # Generate message
        if risk_score > 0.5:
            message = f"Patient has {risk_score*100:.1f}% probability of CLPP"
            recommendation = "Recommend immediate clinical assessment and preventive intervention"
        else:
            message = f"Patient has low risk ({(1-risk_score)*100:.1f}% probability of not having CLPP)"
            recommendation = "Continue regular physical activity and stress management"
        
        return PredictionResponse(
            risk_score=risk_score,
            risk_level=risk_level,
            confidence=confidence,
            message=message,
            recommendation=recommendation
        )
    
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/batch-predict")
def batch_predict(patients: list[PatientInput]):
    """Predict for multiple patients at once"""
    results = []
    for patient in patients:
        result = predict(patient)
        results.append(result)
    return {"predictions": results, "count": len(results)}


@app.get("/model-info")
def get_model_info():
    """Get information about the loaded model"""
    return {
        "model_type": "Logistic Regression",
        "parameters": [
            "Hamstring Tightness",
            "Lumbar Lordosis",
            "Hip Flexibility",
            "Foot Posture",
            "Psychological Stress",
            "Physical Activity",
            "Core Performance"
        ],
        "risk_threshold": 0.5,
        "version": "1.0.0"
    }


# ==================== STARTUP ====================

@app.on_event("startup")
async def startup_event():
    """Load model on startup"""
    global model
    try:
        model = joblib.load("../models/trained_model.pkl")
        logger.info("Model loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load model: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

Create `backend/requirements.txt`:

```txt
fastapi==0.104.1
uvicorn==0.24.0
scikit-learn==1.3.2
joblib==1.3.2
pandas==2.1.3
numpy==1.26.2
python-multipart==0.0.6
python-dotenv==1.0.0
```

### Step 4: Frontend Setup Template
Create `frontend/src/components/PatientForm.jsx`:

```jsx
import React, { useState } from 'react';
import axios from 'axios';

const PatientForm = ({ onPrediction }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  const [data, setData] = useState({
    hamstring_tightness: 50,
    lumbar_lordosis: 50,
    hip_flexibility: 50,
    foot_posture: 50,
    psychological_stress: 50,
    physical_activity: 50,
    core_performance: 50,
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setData(prev => ({
      ...prev,
      [name]: parseFloat(value)
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await axios.post(
        `${import.meta.env.VITE_API_URL}/predict`,
        data
      );
      onPrediction(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to get prediction');
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setData({
      hamstring_tightness: 50,
      lumbar_lordosis: 50,
      hip_flexibility: 50,
      foot_posture: 50,
      psychological_stress: 50,
      physical_activity: 50,
      core_performance: 50,
    });
    setError(null);
  };

  return (
    <div className="bg-white p-8 rounded-lg shadow-lg max-w-md mx-auto">
      <h2 className="text-2xl font-bold mb-6 text-gray-800">Patient Assessment Form</h2>
      
      <form onSubmit={handleSubmit}>
        {/* Hamstring Tightness */}
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Hamstring Tightness: {data.hamstring_tightness.toFixed(1)}
          </label>
          <input
            type="range"
            name="hamstring_tightness"
            value={data.hamstring_tightness}
            onChange={handleChange}
            min="0"
            max="100"
            step="0.1"
            className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
          />
        </div>

        {/* Lumbar Lordosis */}
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Lumbar Lordosis: {data.lumbar_lordosis.toFixed(1)}
          </label>
          <input
            type="range"
            name="lumbar_lordosis"
            value={data.lumbar_lordosis}
            onChange={handleChange}
            min="0"
            max="100"
            step="0.1"
            className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
          />
        </div>

        {/* Hip Flexibility */}
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Hip Flexibility: {data.hip_flexibility.toFixed(1)}
          </label>
          <input
            type="range"
            name="hip_flexibility"
            value={data.hip_flexibility}
            onChange={handleChange}
            min="0"
            max="100"
            step="0.1"
            className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
          />
        </div>

        {/* Foot Posture */}
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Foot Posture: {data.foot_posture.toFixed(1)}
          </label>
          <input
            type="range"
            name="foot_posture"
            value={data.foot_posture}
            onChange={handleChange}
            min="0"
            max="100"
            step="0.1"
            className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
          />
        </div>

        {/* Psychological Stress */}
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Psychological Stress: {data.psychological_stress.toFixed(1)}
          </label>
          <input
            type="range"
            name="psychological_stress"
            value={data.psychological_stress}
            onChange={handleChange}
            min="0"
            max="100"
            step="0.1"
            className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
          />
        </div>

        {/* Physical Activity */}
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Physical Activity: {data.physical_activity.toFixed(1)}
          </label>
          <input
            type="range"
            name="physical_activity"
            value={data.physical_activity}
            onChange={handleChange}
            min="0"
            max="100"
            step="0.1"
            className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
          />
        </div>

        {/* Core Performance */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Core Performance: {data.core_performance.toFixed(1)}
          </label>
          <input
            type="range"
            name="core_performance"
            value={data.core_performance}
            onChange={handleChange}
            min="0"
            max="100"
            step="0.1"
            className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
          />
        </div>

        {error && (
          <div className="mb-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
            {error}
          </div>
        )}

        <div className="flex gap-2">
          <button
            type="submit"
            disabled={loading}
            className="flex-1 bg-blue-600 text-white font-semibold py-2 px-4 rounded hover:bg-blue-700 disabled:bg-gray-400"
          >
            {loading ? 'Analyzing...' : 'Get Risk Assessment'}
          </button>
          <button
            type="button"
            onClick={handleReset}
            className="flex-1 bg-gray-300 text-gray-700 font-semibold py-2 px-4 rounded hover:bg-gray-400"
          >
            Reset
          </button>
        </div>
      </form>
    </div>
  );
};

export default PatientForm;
```

Create `frontend/.env.example`:

```
VITE_API_URL=http://localhost:8000
```

### Step 5: Model Training Script
Create `backend/train_model.py`:

```python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, 
    f1_score, confusion_matrix, roc_auc_score, roc_curve
)
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
print("Loading data...")
df = pd.read_csv('../data/Patient_data.csv')

print(df.head())
print(f"\nDataset shape: {df.shape}")
print(f"\nMissing values:\n{df.isnull().sum()}")

# Define features and target
FEATURES = [
    'Hamstring Tightness',
    'Lumbar Lordosis',
    'Hip Flexibility',
    'Foot Posture',
    'Psychological Stress',
    'Physical Activity',
    'Core Performance'
]

# Check if column names match your CSV exactly
print(f"\nCSV Columns: {df.columns.tolist()}")

# Adjust column names if needed
X = df[FEATURES]
# Assuming LPP Group is your target (1=Case, 2=Control) -> convert to 0/1
y = (df['LPP Group'] == 1).astype(int)

print(f"\nFeature matrix shape: {X.shape}")
print(f"Target distribution:\n{y.value_counts()}")

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"\nTraining set size: {X_train.shape[0]}")
print(f"Test set size: {X_test.shape[0]}")

# Standardize features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train Logistic Regression
print("\nTraining Logistic Regression model...")
model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_train_scaled, y_train)

# Make predictions
y_pred_train = model.predict(X_train_scaled)
y_pred_test = model.predict(X_test_scaled)
y_pred_proba_test = model.predict_proba(X_test_scaled)

# Evaluate model
print("\n" + "="*50)
print("MODEL PERFORMANCE METRICS")
print("="*50)

print(f"\nTraining Accuracy: {accuracy_score(y_train, y_pred_train):.4f}")
print(f"Test Accuracy: {accuracy_score(y_test, y_pred_test):.4f}")
print(f"Test Precision: {precision_score(y_test, y_pred_test):.4f}")
print(f"Test Recall: {recall_score(y_test, y_pred_test):.4f}")
print(f"Test F1-Score: {f1_score(y_test, y_pred_test):.4f}")
print(f"Test ROC-AUC: {roc_auc_score(y_test, y_pred_proba_test[:, 1]):.4f}")

print(f"\nConfusion Matrix:\n{confusion_matrix(y_test, y_pred_test)}")

# Feature importance
print(f"\nFeature Coefficients:")
for feat, coef in zip(FEATURES, model.coef_[0]):
    print(f"  {feat}: {coef:.4f}")

# Save model and scaler
print("\nSaving model...")
joblib.dump(model, '../models/trained_model.pkl')
joblib.dump(scaler, '../models/scaler.pkl')
print("✓ Model saved to ../models/trained_model.pkl")
print("✓ Scaler saved to ../models/scaler.pkl")

print("\n✓ Model training complete!")
```

---

## 📝 Checklist for Week 1

- [ ] Analyze Patient_data.csv (check columns, target variable, data ranges)
- [ ] Create folder structure (frontend, backend, data, models, notebooks)
- [ ] Set up Python virtual environment
- [ ] Install backend dependencies
- [ ] Create `app.py` with API endpoints
- [ ] Create model training script
- [ ] Train logistic regression model on your data
- [ ] Verify model generates predictions (0.0-1.0 range)
- [ ] Test API locally with Postman/Insomnia
- [ ] Create basic React setup with Vite
- [ ] Create PatientForm component
- [ ] Test frontend-backend integration

---

## 🔍 Important Next Step

Before proceeding, **run the `train_model.py` script** to verify:
1. Your CSV columns match the feature names exactly
2. Your target variable (LPP Group) is properly formatted
3. Model achieves acceptable accuracy (>80% is good for medical applications)

If column names don't match, adjust the `FEATURES` list in `train_model.py`.

---

## 💡 Tips for Success

1. **Start small**: Get basic form submission working first
2. **Test locally**: Always test locally before deploying
3. **Use Postman**: Test all API endpoints in Postman before frontend
4. **Keep secrets safe**: Never commit `.env` files to Git
5. **Document as you go**: Update README.md with setup steps

---

Good luck! Start with Phase 1, and reach out if you get stuck! 🚀
