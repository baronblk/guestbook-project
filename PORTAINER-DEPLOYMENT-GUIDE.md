# Gästebuch - Portainer Stack Deployment Guide

## 🚀 Deployment-Optionen für Ugree NAS

### Option 1: Einfaches Update (Empfohlen)
Verwenden Sie `portainer-stack-simple.yml` für ein direktes Update Ihres bestehenden Systems:

```yaml
# Diese Konfiguration ist identisch mit Ihrer aktuellen, 
# aber mit NODE_ENV=production für bessere Performance
```

### Option 2: Erweiterte Konfiguration (Optional)
Verwenden Sie `portainer-stack-enhanced.yml` für automatische Backups und Updates:

```yaml
# Zusätzliche Features:
# - Automatische Datenbank-Backups alle 6 Stunden
# - Watchtower für automatische Container-Updates
# - Erweiterte Logs und Monitoring
```

## 📋 Deployment-Schritte in Portainer

### 1. Vorbereitung
```bash
# Erstellen Sie die notwendigen Ordner auf Ihrem NAS:
mkdir -p /volume2/docker/guestbook/{db,uploads,backups,logs}
chmod 755 /volume2/docker/guestbook/{db,uploads,backups,logs}
```

### 2. Stack in Portainer aktualisieren

1. **Öffnen Sie Portainer** in Ihrem Browser
2. **Navigieren Sie zu "Stacks"**
3. **Wählen Sie Ihren Guestbook-Stack aus**
4. **Klicken Sie auf "Editor"**
5. **Ersetzen Sie den Inhalt** mit einer der beiden Konfigurationen unten
6. **Klicken Sie auf "Update the stack"**

### 3. Einfache Konfiguration (portainer-stack-simple.yml)

```yaml
version: "3.9"

services:
  db:
    image: mariadb:11
    restart: unless-stopped
    platform: linux/amd64
    environment:
      MYSQL_ROOT_PASSWORD: Kx9mP2vR8nQ5wE7tY3uI6oL1sA4hG9jB
      MYSQL_DATABASE: guestbook
      MYSQL_USER: guestuser
      MYSQL_PASSWORD: whHBJveMvwjs5a6p
    volumes:
      - /volume2/docker/guestbook/db:/var/lib/mysql
    healthcheck:
      test: ["CMD", "mariadb-admin", "ping", "-h", "localhost", "-u", "root", "-pKx9mP2vR8nQ5wE7tY3uI6oL1sA4hG9jB"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s
    networks:
      - guestbook-network

  app:
    image: ghcr.io/baronblk/guestbook-project/combined:2.0.0
    restart: unless-stopped
    platform: linux/amd64
    ports:
      - "3000:80"
    depends_on:
      db:
        condition: service_healthy
    environment:
      DB_HOST: db
      DB_USER: guestuser
      DB_PASSWORD: whHBJveMvwjs5a6p
      DB_NAME: guestbook
      JWT_SECRET_KEY: DeRBC3FDeY8d9nw9WMBwNJ0LpVyvB5ty607r2PHdmQBpqn
      ADMIN_USERNAME: admin
      ADMIN_EMAIL: support@dcng.de
      ADMIN_PASSWORD: whHBJveMvwjs5a6p
      NODE_ENV: production
    volumes:
      - /volume2/docker/guestbook/uploads:/app/uploads
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    networks:
      - guestbook-network

networks:
  guestbook-network:
    driver: bridge
```

## 🛡️ Erweiterte Konfiguration (Optional)

Wenn Sie automatische Backups und Updates möchten, verwenden Sie diese Konfiguration:

### Zusätzliche Features:
- ✅ **Automatische Backups** alle 6 Stunden
- ✅ **30 Tage Backup-Retention**
- ✅ **Watchtower** für automatische Updates
- ✅ **Erweiterte Logs** und Monitoring

### Backup-System:
- **Speicherort**: `/volume2/docker/guestbook/backups/`
- **Format**: `guestbook_backup_YYYYMMDD_HHMMSS.sql.gz`
- **Automatische Bereinigung**: Backups älter als 30 Tage werden gelöscht

## 🔧 Troubleshooting

### Problem: 422 Fehler beim Laden der Bewertungen

**Ursache**: Meist ein Problem mit der Datenbank-Verbindung oder fehlende Tabellen.

**Lösung**:
1. **Überprüfen Sie die Logs**:
   ```bash
   # In Portainer: Containers → guestbook_app → Logs
   ```

2. **Datenbank-Schema prüfen**:
   ```bash
   # In Portainer: Containers → guestbook_db → Console
   mariadb -u root -p
   # Passwort: Kx9mP2vR8nQ5wE7tY3uI6oL1sA4hG9jB
   
   USE guestbook;
   SHOW TABLES;
   DESCRIBE reviews;
   ```

3. **Admin-User prüfen**:
   ```sql
   SELECT * FROM admin_users;
   # Falls Fehler: Tabelle existiert nicht oder fehlt die 'role' Spalte
   
   # Falls nötig, Spalte hinzufügen:
   ALTER TABLE admin_users ADD COLUMN role ENUM('SUPERUSER', 'ADMIN', 'MODERATOR') NOT NULL DEFAULT 'ADMIN';
   ```

### Problem: Container startet nicht

**Lösung**:
1. **Ordner-Berechtigungen prüfen**:
   ```bash
   chmod -R 775 /volume2/docker/guestbook/
   chown -R 1000:1000 /volume2/docker/guestbook/
   ```

2. **Health Check Status prüfen** in Portainer

### Problem: Backup funktioniert nicht

**Lösung**:
1. **Backup-Ordner erstellen**:
   ```bash
   mkdir -p /volume2/docker/guestbook/backups
   chmod 755 /volume2/docker/guestbook/backups
   ```

2. **Backup-Service Logs prüfen** in Portainer

## 📊 Nach dem Update prüfen

1. **Website aufrufen**: `http://your-nas-ip:3000`
2. **Admin-Login testen**: 
   - Username: `admin`
   - Password: `whHBJveMvwjs5a6p`
3. **Health Status prüfen**: `http://your-nas-ip:3000/health`

## 🎯 Empfehlung

**Für sofortiges Update**: Verwenden Sie die **einfache Konfiguration**
**Für langfristige Nutzung**: Erwägen Sie die **erweiterte Konfiguration** mit Backups

## 🆘 Support

Bei Problemen:
1. Prüfen Sie die Container-Logs in Portainer
2. Stellen Sie sicher, dass alle Ordner existieren und die richtigen Berechtigungen haben
3. Kontaktieren Sie mich mit den spezifischen Fehlermeldungen
