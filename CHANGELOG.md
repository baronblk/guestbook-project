# Changelog

Alle wichtigen Änderungen an diesem Projekt werden in dieser Datei dokumentiert.

Das Format basiert auf [Keep a Changelog](https://keepachangelog.com/de/1.0.0/),
und dieses Projekt folgt [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.0.0] - 2025-07-30

### 🔐 Security Enhancements
- **MAJOR**: Implementierung eines enterprise-grade Authentifizierungssystems mit bcrypt Passwort-Hashing
- Umfassender Brute-Force-Schutz mit LoginAttemptTracker
  - 5 fehlgeschlagene Versuche in 5 Minuten führen zu 15-minütiger IP-Blockierung
  - Automatische Eskalation bei persistenten Angreifern
- Endpunkt-spezifisches Rate-Limiting-System
  - Login-Endpunkt: 10 Anfragen/Minute
  - Refresh-Endpunkt: 20 Anfragen/Minute  
  - Admin-Endpunkte: 30 Anfragen/Minute
- Echtzeit-Sicherheitsüberwachung mit SecurityMonitor
  - Event-Tracking und Protokollierung
  - Automatische Bedrohungsmuster-Erkennung
  - Sicherheits-Dashboard für Administratoren
- Erweiterte HTTP-Sicherheitsheader
  - Content Security Policy (CSP)
  - HTTP Strict Transport Security (HSTS)
  - X-Frame-Options, X-Content-Type-Options
  - Referrer-Policy und Permissions-Policy
- CORS-Beschränkungen auf spezifische Origins
- Umfassende Sicherheitsprotokollierung in `/app/logs/security.log`

### 🔧 Authentifizierungssystem-Fixes
- Behebung doppelter RateLimiter-Klassen-Konflikte im Auth-Modul
- Korrektur der CRUD-Methoden-Benennung
- Passwort-Verifikation mit korrekten SecurityUtils behoben
- Frontend-Backend API-Call Format-Mismatch behoben
- JWT-Token-Refresh-Mechanismus verbessert
  - 30-Minuten Access-Tokens
  - 24-Stunden Refresh-Tokens
  - Automatische Token-Erneuerung bei API-Aufrufen

### 🏗️ Infrastruktur-Verbesserungen
- Ungültiges 'secrets' Paket aus requirements.txt entfernt (Docker-Build-Fehler behoben)
- Sicherheits-Logging-Verzeichnisstruktur hinzugefügt
- Docker-Build-Prozess für Sicherheitsfeatures erweitert
- Frontend-API-Aufrufe für korrekte Authentifizierung aktualisiert
- Session-Management mit automatischer Verlängerung verbessert

### 📚 Dokumentation hinzugefügt
- `SECURITY-HARDENING.md` - Umfassender Sicherheitsimplementierungs-Leitfaden
- `SECURITY-VALIDATION-REPORT.md` - Sicherheitstests und Validierungsergebnisse
- `SESSION-MANAGEMENT.md` - Session-Handling-Dokumentation
- `SECURITY-FEATURES.md` - Übersicht der Sicherheitsfeatures

### 🐛 Bug Fixes
- Nicht reagierendes Admin-Login-Formular behoben
- Docker-Build-Fehler durch ungültige Dependencies behoben
- Session-Management und automatisches Logout behoben
- 10-Minuten Session-Verlängerung korrigiert
- Kommentar-Moderationssystem behoben (Kommentare benötigen jetzt standardmäßig Genehmigung)

### 🔄 Technische Verbesserungen
- Verbesserte Fehlerbehandlung und Protokollierung in der gesamten Anwendung
- Optimiertes Frontend-State-Management für Authentifizierung
- Umfassende Input-Validierung und Sanitization
- Korrekte API-Response-Behandlung implementiert
- Verbesserte Datenbankverbindungsverwaltung

### 📊 Performance-Optimierungen
- Authentifizierungs-Middleware für bessere Performance optimiert
- Datenbankabfrage-Effizienz verbessert
- Erweiterte Caching-Strategien für Sicherheitsprüfungen
- Frontend-Bundle-Größe und Ladezeiten optimiert

### 🧪 Testing
- Umfassende Sicherheitstests hinzugefügt
- Authentifizierungsflow-Tests implementiert
- Rate-Limiting-Validierungstests hinzugefügt
- Sicherheitsüberwachungs-Verifikationstests erstellt

### Migration Notes
- Keine Datenbankmigration erforderlich
- Bestehende Admin-Konten funktionieren weiterhin
- Neue Sicherheitsfeatures sind automatisch aktiviert
- Passwörter werden beim nächsten Login mit bcrypt neu gehasht

### [1.0.0] - Vorherige Version
- Repository nach Best Practices bereinigt
- .gitignore für Python, Node.js und temporäre Dateien ergänzt
- GitHub Workflows für CI/CD, Security und Dependency Updates
- Kommentar-System mit CRUD-Operationen
- Admin-Dashboard für Kommentar-Management
- Projekt-Dokumentation erweitert (CHANGELOG, CONTRIBUTING, docs/)
- Archive-Ordner für temporäre Import-Skripte
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
