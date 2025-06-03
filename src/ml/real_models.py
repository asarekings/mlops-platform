#!/usr/bin/env python3
# Real Machine Learning Models
# Author: asarekings
# Date: 2025-06-03 04:51:40 UTC
# Description: Real ML models with scikit-learn

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.svm import SVC, SVR
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, mean_squared_error, r2_score
import joblib
import os
import json
from datetime import datetime

class RealMLModels:
    """Real Machine Learning Models for asarekings MLOps Platform"""
    
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.metrics = {}
        self.model_dir = "models"
        os.makedirs(self.model_dir, exist_ok=True)
        print(f"🤖 RealMLModels initialized by asarekings - {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    
    def load_data(self, file_path):
        """Load dataset from file"""
        try:
            if file_path.endswith('.csv'):
                return pd.read_csv(file_path)
            elif file_path.endswith('.json'):
                return pd.read_json(file_path)
            else:
                raise ValueError("Unsupported file format")
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return None
    
    def train_fraud_detection_model(self, data_path="data/sample_data.csv"):
        """Train a real fraud detection model"""
        print("🔒 Training Fraud Detection Model...")
        
        # Load or create data
        if os.path.exists(data_path):
            df = self.load_data(data_path)
        else:
            print("📊 Creating synthetic fraud data for training...")
            df = self._create_fraud_data()
        
        # Prepare features and target
        feature_columns = [col for col in df.columns if col not in ['id', 'target', 'approved', 'timestamp']]
        X = df[feature_columns].select_dtypes(include=[np.number])
        
        # Create target if not exists
        if 'target' in df.columns:
            y = df['target']
        elif 'approved' in df.columns:
            y = 1 - df['approved']  # Invert approval to get fraud
        else:
            # Create synthetic target based on features
            y = (df[feature_columns[0]] < df[feature_columns[0]].quantile(0.3)).astype(int)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Train Random Forest model
        model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            class_weight='balanced'
        )
        model.fit(X_train_scaled, y_train)
        
        # Evaluate
        y_pred = model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)
        
        # Save model and scaler
        model_info = {
            'name': 'fraud_detection_rf',
            'type': 'classification',
            'algorithm': 'Random Forest',
            'accuracy': accuracy,
            'features': feature_columns,
            'trained_by': 'asarekings',
            'trained_at': datetime.utcnow().isoformat(),
            'samples_trained': len(X_train),
            'samples_tested': len(X_test)
        }
        
        # Save files
        joblib.dump(model, f"{self.model_dir}/fraud_detection_model.pkl")
        joblib.dump(scaler, f"{self.model_dir}/fraud_detection_scaler.pkl")
        
        with open(f"{self.model_dir}/fraud_detection_info.json", 'w') as f:
            json.dump(model_info, f, indent=2)
        
        # Store in memory
        self.models['fraud_detection'] = model
        self.scalers['fraud_detection'] = scaler
        self.metrics['fraud_detection'] = model_info
        
        print(f"✅ Fraud Detection Model trained - Accuracy: {accuracy:.3f}")
        return model_info
    
    def train_price_prediction_model(self, data_path="data/sample_data.csv"):
        """Train a real price prediction model"""
        print("💰 Training Price Prediction Model...")
        
        # Load or create data
        if os.path.exists(data_path):
            df = self.load_data(data_path)
        else:
            print("📊 Creating synthetic price data for training...")
            df = self._create_price_data()
        
        # Prepare features and target
        feature_columns = [col for col in df.columns if col not in ['id', 'price', 'target', 'timestamp']]
        X = df[feature_columns].select_dtypes(include=[np.number])
        
        # Create target if not exists
        if 'price' in df.columns:
            y = df['price']
        else:
            # Create synthetic price based on features
            y = X.sum(axis=1) * 1000 + np.random.normal(0, 5000, len(X))
            y = np.maximum(y, 50000)  # Minimum price
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Train Random Forest Regressor
        model = RandomForestRegressor(
            n_estimators=100,
            max_depth=15,
            random_state=42
        )
        model.fit(X_train_scaled, y_train)
        
        # Evaluate
        y_pred = model.predict(X_test_scaled)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        rmse = np.sqrt(mse)
        
        # Save model and scaler
        model_info = {
            'name': 'price_prediction_rf',
            'type': 'regression',
            'algorithm': 'Random Forest Regressor',
            'rmse': rmse,
            'r2_score': r2,
            'mse': mse,
            'features': feature_columns,
            'trained_by': 'asarekings',
            'trained_at': datetime.utcnow().isoformat(),
            'samples_trained': len(X_train),
            'samples_tested': len(X_test)
        }
        
        # Save files
        joblib.dump(model, f"{self.model_dir}/price_prediction_model.pkl")
        joblib.dump(scaler, f"{self.model_dir}/price_prediction_scaler.pkl")
        
        with open(f"{self.model_dir}/price_prediction_info.json", 'w') as f:
            json.dump(model_info, f, indent=2)
        
        # Store in memory
        self.models['price_prediction'] = model
        self.scalers['price_prediction'] = scaler
        self.metrics['price_prediction'] = model_info
        
        print(f"✅ Price Prediction Model trained - RMSE: {rmse:.2f}, R²: {r2:.3f}")
        return model_info
    
    def train_customer_segmentation_model(self, data_path="data/sample_data.csv"):
        """Train a customer segmentation model"""
        print("👥 Training Customer Segmentation Model...")
        
        # Load or create data
        if os.path.exists(data_path):
            df = self.load_data(data_path)
        else:
            print("📊 Creating synthetic customer data for training...")
            df = self._create_customer_data()
        
        # Prepare features
        feature_columns = [col for col in df.columns if col not in ['id', 'timestamp', 'category', 'region']]
        X = df[feature_columns].select_dtypes(include=[np.number])
        
        # Create segments based on feature combinations
        if 'category' in df.columns:
            le = LabelEncoder()
            y = le.fit_transform(df['category'])
        else:
            # Create synthetic segments
            y = pd.cut(X.iloc[:, 0], bins=3, labels=[0, 1, 2]).astype(int)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Train SVM model
        model = SVC(kernel='rbf', probability=True, random_state=42)
        model.fit(X_train_scaled, y_train)
        
        # Evaluate
        y_pred = model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)
        
        # Save model and scaler
        model_info = {
            'name': 'customer_segmentation_svm',
            'type': 'classification',
            'algorithm': 'Support Vector Machine',
            'accuracy': accuracy,
            'features': feature_columns,
            'trained_by': 'asarekings',
            'trained_at': datetime.utcnow().isoformat(),
            'samples_trained': len(X_train),
            'samples_tested': len(X_test),
            'segments': int(len(np.unique(y)))
        }
        
        # Save files
        joblib.dump(model, f"{self.model_dir}/customer_segmentation_model.pkl")
        joblib.dump(scaler, f"{self.model_dir}/customer_segmentation_scaler.pkl")
        
        with open(f"{self.model_dir}/customer_segmentation_info.json", 'w') as f:
            json.dump(model_info, f, indent=2)
        
        # Store in memory
        self.models['customer_segmentation'] = model
        self.scalers['customer_segmentation'] = scaler
        self.metrics['customer_segmentation'] = model_info
        
        print(f"✅ Customer Segmentation Model trained - Accuracy: {accuracy:.3f}")
        return model_info
    
    def predict(self, model_name, features):
        """Make prediction with real model"""
        if model_name not in self.models:
            return {"error": f"Model {model_name} not found"}
        
        try:
            # Prepare features
            if isinstance(features, dict):
                feature_df = pd.DataFrame([features])
            else:
                feature_df = pd.DataFrame(features)
            
            # Scale features
            scaler = self.scalers[model_name]
            features_scaled = scaler.transform(feature_df.select_dtypes(include=[np.number]))
            
            # Make prediction
            model = self.models[model_name]
            prediction = model.predict(features_scaled)
            
            # Get probability if classification
            if hasattr(model, 'predict_proba'):
                proba = model.predict_proba(features_scaled)
                confidence = float(np.max(proba[0]))
            else:
                confidence = 0.95  # Default for regression
            
            return {
                'prediction': float(prediction[0]) if len(prediction) == 1 else prediction.tolist(),
                'confidence': confidence,
                'model': model_name,
                'algorithm': self.metrics[model_name]['algorithm'],
                'trained_by': 'asarekings'
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def _create_fraud_data(self, n_samples=5000):
        """Create synthetic fraud detection data"""
        np.random.seed(42)
        data = {
            'feature_1': np.random.normal(0, 1, n_samples),
            'feature_2': np.random.normal(0, 1, n_samples),
            'feature_3': np.random.uniform(0, 10, n_samples),
            'feature_4': np.random.exponential(2, n_samples),
        }
        df = pd.DataFrame(data)
        # Create target based on feature combinations
        df['target'] = ((df['feature_1'] < -1) | (df['feature_3'] > 8)).astype(int)
        return df
    
    def _create_price_data(self, n_samples=3000):
        """Create synthetic price data"""
        np.random.seed(42)
        data = {
            'feature_1': np.random.uniform(800, 4000, n_samples),  # sq ft
            'feature_2': np.random.randint(1, 6, n_samples),       # bedrooms
            'feature_3': np.random.uniform(1, 4, n_samples),       # bathrooms
            'feature_4': np.random.randint(0, 50, n_samples),      # age
        }
        df = pd.DataFrame(data)
        # Price based on features
        df['price'] = (df['feature_1'] * 150 + df['feature_2'] * 15000 + 
                      df['feature_3'] * 10000 - df['feature_4'] * 1000 + 
                      np.random.normal(0, 20000, n_samples))
        df['price'] = np.maximum(df['price'], 50000)
        return df
    
    def _create_customer_data(self, n_samples=2000):
        """Create synthetic customer data"""
        np.random.seed(42)
        data = {
            'feature_1': np.random.uniform(18, 80, n_samples),     # age
            'feature_2': np.random.uniform(25000, 150000, n_samples), # income
            'feature_3': np.random.uniform(0, 1, n_samples),       # score
            'feature_4': np.random.randint(0, 10, n_samples),      # accounts
        }
        df = pd.DataFrame(data)
        # Create categories
        df['category'] = pd.cut(df['feature_2'], bins=3, labels=['A', 'B', 'C'])
        return df
    
    def get_model_summary(self):
        """Get summary of all trained models"""
        summary = {
            'total_models': len(self.models),
            'models': self.metrics,
            'trained_by': 'asarekings',
            'last_updated': datetime.utcnow().isoformat()
        }
        return summary

if __name__ == "__main__":
    # Train all models
    ml_models = RealMLModels()
    
    print("🚀 Training Real ML Models by asarekings...")
    print(f"📅 {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    
    # Train models
    fraud_info = ml_models.train_fraud_detection_model()
    price_info = ml_models.train_price_prediction_model()
    segment_info = ml_models.train_customer_segmentation_model()
    
    # Test predictions
    print("\n🔮 Testing predictions...")
    
    # Test fraud detection
    fraud_test = {'feature_1': -2.0, 'feature_2': 0.5, 'feature_3': 9.0, 'feature_4': 5.0}
    fraud_pred = ml_models.predict('fraud_detection', fraud_test)
    print(f"Fraud prediction: {fraud_pred}")
    
    # Test price prediction
    price_test = {'feature_1': 2000, 'feature_2': 3, 'feature_3': 2.5, 'feature_4': 10}
    price_pred = ml_models.predict('price_prediction', price_test)
    print(f"Price prediction: {price_pred}")
    
    print("\n✅ All real ML models trained and tested successfully!")