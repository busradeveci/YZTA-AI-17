@echo off
rem YZTA-AI-17 Tıbbi Tahmin Sistemi Başlatma Scripti
rem Windows için

echo 🏥 YZTA-AI-17 Tıbbi Tahmin Sistemi
echo ==================================

rem Python kontrolü
python --version >nul 2>&1
if %errorlevel% neq 0 (
    py --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo ❌ Python bulunamadı! Lütfen Python 3.8+ yükleyin.
        pause
        exit /b 1
    ) else (
        set PYTHON_CMD=py
    )
) else (
    set PYTHON_CMD=python
)

rem Python versiyonunu göster
for /f "tokens=2" %%i in ('%PYTHON_CMD% --version 2^>^&1') do set PYTHON_VERSION=%%i
echo 🐍 Python versiyon: %PYTHON_VERSION%

rem Virtual environment kontrolü
if exist ".venv" (
    echo 📦 Virtual environment bulundu, aktifleştiriliyor...
    call .venv\Scripts\activate.bat
) else (
    echo ⚠️  Virtual environment bulunamadı
    echo 💡 Oluşturmak için: python -m venv .venv
)

rem Sistemi başlat
echo 🚀 Sistem başlatılıyor...
%PYTHON_CMD% run.py %*
