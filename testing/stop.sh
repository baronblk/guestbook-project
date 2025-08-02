#!/bin/bash
# Stoppt das Gästebuch-System

set -e

echo "🛑 Stoppe Gästebuch-System..."

# Zum Hauptverzeichnis wechseln
cd "$(dirname "$0")/.."

# Container stoppen
docker-compose -f docker-compose.test.yml down

echo "✅ System gestoppt!"
