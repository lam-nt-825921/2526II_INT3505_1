# Thiết lập biến môi trường
$DbPath = Join-Path (Get-Location) "server/sqlite_app.db"
$env:SQLALCHEMY_DATABASE_URL = "sqlite:///$DbPath"
$env:SECRET_KEY = "test_secret_key_1234567890"
$env:ALGORITHM = "HS256"
$env:ACCESS_TOKEN_EXPIRE_MINUTES = "30"
$env:REFRESH_TOKEN_EXPIRE_DAYS = "7"
$env:ENVIRONMENT = "dev"
$env:PYTHONPATH = "server"

# 1. Khởi tạo lại Database (Seed)
Write-Host "--- Step 1: Seeding Database ---" -ForegroundColor Cyan
python server/seed_test.py

# 2. Khởi động Server FastAPI
Write-Host "--- Step 2: Starting FastAPI Server ---" -ForegroundColor Cyan
# Chạy từ thư mục server và dùng module mode để tránh ModuleNotFoundError
$ServerProcess = Start-Process python -ArgumentList "-m app.main" -WorkingDirectory "server" -PassThru -NoNewWindow

# Đợi server khởi động
Write-Host "Waiting for server to start..."
Start-Sleep -Seconds 5

# 3. Chạy Newman Test (CLI + HTML Report)
Write-Host "--- Step 3: Running Postman Tests with Newman ---" -ForegroundColor Cyan
$ReportPath = "server/tests/postman/report.html"
newman run server/tests/postman/library_collection.json `
    -e server/tests/postman/library_env.json `
    --env-var "baseUrl=http://localhost:3000/api/v1" `
    --reporters "cli,htmlextra" `
    --reporter-htmlextra-export $ReportPath

Write-Host "HTML Report generated at: $ReportPath" -ForegroundColor Yellow

# 4. Tắt Server
Write-Host "--- Step 4: Cleaning up ---" -ForegroundColor Cyan
if ($ServerProcess) { Stop-Process -Id $ServerProcess.Id -ErrorAction SilentlyContinue }
Write-Host "Done!" -ForegroundColor Green
