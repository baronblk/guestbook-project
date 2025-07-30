# Changelog

Alle wichtigen Änderungen an diesem Projekt werden in dieser Datei dokumentiert.

Das Format basiert auf [Keep a Changelog](https://keepachangelog.com/de/1.0.0/),
und dieses Projekt folgt [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Repository nach Best Practices bereinigt
- .gitignore für Python, Node.js und temporäre Dateien ergänzt
- GitHub Workflows für CI/CD, Security und Dependency Updates
- Kommentar-System mit CRUD-Operationen
- Admin-Dashboard für Kommentar-Management
- Projekt-Dokumentation erweitert (CHANGELOG, CONTRIBUTING, docs/)
- Archive-Ordner für temporäre Import-Skripte

### Changed
- Temporäre Import-Skripte ins archive/ Verzeichnis verschoben
- Frontend um Admin-Dashboard und Kommentar-Funktionen erweitert

### Removed
- Build-Ordner, node_modules und sensible Dateien aus Versionierung entfernt
- Temporäre Import-Skripte aus Hauptverzeichnis entfernt

## [1.0.0] - 2025-07-30

### Added
- Vollständiges Gästebuch-System mit React Frontend und FastAPI Backend
- MariaDB Datenbank-Integration
- Docker-Container für alle Services
- JWT-Authentication für Admin-Bereich
- Bild-Upload-Funktionalität
- Responsive Design mit TailwindCSS
- Rate Limiting und Spam-Schutz
- Import/Export-Funktionen für Bewertungen
- Einbettbares Widget für externe Websites
- Umfassende API-Dokumentation
- MIT-Lizenz
