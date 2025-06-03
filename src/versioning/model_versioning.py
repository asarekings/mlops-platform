#!/usr/bin/env python3
# Model Versioning System
# Author: asarekings
# Date: 2025-06-03 19:12:59 UTC

import os
import json
import shutil
from datetime import datetime
import hashlib

class ModelVersioning:
    """Version control for ML models"""
    
    def __init__(self):
        self.versions_dir = "model_versions"
        os.makedirs(self.versions_dir, exist_ok=True)
    
    def create_version(self, model_name, model_file, metadata):
        """Create a new version of a model"""
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
            "file_hash": self.calculate_file_hash(model_file)
        }
        
        with open(os.path.join(version_dir, "metadata.json"), "w") as f:
            json.dump(version_metadata, f, indent=2)
        
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