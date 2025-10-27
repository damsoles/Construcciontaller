# Script para descargar MobileNet-SSD
# Compatible con PowerShell 5.1 (sin emojis)

Write-Host "=== Descargando modelo MobileNet-SSD para OpenCV ===" -ForegroundColor Cyan
Write-Host ""

# Crear carpeta models
$modelsDir = "detector\models"
if (-not (Test-Path $modelsDir)) {
    New-Item -ItemType Directory -Path $modelsDir -Force | Out-Null
    Write-Host "[OK] Carpeta 'detector\models' creada" -ForegroundColor Green
}

# URLs de los archivos (repositorio alternativo confiable)
$prototxtUrl = "https://github.com/PINTO0309/MobileNet-SSD-RealSense/raw/master/caffemodel/MobileNetSSD/MobileNetSSD_deploy.prototxt"
$caffemodelUrl = "https://github.com/PINTO0309/MobileNet-SSD-RealSense/raw/master/caffemodel/MobileNetSSD/MobileNetSSD_deploy.caffemodel"

try {
    # Descargar prototxt
    Write-Host "[1/2] Descargando MobileNetSSD_deploy.prototxt..." -ForegroundColor Yellow
    Invoke-WebRequest -Uri $prototxtUrl -OutFile "$modelsDir\MobileNetSSD_deploy.prototxt"
    Write-Host "[OK] Prototxt descargado (30 KB)" -ForegroundColor Green
    
    # Descargar caffemodel
    Write-Host "[2/2] Descargando MobileNetSSD_deploy.caffemodel (23 MB)..." -ForegroundColor Yellow
    Write-Host "      Esto puede tardar 1-2 minutos..." -ForegroundColor Yellow
    Invoke-WebRequest -Uri $caffemodelUrl -OutFile "$modelsDir\MobileNetSSD_deploy.caffemodel"
    Write-Host "[OK] Caffemodel descargado (23 MB)" -ForegroundColor Green
    
    Write-Host ""
    Write-Host "*** MODELO DESCARGADO EXITOSAMENTE! ***" -ForegroundColor Green
    Write-Host "Ubicacion: $modelsDir" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Ahora ejecuta: python manage.py runserver" -ForegroundColor Yellow
}
catch {
    Write-Host ""
    Write-Host "[ERROR] No se pudo descargar el modelo:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host ""
    Write-Host "Solucion alternativa:" -ForegroundColor Yellow
    Write-Host "1. Descarga manualmente desde:" -ForegroundColor Yellow
    Write-Host "   - Prototxt: $prototxtUrl" -ForegroundColor Gray
    Write-Host "   - Caffemodel: $caffemodelUrl" -ForegroundColor Gray
    Write-Host "2. Guarda los archivos en: $modelsDir" -ForegroundColor Yellow
    exit 1
}
