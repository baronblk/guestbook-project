
- **JWT-Token Authentifizierung** für Admin-Bereich
- **Rate Limiting** gegen Spam (IP-basiert)
- **Input-Validierung** mit Pydantic
- **SQL-Injection Schutz** durch SQLAlchemy ORM
- **Bild-Upload Validierung** (Dateityp, Größe)
- **CORS-Konfiguration**

## 🚧 Entwicklung

### Backend-Entwicklung
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend-Entwicklung
```bash
cd frontend
npm install
npm start
```

### Database-Setup
```bash
# Admin-User erstellen
docker exec -it guestbook-project-backend-1 python create_admin.py

# Direkt zur Datenbank verbinden
docker exec -it guestbook-project-db-1 mariadb -u guestuser -p guestbook
```

## 🔄 Import/Export

### JSON-Import (Google Reviews Format)
```json
{
  "reviews": [
    {
      "name": "Max Mustermann",
      "rating": 5,
      "content": "Excellent service!",
      "title": "Great experience",
      "external_id": "google_123",
      "created_at": "2024-01-01T12:00:00Z"
    }
  ],
  "source": "google_reviews"
}
```

### Export
Über Admin-Panel → Export → JSON-Download

## 🎯 Production-Tipps

1. **Sicherheit**:
   - JWT_SECRET_KEY ändern
   - Admin-Passwort ändern
   - CORS Origins konfigurieren
   - Reverse Proxy (nginx) vorschalten

2. **Performance**:
   - Datenbank-Indizes optimieren
   - CDN für statische Assets
   - Caching implementieren

3. **Monitoring**:
   - Logs sammeln
   - Health Checks einrichten
   - Backup-Strategie

## 📱 Mobile-Optimierung

- Touch-friendly Buttons
- Responsive Formulare
- Optimierte Bildgrößen
- Progressive Web App bereit

## 🌍 Mehrsprachigkeit

Vorbereitet für i18n:
- String-Externalisierung
- Date/Number-Formatierung
- RTL-Support möglich

## 🤝 Beitragen

1. Fork das Repository
2. Feature Branch erstellen
3. Changes committen
4. Pull Request erstellen

## 📄 Lizenz

MIT License - Siehe LICENSE Datei

## 🆘 Support & Troubleshooting

### Häufige Probleme und Lösungen

#### 1. **Bilder werden nicht angezeigt** (behoben in v3.0.5)
```bash
# Problem: nginx "Permission denied" für /uploads/*
# Symptom: Hochgeladene Bilder zeigen 403-Fehler
# Lösung: Update auf v3.0.5-uploads-fix
docker pull ghcr.io/baronblk/guestbook-project:3.0.5-uploads-fix
```

#### 2. **Logs nicht in Portainer sichtbar** (behoben in v3.0.4)
```bash
# Problem: Logs werden nur in Dateien geschrieben
# Lösung: stdout/stderr Logging in v3.0.4+
# Alle Logs erscheinen jetzt im Portainer "Container Logs" Tab
```

#### 3. **422 Fehler bei externen Domains** (behoben in v3.0.3)
```bash
# Problem: TrustedHostMiddleware blockt externe Domains
# Lösung: ALLOWED_HOSTS="*" in v3.0.3+
```

### Debug-Befehle
```bash
# Container-Status prüfen
docker ps -a

# Logs anzeigen
docker logs guestbook-app-container

# In Container einsteigen
docker exec -it guestbook-app-container /bin/bash

# Upload-Berechtigungen prüfen
docker exec -it guestbook-app-container ls -la /app/uploads/

# Nginx-Konfiguration prüfen
docker exec -it guestbook-app-container cat /etc/nginx/sites-available/default
```

Bei Problemen:
1. **Logs prüfen**: Portainer Container Logs Tab oder `docker logs`
2. **Container neu starten**: `docker restart guestbook-app-container`
3. **Clean Build**: `docker-compose down && docker-compose up --build`
4. **Image Update**: `docker pull ghcr.io/baronblk/guestbook-project:3.0.5-uploads-fix`
5. **Portainer Stack**: Verwende die finale `portainer-stack.yml` für Deployment

## 🐳 Docker-Images

### Verfügbare Dockerfiles
- **`fix-uploads-permissions.dockerfile`** - Finale Version v3.0.5-uploads-fix (produktiv)
- **`Dockerfile.combined`** - Kombiniertes Frontend + Backend Image
- **`backend/Dockerfile`** - Separates Backend für Entwicklung
- **`frontend/Dockerfile`** - Separates Frontend für Entwicklung

### Build-Befehle
```bash
# Finale Version (Upload-Fix)
docker buildx build --platform linux/amd64,linux/arm64 \
  -f fix-uploads-permissions.dockerfile \
  -t ghcr.io/baronblk/guestbook-project:3.0.5-uploads-fix \
  --push .

# Kombinierte Version
docker buildx build --platform linux/amd64,linux/arm64 \
  -f Dockerfile.combined \
  -t ghcr.io/baronblk/guestbook-project:latest \
  --push .
```

---

**🎉 Viel Erfolg mit Ihrem Gästebuch-System!**
