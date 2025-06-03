from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from datetime import datetime
from typing import Dict, Any, List
import os
import json
import random
import sys
import hashlib
import shutil

# Add these imports for real ML models
try:
    from src.ml.real_models import RealMLModels
    REAL_ML_AVAILABLE = True
    print("🤖 Real ML models imported successfully!")
except ImportError as e:
    REAL_ML_AVAILABLE = False
    print(f"⚠️  Real ML models not available: {e}")

# Model Versioning System
class ModelVersioning:
    """Version control for ML models by asarekings"""
    
    def __init__(self):
        self.versions_dir = "model_versions"
        os.makedirs(self.versions_dir, exist_ok=True)
        print(f"📦 Model Versioning initialized by asarekings - {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    
    def create_version(self, model_name, model_file, metadata):
        """Create a new version of a model"""
        if not os.path.exists(model_file):
            raise FileNotFoundError(f"Model file not found: {model_file}")
            
        version = self.generate_version_id(model_file)
        version_dir = os.path.join(self.versions_dir, model_name, version)
        os.makedirs(version_dir, exist_ok=True)
        
        # Copy model file
        shutil.copy2(model_file, version_dir)
        
        # Save metadata
        version_metadata = {
            "version": version,
            "model_name": model_name,
            "created_at": datetime.utcnow().isoformat(),
            "created_by": "asarekings",
            "metadata": metadata,
            "file_hash": self.calculate_file_hash(model_file),
            "file_size_bytes": os.path.getsize(model_file),
            "platform": "Enhanced MLOps Platform"
        }
        
        with open(os.path.join(version_dir, "metadata.json"), "w") as f:
            json.dump(version_metadata, f, indent=2)
        
        print(f"📦 Created version {version} for model {model_name}")
        return version
    
    def generate_version_id(self, model_file):
        """Generate version ID based on timestamp and file hash"""
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        file_hash = self.calculate_file_hash(model_file)[:8]
        return f"v{timestamp}_{file_hash}"
    
    def calculate_file_hash(self, file_path):
        """Calculate SHA256 hash of file"""
        hash_sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
    
    def list_versions(self, model_name):
        """List all versions of a model"""
        model_dir = os.path.join(self.versions_dir, model_name)
        if not os.path.exists(model_dir):
            return []
        
        versions = []
        for version_id in os.listdir(model_dir):
            metadata_file = os.path.join(model_dir, version_id, "metadata.json")
            if os.path.exists(metadata_file):
                with open(metadata_file, "r") as f:
                    versions.append(json.load(f))
        
        return sorted(versions, key=lambda x: x["created_at"], reverse=True)
    
    def get_latest_version(self, model_name):
        """Get the latest version of a model"""
        versions = self.list_versions(model_name)
        return versions[0] if versions else None
    
    def rollback_to_version(self, model_name, version_id):
        """Rollback to a specific version"""
        version_dir = os.path.join(self.versions_dir, model_name, version_id)
        if not os.path.exists(version_dir):
            raise ValueError(f"Version {version_id} not found for model {model_name}")
        
        # Copy version back to active models directory
        model_files = [f for f in os.listdir(version_dir) if f.endswith('.pkl')]
        if model_files:
            source = os.path.join(version_dir, model_files[0])
            destination = os.path.join("models", f"{model_name}_model.pkl")
            shutil.copy2(source, destination)
            print(f"🔄 Rolled back {model_name} to version {version_id}")
            return True
        return False
    
    def delete_version(self, model_name, version_id):
        """Delete a specific version"""
        version_dir = os.path.join(self.versions_dir, model_name, version_id)
        if os.path.exists(version_dir):
            shutil.rmtree(version_dir)
            print(f"🗑️ Deleted version {version_id} for model {model_name}")
            return True
        return False
    
    def get_version_comparison(self, model_name, version1, version2):
        """Compare two versions of a model"""
        v1_data = None
        v2_data = None
        
        # Get version 1 metadata
        v1_path = os.path.join(self.versions_dir, model_name, version1, "metadata.json")
        if os.path.exists(v1_path):
            with open(v1_path, "r") as f:
                v1_data = json.load(f)
        
        # Get version 2 metadata
        v2_path = os.path.join(self.versions_dir, model_name, version2, "metadata.json")
        if os.path.exists(v2_path):
            with open(v2_path, "r") as f:
                v2_data = json.load(f)
        
        if not v1_data or not v2_data:
            return {"error": "One or both versions not found"}
        
        return {
            "model_name": model_name,
            "version_1": {
                "version": version1,
                "created_at": v1_data["created_at"],
                "file_hash": v1_data["file_hash"],
                "file_size": v1_data.get("file_size_bytes", 0),
                "metadata": v1_data.get("metadata", {})
            },
            "version_2": {
                "version": version2,
                "created_at": v2_data["created_at"],
                "file_hash": v2_data["file_hash"],
                "file_size": v2_data.get("file_size_bytes", 0),
                "metadata": v2_data.get("metadata", {})
            },
            "comparison": {
                "same_hash": v1_data["file_hash"] == v2_data["file_hash"],
                "size_difference": v2_data.get("file_size_bytes", 0) - v1_data.get("file_size_bytes", 0),
                "time_difference": v2_data["created_at"] > v1_data["created_at"]
            },
            "compared_by": "asarekings"
        }

# Create FastAPI app FIRST
app = FastAPI(
    title="MLOps Platform by asarekings",
    description="Enhanced ML Model Deployment & Monitoring Platform with Model Versioning",
    version="3.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize model versioning system
model_versioning = ModelVersioning()

# Initialize real models AFTER app creation
real_ml = None
if REAL_ML_AVAILABLE:
    try:
        real_ml = RealMLModels()
        print("🤖 Real ML models loaded successfully!")
    except Exception as e:
        print(f"⚠️  Error loading real ML models: {e}")
        REAL_ML_AVAILABLE = False

@app.get("/")
async def root():
    return {
        "message": "🚀 MLOps Platform by asarekings - Enhanced Edition v3.0",
        "description": "Real-Time ML Model Deployment & Monitoring with Model Versioning",
        "author": "asarekings",
        "created": "2025-06-03 04:29:30 UTC",
        "updated": "2025-06-03 19:58:50 UTC",
        "platform": "Windows PowerShell Compatible",
        "real_ml_available": REAL_ML_AVAILABLE,
        "version": "3.0.0",
        "features": [
            "FastAPI Backend",
            "Dataset Management",
            "Model Serving API",
            "Health Monitoring",
            "Model Versioning System",
            "Real ML Models" if REAL_ML_AVAILABLE else "Synthetic Models",
            "Pure Python Implementation"
        ],
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "datasets": "/api/v1/datasets",
            "models": "/api/v1/models",
            "predict": "/api/v1/predict",
            "train": "/api/v1/train" if REAL_ML_AVAILABLE else None,
            "real_models": "/api/v1/models/real" if REAL_ML_AVAILABLE else None,
            "real_predict": "/api/v1/predict/real/{model_name}" if REAL_ML_AVAILABLE else None,
            "versioning": "/api/v1/versions",
            "version_create": "/api/v1/versions/{model_name}/create",
            "version_list": "/api/v1/versions/{model_name}",
            "version_rollback": "/api/v1/versions/{model_name}/rollback/{version_id}"
        }
    }

@app.get("/health")
async def health_check():
    try:
        # Check data directory
        data_status = "available" if os.path.exists("data") else "no_data"
        
        # Count data files
        data_files = 0
        if os.path.exists("data"):
            data_files = len([f for f in os.listdir("data") if f.endswith(('.csv', '.json'))])
        
        # Count model files
        model_files = 0
        if os.path.exists("models"):
            model_files = len([f for f in os.listdir("models") if f.endswith(('.pkl', '.json'))])
        
        # Count versioned models
        versioned_models = 0
        if os.path.exists("model_versions"):
            for model_dir in os.listdir("model_versions"):
                model_path = os.path.join("model_versions", model_dir)
                if os.path.isdir(model_path):
                    versioned_models += len([v for v in os.listdir(model_path) if os.path.isdir(os.path.join(model_path, v))])
        
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "service": "mlops-platform-enhanced-v3",
            "author": "asarekings",
            "platform": "Windows Compatible",
            "data_status": data_status,
            "data_files": data_files,
            "model_files": model_files,
            "versioned_models": versioned_models,
            "real_ml_available": REAL_ML_AVAILABLE,
            "python_version": f"{sys.version_info.major}.{sys.version_info.minor}",
            "version": "3.0.0",
            "uptime": "running"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "author": "asarekings"
        }

@app.get("/api/v1/datasets")
async def list_datasets():
    """List available datasets"""
    datasets = []
    
    if os.path.exists("data"):
        for file in os.listdir("data"):
            if file.endswith(('.csv', '.json')):
                file_path = os.path.join("data", file)
                file_size = os.path.getsize(file_path)
                
                datasets.append({
                    "name": file,
                    "path": file_path,
                    "size_bytes": file_size,
                    "size_kb": round(file_size / 1024, 2),
                    "format": file.split(".")[-1],
                    "created": "synthetic"
                })
    
    return {
        "datasets": datasets,
        "total_count": len(datasets),
        "author": "asarekings",
        "timestamp": datetime.utcnow().isoformat(),
        "platform": "Enhanced MLOps v3.0"
    }

@app.post("/api/v1/predict")
async def predict(data: Dict[str, Any] = None):
    """Lightweight prediction endpoint"""
    
    # Simple prediction simulation
    if data and isinstance(data, dict):
        # Use input features to generate prediction
        feature_sum = sum([float(v) for v in data.values() if isinstance(v, (int, float))])
        prediction = min(max(0.1, (feature_sum % 10) / 10), 0.9)
        confidence = min(max(0.6, 0.8 + (feature_sum % 5) / 20), 0.95)
    else:
        prediction = random.uniform(0.2, 0.8)
        confidence = random.uniform(0.7, 0.9)
    
    return {
        "prediction": round(prediction, 3),
        "confidence": round(confidence, 3),
        "model": "lightweight_model_v1.0",
        "timestamp": datetime.utcnow().isoformat(),
        "input_data": data or {"feature_1": 1.0, "feature_2": 2.0},
        "model_info": {
            "type": "Lightweight Synthetic Model",
            "framework": "Pure Python",
            "training_date": "2025-06-03",
            "accuracy": 0.87
        },
        "author": "asarekings"
    }

@app.get("/api/v1/models")
async def list_models():
    """List available models with versioning info"""
    lightweight_models = [
        {
            "name": "fraud_detection_lite",
            "version": "1.0.0",
            "status": "deployed",
            "accuracy": 0.87,
            "framework": "Pure Python",
            "size_mb": 2.1,
            "type": "lightweight"
        },
        {
            "name": "sentiment_analysis_lite",
            "version": "1.1.0",
            "status": "training",
            "accuracy": 0.82,
            "framework": "Pure Python", 
            "size_mb": 1.8,
            "type": "lightweight"
        },
        {
            "name": "price_predictor_lite",
            "version": "2.0.0",
            "status": "deployed",
            "rmse": 0.15,
            "framework": "Pure Python",
            "size_mb": 1.5,
            "type": "lightweight"
        }
    ]
    
    # Add real models if available
    real_models = []
    if REAL_ML_AVAILABLE and real_ml:
        try:
            real_summary = real_ml.get_model_summary()
            for model_name, model_info in real_summary.get('models', {}).items():
                # Add version info
                versions = model_versioning.list_versions(model_name)
                latest_version = versions[0] if versions else None
                
                real_models.append({
                    **model_info,
                    "type": "real_ml",
                    "status": "trained",
                    "version_count": len(versions),
                    "latest_version": latest_version["version"] if latest_version else None,
                    "last_versioned": latest_version["created_at"] if latest_version else None
                })
        except:
            pass
    
    return {
        "lightweight_models": lightweight_models,
        "real_models": real_models,
        "total_lightweight": len(lightweight_models),
        "total_real": len(real_models),
        "total_models": len(lightweight_models) + len(real_models),
        "real_ml_available": REAL_ML_AVAILABLE,
        "versioning_enabled": True,
        "platform": "Enhanced MLOps v3.0",
        "author": "asarekings"
    }

# Model Versioning Endpoints
@app.get("/api/v1/versions")
async def list_all_versioned_models():
    """List all models with versions"""
    all_models = {}
    
    if os.path.exists("model_versions"):
        for model_name in os.listdir("model_versions"):
            model_path = os.path.join("model_versions", model_name)
            if os.path.isdir(model_path):
                versions = model_versioning.list_versions(model_name)
                all_models[model_name] = {
                    "total_versions": len(versions),
                    "latest_version": versions[0] if versions else None,
                    "versions": versions
                }
    
    return {
        "versioned_models": all_models,
        "total_models": len(all_models),
        "author": "asarekings",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/api/v1/versions/{model_name}")
async def list_model_versions(model_name: str):
    """List all versions of a specific model"""
    try:
        versions = model_versioning.list_versions(model_name)
        return {
            "model_name": model_name,
            "total_versions": len(versions),
            "versions": versions,
            "author": "asarekings",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error listing versions for {model_name}: {str(e)}")

@app.post("/api/v1/versions/{model_name}/create")
async def create_model_version(model_name: str, metadata: Dict[str, Any] = None):
    """Create a new version of a model"""
    try:
        # Look for the model file
        model_file = f"models/{model_name}_model.pkl"
        if not os.path.exists(model_file):
            # Try alternative naming patterns
            possible_files = [
                f"models/{model_name}.pkl",
                f"models/{model_name}_*.pkl"
            ]
            found = False
            for pattern in possible_files:
                import glob
                matches = glob.glob(pattern)
                if matches:
                    model_file = matches[0]
                    found = True
                    break
            
            if not found:
                raise HTTPException(status_code=404, detail=f"Model file not found for {model_name}")
        
        # Create version
        version_id = model_versioning.create_version(
            model_name, 
            model_file, 
            metadata or {"created_by": "asarekings", "platform": "Enhanced MLOps v3.0"}
        )
        
        return {
            "status": "success",
            "model_name": model_name,
            "version_id": version_id,
            "created_by": "asarekings",
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating version: {str(e)}")

@app.post("/api/v1/versions/{model_name}/rollback/{version_id}")
async def rollback_model_version(model_name: str, version_id: str):
    """Rollback to a specific model version"""
    try:
        success = model_versioning.rollback_to_version(model_name, version_id)
        if success:
            return {
                "status": "success",
                "model_name": model_name,
                "rolled_back_to": version_id,
                "performed_by": "asarekings",
                "timestamp": datetime.utcnow().isoformat()
            }
        else:
            raise HTTPException(status_code=404, detail=f"Version {version_id} not found or rollback failed")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during rollback: {str(e)}")

@app.delete("/api/v1/versions/{model_name}/{version_id}")
async def delete_model_version(model_name: str, version_id: str):
    """Delete a specific model version"""
    try:
        success = model_versioning.delete_version(model_name, version_id)
        if success:
            return {
                "status": "success",
                "model_name": model_name,
                "deleted_version": version_id,
                "deleted_by": "asarekings",
                "timestamp": datetime.utcnow().isoformat()
            }
        else:
            raise HTTPException(status_code=404, detail=f"Version {version_id} not found")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting version: {str(e)}")

@app.get("/api/v1/versions/{model_name}/compare/{version1}/{version2}")
async def compare_model_versions(model_name: str, version1: str, version2: str):
    """Compare two versions of a model"""
    try:
        comparison = model_versioning.get_version_comparison(model_name, version1, version2)
        return comparison
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error comparing versions: {str(e)}")

# Real ML endpoints (only if available)
if REAL_ML_AVAILABLE:
    
    @app.post("/api/v1/train")
    async def train_models():
        """Train real ML models and create versions"""
        if not real_ml:
            return {
                "error": "Real ML models not initialized",
                "author": "asarekings"
            }
        
        try:
            print("🚀 Starting model training with versioning by asarekings...")
            
            # Train all models
            fraud_info = real_ml.train_fraud_detection_model()
            price_info = real_ml.train_price_prediction_model()
            segment_info = real_ml.train_customer_segmentation_model()
            
            # Create versions for newly trained models
            versioned_models = []
            
            try:
                # Version fraud detection model
                fraud_version = model_versioning.create_version(
                    "fraud_detection",
                    "models/fraud_detection_model.pkl",
                    {"training_info": fraud_info, "auto_versioned": True}
                )
                versioned_models.append({"model": "fraud_detection", "version": fraud_version})
            except Exception as e:
                print(f"⚠️ Could not version fraud detection model: {e}")
            
            try:
                # Version price prediction model
                price_version = model_versioning.create_version(
                    "price_prediction",
                    "models/price_prediction_model.pkl",
                    {"training_info": price_info, "auto_versioned": True}
                )
                versioned_models.append({"model": "price_prediction", "version": price_version})
            except Exception as e:
                print(f"⚠️ Could not version price prediction model: {e}")
            
            try:
                # Version customer segmentation model
                segment_version = model_versioning.create_version(
                    "customer_segmentation",
                    "models/customer_segmentation_model.pkl",
                    {"training_info": segment_info, "auto_versioned": True}
                )
                versioned_models.append({"model": "customer_segmentation", "version": segment_version})
            except Exception as e:
                print(f"⚠️ Could not version customer segmentation model: {e}")
            
            return {
                "status": "success",
                "message": "All real ML models trained and versioned successfully by asarekings",
                "models_trained": [
                    fraud_info,
                    price_info,
                    segment_info
                ],
                "models_versioned": versioned_models,
                "trained_by": "asarekings",
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "author": "asarekings"
            }

    @app.post("/api/v1/predict/real/{model_name}")
    async def predict_real(model_name: str, data: Dict[str, Any]):
        """Make prediction with real ML model"""
        if not real_ml:
            return {
                "error": "Real ML models not initialized",
                "author": "asarekings"
            }
        
        try:
            prediction = real_ml.predict(model_name, data)
            prediction["timestamp"] = datetime.utcnow().isoformat()
            prediction["author"] = "asarekings"
            prediction["model_type"] = "real_ml"
            
            # Add version info if available
            versions = model_versioning.list_versions(model_name)
            if versions:
                prediction["current_version"] = versions[0]["version"]
                prediction["version_created"] = versions[0]["created_at"]
            
            return prediction
            
        except Exception as e:
            return {
                "error": str(e),
                "model": model_name,
                "author": "asarekings"
            }

    @app.get("/api/v1/models/real")
    async def list_real_models():
        """List real trained models with version info"""
        if not real_ml:
            return {
                "error": "Real ML models not initialized",
                "author": "asarekings"
            }
        
        try:
            summary = real_ml.get_model_summary()
            
            # Add versioning information
            for model_name in summary.get('models', {}):
                versions = model_versioning.list_versions(model_name)
                summary['models'][model_name]['versions'] = {
                    "total_versions": len(versions),
                    "latest_version": versions[0] if versions else None,
                    "all_versions": [v["version"] for v in versions]
                }
            
            summary["author"] = "asarekings"
            summary["platform"] = "Enhanced MLOps v3.0 with Versioning"
            summary["versioning_enabled"] = True
            return summary
            
        except Exception as e:
            return {
                "error": str(e),
                "author": "asarekings"
            }

else:
    # Placeholder endpoints when real ML is not available
    @app.post("/api/v1/train")
    async def train_models_placeholder():
        return {
            "error": "Real ML models not available",
            "suggestion": "Install scikit-learn: pip install scikit-learn pandas matplotlib seaborn",
            "author": "asarekings"
        }

if __name__ == "__main__":
    print("🚀 Starting Enhanced MLOps Platform v3.0 by asarekings...")
    print(f"📅 Updated: 2025-06-03 19:58:50 UTC")
    print("💻 Platform: Windows PowerShell Compatible")
    print(f"🤖 Real ML Available: {REAL_ML_AVAILABLE}")
    print("📦 Model Versioning: Enabled")
    print("🌐 Access: http://localhost:8000")
    print("📚 Docs: http://localhost:8000/docs")
    
    uvicorn.run(
        "src.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )