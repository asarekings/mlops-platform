#!/usr/bin/env python3
# Real ML Model Training Script
# Author: asarekings
# Date: 2025-06-03 04:51:40 UTC

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from src.ml.real_models import RealMLModels
    
    def main():
        print("🤖 Real ML Model Training by asarekings")
        print("📅 2025-06-03 04:51:40 UTC")
        print("-" * 50)
        
        # Initialize and train models
        ml_models = RealMLModels()
        
        # Train all models
        print("Training fraud detection model...")
        fraud_info = ml_models.train_fraud_detection_model()
        
        print("Training price prediction model...")
        price_info = ml_models.train_price_prediction_model()
        
        print("Training customer segmentation model...")
        segment_info = ml_models.train_customer_segmentation_model()
        
        print("\n✅ All models trained successfully!")
        print("📁 Models saved in: models/")
        print("🚀 Start your API to use real ML models!")

    if __name__ == "__main__":
        main()
        
except ImportError as e:
    print(f"❌ Error: {e}")
    print("💡 Install required packages:")
    print("   pip install scikit-learn pandas matplotlib seaborn")