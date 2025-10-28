# PowerShell script to run all tests and linting

Write-Host "🚀 Starting test suite..." -ForegroundColor Green

# Check if Docker is running
$dockerRunning = docker info 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Docker is not running. Please start Docker first." -ForegroundColor Red
    exit 1
}

# Build and run tests
Write-Host "`n📦 Building test containers..." -ForegroundColor Yellow
docker-compose -f docker-compose.test.yml build

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to build test containers." -ForegroundColor Red
    exit 1
}

Write-Host "`n🧪 Running tests with linting..." -ForegroundColor Yellow
docker-compose -f docker-compose.test.yml up --abort-on-container-exit

# Get exit code
$exitCode = $LASTEXITCODE

# Cleanup
Write-Host "`n🧹 Cleaning up..." -ForegroundColor Yellow
docker-compose -f docker-compose.test.yml down

if ($exitCode -eq 0) {
    Write-Host "`n✅ All tests passed! Coverage report available at htmlcov/index.html" -ForegroundColor Green
} else {
    Write-Host "`n❌ Tests failed. Please check the output above." -ForegroundColor Red
}

exit $exitCode
