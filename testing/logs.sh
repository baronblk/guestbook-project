#!/bin/bash
# Zeigt aktuelle Logs an

set -e

echo "📋 Aktuelle System Logs..."

# Zum Hauptverzeichnis wechseln
cd "$(dirname "$0")/.."

# Prüfe ob Container läuft
if ! docker ps | grep -q "guestbook-project_old-app-1"; then
    echo "❌ Container läuft nicht. Starte zuerst das System mit: ./start.sh"
    exit 1
fi

echo ""
echo "=== 🖥️ APP CONTAINER LOGS ==="
docker logs guestbook-project_old-app-1 --tail 20

echo ""
echo "=== 🗄️ DATABASE CONTAINER LOGS ==="
docker logs guestbook-project_old-db-1 --tail 10

echo ""
echo "=== ⚡ FASTAPI LOGS ==="
docker exec guestbook-project_old-app-1 tail -10 /var/log/supervisor/fastapi.log 2>/dev/null || echo "FastAPI Logs nicht verfügbar"

echo ""
echo "=== 🔒 SECURITY LOGS ==="
docker exec guestbook-project_old-app-1 tail -10 /app/logs/security.log 2>/dev/null || echo "Security Logs nicht verfügbar"

echo ""
echo "📊 Für Live-Logs: docker logs -f guestbook-project_old-app-1"
