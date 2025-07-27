# 🚀 Guestbook Deployment auf NAS mit Portainer

## 📋 Voraussetzungen

- ✅ Portainer auf Ihrem NAS installiert
- ✅ Docker und Docker Compose auf dem NAS verfügbar
- ✅ GitHub Container Registry (GHCR) Zugriff

## 🔧 1. GitHub Actions Workflow ausführen

### 1.1 Repository Secrets konfigurieren
Gehen Sie zu GitHub → Settings → Secrets and variables → Actions:

```
GITHUB_TOKEN: [Ihr GitHub Personal Access Token mit packages:write]
```

### 1.2 Workflow triggern
```bash
# Container bauen und zu GHCR hochladen
git add .
git commit -m "Production deployment ready"
git push origin main
```

Die GitHub Actions bauen automatisch die Container und laden sie zu GHCR hoch.

## 🐳 2. Portainer Stack Deployment

### 2.1 In Portainer einloggen
Öffnen Sie Portainer auf Ihrem NAS (normalerweise Port 9000).

### 2.2 Neuen Stack erstellen
1. **Stacks** → **Add stack**
2. **Name**: `guestbook-production`
3. **Build method**: `Web editor`

### 2.3 Stack-Konfiguration einfügen
Kopieren Sie den Inhalt von `portainer-stack.yml` in den Web Editor.

### 2.4 Environment Variables konfigurieren
Scrollen Sie nach unten zu **Environment variables** und fügen Sie hinzu:

```env
# Repository Info
GITHUB_REPOSITORY=baronblk/guestbook-project
IMAGE_TAG=latest

# Database
DB_NAME=guestbook
DB_USER=guestbook_user
DB_PASSWORD=IhrSicheresPassword123
DB_ROOT_PASSWORD=IhrSuperSicheresRootPassword456

# Admin User
ADMIN_USERNAME=admin
ADMIN_EMAIL=admin@ihredomain.de
ADMIN_PASSWORD=AdminPassword789

# Security (WICHTIG: Ändern Sie diese Werte!)
SECRET_KEY=ihr-super-geheimer-schluessel-xyz123
JWT_SECRET=ihr-jwt-geheimer-schluessel-abc456

# Network (Anpassen an Ihre NAS-IP)
FRONTEND_PORT=80
REACT_APP_API_URL=http://192.168.1.100:8000
API_CORS_ORIGINS=http://localhost,http://192.168.1.100
```

**⚠️ WICHTIG**: Ersetzen Sie `192.168.1.100` mit der IP-Adresse Ihres NAS!

### 2.5 Stack deployen
Klicken Sie auf **Deploy the stack**.

## 🌐 3. Zugriff auf die Anwendung

Nach erfolgreichem Deployment:

- **Frontend**: `http://ihre-nas-ip` (Port 80)
- **Backend API**: `http://ihre-nas-ip:8000`
- **Admin Login**: 
  - URL: `http://ihre-nas-ip/admin`
  - Benutzername: `admin` (oder wie konfiguriert)
  - Passwort: Ihr `ADMIN_PASSWORD`

## 🔍 4. Monitoring und Logs

### 4.1 Container Status prüfen
In Portainer → Stacks → guestbook-production → Container anzeigen

### 4.2 Logs anzeigen
Klicken Sie auf einen Container → **Logs** Tab

### 4.3 Health Checks
Alle Services haben Health Checks konfiguriert:
- ✅ Grün: Service läuft korrekt
- ❌ Rot: Service hat Probleme

## 🔧 5. Wartung und Updates

### 5.1 Container Updates
1. Neuen Code zu GitHub pushen
2. GitHub Actions bauen neue Images
3. In Portainer: Stack → **Update the stack** → **Pull and redeploy**

### 5.2 Datenbank Backup
```bash
# In Portainer Terminal des MariaDB Containers
mysqldump -u root -p guestbook > backup.sql
```

### 5.3 Volume Management
Persistente Daten werden in Docker Volumes gespeichert:
- `mariadb_data`: Datenbankdaten
- `backend_uploads`: Hochgeladene Dateien

## 🛠️ 6. Troubleshooting

### Problem: Container starten nicht
- **Lösung**: Prüfen Sie die Environment Variables
- **Log-Check**: Portainer → Container → Logs

### Problem: Frontend kann Backend nicht erreichen
- **Lösung**: `REACT_APP_API_URL` und `API_CORS_ORIGINS` prüfen
- **Network-Check**: Beide Container im gleichen Netzwerk?

### Problem: Datenbankverbindung fehlgeschlagen
- **Lösung**: MariaDB Health Check abwarten (kann bis zu 30 Sekunden dauern)
- **Passwort-Check**: `DB_PASSWORD` korrekt?

### Problem: Images nicht gefunden
- **Lösung**: GitHub Actions erfolgreich durchgelaufen?
- **Registry-Check**: Images in GHCR verfügbar?

## 🔒 7. Sicherheitshinweise

1. **Secrets ändern**: Verwenden Sie starke, einzigartige Passwörter
2. **Network Security**: Verwenden Sie Reverse Proxy für HTTPS
3. **Firewall**: Nur notwendige Ports öffentlich verfügbar machen
4. **Updates**: Regelmäßig Container-Images aktualisieren

## 📞 Support

Bei Problemen prüfen Sie:
1. Portainer Logs der Container
2. GitHub Actions Status
3. NAS Docker Service Status

Happy Deploying! 🎉
