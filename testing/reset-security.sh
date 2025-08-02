#!/bin/bash
# Setzt Security Monitoring zurück

set -e

echo "🔒 Setze Security Monitoring zurück..."

# Zum Hauptverzeichnis wechseln
cd "$(dirname "$0")/.."

# Prüfe ob Container läuft
if ! docker ps | grep -q "guestbook-project_old-app-1"; then
    echo "❌ Container läuft nicht. Starte zuerst das System mit: ./start.sh"
    exit 1
fi

# Blockierte IPs löschen
echo "🧹 Lösche blockierte IPs..."
docker exec -it guestbook-project_old-app-1 python3 -c "
from backend.app.security_monitor import security_monitor
security_monitor.clear_all_blocked_ips()
print('✅ Alle blockierten IPs gelöscht')
"

echo "✅ Security Monitoring zurückgesetzt!"
