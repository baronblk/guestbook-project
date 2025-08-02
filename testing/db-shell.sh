#!/bin/bash
# Öffnet eine Datenbank-Shell

set -e

echo "🗄️ Öffne Datenbank Shell..."

# Zum Hauptverzeichnis wechseln
cd "$(dirname "$0")/.."

# Prüfe ob Container läuft
if ! docker ps | grep -q "guestbook-project_old-db-1"; then
    echo "❌ Datenbank Container läuft nicht. Starte zuerst das System mit: ./start.sh"
    exit 1
fi

echo "📊 Verbinde zur MariaDB..."
echo "Database: guestbook"
echo "Username: guestuser"
echo ""
echo "💡 Nützliche Befehle:"
echo "   SHOW TABLES;"
echo "   SELECT * FROM admin_users;"
echo "   SELECT * FROM reviews LIMIT 5;"
echo "   DESCRIBE admin_users;"
echo ""

docker exec -it guestbook-project_old-db-1 mariadb -u guestuser -p'whHBJveMvwjs5a6p' -D guestbook
