#!/bin/bash
# Startet das Gästebuch-System für lokales Testing

set -e

echo "🚀 Starte Gästebuch-System für lokales Testing..."

# Zum Hauptverzeichnis wechseln
cd "$(dirname "$0")/.."

# Container stoppen falls sie laufen
echo "📦 Stoppe eventuell laufende Container..."
docker-compose -f docker-compose.test.yml down 2>/dev/null || true

# Container starten
echo "🔧 Starte Container..."
docker-compose -f docker-compose.test.yml up -d

# Warten bis Services bereit sind
echo "⏳ Warte auf Services..."
sleep 15

# Status prüfen
echo "📊 Prüfe Container Status..."
docker-compose -f docker-compose.test.yml ps

# Gesundheitscheck
echo "🏥 Teste Service-Verfügbarkeit..."
echo "Testing Frontend: http://localhost:8080"
curl -s -o /dev/null -w "Frontend: %{http_code}\n" http://localhost:8080/ || echo "Frontend: ERROR"

echo "Testing API: http://localhost:8080/docs"
curl -s -o /dev/null -w "API Docs: %{http_code}\n" http://localhost:8080/docs || echo "API Docs: ERROR"

echo ""
echo "✅ System gestartet!"
echo "🌐 Frontend: http://localhost:8080"
echo "🔧 Admin Panel: http://localhost:8080/admin"
echo "📖 API Docs: http://localhost:8080/docs"
echo ""
echo "👤 Admin Login:"
echo "   Username: admin"
echo "   Password: whHBJveMvwjs5a6p"
echo ""
echo "📝 Logs anzeigen: ./logs.sh"
echo "🛑 System stoppen: ./stop.sh"
