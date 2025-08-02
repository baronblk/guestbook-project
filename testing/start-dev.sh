#!/bin/bash
# Startet das System mit einfachen Test-Credentials

set -e

echo "🧪 Starte Entwicklungs-Setup (einfache Credentials)..."

# Zum testing Verzeichnis wechseln
cd "$(dirname "$0")"

# Container stoppen falls sie laufen
echo "📦 Stoppe eventuell laufende Container..."
docker-compose -f docker-compose.dev.yml down 2>/dev/null || true

# Zum Hauptverzeichnis für Docker Build
cd ..

# Image bauen falls nicht vorhanden
if ! docker images | grep -q "guestbook-test.*latest"; then
    echo "🏗️ Baue Docker Image..."
    docker build -t guestbook-test:latest -f Dockerfile.combined .
fi

# Zurück zu testing
cd testing

# Container starten
echo "🔧 Starte Container..."
docker-compose -f docker-compose.dev.yml up -d

# Warten bis Services bereit sind
echo "⏳ Warte auf Services..."
sleep 15

# Status prüfen
echo "📊 Prüfe Container Status..."
docker-compose -f docker-compose.dev.yml ps

echo ""
echo "✅ Entwicklungs-System gestartet!"
echo "🌐 Frontend: http://localhost:8080"
echo "🔧 Admin Panel: http://localhost:8080/admin"
echo "📖 API Docs: http://localhost:8080/docs"
echo ""
echo "👤 EINFACHE TEST-CREDENTIALS:"
echo "   Username: admin"
echo "   Password: admin123"
echo ""
echo "🔓 Security Features deaktiviert für Testing!"
echo "⚠️  NUR FÜR LOKALE ENTWICKLUNG!"
