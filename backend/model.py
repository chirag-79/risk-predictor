"""
CLPP Risk Prediction Model Training Module
Trains a Logistic Regression model using the exact equation from research paper
to predict Chronic Lumbopelvic Pain risk
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

# Research Paper Coefficients from Logistic Regression Equation
# Logit(CLPP) = −10.62 + (Hamstring * 1.23) + (LI * 3.56) + (BKFT * 1.29) 
#             + (FPI * 2.80) + (PSS * 3.57) + (IPAQ * 3.58) + (DMC * 3.43)
RESEARCH_COEFFICIENTS = {
    'intercept': -10.62,
    'hamstring_tightness': 1.23,      # PKEA > 20°
    'lumbar_lordosis': 3.56,          # LI > 11.5 cm
    'hip_flexibility': 1.29,          # BKFT score > 15 cm
    'foot_posture': 2.80,             # FPI score ≥ 20
    'psychological_stress': 3.57,     # PSS − 10 score > 25
    'physical_activity': 3.58,        # IPAQ score < 475 MET/minute
    'core_performance': 3.43          # DMC score ≤ 5
}

# Clinical Thresholds from Research Paper
CLINICAL_THRESHOLDS = {
    'hamstring_tightness': 20.0,      # PKEA > 20°
    'lumbar_lordosis': 11.5,          # LI > 11.5 cm
    'hip_flexibility': 15.0,          # BKFT score > 15 cm
    'foot_posture': 20.0,             # FPI score ≥ 20
    'psychological_stress': 25.0,     # PSS − 10 score > 25
    'physical_activity': 475.0,       # IPAQ score < 475 MET/minute (INVERTED)
    'core_performance': 5.0           # DMC score ≤ 5 (INVERTED)
}


class CLPPModel:
    """Logistic Regression model for CLPP risk prediction using research paper equation"""
    
    def __init__(self, model_path='trained_model.pkl', scaler_path='scaler.pkl', threshold_path='threshold.pkl'):
        self.model_path = model_path
        self.scaler_path = scaler_path
        self.threshold_path = threshold_path
        self.model = None
        self.scaler = None
        self.threshold = 0.5  # Default threshold
        self.feature_names = FEATURE_NAMES
        self.coefficients = None
        self.intercept = None
        
    def convert_to_binary_features(self, continuous_features):
        """
        Convert continuous feature values to binary (0/1) based on clinical thresholds
        from the research paper
        
        Args:
            continuous_features: DataFrame or array of continuous values
        
        Returns:
            DataFrame: Binary features (0 or 1)
        """
        if isinstance(continuous_features, np.ndarray):
            continuous_features = pd.DataFrame(continuous_features, columns=FEATURE_NAMES)
        else:
            continuous_features = continuous_features.copy()
        
        binary_features = pd.DataFrame(index=continuous_features.index)
        
        # Apply clinical thresholds
        # Hamstring: PKEA > 20°
        binary_features['hamstring_tightness'] = (continuous_features['hamstring_tightness'] > CLINICAL_THRESHOLDS['hamstring_tightness']).astype(int)
        
        # Lumbar Lordosis: LI > 11.5 cm
        binary_features['lumbar_lordosis'] = (continuous_features['lumbar_lordosis'] > CLINICAL_THRESHOLDS['lumbar_lordosis']).astype(int)
        
        # Hip Flexibility: BKFT > 15 cm
        binary_features['hip_flexibility'] = (continuous_features['hip_flexibility'] > CLINICAL_THRESHOLDS['hip_flexibility']).astype(int)
        
        # Foot Posture: FPI ≥ 20
        binary_features['foot_posture'] = (continuous_features['foot_posture'] >= CLINICAL_THRESHOLDS['foot_posture']).astype(int)
        
        # Psychological Stress: PSS > 25
        binary_features['psychological_stress'] = (continuous_features['psychological_stress'] > CLINICAL_THRESHOLDS['psychological_stress']).astype(int)
        
        # Physical Activity: IPAQ < 475 (INVERTED - lower activity = higher risk)
        binary_features['physical_activity'] = (continuous_features['physical_activity'] < CLINICAL_THRESHOLDS['physical_activity']).astype(int)
        
        # Core Performance: DMC ≤ 5 (INVERTED - lower score = higher risk)
        binary_features['core_performance'] = (continuous_features['core_performance'] <= CLINICAL_THRESHOLDS['core_performance']).astype(int)
        
        return binary_features
        
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
        
        # Extract continuous features according to mapping
        X = df[[FEATURE_MAPPING[feat] for feat in FEATURE_NAMES]].copy()
        X.columns = FEATURE_NAMES
        
        # Target variable: LPP Group (1 = Case/High Risk, 2 = Control/Low Risk)
        # Convert to binary: 1 = High Risk (LPP Group = 1), 0 = Low Risk (LPP Group = 2)
        y = (df['LPP Group'] == 1).astype(int)
        
        print(f"\nContinuous Features shape: {X.shape}")
        print(f"Feature names: {X.columns.tolist()}")
        print(f"\nTarget distribution:")
        print(y.value_counts())
        print(f"High Risk (1): {(y == 1).sum()}")
        print(f"Low Risk (0): {(y == 0).sum()}")
        
        # Display sample continuous features
        print(f"\nSample continuous data:")
        print(X.head())
        
        # Convert to binary features based on clinical thresholds
        print(f"\n{'='*70}")
        print("CONVERTING TO BINARY FEATURES (Using Clinical Thresholds):")
        print(f"{'='*70}")
        X_binary = self.convert_to_binary_features(X)
        
        print(f"\nBinary Features shape: {X_binary.shape}")
        print(f"\nSample binary data (0 or 1):")
        print(X_binary.head())
        
        print(f"\nBinary feature distribution:")
        for col in X_binary.columns:
            ones = (X_binary[col] == 1).sum()
            zeros = (X_binary[col] == 0).sum()
            print(f"  {col}: {ones} HIGH, {zeros} LOW")
        
        return X, X_binary, y
    
    def train(self, X_continuous, X_binary, y_train):
        """Train the logistic regression model on binary features"""
        print("\n" + "="*70)
        print("TRAINING LOGISTIC REGRESSION MODEL")
        print("="*70)
        print("\nUsing Research Paper Coefficients as reference:")
        for feat in FEATURE_NAMES:
            coeff = RESEARCH_COEFFICIENTS[feat]
            print(f"  {feat}: {coeff}")
        print(f"  Intercept: {RESEARCH_COEFFICIENTS['intercept']}")
        
        # Train logistic regression model on binary features
        self.model = LogisticRegression(
            random_state=42,
            max_iter=1000,
            solver='lbfgs',
            C=1.0
        )
        
        self.model.fit(X_binary, y_train)
        
        # Store coefficients and intercept
        self.coefficients = dict(zip(FEATURE_NAMES, self.model.coef_[0]))
        self.intercept = self.model.intercept_[0]
        
        print("\nModel training completed!")
        print(f"\nLearned Model Coefficients:")
        for feat in FEATURE_NAMES:
            coeff = self.coefficients[feat]
            research_coeff = RESEARCH_COEFFICIENTS[feat]
            print(f"  {feat}: {coeff:.4f} (Research: {research_coeff})")
        print(f"  Intercept: {self.intercept:.4f} (Research: {RESEARCH_COEFFICIENTS['intercept']})")
        
        return self.model
    
    def evaluate(self, X_test_binary, y_test):
        """Evaluate model on test set and find optimal threshold"""
        print("\n" + "="*70)
        print("EVALUATING MODEL ON TEST SET")
        print("="*70)
        
        y_pred_proba = self.model.predict_proba(X_test_binary)[:, 1]
        
        # Find optimal threshold using Youden's Index (Sensitivity + Specificity - 1)
        thresholds = np.arange(0.1, 1.0, 0.01)
        best_threshold = 0.5
        best_youden = 0
        
        print("\nCalculating optimal threshold...")
        for thresh in thresholds:
            y_pred_thresh = (y_pred_proba >= thresh).astype(int)
            
            # Calculate sensitivity (recall) and specificity
            tn = ((y_test == 0) & (y_pred_thresh == 0)).sum()
            fp = ((y_test == 0) & (y_pred_thresh == 1)).sum()
            fn = ((y_test == 1) & (y_pred_thresh == 0)).sum()
            tp = ((y_test == 1) & (y_pred_thresh == 1)).sum()
            
            sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 0
            specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
            youden = sensitivity + specificity - 1
            
            if youden > best_youden:
                best_youden = youden
                best_threshold = thresh
        
        self.threshold = best_threshold
        print(f"\n✅ Optimal Threshold: {best_threshold:.4f} (Youden's Index: {best_youden:.4f})")
        
        # Evaluate with optimal threshold
        y_pred = (y_pred_proba >= self.threshold).astype(int)
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, zero_division=0)
        recall = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        roc_auc = roc_auc_score(y_test, y_pred_proba)
        
        print(f"\n{'='*70}")
        print("MODEL PERFORMANCE METRICS")
        print(f"{'='*70}")
        print(f"Accuracy:  {accuracy:.4f} ({accuracy*100:.2f}%)")
        print(f"Precision: {precision:.4f}")
        print(f"Recall:    {recall:.4f}")
        print(f"F1-Score:  {f1:.4f}")
        print(f"ROC-AUC:   {roc_auc:.4f}")
        
        print("\nConfusion Matrix:")
        cm = confusion_matrix(y_test, y_pred)
        print(f"  True Negatives:  {cm[0, 0]}")
        print(f"  False Positives: {cm[0, 1]}")
        print(f"  False Negatives: {cm[1, 0]}")
        print(f"  True Positives:  {cm[1, 1]}")
        
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred, 
                                  target_names=['Low Risk', 'High Risk'],
                                  zero_division=0))
        
        return {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1': f1,
            'roc_auc': roc_auc,
            'confusion_matrix': cm,
            'threshold': self.threshold
        }
    
    def save_model(self):
        """Save trained model and threshold"""
        print(f"\n{'='*70}")
        print("SAVING MODEL")
        print(f"{'='*70}")
        print(f"Saving model to {self.model_path}...")
        joblib.dump(self.model, self.model_path)
        joblib.dump(self.threshold, self.threshold_path)
        print(f"✅ Model saved successfully!")
        print(f"✅ Threshold saved: {self.threshold:.4f}")
    
    def load_model(self):
        """Load pre-trained model and threshold"""
        if (os.path.exists(self.model_path) and 
            os.path.exists(self.threshold_path)):
            print(f"Loading model from {self.model_path}...")
            self.model = joblib.load(self.model_path)
            self.threshold = joblib.load(self.threshold_path)
            print(f"✅ Model loaded successfully!")
            print(f"✅ Using threshold: {self.threshold:.4f}")
            return True
        return False
    
    def predict(self, features_dict):
        """
        Make prediction for a single patient using the trained model
        
        Args:
            features_dict: Dictionary with patient continuous data
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
                'risk_percentage': float (0-100),
                'risk_classification': str ('HIGH RISK' or 'LOW RISK'),
                'threshold': float,
                'recommendation': str,
                'binary_features': dict (the binary features used)
            }
        """
        # Extract features in order
        features_list = [features_dict.get(feat, 0) for feat in FEATURE_NAMES]
        features_array = np.array([features_list])
        
        # Convert to binary features based on clinical thresholds
        features_binary = self.convert_to_binary_features(features_array)
        
        # Get probability
        probability = self.model.predict_proba(features_binary)[0, 1]
        
        # Classify using optimized threshold
        classification = 'HIGH RISK' if probability >= self.threshold else 'LOW RISK'
        
        # Recommendation based on risk level
        if probability >= self.threshold:
            recommendation = f"Patient is at HIGH RISK ({probability*100:.1f}%) for CLPP. Schedule consultation with clinician for detailed assessment and intervention planning."
        else:
            recommendation = f"Patient is at LOW RISK ({probability*100:.1f}%) for CLPP. Continue monitoring and encourage preventive lifestyle modifications."
        
        # Get binary features for explanation
        binary_feat_dict = features_binary.iloc[0].to_dict()
        
        return {
            'risk_probability': float(probability),
            'risk_percentage': float(probability * 100),
            'risk_classification': classification,
            'threshold': float(self.threshold),
            'recommendation': recommendation,
            'binary_features': binary_feat_dict,
            'clinical_thresholds': CLINICAL_THRESHOLDS
        }


def main():
    """Main training pipeline using research paper equation"""
    
    print("\n" + "="*70)
    print("CLPP RISK PREDICTION MODEL TRAINING")
    print("Using Research Paper Logistic Regression Equation")
    print("="*70)
    
    # Get the path to Patient_data.csv (one level up from backend)
    backend_dir = Path(__file__).parent
    project_root = backend_dir.parent
    csv_path = project_root / 'Patient_data.csv'
    
    # Initialize model
    model = CLPPModel()
    
    # Load and preprocess data
    X_continuous, X_binary, y = model.load_and_preprocess_data(str(csv_path))
    
    # Split data
    X_train_cont, X_test_cont, X_train_binary, X_test_binary, y_train, y_test = train_test_split(
        X_continuous, X_binary, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"\nTrain set size: {X_train_binary.shape[0]}")
    print(f"Test set size: {X_test_binary.shape[0]}")
    
    # Train model
    model.train(X_train_cont, X_train_binary, y_train)
    
    # Evaluate model
    metrics = model.evaluate(X_test_binary, y_test)
    
    # Save model
    model.save_model()
    
    # Test prediction on sample data
    print(f"\n{'='*70}")
    print("TESTING PREDICTIONS ON SAMPLE DATA")
    print(f"{'='*70}")
    
    # Create a test sample
    test_sample = {
        'hamstring_tightness': 45,
        'lumbar_lordosis': 60,
        'hip_flexibility': 55,
        'foot_posture': 50,
        'psychological_stress': 7,
        'physical_activity': 400,
        'core_performance': 2
    }
    
    print(f"\nSample Patient Data (Continuous Values):")
    for feat, val in test_sample.items():
        threshold = CLINICAL_THRESHOLDS[feat]
        print(f"  {feat}: {val} (Threshold: {threshold})")
    
    result = model.predict(test_sample)
    
    print(f"\nBinary Features Generated:")
    for feat, binary_val in result['binary_features'].items():
        continuous_val = test_sample[feat]
        threshold = CLINICAL_THRESHOLDS[feat]
        print(f"  {feat}: {binary_val} (Value: {continuous_val}, Threshold: {threshold})")
    
    print(f"\n{'='*70}")
    print("PREDICTION RESULT")
    print(f"{'='*70}")
    print(f"  Risk Percentage: {result['risk_percentage']:.2f}%")
    print(f"  Risk Probability: {result['risk_probability']:.4f}")
    print(f"  Classification: {result['risk_classification']}")
    print(f"  Threshold: {result['threshold']:.4f}")
    print(f"\nRecommendation:")
    print(f"  {result['recommendation']}")
    
    print(f"\n{'='*70}")
    print("✅ MODEL TRAINING COMPLETE!")
    print("✅ Model is ready for predictions!")
    print(f"{'='*70}\n")
    
    return model


if __name__ == "__main__":
    model = main()
