"""
FastAPI Application for CLPP Risk Prediction
Provides REST API endpoints for patient risk assessment
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
import os
from pathlib import Path

# Import the model
from backend.model import CLPPModel, FEATURE_NAMES

# Initialize FastAPI app
app = FastAPI(
    title="CLPP Risk Prediction API",
    description="AI-Driven Risk Prediction System for Chronic Lumbopelvic Pain",
    version="1.0.0"
)

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize model at startup
model = None


# ============================================================================
# Pydantic Models (Request/Response schemas)
# ============================================================================

class PatientData(BaseModel):
    """Patient clinical parameters for prediction"""
    hamstring_tightness: float = Field(
        ..., 
        ge=0, 
        le=100,
        description="Hamstring Tightness (0-100)"
    )
    lumbar_lordosis: float = Field(
        ..., 
        ge=0, 
        le=100,
        description="Lumbar Lordosis angle (0-100°)"
    )
    hip_flexibility: float = Field(
        ..., 
        ge=0, 
        le=100,
        description="Hip Flexibility (0-100 cm)"
    )
    foot_posture: float = Field(
        ..., 
        ge=0, 
        le=100,
        description="Foot Posture Index (0-100)"
    )
    psychological_stress: float = Field(
        ..., 
        ge=0, 
        le=10,
        description="Psychological Stress Score (0-10)"
    )
    physical_activity: float = Field(
        ..., 
        ge=0, 
        le=10000,
        description="Physical Activity (0-10000 MET min/week)"
    )
    core_performance: float = Field(
        ..., 
        ge=0, 
        le=10,
        description="Core Performance Test Score (0-10)"
    )

    class Config:
        schema_extra = {
            "example": {
                "hamstring_tightness": 45,
                "lumbar_lordosis": 60,
                "hip_flexibility": 55,
                "foot_posture": 50,
                "psychological_stress": 7,
                "physical_activity": 400,
                "core_performance": 2
            }
        }


class PredictionResult(BaseModel):
    """Risk prediction result"""
    risk_probability: float = Field(
        description="Probability of CLPP (0.0-1.0)"
    )
    risk_percentage: float = Field(
        description="Risk percentage (0-100%)"
    )
    risk_classification: str = Field(
        description="Classification: 'HIGH RISK' or 'LOW RISK'"
    )
    recommendation: str = Field(
        description="Clinical recommendation based on risk level"
    )


class HealthStatus(BaseModel):
    """API health status"""
    status: str
    model_loaded: bool
    message: Optional[str] = None


class ErrorResponse(BaseModel):
    """Error response"""
    detail: str
    error_code: Optional[str] = None


# ============================================================================
# Startup/Shutdown Events
# ============================================================================

@app.on_event("startup")
def startup_event():
    """Load model on startup"""
    global model
    print("🚀 Starting CLPP Risk Prediction API...")
    
    try:
        # Get the backend directory
        backend_dir = Path(__file__).parent
        print(f"Backend directory: {backend_dir}")
        
        # Initialize model with explicit paths
        model_path = backend_dir / 'trained_model.pkl'
        scaler_path = backend_dir / 'scaler.pkl'
        
        print(f"Looking for model at: {model_path}")
        print(f"Looking for scaler at: {scaler_path}")
        print(f"Model exists: {model_path.exists()}")
        print(f"Scaler exists: {scaler_path.exists()}")
        
        model = CLPPModel(model_path=str(model_path), scaler_path=str(scaler_path))
        
        # Try to load existing model
        if model.load_model():
            print("✅ Model loaded successfully from disk")
        else:
            print("⚠️  Pre-trained model not found. Training model now...")
            csv_path = backend_dir.parent / 'Patient_data.csv'
            print(f"Training from: {csv_path}")
            if csv_path.exists():
                model.train(str(csv_path))
                print("✅ Model trained successfully")
            else:
                print(f"❌ CSV file not found at {csv_path}")
    except Exception as e:
        import traceback
        print(f"❌ Error during startup: {str(e)}")
        print(traceback.format_exc())


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("🛑 Shutting down CLPP Risk Prediction API...")


# ============================================================================
# API Endpoints
# ============================================================================

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information"""
    return {
        "name": "CLPP Risk Prediction API",
        "version": "1.0.0",
        "description": "AI-Driven Risk Prediction System for Chronic Lumbopelvic Pain",
        "endpoints": {
            "health": "/health",
            "predict": "/predict",
            "docs": "/docs"
        }
    }


@app.get("/health", response_model=HealthStatus, tags=["Health"])
async def health_check():
    """
    Health check endpoint
    
    Returns:
        HealthStatus: Current API and model status
    """
    if model is None or model.model is None:
        return HealthStatus(
            status="unhealthy",
            model_loaded=False,
            message="Model not loaded. Please train the model first."
        )
    
    return HealthStatus(
        status="healthy",
        model_loaded=True,
        message="API is ready. Model is loaded and ready for predictions."
    )


@app.post("/predict", response_model=PredictionResult, tags=["Prediction"])
async def predict(patient_data: PatientData):
    """
    Predict CLPP risk for a patient
    
    Takes patient clinical parameters and returns risk classification.
    
    Args:
        patient_data: Patient clinical measurements
    
    Returns:
        PredictionResult: Risk probability, classification, and recommendation
    
    Raises:
        HTTPException: If model is not loaded or prediction fails
    """
    
    if model is None or model.model is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Please train the model first by running: python model.py"
        )
    
    try:
        # Convert patient data to dictionary
        patient_dict = patient_data.dict()
        
        # Make prediction
        result = model.predict(patient_dict)
        
        # Return prediction result
        return PredictionResult(**result)
    
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid input data: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction error: {str(e)}"
        )


@app.get("/info", tags=["Information"])
async def get_model_info():
    """
    Get model information
    
    Returns:
        Information about the trained model
    """
    if model is None or model.model is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded"
        )
    
    return {
        "model_type": "Logistic Regression",
        "features": FEATURE_NAMES,
        "feature_count": len(FEATURE_NAMES),
        "feature_ranges": {
            "hamstring_tightness": "0-100",
            "lumbar_lordosis": "0-100°",
            "hip_flexibility": "0-100 cm",
            "foot_posture": "0-100",
            "psychological_stress": "0-10",
            "physical_activity": "0-10000 MET min/week",
            "core_performance": "0-10"
        },
        "output": {
            "risk_probability": "0.0-1.0",
            "risk_threshold": 0.5,
            "high_risk": "> 0.5",
            "low_risk": "<= 0.5"
        }
    }


@app.get("/sample-prediction", response_model=PredictionResult, tags=["Testing"])
async def sample_prediction():
    """
    Get a sample prediction with test data
    
    Useful for testing the API without sending real patient data
    """
    if model is None or model.model is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded"
        )
    
    # Sample patient data matching the example in PatientData
    sample_patient = {
        'hamstring_tightness': 45,
        'lumbar_lordosis': 60,
        'hip_flexibility': 55,
        'foot_posture': 50,
        'psychological_stress': 7,
        'physical_activity': 400,
        'core_performance': 2
    }
    
    result = model.predict(sample_patient)
    return PredictionResult(**result)


# ============================================================================
# Error Handlers
# ============================================================================

@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    """Handle validation errors"""
    return {
        "detail": str(exc),
        "error_code": "VALIDATION_ERROR"
    }


# ============================================================================
# For manual testing
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    print("Starting CLPP Risk Prediction API...")
    print("📍 API will be available at: http://localhost:8000")
    print("📖 API documentation at: http://localhost:8000/docs")
    
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
