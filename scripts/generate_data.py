#!/usr/bin/env python3
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from src.data.synthetic_generator import LightweightDataGenerator
except ImportError as e:
    print(f"Import error: {e}")
    print("Using fallback data generation...")
    
    # Fallback implementation
    import json
    import random
    from datetime import datetime
    
    def generate_fallback_data():
        data = []
        for i in range(1000):
            data.append({
                "id": i,
                "value": random.uniform(0, 100),
                "category": random.choice(["A", "B", "C"]),
                "timestamp": datetime.now().isoformat()
            })
        
        os.makedirs("data", exist_ok=True)
        with open("data/fallback_data.json", 'w') as f:
            json.dump(data, f, indent=2)
        
        print("✅ Fallback data generated: data/fallback_data.json")
    
    generate_fallback_data()
    sys.exit(0)

def main():
    print("🎲 Lightweight Data Generator by asarekings")
    print("📅 2025-06-03 04:29:30 UTC")
    
    generator = LightweightDataGenerator()
    summary = generator.save_datasets()
    
    print("\n✅ Data generation complete!")
    print(f"📊 Total records: {summary['total_records']:,}")

if __name__ == "__main__":
    main()
