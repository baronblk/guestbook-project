#!/bin/bash
# Startet das System neu

set -e

echo "🔄 Starte System neu..."

# Stoppen
./stop.sh

# Kurz warten
sleep 2

# Starten
./start.sh
