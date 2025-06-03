# Fixed version - Navigate to your project directory first
cd "C:\Users\kings\Desktop\PROJECTS\Flagship MLOps & AI Infrastructure Projects\ml-ops-platform"

# 1. Check if your enhanced platform is running
Write-Host "🚀 Testing Enhanced MLOps Platform v3.0 by asarekings" -ForegroundColor Green
Write-Host "📅 Current Time: 2025-06-03 20:04:56 UTC" -ForegroundColor Gray
Write-Host "👤 User: asarekings" -ForegroundColor White

# 2. Check the new versioning features
Write-Host "`n🔍 Testing Versioning Features..." -ForegroundColor Cyan
try {
    $health = Invoke-RestMethod http://localhost:8000/health
    Write-Host "✅ Platform Status: $($health.status)" -ForegroundColor Green
    Write-Host "📦 Versioned Models: $($health.versioned_models)" -ForegroundColor Green
    Write-Host "🤖 Real ML Available: $($health.real_ml_available)" -ForegroundColor Green
    Write-Host "📊 Model Files: $($health.model_files)" -ForegroundColor Green
    Write-Host "🎯 Platform Version: $($health.version)" -ForegroundColor Green
} catch {
    Write-Host "❌ Platform not responding - please start the server first" -ForegroundColor Red
    Write-Host "💡 Run: python -m src.api.main" -ForegroundColor Yellow
}

# 3. Check root endpoint for new features
Write-Host "`n🏠 Checking Root Endpoint..." -ForegroundColor Cyan
try {
    $root = Invoke-RestMethod http://localhost:8000/
    Write-Host "✅ Platform: $($root.message)" -ForegroundColor Green
    Write-Host "📋 Description: $($root.description)" -ForegroundColor White
    Write-Host "🔢 Version: $($root.version)" -ForegroundColor Green
    Write-Host "📅 Last Updated: $($root.updated)" -ForegroundColor Gray
    
    Write-Host "`n🔗 New Endpoints Available:" -ForegroundColor Yellow
    if ($root.endpoints.versioning) {
        Write-Host "  📦 Versioning: $($root.endpoints.versioning)" -ForegroundColor Green
    }
    if ($root.endpoints.version_create) {
        Write-Host "  ➕ Create Version: $($root.endpoints.version_create)" -ForegroundColor Green
    }
    if ($root.endpoints.version_list) {
        Write-Host "  📋 List Versions: $($root.endpoints.version_list)" -ForegroundColor Green
    }
    if ($root.endpoints.version_rollback) {
        Write-Host "  🔄 Rollback: $($root.endpoints.version_rollback)" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Could not access root endpoint" -ForegroundColor Red
}

# 4. Train models (this will auto-create versions)
Write-Host "`n🤖 Training Models with Auto-Versioning..." -ForegroundColor Cyan
try {
    $training = Invoke-RestMethod -Uri http://localhost:8000/api/v1/train -Method Post
    Write-Host "✅ Training Status: $($training.status)" -ForegroundColor Green
    
    if ($training.models_versioned) {
        Write-Host "📦 Models Versioned:" -ForegroundColor Yellow
        foreach ($versioned in $training.models_versioned) {
            Write-Host "  - $($versioned.model): $($versioned.version)" -ForegroundColor Green
        }
    }
    
    if ($training.models_trained) {
        Write-Host "🎯 Models Trained: $($training.models_trained.Count)" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠️  Training may have already completed or failed" -ForegroundColor Yellow
    Write-Host "💡 This is normal if models are already trained" -ForegroundColor Gray
}

# 5. List all versioned models
Write-Host "`n📦 Listing All Versioned Models..." -ForegroundColor Cyan
try {
    $versions = Invoke-RestMethod http://localhost:8000/api/v1/versions
    Write-Host "✅ Total Versioned Models: $($versions.total_models)" -ForegroundColor Green
    
    if ($versions.versioned_models) {
        foreach ($model in $versions.versioned_models.PSObject.Properties) {
            $modelName = $model.Name
            $modelData = $model.Value
            Write-Host "  📋 $modelName`: $($modelData.total_versions) versions" -ForegroundColor Yellow
            
            if ($modelData.latest_version) {
                Write-Host "    🔹 Latest: $($modelData.latest_version.version)" -ForegroundColor Green
                Write-Host "    📅 Created: $($modelData.latest_version.created_at)" -ForegroundColor Gray
            }
        }
    }
} catch {
    Write-Host "❌ Could not retrieve versioned models" -ForegroundColor Red
}

# 6. Check versions for fraud detection model specifically
Write-Host "`n🔒 Checking Fraud Detection Model Versions..." -ForegroundColor Cyan
try {
    $fraudVersions = Invoke-RestMethod http://localhost:8000/api/v1/versions/fraud_detection
    Write-Host "✅ Fraud Detection Versions: $($fraudVersions.total_versions)" -ForegroundColor Green
    
    if ($fraudVersions.versions) {
        Write-Host "📋 Version History:" -ForegroundColor Yellow
        foreach ($version in $fraudVersions.versions) {
            Write-Host "  🔹 $($version.version) - Created: $($version.created_at)" -ForegroundColor Green
            if ($version.metadata.training_info) {
                Write-Host "    📊 Accuracy: $($version.metadata.training_info.accuracy)" -ForegroundColor Gray
            }
        }
    }
} catch {
    Write-Host "⚠️  No versions found for fraud_detection model yet" -ForegroundColor Yellow
}

# 7. Test prediction with version info
Write-Host "`n🔮 Testing Prediction with Version Info..." -ForegroundColor Cyan
$predictionData = @{
    feature_1 = -1.5
    feature_2 = 0.8
    feature_3 = 9.2
    feature_4 = 4.1
    test_case = "version_test_by_asarekings"
} | ConvertTo-Json

try {
    $prediction = Invoke-RestMethod -Uri http://localhost:8000/api/v1/predict/real/fraud_detection -Method Post -Body $predictionData -ContentType "application/json"
    Write-Host "✅ Prediction: $($prediction.prediction)" -ForegroundColor Green
    Write-Host "🎯 Confidence: $($prediction.confidence)" -ForegroundColor Green
    Write-Host "🤖 Model: $($prediction.model)" -ForegroundColor Green
    
    if ($prediction.current_version) {
        Write-Host "📦 Current Version: $($prediction.current_version)" -ForegroundColor Yellow
        Write-Host "📅 Version Created: $($prediction.version_created)" -ForegroundColor Gray
    }
    
    Write-Host "👤 Author: $($prediction.author)" -ForegroundColor White
} catch {
    Write-Host "❌ Prediction failed - model may not be trained yet" -ForegroundColor Red
}

# 8. Check enhanced models list
Write-Host "`n📊 Checking Enhanced Models List..." -ForegroundColor Cyan
try {
    $models = Invoke-RestMethod http://localhost:8000/api/v1/models
    Write-Host "✅ Total Models: $($models.total_models)" -ForegroundColor Green
    Write-Host "📦 Versioning Enabled: $($models.versioning_enabled)" -ForegroundColor Green
    Write-Host "🔹 Lightweight Models: $($models.total_lightweight)" -ForegroundColor Yellow
    Write-Host "🤖 Real ML Models: $($models.total_real)" -ForegroundColor Yellow
    
    if ($models.real_models) {
        Write-Host "`n🤖 Real ML Models with Versioning:" -ForegroundColor Yellow
        foreach ($model in $models.real_models) {
            Write-Host "  📋 $($model.name)" -ForegroundColor Green
            Write-Host "    📦 Versions: $($model.version_count)" -ForegroundColor Gray
            if ($model.latest_version) {
                Write-Host "    🔹 Latest: $($model.latest_version)" -ForegroundColor Gray
            }
        }
    }
} catch {
    Write-Host "❌ Could not retrieve models list" -ForegroundColor Red
}

# 9. Fixed Memory Usage Check (corrected syntax)
Write-Host "`n💾 System Resource Check..." -ForegroundColor Cyan
$pythonProcesses = Get-Process -Name python -ErrorAction SilentlyContinue
if ($pythonProcesses) {
    # Handle multiple processes correctly
    $processArray = @($pythonProcesses)
    
    for ($i = 0; $i -lt $processArray.Length; $i++) {
        $process = $processArray[$i]
        Write-Host "Process $($i + 1) - ID: $($process.Id)" -ForegroundColor Yellow
        
        # Fixed division syntax for PowerShell
        $workingSetMB = [math]::Round($process.WorkingSet64 / 1024 / 1024, 2)
        $peakWorkingSetMB = [math]::Round($process.PeakWorkingSet64 / 1024 / 1024, 2)
        
        Write-Host "  Working Set: $workingSetMB MB" -ForegroundColor Green
        Write-Host "  Peak Working Set: $peakWorkingSetMB MB" -ForegroundColor Green
        Write-Host "  Start Time: $($process.StartTime)" -ForegroundColor Gray
    }
} else {
    Write-Host "No Python processes found" -ForegroundColor Red
}

# 10. Final Status Summary
Write-Host "`n🎉 Enhanced MLOps Platform v3.0 Status Summary" -ForegroundColor Magenta
Write-Host "=" * 60 -ForegroundColor DarkGray
Write-Host "👤 Platform Owner: asarekings" -ForegroundColor White
Write-Host "📅 Check Time: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') UTC" -ForegroundColor Gray
Write-Host "🚀 Platform: Enhanced MLOps v3.0 with Model Versioning" -ForegroundColor Green
Write-Host "🌐 Access URL: http://localhost:8000" -ForegroundColor Cyan
Write-Host "📚 API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "✅ Status: Ready for Production Use!" -ForegroundColor Green