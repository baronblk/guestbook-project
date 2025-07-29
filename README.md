# 📝 Professional Guestbook System

Ein professionelles, vollständig containerisiertes Gästebuch-System mit Admin-Panel und Kommentar-Moderation.

![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?style=flat&logo=react&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat&logo=typescript&logoColor=white)
![MariaDB](https://img.shields.io/badge/MariaDB-003545?style=flat&logo=mariadb&logoColor=white)

## 📋 Inhaltsverzeichnis

- [✨ Features](#-features)
- [🏗️ Architektur](#️-architektur)
- [🚀 Quick Start](#-quick-start)
- [📁 Projektstruktur](#-projektstruktur)
- [🔧 Konfiguration](#-konfiguration)
- [📚 API Dokumentation](#-api-dokumentation)
- [🛠️ Development](#️-development)
- [🚀 Deployment](#-deployment)
- [📖 Dokumentation](#-dokumentation)

## ✨ Features

### 🌟 Benutzer-Features
- **📝 Bewertungseinträge** mit 5-Sterne-Bewertung
- **📷 Bild-Upload** mit automatischer Optimierung
- **📱 Responsive Design** für alle Geräte
- **🔍 Such- und Filterfunktionen**
- **📄 Pagination** für große Mengen von Einträgen
- **🌐 iFrame-Einbettung** für externe Websites

### 👤 Admin-Features
- **🔐 JWT-basierte Authentifizierung**
- **✅ Kommentar-Moderation** (Freischaltung erforderlich)
- **⭐ Featured Reviews** hervorheben
- **📊 Dashboard** mit Statistiken
- **📋 CRUD-Operationen** für alle Einträge
- **💾 Export/Import-Funktionen**

### 🔧 Technische Features
- **🐳 Vollständig containerisiert** mit Docker
- **⚡ Multi-Platform Support** (AMD64/ARM64)
- **🔄 Health Checks** für alle Services
- **📈 Performance-optimiert**
- **🔒 Sicherheits-Features** (Rate Limiting, Input Validation)

## 🏗️ Architektur

- **Frontend**: React 18 + TypeScript + Zustand (State Management)
- **Backend**: FastAPI + SQLAlchemy + JWT Authentication
- **Database**: MariaDB 10.11
- **Containerization**: Docker + Docker Compose
- **Deployment**: GitHub Container Registry (GHCR) + Portainer

## ✨ Features

### 🌟 **Frontend (React + TypeScript + TailwindCSS)**
- ✅ **Bewertungsformular** mit Sterne-Rating (1-5), Name, E-Mail, Titel, Text (max. 5000 Zeichen)
- ✅ **Bild-Upload** mit automatischer Größenänderung und Optimierung
- ✅ **Live-Zeichenzähler** und Validierung
- ✅ **Bewertungsliste** mit Pagination, Filterung und Sortierung
- ✅ **Responsive Design** für Mobile/Desktop
- ✅ **iFrame-kompatible Einbettung** (`/embed`)
- ✅ **Admin-Panel** mit Login und Verwaltungsfunktionen
- ✅ **Toast-Benachrichtigungen** und Loading-States

### ⚡ **Backend (FastAPI + SQLAlchemy + Python)**
- ✅ **REST API** mit automatischer OpenAPI-Dokumentation
- ✅ **Datenbankmodelle** für Reviews und Admin-Users
- ✅ **JWT-Authentifizierung** für Admin-Zugang
- ✅ **Bild-Upload** mit Validierung und Verarbeitung (PIL)
- ✅ **Rate Limiting** gegen Spam
- ✅ **Bulk-Import** von externen Bewertungen (JSON)
- ✅ **Export-Funktion** für Datenbackups
- ✅ **Admin-Features**: Moderierung, Featured Reviews, Statistiken

### 🗄️ **Datenbank (MariaDB)**
- ✅ **Vollständiges Schema** mit Reviews, Admin-Users
- ✅ **Health Checks** und Retry-Logik
- ✅ **Persistent Storage** mit Docker Volumes

## 🚀 Installation & Setup

### Voraussetzungen
- Docker & Docker Compose
- Git

### 1. Repository klonen
```bash
git clone <repository-url>
cd guestbook-project
```

### 2. System starten
```bash
docker-compose up --build
```

### 3. Zugriff
- **Bewertungssystem**: http://localhost:3000
- **Admin-Panel**: http://localhost:3000/admin

### 4. Admin-Login
- **Username**: `admin`
- **Passwort**: `admin123`
- ⚠️ **Bitte nach dem ersten Login ändern!**

## 📁 Projektstruktur

```
guestbook-project/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI App
│   │   ├── models.py            # SQLAlchemy Models
│   │   ├── schemas.py           # Pydantic Schemas
│   │   ├── crud.py              # Database Operations
│   │   ├── database.py          # DB Connection & Config
│   │   ├── auth.py              # JWT Authentication
│   │   └── utils.py             # File Management & Utils
│   ├── uploads/                 # Uploaded Images
│   ├── wait-for-db.py          # DB Connection Wait Script
│   ├── create_admin.py         # Admin User Setup
│   ├── requirements.txt        # Python Dependencies
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/         # React Components
│   │   ├── store/             # Zustand State Management
│   │   ├── types.ts           # TypeScript Types
│   │   ├── api.ts             # API Service Layer
│   │   ├── App.tsx            # Main App Component
│   │   ├── index.tsx          # React Entry Point
│   │   └── index.css          # TailwindCSS Styles
│   ├── public/
│   ├── package.json
│   ├── tailwind.config.js
│   └── Dockerfile
└── docker-compose.yml
```

## 🔧 Konfiguration

### Umgebungsvariablen (docker-compose.yml)

#### Backend
```yaml
environment:
  DB_HOST: db
  DB_USER: guestuser
  DB_PASSWORD: guestpw
  DB_NAME: guestbook
  JWT_SECRET_KEY: your-super-secret-jwt-key-change-in-production
  ADMIN_USERNAME: admin
  ADMIN_EMAIL: admin@guestbook.local
  ADMIN_PASSWORD: admin123
```

#### Frontend
```yaml
environment:
  REACT_APP_API_URL: http://localhost:8000
```

## 📊 API-Endpunkte

### 🌐 **Öffentliche API**
- `GET /api/reviews` - Bewertungen abrufen (mit Filterung/Pagination)
- `POST /api/reviews` - Neue Bewertung erstellen
- `POST /api/reviews/{id}/image` - Bild zu Bewertung hochladen
- `GET /api/reviews/{id}` - Einzelne Bewertung abrufen
- `GET /api/stats` - Öffentliche Statistiken
- `GET /embed` - Einbettbares Widget

### 🔐 **Admin API** (JWT-Token erforderlich)
- `POST /api/admin/login` - Admin-Login
- `GET /api/admin/reviews` - Alle Bewertungen (inkl. nicht genehmigte)
- `PUT /api/admin/reviews/{id}` - Bewertung bearbeiten
- `DELETE /api/admin/reviews/{id}` - Bewertung löschen
- `POST /api/admin/reviews/import` - Bulk-Import
- `GET /api/admin/stats` - Vollständige Statistiken
- `GET /api/admin/export` - Datenexport

## 🎨 Frontend-Features

### Komponenten
- **RatingStars**: Interaktive Sterne-Bewertung
- **Pagination**: Intelligente Seitennavigation
- **ReviewForm**: Vollständiges Formular mit Validierung
- **ReviewList**: Gefilterte und sortierte Bewertungsliste
- **AdminDashboard**: Umfassendes Verwaltungspanel
- **Layout**: Responsive Hauptlayout

### State Management (Zustand)
- **ReviewStore**: Bewertungen, Filter, Pagination
- **AuthStore**: Admin-Authentifizierung mit Persistierung

### Styling (TailwindCSS)
- Responsive Design
- Custom Components & Utilities
- Dark Mode vorbereitet
- Print-Styles
- Animationen & Transitions

## 💾 Datenbank-Schema

### Reviews Table
```sql
id, name, email, rating, title, content, image_path,
created_at, updated_at, is_approved, is_featured,
admin_notes, import_source, external_id, ip_address
```

### Admin Users Table
```sql
id, username, email, hashed_password, is_active,
is_superuser, created_at, last_login
```

## 🛡️ Sicherheitsfeatures

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
2. Erstelle einen Feature Branch (`git checkout -b feature/amazing-feature`)
3. Commit deine Änderungen (`git commit -m 'Add amazing feature'`)
4. Push zum Branch (`git push origin feature/amazing-feature`)
5. Öffne einen Pull Request

## 📄 License

Dieses Projekt ist unter der [MIT License](LICENSE) lizenziert.

## 🏆 Aktueller Status

✅ **Produktiv im Einsatz**  
✅ **Kommentar-Moderation implementiert**  
✅ **Multi-Platform Docker Images**  
✅ **Vollständig dokumentiert**  

---

**Professionelles Bewertungssystem für moderne Anwendungen** 🚀
