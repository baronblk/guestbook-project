#!/bin/bash
# Rebuilt Docker Image und startet System neu

set -e

echo "🔨 Rebuild Docker Image und Neustart..."

# Zum Hauptverzeichnis wechseln
cd "$(dirname "$0")/.."

# Container stoppen
echo "📦 Stoppe Container..."
docker-compose -f docker-compose.test.yml down

# Image neu bauen
echo "🏗️ Baue Docker Image neu..."
docker build -t guestbook-test:latest -f Dockerfile.combined .

# System starten
echo "🚀 Starte System..."
cd testing
./start.sh
