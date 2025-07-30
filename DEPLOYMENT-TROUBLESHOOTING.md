# Guestbook Deployment Troubleshooting

## ✅ Aktuelle Problembehebungen

### Problem 1: Database Container ist unhealthy
**Ursache:** Falsche MariaDB-Variablen oder Volume-Berechtigungen  
**Lösung:** Verwende die korrigierten Stack-Dateien mit Docker Named Volumes

### Problem 2: API 400 Bad Request Fehler
**Ursache:** Backend startet nicht korrekt aufgrund falscher Pfade  
**Lösung:** Korrigierte supervisord-Konfiguration in Version 2.0.1

## 📁 Verfügbare Deployment-Dateien

### 1. `portainer-stack-fixed.yml` ⭐ **EMPFOHLEN**
- **Zweck:** Produktive Deployment mit korrigierten Einstellungen
- **Features:** 
  - Docker Named Volumes (automatisch persistent)
  - Korrigierte MariaDB-Umgebungsvariablen
  - Backend-Fix für Version 2.0.1
  - CORS-Unterstützung für alle Origins

### 2. `portainer-stack-debug.yml`
- **Zweck:** Debugging und Problemdiagnose
- **Features:**
  - Erweiterte Health Checks
  - Database Port 3306 für externe Verbindungen
  - Debug-Logging aktiviert
  - Verlängerte Startup-Zeiten

### 3. `portainer-stack-enhanced.yml` 
- **Zweck:** Enterprise-Features (nach Grundfunktion getestet)
- **Features:**
  - Automatische Backups
  - Watchtower für Updates
  - Erweiterte Logging

## 🚀 Deployment-Schritte

### Schritt 1: Stack in Portainer erstellen
1. Öffne Portainer
2. Gehe zu "Stacks" → "Add stack"
3. Namen eingeben: `guestbook-prod`
4. Inhalt von `portainer-stack-fixed.yml` einfügen

### Schritt 2: Deployment überwachen
1. Prüfe Container-Status in Portainer
2. Schaue in die Logs wenn Probleme auftreten
3. Verwende Health Checks zum Status überprüfen

### Schritt 3: Anwendung testen
1. Öffne `http://YOUR-NAS-IP:3000`
2. Teste Gästebuch-Funktionen
3. Teste Admin-Login: `admin` / `whHBJveMvwjs5a6p`

## 🔧 Troubleshooting-Kommandos

### Container Logs anzeigen
```bash
# In Portainer → Container → Logs
# Oder via Docker CLI:
docker logs guestbook-prod_app_1
docker logs guestbook-prod_db_1
```

### Health Status prüfen
```bash
docker ps --format "table {{.Names}}\t{{.Status}}"
```

### Database-Verbindung testen
```bash
# Nur wenn Debug-Stack mit Port 3306 verwendet wird
mysql -h YOUR-NAS-IP -P 3306 -u guestuser -pwhHBJveMvwjs5a6p guestbook
```

## 📝 Bekannte Probleme und Lösungen

### 1. "no matching manifest for linux/amd64"
- **Lösung:** Verwende Version 2.0.1 (bereits in allen Stacks konfiguriert)

### 2. "dependency failed to start: container is unhealthy"
- **Lösung:** 
  1. Verwende `portainer-stack-fixed.yml`
  2. Warte 2-3 Minuten für Database-Initialisierung
  3. Prüfe Database-Logs für Details

### 3. "Failed to load reviews" - API 400 Fehler
- **Lösung:** 
  1. Verwende Version 2.0.1 Image
  2. Prüfe App-Container-Logs
  3. Verwende CORS `*` Setting

### 4. Admin-Login funktioniert nicht
- **Lösung:**
  1. Username: `admin`
  2. Password: `whHBJveMvwjs5a6p`
  3. Nach Deployment 1-2 Minuten warten

## 📊 Monitoring

### Container Health Status
- Database: Sollte "healthy" sein nach 60-90s
- App: Sollte "healthy" sein nach 40-60s

### Erwartete Ports
- **3000:** Hauptanwendung (nginx + frontend)
- **3306:** Database (nur im Debug-Stack)

### Log-Levels
- **Production:** INFO
- **Debug:** DEBUG
- **Database:** Standard MariaDB Logging

## 🔄 Updates

### Neue Version deployen
1. Stoppe den Stack in Portainer
2. Ändere Image-Version in der Stack-Konfiguration
3. Starte den Stack neu
4. Volumes bleiben persistent!

### Backup vor Updates
- Database-Daten: Automatisch in `guestbook-backup-data` Volume
- Uploads: Persistent in `guestbook-upload-data` Volume

## ⚠️ Wichtige Hinweise

1. **Volumes sind persistent:** Daten gehen nicht verloren bei Container-Updates
2. **Health Checks:** Warte bis Container "healthy" sind bevor du Probleme meldest
3. **Logs:** Schaue immer zuerst in die Container-Logs bei Problemen
4. **Ports:** Port 3000 muss auf dem NAS verfügbar sein

## 📞 Support

Bei weiteren Problemen:
1. Sammle Container-Logs
2. Screenshot von Portainer Stack Status
3. Beschreibe genaue Fehlermeldung
4. URL und Browser-Info
