# Changelog

Alle wichtigen Änderungen an diesem Projekt werden in dieser Datei dokumentiert.

Das Format basiert auf [Keep a Changelog](https://keepachangelog.com/de/1.0.0/),
und dieses Projekt folgt [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2025-07-29

### ✨ Hinzugefügt
- **Kommentar-Moderation**: Neue Kommentare erfordern Admin-Freischaltung
- **Vollständige Dokumentation**: README, Development Guide, Project Overview
- **Projekt-Strukturierung**: Archiv, Deployment, Config, Scripts Verzeichnisse
- **Multi-Platform Docker Images**: AMD64 und ARM64 Support
- **GitHub Container Registry**: Automatisiertes Image Building
- **Admin-Panel**: Erweiterte Verwaltungsfunktionen
- **Comment System**: Kommentarfunktion für Reviews

### 🔧 Geändert
- **Projektstruktur**: Temporäre Dateien in `archive/` verschoben
- **Docker Setup**: Combined Container für Production
- **README.md**: Vollständig überarbeitet mit professionellem Layout
- **Backend Models**: Comment-Moderation mit `is_approved` Flag
- **Frontend**: TypeScript Refactoring und neue Komponenten

### 🗂️ Organisiert
- **`archive/`**: Alle Import-Scripts und temporäre Entwicklungsdateien
- **`deployment/`**: Docker-Compose Konfigurationen für verschiedene Umgebungen
- **`docs/`**: Vollständige Projektdokumentation
- **`config/`**: Environment-Dateien zentral gesammelt
- **`scripts/`**: Utility-Scripts für Wartung

### ✅ Behoben
- **Date Display**: Korrekte Datumsanzeige für importierte Reviews
- **Comment Approval**: Neue Kommentare werden nicht sofort angezeigt
- **Docker Build**: Multi-Platform Support für verschiedene Architekturen

### 📊 Daten
- **Sample reviews** successfully imported for testing
- **Comment-System** productive ready
- **Admin-Moderation** fully functional

## [1.1.0] - 2025-07-27

### ✨ Hinzugefügt
- **Test Data Import**: Sample reviews for development
- **Date Correction**: Korrekte Datumsanzeige für alle Reviews
- **Production Deployment**: Stabile Deployment-Konfiguration

### 🔧 Geändert
- **Review Schema**: Erweitert um Import-Metadaten
- **Database Migration**: Unterstützung für Bulk-Import

## [1.0.0] - 2025-07-26

### ✨ Hinzugefügt
- **Initial Release**: Complete guestbook system
- **React Frontend**: Moderne UI mit TypeScript und TailwindCSS
- **FastAPI Backend**: RESTful API mit SQLAlchemy
- **MariaDB Database**: Persistente Datenspeicherung
- **Docker Containerization**: Vollständige Container-Lösung
- **Admin Panel**: JWT-basierte Authentifizierung
- **Image Upload**: Bildverarbeitung und -optimierung
- **Rating System**: 5-Sterne Bewertungssystem
- **Responsive Design**: Mobile und Desktop optimiert

### 🔧 Features
- **CRUD Operations**: Vollständige Review-Verwaltung
- **Pagination**: Effiziente Datennavigation  
- **Search & Filter**: Erweiterte Suchfunktionen
- **Health Checks**: Service-Überwachung
- **Rate Limiting**: Spam-Schutz
- **Input Validation**: Sicherheitsvalidierung

---

## Version Schema

- **MAJOR**: Grundlegende Architektur-Änderungen
- **MINOR**: Neue Features und Funktionalitäten  
- **PATCH**: Bugfixes und kleine Verbesserungen

## Links

- [GitHub Repository](https://github.com/baronblk/guestbook-project)
- [Container Registry](https://ghcr.io/baronblk/guestbook-project/combined)
- [Production URL](http://192.168.2.12:3000)
