#!/bin/bash

# Backup Script für Gästebuch-Datenbank
# Wird automatisch alle 6 Stunden ausgeführt

set -e

# Konfiguration
DB_HOST=${DB_HOST:-db}
DB_USER=${DB_USER:-root}
DB_PASSWORD=${DB_PASSWORD}
DB_NAME=${DB_NAME:-guestbook}
BACKUP_DIR="/backups"
RETENTION_DAYS=${BACKUP_RETENTION_DAYS:-30}

# Funktionen
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

create_backup() {
    local timestamp=$(date +%Y%m%d_%H%M%S)
    local backup_file="${BACKUP_DIR}/guestbook_backup_${timestamp}.sql"

    log "Starting backup to ${backup_file}"

    # Erstelle Backup mit vollständiger Konsistenz
    mariadb-dump \
        -h "${DB_HOST}" \
        -u "${DB_USER}" \
        -p"${DB_PASSWORD}" \
        --single-transaction \
        --routines \
        --triggers \
        --complete-insert \
        --extended-insert \
        --quick \
        --lock-tables=false \
        "${DB_NAME}" > "${backup_file}"

    if [ $? -eq 0 ]; then
        log "Backup created successfully"

        # Komprimiere das Backup
        gzip "${backup_file}"
        log "Backup compressed to ${backup_file}.gz"

        # Zeige Backup-Größe
        local size=$(du -h "${backup_file}.gz" | cut -f1)
        log "Backup size: ${size}"

        return 0
    else
        log "ERROR: Backup failed!"
        rm -f "${backup_file}" 2>/dev/null || true
        return 1
    fi
}

cleanup_old_backups() {
    log "Cleaning up backups older than ${RETENTION_DAYS} days"

    local deleted_count=$(find "${BACKUP_DIR}" -name "guestbook_backup_*.sql.gz" -type f -mtime +${RETENTION_DAYS} -delete -print | wc -l)

    if [ ${deleted_count} -gt 0 ]; then
        log "Deleted ${deleted_count} old backup(s)"
    else
        log "No old backups to clean up"
    fi
}

list_backups() {
    log "Current backups:"
    find "${BACKUP_DIR}" -name "guestbook_backup_*.sql.gz" -type f -exec ls -lh {} \; | sort
}

# Hauptfunktion
main() {
    log "=== Guestbook Database Backup Script ==="

    # Prüfe ob Backup-Verzeichnis existiert
    mkdir -p "${BACKUP_DIR}"

    # Warte bis Datenbank verfügbar ist
    log "Waiting for database to be ready..."
    while ! mariadb-admin ping -h "${DB_HOST}" -u "${DB_USER}" -p"${DB_PASSWORD}" --silent; do
        sleep 5
    done
    log "Database is ready"

    # Erstelle Backup
    if create_backup; then
        cleanup_old_backups
        list_backups
        log "Backup process completed successfully"
    else
        log "ERROR: Backup process failed"
        exit 1
    fi
}

# Führe Script aus wenn direkt aufgerufen
if [ "${BASH_SOURCE[0]}" == "${0}" ]; then
    main "$@"
fi
