#!/bin/bash

# 🧹 Guestbook Project Cleanup Script
# Dieses Script organisiert und bereinigt das Projekt nach Best Practices

echo "🧹 Starte Projekt-Cleanup..."

# Erstelle .gitignore falls nicht vorhanden
if [ ! -f .gitignore ]; then
    echo "📝 Erstelle .gitignore..."
    cat > .gitignore << EOF
# Dependencies
node_modules/
.venv/
__pycache__/
*.pyc

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Environment
.env.local
.env.production.local

# Build outputs
build/
dist/
*.egg-info/

# Database
*.sqlite
*.db

# Uploads (in development)
uploads/

# Docker
.docker/
EOF
fi

# Bereinige Python Cache
echo "🐍 Bereinige Python Cache..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true
find . -name "*.pyo" -delete 2>/dev/null || true

# Bereinige Node.js
echo "📦 Bereinige Node.js Cache..."
rm -rf frontend/node_modules/.cache 2>/dev/null || true

# Bereinige macOS Dateien
echo "🍎 Bereinige macOS Dateien..."
find . -name ".DS_Store" -delete 2>/dev/null || true

# Bereinige temporäre Dateien
echo "🗑️  Bereinige temporäre Dateien..."
find . -name "*.tmp" -delete 2>/dev/null || true
find . -name "*.temp" -delete 2>/dev/null || true

echo "✅ Cleanup abgeschlossen!"
echo ""
echo "📁 Projektstruktur nach Cleanup:"
tree -I 'node_modules|.venv|__pycache__|.git|*.pyc' -L 3 || ls -la
