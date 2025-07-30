# Security Policy

## Unterstützte Versionen

Aktuell werden folgende Versionen mit Sicherheitsupdates unterstützt:

| Version | Unterstützt        |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Sicherheitslücken melden

Wir nehmen die Sicherheit unseres Projekts ernst. Wenn du eine Sicherheitslücke entdeckst, melde sie bitte verantwortungsvoll.

### Reporting Process

**Bitte erstelle KEINE öffentlichen Issues für Sicherheitslücken.**

Stattdessen:
1. Sende eine E-Mail an die Projekt-Maintainer
2. Oder nutze GitHub's [Private Security Advisory](../../security/advisories/new)
3. Beschreibe das Problem so detailliert wie möglich:
   - Betroffene Komponenten
   - Schritte zur Reproduktion
   - Potenzielle Auswirkungen
   - Mögliche Lösungsansätze (falls bekannt)

### Was du erwarten kannst

- **Bestätigung** deines Reports innerhalb von 48 Stunden
- **Erste Bewertung** innerhalb von 7 Tagen
- **Status-Updates** während der Untersuchung
- **Anerkennung** in den Release Notes (falls gewünscht)

## Sicherheits-Best Practices

### Für Deployment
- **Ändere Standard-Passwörter** sofort nach der Installation
- **Nutze starke JWT-Secrets** in der Produktion
- **Aktiviere HTTPS** für alle öffentlichen Deployments
- **Limitiere Netzwerk-Zugriff** auf notwendige Ports
- **Halte Dependencies aktuell** mit regelmäßigen Updates

### Für Development
- **Speichere nie Secrets** in Code oder Konfigurationsdateien
- **Nutze Environment-Variablen** für sensible Daten
- **Validiere alle Eingaben** auf Client- und Server-Seite
- **Implementiere Rate Limiting** für API-Endpunkte

### Bekannte Sicherheitsüberlegungen
- **Datei-Uploads**: Werden validiert und in separatem Ordner gespeichert
- **SQL-Injection**: Verhindert durch SQLAlchemy ORM
- **XSS**: React bietet eingebauten Schutz
- **CSRF**: JWT-Tokens bieten Schutz

## Security-Features

### Implementierte Schutzmaßnahmen
- ✅ JWT-basierte Authentifizierung
- ✅ Input-Validierung mit Pydantic
- ✅ Rate Limiting für API-Endpunkte
- ✅ Sichere Datei-Upload-Verarbeitung
- ✅ SQL-Injection-Schutz durch ORM
- ✅ CORS-Konfiguration

### Geplante Verbesserungen
- [ ] HTTPS-Redirect-Middleware
- [ ] Security Headers (HSTS, CSP, etc.)
- [ ] Audit-Logging für Admin-Aktionen
- [ ] Automatische Dependency-Vulnerability-Scans

## Verantwortliche Disclosure

Wir verpflichten uns zu:
- **Transparenter Kommunikation** über Sicherheitsprobleme
- **Zeitnaher Behebung** von kritischen Sicherheitslücken
- **Koordinierter Veröffentlichung** von Sicherheitsupdates
- **Anerkennung** der Reporter (falls gewünscht)

Vielen Dank, dass du zur Sicherheit dieses Projekts beiträgst! 🔒
