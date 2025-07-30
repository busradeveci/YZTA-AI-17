#!/bin/bash
# YZTA-AI-17 Tam Başlatma Scripti
# Usage: ./start.sh

echo "🚀 YZTA-AI-17 uygulaması başlatılıyor..."

# Backend'i arka planda başlat
echo "📡 Backend başlatılıyor..."
python run.py &
BACKEND_PID=$!

# Backend'in tamamen başlamasını bekle
sleep 5

# Backend'in çalıştığı portu bul
BACKEND_PORT=$(lsof -ti :8000 2>/dev/null && echo "8000" || echo "8001")

# package.json proxy'sini güncelle
if [ -f "package.json" ]; then
    sed -i '' "s|\"proxy\": \"http://localhost:[0-9]*\"|\"proxy\": \"http://localhost:$BACKEND_PORT\"|" package.json
    echo "📝 package.json proxy güncellendi: http://localhost:$BACKEND_PORT"
fi

# Frontend'i başlat
echo "🎨 Frontend başlatılıyor..."
PORT=3001 npm start &
FRONTEND_PID=$!

echo ""
echo "🌐 Uygulama başlatıldı!"
echo "📱 Frontend: http://localhost:3001"
echo "🔧 Backend: http://localhost:$BACKEND_PORT"
echo "📖 API Docs: http://localhost:$BACKEND_PORT/docs"
echo ""
echo "Kapatmak için Ctrl+C tuşlayın"

# Cleanup function
cleanup() {
    echo ""
    echo "🛑 Uygulamalar kapatılıyor..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    # Kill any remaining processes
    pkill -f "python run.py" 2>/dev/null
    pkill -f "react-scripts start" 2>/dev/null
    echo "👋 Uygulamalar kapatıldı"
    exit 0
}

# Set up signal handling
trap cleanup INT TERM

# Wait for processes
wait
