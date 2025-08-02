#!/bin/bash
# Quick Setup für lokales Testing

set -e

echo "⚡ Quick Testing Setup..."

# Zum Hauptverzeichnis wechseln
cd "$(dirname "$0")/.."

# Prüfe ob docker-compose.test.yml existiert
if [ ! -f "docker-compose.test.yml" ]; then
    echo "❌ docker-compose.test.yml nicht gefunden!"
    exit 1
fi

# Prüfe ob Docker läuft
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker läuft nicht. Bitte Docker starten."
    exit 1
fi

echo "✅ Docker läuft"
echo "✅ Konfiguration gefunden"

cd testing
echo "🚀 Starte System..."
./start.sh
