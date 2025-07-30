# 🔒 Security Hardening - Gästebuch System

## Übersicht der implementierten Sicherheitsmaßnahmen

Das Gästebuch-System wurde umfassend mit modernen Sicherheitsstandards gehärtet. Diese Dokumentation beschreibt alle implementierten Security-Features.

## 🛡️ Authentifizierung & Autorisierung

### JWT Token System
- **Algorithmus**: HS256 mit sicherem Secret Key
- **Access Token**: 30 Minuten Gültigkeit (reduziert von 60 Min)
- **Refresh Token**: 24 Stunden Gültigkeit
- **Token Claims**: 
  - Erweiterte Metadaten (iat, jti, type)
  - Eindeutige Session-IDs für Token-Invalidierung
  - Token-Typ-Validierung (access/refresh)

### Password Security
- **Hashing**: bcrypt mit automatischen Salts
- **Passwort-Verifizierung**: Sichere Vergleichsfunktionen
- **Legacy-Support**: Kompatibilität mit bestehenden Passwörtern

## 🚫 Brute-Force & Rate Limiting

### Login-Schutz (LoginAttemptTracker)
- **Fehlversuche**: Max 5 Versuche pro IP/Username-Kombination
- **Zeitfenster**: 5 Minuten
- **Block-Dauer**: 15 Minuten bei Überschreitung
- **Eskalation**: Längere Blocks bei wiederholten Verstößen

### Rate Limiting (RateLimiter)
- **Allgemein**: 60 Requests pro Minute
- **Login-Endpoint**: 5 Versuche pro 5 Minuten
- **Token-Refresh**: 10 Versuche pro Minute
- **IP-basiert**: Separate Limits pro Client-IP

### Client-IP-Erkennung
- **X-Forwarded-For** Header Support
- **X-Real-IP** Header Support
- **Proxy-kompatibel**: Echte Client-IP hinter Load Balancern

## 📊 Security Monitoring

### SecurityMonitor System
- **Event-Tracking**: Alle Sicherheitsereignisse werden protokolliert
- **Bedrohungsanalyse**: Automatische Mustererkennung
- **Incident Response**: Automatische Blockierung bei kritischen Events
- **Persistente Logs**: Security-Events in `/app/logs/security.log`

### Event-Typen
1. **failed_login_attempts**: Fehlgeschlagene Anmeldungen
2. **rate_limit_violations**: Rate-Limit-Überschreitungen  
3. **suspicious_patterns**: Verdächtige Aktivitätsmuster
4. **successful_login**: Erfolgreiche Anmeldungen (Audit-Trail)
5. **admin_action**: Administrative Aktionen

### Automatische Responses
- **IP-Blockierung**: Bei Threshold-Überschreitung
- **Eskalation**: Längere Blocks bei wiederholten Verstößen
- **Critical Alerts**: 24h-Blocks bei kritischen Bedrohungen

## 🔐 HTTP Security Headers

### Content Security Policy (CSP)
```
default-src 'self';
script-src 'self' 'unsafe-inline' 'unsafe-eval';
style-src 'self' 'unsafe-inline';
img-src 'self' data: blob:;
object-src 'none';
frame-ancestors 'none';
```

### Security Headers
- **X-Content-Type-Options**: `nosniff`
- **X-Frame-Options**: `DENY`
- **X-XSS-Protection**: `1; mode=block`
- **Referrer-Policy**: `strict-origin-when-cross-origin`
- **Permissions-Policy**: Deaktiviert Geolocation, Mikrofon, Kamera
- **HSTS**: `max-age=31536000; includeSubDomains` (nur HTTPS)

## 🌐 CORS & Network Security

### CORS-Konfiguration
- **Spezifische Origins**: Nur localhost:3000 und localhost:8080
- **Credentials**: Erlaubt für authentifizierte Requests
- **HTTP-Methods**: GET, POST, PUT, DELETE, PATCH
- **Eingeschränkt**: Keine Wildcard-Origins mehr

### Trusted Host Middleware
- **Allowed Hosts**: localhost, 127.0.0.1, *.localhost
- **Host Header Validation**: Schutz vor Host Header Injection

## 📈 Admin Security Dashboard

### Security Endpoints
- **GET /api/admin/security/dashboard**: Sicherheitsübersicht
- **POST /api/admin/security/unblock-ip**: IP-Entsperrung

### Dashboard Features
- **24h Security Summary**: Event-Statistiken
- **Recent Events**: Letzte 20 Sicherheitsereignisse
- **Blocked IPs**: Liste blockierter IP-Adressen
- **Active Threats**: Anzahl aktiver Bedrohungen

## 🔍 Logging & Auditing

### Security Logger
- **Level**: INFO für normale Events, WARNING/ERROR für Probleme
- **Format**: Timestamp, Event-Type, Severity, IP, Username, Details
- **Rotation**: Automatische Log-Rotation (OS-abhängig)

### Audit Trail
- Alle Login-Versuche (erfolgreich und fehlgeschlagen)
- Rate-Limit-Verletzungen
- Administrative Aktionen
- Token-Generierung und -Validierung

## ⚡ Performance & Skalierung

### Memory-Efficient Tracking
- **Circular Buffers**: Max 10.000 Events im Speicher
- **Auto-Cleanup**: Alte Events werden automatisch entfernt
- **Time-Window-basiert**: Nur relevante Zeitfenster werden gespeichert

### Background Processing
- **Non-blocking**: Security-Checks blockieren nicht die Anwendung
- **Async Processing**: Event-Logging erfolgt asynchron

## 🔧 Konfiguration

### Umgebungsvariablen
```bash
# JWT Configuration
JWT_SECRET_KEY=DeRBC3FDeY8d9nw9WMBwNJ0LpVyvB5ty607r2PHdmQBpqn
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_HOURS=24

# Admin Credentials
ADMIN_USERNAME=admin
ADMIN_EMAIL=support@dcng.de
ADMIN_PASSWORD=whHBJveMvwjs5a6p
```

### Rate Limiting Schwellenwerte
```python
# Login-Versuche
MAX_LOGIN_ATTEMPTS = 5
LOGIN_BLOCK_DURATION = 900  # 15 Minuten

# Rate Limits
GENERAL_RATE_LIMIT = 60  # pro Minute
LOGIN_RATE_LIMIT = 5     # pro 5 Minuten
REFRESH_RATE_LIMIT = 10  # pro Minute
```

## 🚨 Monitoring & Alerting

### Kritische Events
- Mehr als 20 fehlgeschlagene Login-Versuche
- Mehrfache Rate-Limit-Verletzungen von derselben IP
- Verdächtige Aktivitätsmuster

### Empfohlene Monitoring-Integration
1. **Log-Aggregation**: ELK Stack oder ähnlich
2. **Metrics**: Prometheus + Grafana
3. **Alerting**: Bei kritischen Security-Events
4. **SIEM**: Integration in Security Information Event Management

## 🔄 Wartung & Updates

### Regelmäßige Aufgaben
1. **Log-Rotation**: Security-Logs regelmäßig archivieren
2. **Blocked-IP-Review**: Manuell blockierte IPs überprüfen
3. **Threshold-Anpassung**: Rate-Limits bei Bedarf anpassen
4. **Security-Patches**: Dependencies regelmäßig aktualisieren

### Security Best Practices
- **Secrets Rotation**: JWT-Keys regelmäßig wechseln
- **Password Policy**: Starke Admin-Passwörter verwenden
- **HTTPS**: In Produktion immer SSL/TLS verwenden
- **Backup**: Security-Logs in Backup-Strategie einbeziehen

## 📚 API-Dokumentation

### Security-relevante Endpoints

#### Login
```http
POST /api/admin/login
Content-Type: application/json

{
  "username": "admin",
  "password": "password"
}
```

#### Token Refresh
```http
POST /api/admin/refresh
Content-Type: application/json

{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### Security Dashboard
```http
GET /api/admin/security/dashboard
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

#### IP Entsperren
```http
POST /api/admin/security/unblock-ip
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json

{
  "ip_address": "192.168.1.100"
}
```

## ✅ Security Checklist

### Implementiert ✓
- [x] JWT-basierte Authentifizierung mit Refresh-Tokens
- [x] bcrypt Password-Hashing
- [x] Brute-Force-Schutz mit IP-Blockierung
- [x] Rate Limiting für alle Endpoints
- [x] Umfassendes Security-Monitoring
- [x] Sichere HTTP-Headers (CSP, HSTS, etc.)
- [x] CORS-Einschränkungen
- [x] Input-Validierung
- [x] Audit-Logging
- [x] Admin Security Dashboard

### Empfohlene Erweiterungen
- [ ] 2FA/MFA für Admin-Accounts
- [ ] Session-Management mit Redis
- [ ] Geo-IP-basierte Blockierung
- [ ] Automated Threat Intelligence
- [ ] WAF-Integration
- [ ] Certificate Pinning

---

**Erstellt**: 30. Juli 2025  
**Version**: 1.0  
**Status**: ✅ Vollständig implementiert

Das System ist jetzt umfassend gegen gängige Webangriffe geschützt und bietet professionelles Security-Monitoring.
