#!/usr/bin/env python3
# Lightweight MLOps Platform Setup
# Author: asarekings
# Date: 2025-06-03 04:29:30 UTC

import os
import sys
import subprocess

def run_command(cmd):
    try:
        print(f"Running: {cmd}")
        result = subprocess.run(cmd, shell=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return False

def main():
    print("🚀 Lightweight MLOps Platform Setup")
    print("👤 Author: asarekings")
    print("📅 Date: 2025-06-03 04:29:30 UTC")
    print("💻 Platform: Windows Compatible (No C++ Build Tools)")
    print("-" * 60)
    
    # Check Python
    version = sys.version_info
    print(f"🐍 Python {version.major}.{version.minor}.{version.micro} detected")
    
    # Install lightweight requirements
    print("\n📦 Installing lightweight packages...")
    success = run_command(f'"{sys.executable}" -m pip install --no-cache-dir fastapi uvicorn pydantic pandas numpy requests pytest black')
    
    if not success:
        print("⚠️  Some packages failed - trying individual installation...")
        packages = ["fastapi", "uvicorn", "pydantic", "pandas", "numpy", "requests"]
        for pkg in packages:
            run_command(f'"{sys.executable}" -m pip install {pkg}')
    
    # Generate data
    print("\n🎲 Generating sample datasets...")
    if not run_command(f'"{sys.executable}" scripts/generate_data.py'):
        print("⚠️  Data generation had issues")
    
    # Test API import
    try:
        sys.path.insert(0, '.')
        from src.api.main import app
        print("\n✅ API imports successfully")
    except Exception as e:
        print(f"\n⚠️  Import test: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Lightweight Setup Completed!")
    print("=" * 60)
    print("\n🚀 Next Steps:")
    print("  1. python -m src.api.main")
    print("  2. Open: http://localhost:8000/docs")
    print("  3. Test: http://localhost:8000/health")
    print("\n🌐 Endpoints:")
    print("  • API Docs: http://localhost:8000/docs")
    print("  • Health: http://localhost:8000/health")
    print("  • Datasets: http://localhost:8000/api/v1/datasets")
    print("  • Models: http://localhost:8000/api/v1/models")
    print("\n💡 This version avoids C++ dependencies!")

if __name__ == "__main__":
    main()
