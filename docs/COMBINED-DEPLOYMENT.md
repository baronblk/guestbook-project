# Guestbook Combined Container - Deployment Guide

## Problem gelöst: Network Error

Das ursprüngliche Problem mit "Network error" beim Laden der Reviews lag an der komplexen NGINX Proxy Manager Konfiguration, die versucht hat, Frontend und Backend getrennt zu routen.

## Lösung: Combined Container

Diese neue Lösung kombiniert Frontend und Backend in einem einzigen Container:

### Architektur

- **Ein Container**: Enthält sowohl React Frontend als auch FastAPI Backend
- **Nginx**: Läuft innerhalb des Containers und routet Anfragen
  - `/` → React Frontend (statische Dateien)
  - `/api/` → FastAPI Backend (localhost:8000)
- **Supervisor**: Verwaltet sowohl nginx als auch FastAPI Prozesse
- **Port**: Container exponsiert Port 80

### Dateien

1. **Dockerfile.combined**: Multi-stage Build für Frontend und Backend
2. **nginx.conf**: Interne Nginx Konfiguration
3. **supervisord.conf**: Prozess-Management
4. **docker-compose.combined.yml**: Deployment Konfiguration
5. **frontend/src/api.ts**: Angepasst für relative URLs

### Deployment auf Synology NAS

#### 1. Alten Stack stoppen
1. In Portainer den bestehenden `guestbook` Stack stoppen
2. Container entfernen (Daten bleiben erhalten)

#### 2. Neuen Stack erstellen
1. In Portainer einen neuen Stack erstellen
2. Name: `guestbook-combined`
3. Docker Compose Datei verwenden: `docker-compose.combined.yml`

#### 3. NGINX Proxy Manager vereinfachen
Da nur noch ein Container läuft, ist die NGINX Konfiguration viel einfacher:

**Proxy Host Settings:**
- Domain: `guestbook.dein-domain.de`
- Scheme: `http`
- Forward Hostname/IP: `IP-der-Synology`
- Forward Port: `3000`
- Block Common Exploits: ✓
- Websockets Support: ✓

**Keine komplexe API-Routing-Konfiguration mehr nötig!**

### Vorteile

1. **Keine API Routing Probleme**: Alle Anfragen gehen an einen Container
2. **Einfachere NGINX Konfiguration**: Nur ein einziger Proxy Host
3. **Relative API URLs**: Frontend nutzt relative Pfade
4. **Ein Image**: Einfacheres Deployment und Management
5. **Interne Kommunikation**: Frontend und Backend kommunizieren über localhost

### Migration

1. **Daten sichern**: Uploads und Database werden über Volumes gesichert
2. **Alten Stack stoppen**: In Portainer
3. **Neuen Stack starten**: Mit `docker-compose.combined.yml`
4. **NGINX Proxy Manager**: Konfiguration vereinfachen
5. **Testen**: Alle Funktionen prüfen

Die Volumes bleiben erhalten, so dass keine Daten verloren gehen.

### Image verfügbar

Das kombinierte Image ist bereits gebaut und verfügbar:
```
ghcr.io/baronblk/guestbook-project/combined:latest
```

Ready für Deployment!
