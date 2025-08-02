# Lokales Testing Setup

Dieses Verzeichnis enthält Scripts und Konfigurationen für einfaches lokales Testing des Gästebuch-Systems.

## 🚀 Schnellstart

### Option 1: Entwicklungsmodus (empfohlen für Testing)
```bash
cd testing
./start-dev.sh
```
- **Einfache Credentials:** admin / admin123
- **Security deaktiviert** für einfaches Testing
- **Keine Rate Limits**

### Option 2: Produktionsähnlich
```bash
cd testing
./start.sh
```
- **Sichere Credentials:** admin / whHBJveMvwjs5a6p
- **Vollständige Security Features**
- **Rate Limiting aktiv**

## 📋 Verfügbare Scripts

### Basis-Scripts
- `start-dev.sh` - 🧪 **Entwicklungsmodus** (einfache Credentials, keine Security)
- `start.sh` - 🔒 Produktionsähnliches Setup
- `stop.sh` - 🛑 Stoppt alle Container
- `restart.sh` - 🔄 Neustart des Systems
- `quick-start.sh` - ⚡ Quick Setup mit Checks

### Build & Maintenance
- `rebuild.sh` - 🔨 Rebuild des Docker Images und Neustart
- `reset-security.sh` - 🔓 Setzt Security Monitoring zurück

### Testing & Debugging
- `test-login.sh` - 🔐 Testet das Admin Login
- `logs.sh` - 📋 Zeigt aktuelle Logs an
- `db-shell.sh` - 🗄️ Öffnet eine Datenbank-Shell

## 🔑 Admin Credentials

### Entwicklungsmodus (`start-dev.sh`)
- **Username:** `admin`
- **Password:** `admin123`
- **Einfach zu merken für Testing!**

### Produktionsmodus (`start.sh`)
- **Username:** `admin`
- **Password:** `whHBJveMvwjs5a6p`
- **Sicher generiert**

## 🌐 URLs

- **Frontend:** http://localhost:8080
- **Admin Panel:** http://localhost:8080/admin
- **API Docs:** http://localhost:8080/docs

## 🛠️ Troubleshooting

### Rate Limit Probleme
```bash
./reset-security.sh
```

### Login funktioniert nicht
```bash
./test-login.sh
```

### System komplett neu aufsetzen
```bash
./stop.sh
./rebuild.sh
```

### Logs anschauen
```bash
./logs.sh
```

## 📁 Konfigurationen

- `docker-compose.dev.yml` - Entwicklungskonfiguration (unsicher, aber einfach)
- Standard verwendet `../docker-compose.test.yml` (produktionsähnlich)

# Schnellstart für Testing
cd testing
./start.sh

# Login testen
./test-login.sh

# Bei Problemen
./reset-security.sh
./logs.sh

# System stoppen
./stop.sh
