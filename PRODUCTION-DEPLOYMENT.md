# Gästebuch - Produktions-Deployment Anleitung

## Übersicht

Diese erweiterte Konfiguration bietet maximale Datensicherheit und automatische Backup-Mechanismen für Ihr Gästebuch-System.

## Neue Features

### 1. Automatische Backups
- **Intervall**: Alle 6 Stunden
- **Retention**: 30 Tage (konfigurierbar)
- **Komprimierung**: Gzip-Komprimierung der Backups
- **Speicherort**: `/volume2/docker/guestbook/backups/`

### 2. Datenbank-Optimierungen
- **Performance**: Optimierte MariaDB-Konfiguration
- **Logging**: Slow-Query-Logging aktiviert
- **Binary Logs**: Für erweiterte Backup-/Recovery-Optionen

### 3. Monitoring & Updates
- **Watchtower**: Automatische Container-Updates
- **Health Checks**: Erweiterte Gesundheitsprüfungen
- **Logs**: Persistente Log-Speicherung

## Ordnerstruktur

```
/volume2/docker/guestbook/
├── db/          # Haupt-Datenbank (wie bisher)
├── uploads/     # Upload-Dateien (wie bisher)
├── backups/     # Automatische DB-Backups (NEU)
└── logs/        # Anwendungs-Logs (NEU)
```

## Deployment-Optionen

### Option 1: Erweiterte Produktion (Empfohlen)
```bash
# Starte mit erweiterter Konfiguration
docker-compose -f docker-compose.production.yml up -d

# Oder verwende das Deployment-Script
./scripts/deploy-production.sh
```

### Option 2: Bestehende Konfiguration
```bash
# Bestehende Konfiguration weiter verwenden
docker-compose -f docker-compose.combined.yml up -d
```

## Backup & Recovery

### Automatische Backups
- Backups werden automatisch alle 6 Stunden erstellt
- Format: `guestbook_backup_YYYYMMDD_HHMMSS.sql.gz`
- Alte Backups werden nach 30 Tagen automatisch gelöscht

### Manuelles Backup
```bash
# Manuelles Backup erstellen
docker-compose -f docker-compose.production.yml exec db-backup /backup.sh
```

### Backup wiederherstellen
```bash
# Verfügbare Backups anzeigen
docker-compose -f docker-compose.production.yml exec db-backup ls -la /backups/

# Backup wiederherstellen
docker-compose -f docker-compose.production.yml exec db-backup /restore.sh guestbook_backup_YYYYMMDD_HHMMSS.sql.gz
```

## Update-Prozess

### Automatischer Update (Empfohlen)
```bash
# Sicheres Update mit automatischem Backup
./scripts/deploy-production.sh update
```

### Manueller Update
```bash
# 1. Backup erstellen (optional aber empfohlen)
./scripts/deploy-production.sh backup

# 2. Neue Images pullen
docker-compose -f docker-compose.production.yml pull

# 3. Services neu starten (Datenbank bleibt online)
docker-compose -f docker-compose.production.yml up -d
```

## Daten-Persistenz Garantie

### Volumen-Mounts
```yaml
# Datenbank-Daten (unveränderlich)
- /volume2/docker/guestbook/db:/var/lib/mysql

# Upload-Dateien (unveränderlich) 
- /volume2/docker/guestbook/uploads:/app/uploads

# Backup-Dateien (neu)
- /volume2/docker/guestbook/backups:/backups
```

### Container-Update Sicherheit
1. **Datenbank**: Läuft in separatem Container mit persistentem Volume
2. **Uploads**: Externe Speicherung bleibt erhalten
3. **Backups**: Zusätzliche Sicherheitsebene
4. **Rolling Updates**: Nur App-Container wird neu gestartet

## Monitoring & Wartung

### Service-Status prüfen
```bash
# Aktueller Status
./scripts/deploy-production.sh status

# Docker Compose Status
docker-compose -f docker-compose.production.yml ps

# Logs einsehen
docker-compose -f docker-compose.production.yml logs -f app
```

### Backup-Status prüfen
```bash
# Backup-Logs einsehen
docker-compose -f docker-compose.production.yml logs db-backup

# Backup-Dateien auflisten
ls -la /volume2/docker/guestbook/backups/
```

## Konfiguration anpassen

### Backup-Intervall ändern
```yaml
# In docker-compose.production.yml
# Ändere: sleep 21600  (6 Stunden)
# Zu:     sleep 3600   (1 Stunde)
# Oder:   sleep 43200  (12 Stunden)
```

### Backup-Retention ändern
```yaml
environment:
  BACKUP_RETENTION_DAYS: 60  # Backups 60 Tage behalten
```

### E-Mail-Benachrichtigungen aktivieren
```yaml
# In watchtower Service
environment:
  WATCHTOWER_NOTIFICATIONS: email
  WATCHTOWER_NOTIFICATION_EMAIL_FROM: system@yourdomain.com
  WATCHTOWER_NOTIFICATION_EMAIL_TO: admin@yourdomain.com
  WATCHTOWER_NOTIFICATION_EMAIL_SERVER: smtp.gmail.com
  WATCHTOWER_NOTIFICATION_EMAIL_SERVER_PORT: 587
  WATCHTOWER_NOTIFICATION_EMAIL_SERVER_USER: your-email@gmail.com
  WATCHTOWER_NOTIFICATION_EMAIL_SERVER_PASSWORD: your-app-password
```

## Troubleshooting

### Backup-Service funktioniert nicht
```bash
# Backup-Service-Logs prüfen
docker-compose -f docker-compose.production.yml logs db-backup

# Manuell testen
docker-compose -f docker-compose.production.yml exec db-backup /backup.sh
```

### Datenbank-Verbindungsprobleme
```bash
# Datenbank-Health prüfen
docker-compose -f docker-compose.production.yml exec db mariadb-admin ping -h localhost -u root -p

# Datenbank-Logs prüfen
docker-compose -f docker-compose.production.yml logs db
```

### Disk-Space prüfen
```bash
# Backup-Ordner-Größe prüfen
du -sh /volume2/docker/guestbook/backups/

# Alte Backups manuell löschen
find /volume2/docker/guestbook/backups/ -name "*.sql.gz" -mtime +30 -delete
```

## Migration von bestehender Installation

Wenn Sie bereits die `docker-compose.combined.yml` verwenden:

1. **Stoppen Sie die Services**:
   ```bash
   docker-compose -f docker-compose.combined.yml down
   ```

2. **Erstellen Sie die neuen Ordner**:
   ```bash
   mkdir -p /volume2/docker/guestbook/{backups,logs}
   ```

3. **Starten Sie mit neuer Konfiguration**:
   ```bash
   docker-compose -f docker-compose.production.yml up -d
   ```

4. **Prüfen Sie den Status**:
   ```bash
   ./scripts/deploy-production.sh status
   ```

## Sicherheitshinweise

- **Passwörter**: Ändern Sie alle Standard-Passwörter
- **Firewall**: Beschränken Sie Zugriff auf Port 3000
- **SSL/TLS**: Verwenden Sie einen Reverse-Proxy mit SSL
- **Backups**: Prüfen Sie regelmäßig die Backup-Integrität
- **Updates**: Lassen Sie Watchtower für automatische Sicherheitsupdates aktiviert

## Support

Bei Problemen:
1. Prüfen Sie die Logs: `./scripts/deploy-production.sh status`
2. Erstellen Sie ein Backup: `./scripts/deploy-production.sh backup`
3. Kontaktieren Sie den Support mit den Log-Ausgaben
