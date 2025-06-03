import json
import csv
import random
import os
from datetime import datetime, timedelta

class LightweightDataGenerator:
    """Generate simple datasets without heavy dependencies"""
    
    def __init__(self, random_state=42):
        self.random_state = random_state
        random.seed(random_state)
        print(f"🎲 LightweightDataGenerator by asarekings - 2025-06-03 04:29:30 UTC")
    
    def generate_sample_data(self, n_samples=5000):
        """Generate sample dataset"""
        print(f"📊 Generating sample dataset ({n_samples} records)...")
        
        data = []
        for i in range(n_samples):
            record = {
                "id": i + 1,
                "feature_1": round(random.uniform(-3, 3), 3),
                "feature_2": round(random.uniform(-2, 2), 3),
                "feature_3": round(random.uniform(0, 10), 3),
                "feature_4": round(random.uniform(-1, 1), 3),
                "category": random.choice(["A", "B", "C", "D"]),
                "region": random.choice(["North", "South", "East", "West"]),
                "timestamp": (datetime.now() - timedelta(days=random.randint(0, 365))).isoformat(),
                "target": random.choice([0, 1]) if random.random() > 0.7 else 0
            }
            data.append(record)
        
        print(f"✅ Generated {len(data)} records")
        return data
    
    def generate_time_series(self, n_points=1000):
        """Generate time series data"""
        print(f"📈 Generating time series ({n_points} points)...")
        
        data = []
        base_value = 100
        
        for i in range(n_points):
            # Simple trend + noise
            trend = i * 0.1
            noise = random.uniform(-5, 5)
            seasonal = 10 * (1 + 0.5 * (i % 24) / 24)  # Daily pattern
            
            value = base_value + trend + seasonal + noise
            
            record = {
                "timestamp": (datetime.now() - timedelta(hours=n_points-i)).isoformat(),
                "value": round(value, 2),
                "trend": round(trend, 2),
                "seasonal": round(seasonal, 2),
                "noise": round(noise, 2)
            }
            data.append(record)
        
        print(f"✅ Generated {len(data)} time series points")
        return data
    
    def save_datasets(self, output_dir="data"):
        """Generate and save all datasets"""
        print(f"💾 Generating lightweight datasets by asarekings...")
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate sample data
        sample_data = self.generate_sample_data()
        sample_file = os.path.join(output_dir, "sample_data.json")
        with open(sample_file, 'w') as f:
            json.dump(sample_data, f, indent=2)
        
        # Also save as CSV
        csv_file = os.path.join(output_dir, "sample_data.csv")
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            if sample_data:
                writer = csv.DictWriter(f, fieldnames=sample_data[0].keys())
                writer.writeheader()
                writer.writerows(sample_data)
        
        # Generate time series
        ts_data = self.generate_time_series()
        ts_file = os.path.join(output_dir, "time_series.json")
        with open(ts_file, 'w') as f:
            json.dump(ts_data, f, indent=2)
        
        # Create summary
        summary = {
            "author": "asarekings",
            "generated_at": "2025-06-03 04:29:30 UTC",
            "platform": "Lightweight MLOps Platform",
            "datasets": {
                "sample_data": {
                    "file": "sample_data.csv",
                    "records": len(sample_data),
                    "features": 8,
                    "format": "CSV/JSON"
                },
                "time_series": {
                    "file": "time_series.json",
                    "points": len(ts_data),
                    "metrics": 4,
                    "format": "JSON"
                }
            },
            "total_records": len(sample_data) + len(ts_data),
            "compatible": "Windows PowerShell",
            "dependencies": "Minimal (No C++ Build Tools Required)"
        }
        
        summary_file = os.path.join(output_dir, "summary.json")
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"\n✅ All datasets saved to {output_dir}/")
        print(f"📊 Sample Data: {len(sample_data)} records")
        print(f"📈 Time Series: {len(ts_data)} points")
        print(f"📋 Summary: {summary_file}")
        
        return summary

if __name__ == "__main__":
    generator = LightweightDataGenerator()
    generator.save_datasets()
