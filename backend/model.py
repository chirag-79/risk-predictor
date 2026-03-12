"""
CLPP Risk Prediction Model Training Module
Trains a Logistic Regression model to predict Chronic Lumbopelvic Pain risk
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, 
    precision_score, 
    recall_score, 
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)
import joblib
import os
from pathlib import Path

# Define feature mapping from CSV columns to clinical parameters
FEATURE_MAPPING = {
    'hamstring_tightness': 'Hamstring muscle tightness test',
    'lumbar_lordosis': 'Spine lordosis test Lordosis ⁰',
    'hip_flexibility': 'Hip Flexibility cm',
    'foot_posture': 'Total FPI scores',
    'psychological_stress': 'PSS scores',
    'physical_activity': 'IPAQ TOTAL Met min VALUE',
    'core_performance': 'Motor control ASLR test'
}

# Features in the expected order for model input
FEATURE_NAMES = [
    'hamstring_tightness',
    'lumbar_lordosis',
    'hip_flexibility',
    'foot_posture',
    'psychological_stress',
    'physical_activity',
    'core_performance'
]


class CLPPModel:
    """Logistic Regression model for CLPP risk prediction"""
    
    def __init__(self, model_path='trained_model.pkl', scaler_path='scaler.pkl'):
        self.model_path = model_path
        self.scaler_path = scaler_path
        self.model = None
        self.scaler = None
        self.feature_names = FEATURE_NAMES
        
    def load_and_preprocess_data(self, csv_path):
        """Load CSV and preprocess data for model training"""
        print(f"Loading data from {csv_path}...")
        df = pd.read_csv(csv_path)
        
        # Display basic info
        print(f"\nDataset shape: {df.shape}")
        print(f"Columns: {df.columns.tolist()}")
        
        # Clean data - handle formatting issues in IPAQ column
        if 'IPAQ TOTAL Met min VALUE' in df.columns:
            df['IPAQ TOTAL Met min VALUE'] = df['IPAQ TOTAL Met min VALUE'].astype(str).str.replace(',', '').astype(float)
        
        # Extract features according to mapping
        X = df[[FEATURE_MAPPING[feat] for feat in FEATURE_NAMES]].copy()
        X.columns = FEATURE_NAMES
        
        # Target variable: LPP Group (1 = Case/High Risk, 2 = Control/Low Risk)
        # Convert to binary: 1 = High Risk (LPP Group = 1), 0 = Low Risk (LPP Group = 2)
        y = (df['LPP Group'] == 1).astype(int)
        
        print(f"\nFeatures shape: {X.shape}")
        print(f"Feature names: {X.columns.tolist()}")
        print(f"\nTarget distribution:")
        print(y.value_counts())
        print(f"High Risk (1): {(y == 1).sum()}")
        print(f"Low Risk (0): {(y == 0).sum()}")
        
        # Display sample features
        print(f"\nSample data:")
        print(X.head())
        
        return X, y
    
    def train(self, X_train, y_train):
        """Train the logistic regression model"""
        print("\nTraining Logistic Regression Model...")
        
        # Initialize and fit scaler
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        
        # Train logistic regression model
        self.model = LogisticRegression(
            random_state=42,
            max_iter=1000,
            solver='lbfgs',
            C=1.0
        )
        self.model.fit(X_train_scaled, y_train)
        
        print("Model training completed!")
        print(f"Model coefficients: {self.model.coef_[0]}")
        print(f"Model intercept: {self.model.intercept_[0]}")
        
        return self.model
    
    def evaluate(self, X_test, y_test):
        """Evaluate model on test set"""
        print("\nEvaluating Model on Test Set...")
        
        X_test_scaled = self.scaler.transform(X_test)
        y_pred = self.model.predict(X_test_scaled)
        y_pred_proba = self.model.predict_proba(X_test_scaled)[:, 1]
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        roc_auc = roc_auc_score(y_test, y_pred_proba)
        
        print(f"\nAccuracy:  {accuracy:.4f}")
        print(f"Precision: {precision:.4f}")
        print(f"Recall:    {recall:.4f}")
        print(f"F1-Score:  {f1:.4f}")
        print(f"ROC-AUC:   {roc_auc:.4f}")
        
        print("\nConfusion Matrix:")
        cm = confusion_matrix(y_test, y_pred)
        print(cm)
        
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred, 
                                  target_names=['Low Risk', 'High Risk']))
        
        return {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1': f1,
            'roc_auc': roc_auc,
            'confusion_matrix': cm
        }
    
    def save_model(self):
        """Save trained model and scaler"""
        print(f"\nSaving model to {self.model_path}...")
        joblib.dump(self.model, self.model_path)
        joblib.dump(self.scaler, self.scaler_path)
        print("Model saved successfully!")
    
    def load_model(self):
        """Load pre-trained model and scaler"""
        if os.path.exists(self.model_path) and os.path.exists(self.scaler_path):
            print(f"Loading model from {self.model_path}...")
            self.model = joblib.load(self.model_path)
            self.scaler = joblib.load(self.scaler_path)
            print("Model loaded successfully!")
            return True
        return False
    
    def predict(self, features_dict):
        """
        Make prediction for a single patient
        
        Args:
            features_dict: Dictionary with patient data
            {
                'hamstring_tightness': float (0-100),
                'lumbar_lordosis': float (0-100),
                'hip_flexibility': float (0-100),
                'foot_posture': float (0-100),
                'psychological_stress': float (0-10),
                'physical_activity': float (0-1000),
                'core_performance': float (0-1)
            }
        
        Returns:
            dict: {
                'risk_probability': float (0.0-1.0),
                'risk_classification': str ('HIGH RISK' or 'LOW RISK'),
                'recommendation': str
            }
        """
        # Extract features in order
        features_list = [features_dict.get(feat, 0) for feat in FEATURE_NAMES]
        features_array = np.array([features_list])
        
        # Scale features
        features_scaled = self.scaler.transform(features_array)
        
        # Get probability
        probability = self.model.predict_proba(features_scaled)[0, 1]
        
        # Classify
        classification = 'HIGH RISK' if probability > 0.5 else 'LOW RISK'
        
        # Recommendation
        if probability > 0.5:
            recommendation = "Patient is at HIGH RISK for CLPP. Schedule consultation with clinician for detailed assessment and intervention planning."
        else:
            recommendation = "Patient is at LOW RISK for CLPP. Continue monitoring and encourage preventive lifestyle modifications."
        
        return {
            'risk_probability': float(probability),
            'risk_percentage': float(probability * 100),
            'risk_classification': classification,
            'recommendation': recommendation
        }


def main():
    """Main training pipeline"""
    
    # Get the path to Patient_data.csv (one level up from backend)
    backend_dir = Path(__file__).parent
    project_root = backend_dir.parent
    csv_path = project_root / 'Patient_data.csv'
    
    # Initialize model
    model = CLPPModel()
    
    # Load and preprocess data
    X, y = model.load_and_preprocess_data(str(csv_path))
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"\nTrain set size: {X_train.shape[0]}")
    print(f"Test set size: {X_test.shape[0]}")
    
    # Train model
    model.train(X_train, y_train)
    
    # Evaluate model
    metrics = model.evaluate(X_test, y_test)
    
    # Save model
    model.save_model()
    
    # Test prediction
    print("\n" + "="*60)
    print("Testing prediction with sample data...")
    print("="*60)
    
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
    print(f"\nSample Patient Data: {sample_patient}")
    print(f"\nPrediction Result:")
    print(f"  Risk Probability: {result['risk_probability']:.4f} ({result['risk_percentage']:.2f}%)")
    print(f"  Classification: {result['risk_classification']}")
    print(f"  Recommendation: {result['recommendation']}")
    
    return model


if __name__ == "__main__":
    model = main()
