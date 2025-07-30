# 🚀 Deployment Guide: Docker Desktop + GHCR.io + UGreen NAS

Dieses Handbuch beschreibt den kompletten Workflow von der lokalen Entwicklung bis zum Production-Deployment.

## 🏗️ Development Setup (Docker Desktop auf Mac)

### Voraussetzungen
- Docker Desktop für Mac installiert
- Git Repository geklont
- VS Code mit empfohlenen Extensions

### Lokale Entwicklung starten

```bash
# Option 1: Standard Development
docker-compose up --build

# Option 2: Development mit Hot Reload
docker-compose -f docker-compose.dev.yml up --build

# Option 3: Nur Services ohne Hot Reload
docker-compose -f docker-compose.yml up --build
```

### Development URLs
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **phpMyAdmin**: http://localhost:8080 (nur bei dev.yml)
- **Database**: localhost:3306

### Development-Features
- ✅ Hot Reload für Backend (FastAPI)
- ✅ Hot Reload für Frontend (React)
- ✅ Volume-Mounting für Live-Code-Editing
- ✅ phpMyAdmin für DB-Management
- ✅ Debugging über VS Code möglich

---

## 🔄 CI/CD Pipeline (GitHub Actions → GHCR.io)

### Automatischer Build-Prozess

1. **Push zu `master`** → Triggert CI/CD Pipeline
2. **Tests ausführen** → Python + Node.js Tests
3. **Images bauen** → Multi-Platform (AMD64 + ARM64)
4. **Push zu GHCR.io** → `ghcr.io/baronblk/guestbook-project/`
5. **Portainer-Dateien generieren** → Als Artifacts verfügbar

### Verfügbare Images
```bash
# Backend
ghcr.io/baronblk/guestbook-project/backend:latest
ghcr.io/baronblk/guestbook-project/backend:master
ghcr.io/baronblk/guestbook-project/backend:v1.0.0

# Frontend  
ghcr.io/baronblk/guestbook-project/frontend:latest
ghcr.io/baronblk/guestbook-project/frontend:master
ghcr.io/baronblk/guestbook-project/frontend:v1.0.0
```

### Release-Workflow
```bash
# Tag für Release erstellen
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0

# → Triggert automatisch:
# - Build + Push der Images mit Version-Tags
# - GitHub Release mit Deployment-Dateien
# - Portainer Stack-Dateien als Download
```

---

## 📦 Production Deployment (UGreen NAS + Portainer)

### 1. Portainer Stack vorbereiten

#### Option A: Von GitHub Release herunterladen
1. Gehe zu [Releases](https://github.com/baronblk/guestbook-project/releases)
2. Lade `portainer-deployment.zip` herunter
3. Entpacke die Dateien

#### Option B: Lokale Datei verwenden
```bash
# Verwende docker-compose.portainer.yml aus dem Repository
```

### 2. Portainer Stack erstellen

1. **Portainer öffnen** → http://YOUR-NAS-IP:9000
2. **Stacks** → **Add Stack**
3. **Name**: `guestbook-project`
4. **Build method**: Web editor
5. **Inhalt kopieren** aus `docker-compose.portainer.yml`

### 3. Environment Variables setzen

Füge diese Variables in Portainer hinzu:

```env
# Database Credentials
DB_PASSWORD=your-secure-db-password-here
MYSQL_ROOT_PASSWORD=your-secure-root-password-here

# JWT Security
JWT_SECRET_KEY=your-super-secret-jwt-key-change-in-production

# Admin Account
ADMIN_USERNAME=admin
ADMIN_EMAIL=admin@guestbook.local
ADMIN_PASSWORD=your-secure-admin-password-here

# Network Configuration (Ersetze YOUR-NAS-IP)
REACT_APP_API_URL=http://192.168.1.100:8000
FRONTEND_PORT=3000
BACKEND_PORT=8000
```

### 4. Stack deployen

1. **Deploy the stack** klicken
2. Warten bis alle Services gestartet sind
3. **Logs prüfen** für eventuelle Fehler

### 5. Services testen

```bash
# Frontend testen
curl http://YOUR-NAS-IP:3000

# Backend API testen  
curl http://YOUR-NAS-IP:8000/health

# API Dokumentation
open http://YOUR-NAS-IP:8000/docs
```

---

## 🔧 Konfiguration & Anpassungen

### Port-Anpassungen für NAS

Falls Standard-Ports belegt sind:

```env
# Custom Ports
FRONTEND_PORT=8080
BACKEND_PORT=8001
REACT_APP_API_URL=http://192.168.1.100:8001
```

### Reverse Proxy (Nginx/Traefik)

Für Domain-basierte Zugriffe:

```yaml
# Zusätzliche Labels für Traefik
labels:
  - "traefik.enable=true"
  - "traefik.http.routers.guestbook.rule=Host(`guestbook.yourdomain.com`)"
  - "traefik.http.routers.guestbook.tls=true"
```

### SSL/HTTPS Setup

1. **Certbot** für Let's Encrypt Zertifikate
2. **Nginx** als Reverse Proxy vor Portainer Stack
3. **Environment Variable** anpassen:
   ```env
   REACT_APP_API_URL=https://api.guestbook.yourdomain.com
   ```

---

## 📊 Monitoring & Maintenance

### Logs einsehen

```bash
# Portainer: Stack → Services → Container-Logs

# Oder via Docker CLI auf NAS:
docker logs guestbook-project_backend_1
docker logs guestbook-project_frontend_1
docker logs guestbook-project_db_1
```

### Database Backup

```bash
# Manueller Backup
docker exec guestbook-project_db_1 mysqldump -u guestuser -p guestbook > backup.sql

# Automatischer Backup (läuft bereits im Stack)
# Siehe backup_data Volume
```

### Updates durchführen

```bash
# In Portainer:
# 1. Stack → Editor
# 2. Image-Tags ändern (z.B. :latest → :v1.1.0)  
# 3. "Update the stack" klicken
```

### Resource-Monitoring

Die Portainer Stack-Datei enthält Resource-Limits:

- **Backend**: 512M RAM, 0.5 CPU
- **Frontend**: 256M RAM, 0.25 CPU  
- **Database**: 1G RAM, 1.0 CPU

---

## 🚨 Troubleshooting

### Häufige Probleme

**1. Frontend kann Backend nicht erreichen**
```bash
# Prüfe REACT_APP_API_URL Environment Variable
# Stelle sicher, dass NAS-IP korrekt ist
```

**2. Database Connection Failed**
```bash
# Prüfe Database Health Check
# Warte bis MariaDB vollständig gestartet ist
```

**3. Images können nicht gepullt werden**
```bash
# Prüfe ob GHCR.io Images public sind
# GitHub Token in Secrets vorhanden?
```

**4. Permission Errors**
```bash
# Prüfe Volume-Permissions auf NAS
# Stelle sicher dass Docker User Schreibrechte hat
```

### Debug-Befehle

```bash
# Services Status prüfen
docker ps

# Container-Details einsehen
docker inspect container_name

# Netzwerk prüfen
docker network ls
docker network inspect guestbook-project_guestbook-network

# Volumes prüfen
docker volume ls
docker volume inspect guestbook-project_db_data
```

---

## 📝 Deployment Checklist

### Vor dem ersten Deployment
- [ ] GitHub Repository ist public oder PAT ist gesetzt
- [ ] CI/CD Pipeline ist erfolgreich durchgelaufen
- [ ] Images sind auf GHCR.io verfügbar
- [ ] NAS-IP ist bekannt und erreichbar
- [ ] Portainer ist installiert und läuft

### Deployment Schritte
- [ ] Environment Variables sind gesetzt
- [ ] Sichere Passwörter sind gewählt
- [ ] docker-compose.portainer.yml ist aktuell
- [ ] Stack wurde erfolgreich deployed
- [ ] Health Checks sind grün
- [ ] Frontend und Backend sind erreichbar

### Nach dem Deployment
- [ ] Admin-Login funktioniert
- [ ] Datei-Upload funktioniert
- [ ] Database Backups sind aktiv
- [ ] Monitoring ist eingerichtet
- [ ] SSL/HTTPS ist konfiguriert (optional)

---

## 🎯 Best Practices

### Security
- ✅ Starke Passwörter für alle Services
- ✅ JWT-Secret regelmäßig rotieren
- ✅ Database nicht öffentlich exponieren
- ✅ Reverse Proxy mit SSL verwenden
- ✅ Regelmäßige Updates der Images

### Performance
- ✅ Resource-Limits definiert
- ✅ Health Checks implementiert
- ✅ Multi-Platform Images (ARM64 + AMD64)
- ✅ Optimierte MariaDB-Konfiguration
- ✅ Volume-Mounting für Persistenz

### Maintenance
- ✅ Automatische Backups
- ✅ Log-Rotation aktiviert
- ✅ Monitoring eingerichtet
- ✅ Update-Strategie definiert
- ✅ Rollback-Plan vorhanden

**Happy Deploying! 🚀**
