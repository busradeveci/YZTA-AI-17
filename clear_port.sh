#!/bin/bash

# Port Temizleme Script'i
# Kullanım: ./clear_port.sh [port_numarası]

PORT=${1:-5000}

echo "🔄 Port $PORT temizleniyor..."

# macOS/Linux için lsof kullan
if command -v lsof &> /dev/null; then
    PIDS=$(lsof -ti:$PORT 2>/dev/null)
    if [ ! -z "$PIDS" ]; then
        echo "Port $PORT'u kullanan process'ler: $PIDS"
        echo "$PIDS" | xargs kill -9 2>/dev/null
        echo "✅ Port $PORT temizlendi"
        
        # Port temizlendiğini doğrula
        sleep 1
        REMAINING=$(lsof -ti:$PORT 2>/dev/null)
        if [ -z "$REMAINING" ]; then
            echo "✅ Port $PORT artık boş"
        else
            echo "⚠️  Bazı process'ler hala çalışıyor: $REMAINING"
        fi
    else
        echo "ℹ️  Port $PORT zaten boş"
    fi
else
    echo "❌ lsof komutu bulunamadı"
    exit 1
fi
