#!/bin/bash
# Testet das Admin Login

set -e

echo "🔐 Teste Admin Login..."

# Zum Hauptverzeichnis wechseln
cd "$(dirname "$0")/.."

# Prüfe ob Container läuft
if ! docker ps | grep -q "guestbook-project_old-app-1"; then
    echo "❌ Container läuft nicht. Starte zuerst das System mit: ./start.sh"
    exit 1
fi

echo "📡 Teste Login API..."
response=$(curl -s -X POST "http://localhost:8080/api/admin/login" \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": "whHBJveMvwjs5a6p"}')

if echo "$response" | grep -q "access_token"; then
    echo "✅ Login erfolgreich!"
    echo "🎫 Access Token erhalten"

    # Token extrahieren (ersten 50 Zeichen)
    token=$(echo "$response" | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4 | head -c 50)
    echo "🔑 Token: ${token}..."

else
    echo "❌ Login fehlgeschlagen!"
    echo "📤 Response: $response"

    if echo "$response" | grep -q "429"; then
        echo "⚠️ Rate Limit erreicht. Führe aus: ./reset-security.sh"
    fi
fi

echo ""
echo "🌐 Teste auch manuell im Browser:"
echo "   http://localhost:8080/admin"
echo "   Username: admin"
echo "   Password: whHBJveMvwjs5a6p"
