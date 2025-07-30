#!/bin/bash

# Deployment Script für Gästebuch-Produktion
# Führt ein sicheres Update mit automatischem Backup durch

set -e

# Konfiguration
COMPOSE_FILE="docker-compose.production.yml"
PROJECT_NAME="guestbook-production"
BACKUP_BEFORE_UPDATE=true

# Farben für Output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funktionen
log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

log_error() {
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

check_requirements() {
    log "Checking requirements..."

    # Prüfe Docker
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed"
        exit 1
    fi

    # Prüfe Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose is not installed"
        exit 1
    fi

    # Prüfe Compose-Datei
    if [ ! -f "$COMPOSE_FILE" ]; then
        log_error "Compose file not found: $COMPOSE_FILE"
        exit 1
    fi

    log_success "Requirements check passed"
}

create_backup() {
    if [ "$BACKUP_BEFORE_UPDATE" = true ]; then
        log "Creating backup before update..."

        # Führe Backup über den backup-Service aus
        docker-compose -f "$COMPOSE_FILE" -p "$PROJECT_NAME" exec db-backup /backup.sh

        if [ $? -eq 0 ]; then
            log_success "Backup created successfully"
        else
            log_error "Backup failed"
            return 1
        fi
    else
        log_warning "Skipping backup (BACKUP_BEFORE_UPDATE=false)"
    fi
}

pull_latest_images() {
    log "Pulling latest images..."

    docker-compose -f "$COMPOSE_FILE" -p "$PROJECT_NAME" pull

    if [ $? -eq 0 ]; then
        log_success "Images pulled successfully"
    else
        log_error "Failed to pull images"
        return 1
    fi
}

deploy_update() {
    log "Deploying update..."

    # Stoppe Services (aber nicht die Datenbank)
    log "Stopping application services..."
    docker-compose -f "$COMPOSE_FILE" -p "$PROJECT_NAME" stop app watchtower

    # Starte Services neu
    log "Starting updated services..."
    docker-compose -f "$COMPOSE_FILE" -p "$PROJECT_NAME" up -d

    if [ $? -eq 0 ]; then
        log_success "Services restarted successfully"
    else
        log_error "Failed to restart services"
        return 1
    fi
}

wait_for_health() {
    log "Waiting for services to become healthy..."

    local max_attempts=60
    local attempt=0

    while [ $attempt -lt $max_attempts ]; do
        # Prüfe App-Health
        if docker-compose -f "$COMPOSE_FILE" -p "$PROJECT_NAME" ps app | grep -q "healthy"; then
            log_success "Application is healthy"
            return 0
        fi

        sleep 5
        attempt=$((attempt + 1))
        log "Waiting... (${attempt}/${max_attempts})"
    done

    log_error "Service did not become healthy within expected time"
    return 1
}

cleanup_old_images() {
    log "Cleaning up old Docker images..."

    # Entferne unbenutzte Images
    docker image prune -f

    log_success "Cleanup completed"
}

show_status() {
    log "Current service status:"
    docker-compose -f "$COMPOSE_FILE" -p "$PROJECT_NAME" ps

    echo ""
    log "Recent logs:"
    docker-compose -f "$COMPOSE_FILE" -p "$PROJECT_NAME" logs --tail=10 app
}

rollback() {
    log_warning "Rolling back to previous version..."

    # Hier könnte eine Rollback-Logik implementiert werden
    # Zum Beispiel das Wiederherstellen eines vorherigen Backups

    log_error "Rollback functionality not implemented yet"
    log "Please restore manually from backup if needed"
}

# Hauptfunktion
main() {
    log "=== Guestbook Production Deployment Script ==="

    # Prüfe Argumente
    case "${1:-deploy}" in
        "deploy"|"update")
            check_requirements
            create_backup
            pull_latest_images
            deploy_update
            wait_for_health
            cleanup_old_images
            show_status
            log_success "Deployment completed successfully!"
            ;;
        "status")
            show_status
            ;;
        "backup")
            create_backup
            ;;
        "rollback")
            rollback
            ;;
        "help"|"-h"|"--help")
            echo "Usage: $0 [command]"
            echo ""
            echo "Commands:"
            echo "  deploy, update  - Deploy/update the application (default)"
            echo "  status          - Show current service status"
            echo "  backup          - Create database backup"
            echo "  rollback        - Rollback to previous version"
            echo "  help            - Show this help"
            ;;
        *)
            log_error "Unknown command: $1"
            echo "Use '$0 help' for usage information"
            exit 1
            ;;
    esac
}

# Führe Script aus
main "$@"
