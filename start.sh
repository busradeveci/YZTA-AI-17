#!/bin/bash
# YZTA-AI-17 Tıbbi Tahmin Sistemi Başlatma Scripti
# Platformlar arası uyumluluk için

echo "🏥 YZTA-AI-17 Tıbbi Tahmin Sistemi"
echo "=================================="

# Python kontrolü
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "❌ Python bulunamadı! Lütfen Python 3.8+ yükleyin."
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

# Python versiyonu kontrolü
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | cut -d' ' -f2)
echo "🐍 Python versiyon: $PYTHON_VERSION"

# Virtual environment kontrolü
if [ -d ".venv" ]; then
    echo "📦 Virtual environment bulundu, aktifleştiriliyor..."
    source .venv/bin/activate
else
    echo "⚠️  Virtual environment bulunamadı"
    echo "💡 Oluşturmak için: python3 -m venv .venv"
fi

# Sistemi başlat
echo "🚀 Sistem başlatılıyor..."
$PYTHON_CMD run.py "$@"
