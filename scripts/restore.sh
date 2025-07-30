#!/bin/bash

# Restore Script für Gästebuch-Datenbank
# Stellt eine Backup-Datei wieder her

set -e

# Konfiguration
DB_HOST=${DB_HOST:-db}
DB_USER=${DB_USER:-root}
DB_PASSWORD=${DB_PASSWORD}
DB_NAME=${DB_NAME:-guestbook}
BACKUP_DIR="/backups"

# Funktionen
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

usage() {
    echo "Usage: $0 <backup-file>"
    echo ""
    echo "Restore a database backup from a compressed SQL file."
    echo ""
    echo "Available backups:"
    find "${BACKUP_DIR}" -name "guestbook_backup_*.sql.gz" -type f -exec basename {} \; | sort -r | head -10
    echo ""
    echo "Example:"
    echo "  $0 guestbook_backup_20240130_120000.sql.gz"
}

restore_backup() {
    local backup_file="$1"
    local full_path="${BACKUP_DIR}/${backup_file}"

    # Prüfe ob Backup-Datei existiert
    if [ ! -f "$full_path" ]; then
        log "ERROR: Backup file not found: $full_path"
        return 1
    fi

    log "Starting restore from ${backup_file}"
    log "WARNING: This will overwrite the current database!"

    # Frage nach Bestätigung (nur wenn interaktiv)
    if [ -t 0 ]; then
        read -p "Are you sure you want to continue? (yes/no): " confirm
        if [ "$confirm" != "yes" ]; then
            log "Restore cancelled by user"
            return 1
        fi
    fi

    # Warte bis Datenbank verfügbar ist
    log "Waiting for database to be ready..."
    while ! mariadb-admin ping -h "${DB_HOST}" -u "${DB_USER}" -p"${DB_PASSWORD}" --silent; do
        sleep 5
    done
    log "Database is ready"

    # Erstelle temporäre Kopie der Datenbank
    local temp_db="guestbook_backup_$(date +%s)"
    log "Creating temporary backup of current database as '${temp_db}'"

    mariadb -h "${DB_HOST}" -u "${DB_USER}" -p"${DB_PASSWORD}" -e "CREATE DATABASE ${temp_db};"
    mariadb-dump -h "${DB_HOST}" -u "${DB_USER}" -p"${DB_PASSWORD}" --single-transaction "${DB_NAME}" | \
        mariadb -h "${DB_HOST}" -u "${DB_USER}" -p"${DB_PASSWORD}" "${temp_db}"

    # Restore das Backup
    log "Restoring backup..."

    if zcat "$full_path" | mariadb -h "${DB_HOST}" -u "${DB_USER}" -p"${DB_PASSWORD}" "${DB_NAME}"; then
        log "Restore completed successfully"

        # Lösche temporäre Backup-Datenbank
        log "Removing temporary backup database"
        mariadb -h "${DB_HOST}" -u "${DB_USER}" -p"${DB_PASSWORD}" -e "DROP DATABASE ${temp_db};"

        return 0
    else
        log "ERROR: Restore failed!"
        log "Restoring from temporary backup..."

        # Restore von temporärer Datenbank
        mariadb-dump -h "${DB_HOST}" -u "${DB_USER}" -p"${DB_PASSWORD}" --single-transaction "${temp_db}" | \
            mariadb -h "${DB_HOST}" -u "${DB_USER}" -p"${DB_PASSWORD}" "${DB_NAME}"

        # Lösche temporäre Backup-Datenbank
        mariadb -h "${DB_HOST}" -u "${DB_USER}" -p"${DB_PASSWORD}" -e "DROP DATABASE ${temp_db};"

        log "Original database restored from temporary backup"
        return 1
    fi
}

# Hauptfunktion
main() {
    log "=== Guestbook Database Restore Script ==="

    if [ $# -ne 1 ]; then
        usage
        exit 1
    fi

    local backup_file="$1"

    if restore_backup "$backup_file"; then
        log "Restore process completed successfully"
    else
        log "ERROR: Restore process failed"
        exit 1
    fi
}

# Führe Script aus wenn direkt aufgerufen
if [ "${BASH_SOURCE[0]}" == "${0}" ]; then
    main "$@"
fi
