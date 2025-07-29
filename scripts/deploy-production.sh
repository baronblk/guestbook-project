#!/bin/bash

# 🚀 Production Deployment Script
# Automatische Aktualisierung des Guestbook-Projekts auf dem Produktionsserver

set -e  # Exit on any error

echo "🚀 Starting Guestbook Project Deployment..."
echo "=================================================="

# Konfiguration
DOCKER_IMAGE="ghcr.io/baronblk/guestbook-project/combined:latest"
CONTAINER_NAME="guestbook-combined"
PRODUCTION_URL="http://192.168.2.12:3000"

echo "📦 Docker Image: $DOCKER_IMAGE"
echo "🏷️  Container Name: $CONTAINER_NAME"
echo "🌐 Production URL: $PRODUCTION_URL"
echo ""

# Funktion: Docker Container Status prüfen
check_container_status() {
    if docker ps -q -f name=$CONTAINER_NAME | grep -q .; then
        echo "✅ Container '$CONTAINER_NAME' is running"
        return 0
    else
        echo "❌ Container '$CONTAINER_NAME' is not running"
        return 1
    fi
}

# Funktion: Gesundheitsprüfung
health_check() {
    echo "🔍 Performing health check..."
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if curl -f -s "$PRODUCTION_URL/health" > /dev/null 2>&1; then
            echo "✅ Health check passed! Application is responding."
            return 0
        fi
        
        echo "⏳ Attempt $attempt/$max_attempts - Health check failed, retrying in 10 seconds..."
        sleep 10
        ((attempt++))
    done
    
    echo "❌ Health check failed after $max_attempts attempts"
    return 1
}

# Funktion: Backup erstellen
create_backup() {
    echo "💾 Creating backup of current deployment..."
    
    if check_container_status; then
        # Container läuft - Backup der Datenbank erstellen
        docker exec $CONTAINER_NAME mysqldump -u root -p"$MYSQL_ROOT_PASSWORD" guestbook > "backup_$(date +%Y%m%d_%H%M%S).sql"
        echo "✅ Database backup created"
    else
        echo "⚠️  Container not running - skipping backup"
    fi
}

# Funktion: Rollback durchführen
rollback() {
    echo "🔄 Rolling back to previous version..."
    
    # Aktuellen Container stoppen
    if check_container_status; then
        echo "🛑 Stopping current container..."
        docker stop $CONTAINER_NAME || true
        docker rm $CONTAINER_NAME || true
    fi
    
    # Zu vorheriger Version zurückkehren (falls vorhanden)
    if docker images --format "table {{.Repository}}:{{.Tag}}" | grep -q "guestbook-project.*backup"; then
        echo "🔄 Starting backup container..."
        # Hier würde der Backup-Container gestartet werden
        echo "⚠️  Manual rollback required - check backup containers"
    else
        echo "❌ No backup version found for rollback"
    fi
    
    exit 1
}

# Hauptdeployment-Prozess
main() {
    echo "🔄 Starting deployment process..."
    
    # 1. Backup erstellen
    create_backup
    
    # 2. Neuestes Image pullen
    echo "📥 Pulling latest Docker image..."
    if docker pull $DOCKER_IMAGE; then
        echo "✅ Successfully pulled latest image"
    else
        echo "❌ Failed to pull Docker image"
        exit 1
    fi
    
    # 3. Aktuellen Container stoppen (falls vorhanden)
    if check_container_status; then
        echo "🛑 Stopping current container..."
        docker stop $CONTAINER_NAME
        docker rm $CONTAINER_NAME
        echo "✅ Container stopped and removed"
    fi
    
    # 4. Neuen Container starten
    echo "🚀 Starting new container..."
    if docker-compose -f docker-compose.yml up -d; then
        echo "✅ Container started successfully"
    else
        echo "❌ Failed to start container"
        rollback
    fi
    
    # 5. Warten auf Container-Start
    echo "⏳ Waiting for container to be ready..."
    sleep 30
    
    # 6. Gesundheitsprüfung
    if health_check; then
        echo "🎉 Deployment successful!"
        echo ""
        echo "📊 Deployment Summary:"
        echo "====================="
        echo "🚀 Container: $CONTAINER_NAME"
        echo "📦 Image: $DOCKER_IMAGE"
        echo "🌐 URL: $PRODUCTION_URL"
        echo "⏰ Deployed: $(date)"
        echo ""
        echo "✅ Your Guestbook application is now running with the latest changes!"
        echo "🔧 Comment moderation is now active - new comments require admin approval."
    else
        echo "❌ Deployment failed - health check unsuccessful"
        rollback
    fi
}

# Script-Ausführung mit Fehlerbehandlung
trap 'echo "❌ Deployment failed with error on line $LINENO"' ERR

# Prüfung, ob Docker läuft
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running or not accessible"
    exit 1
fi

# Prüfung, ob docker-compose verfügbar ist
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose is not installed or not in PATH"
    exit 1
fi

# Hauptfunktion ausführen
main

echo ""
echo "🎯 Next Steps:"
echo "=============="
echo "1. Visit $PRODUCTION_URL to verify the application"
echo "2. Test comment moderation in the admin dashboard"
echo "3. Check that new comments require approval"
echo "4. Monitor logs: docker logs $CONTAINER_NAME"
echo ""
echo "📚 For more information, see docs/DEPLOYMENT.md"
