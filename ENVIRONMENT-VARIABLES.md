# 📋 ENVIRONMENT VARIABLES DOCUMENTATION
## Komplette Referenz aller Konfigurationsmöglichkeiten

---

## 📖 **ÜBERSICHT**

Diese Dokumentation beschreibt alle verfügbaren Umgebungsvariablen für das Guestbook-Projekt. Jede Variable wird mit Standardwerten, möglichen Optionen und Anwendungsbeispielen erklärt.

---

## 🗄️ **DATABASE CONFIGURATION**

### **MYSQL_ROOT_PASSWORD**
- **Beschreibung**: Root-Passwort für MariaDB/MySQL
- **Typ**: String
- **Standard**: `Kx9mP2vR8nQ5wE7tY3uI6oL1sA4hG9jB`
- **Sicherheit**: ⚠️ **KRITISCH** - Immer ändern in Produktion
- **Beispiel**: `MYSQL_ROOT_PASSWORD=SuperSicheresRootPasswort123!`

### **MYSQL_DATABASE**
- **Beschreibung**: Name der Datenbank
- **Typ**: String
- **Standard**: `guestbook`
- **Mögliche Werte**: Beliebiger Datenbankname
- **Beispiel**: `MYSQL_DATABASE=mein_gaestebuch`

### **MYSQL_USER**
- **Beschreibung**: MySQL-Benutzername für die Anwendung
- **Typ**: String
- **Standard**: `guestuser`
- **Empfehlung**: Spezifischen Namen verwenden
- **Beispiel**: `MYSQL_USER=gaestebuch_app`

### **MYSQL_PASSWORD**
- **Beschreibung**: Passwort für den MySQL-Benutzer
- **Typ**: String
- **Standard**: `whHBJveMvwjs5a6p`
- **Sicherheit**: ⚠️ **KRITISCH** - Starkes Passwort verwenden
- **Beispiel**: `MYSQL_PASSWORD=App123Database456!`

---

## 🔗 **DATABASE CONNECTION (APP)**

### **DB_HOST**
- **Beschreibung**: Hostname/IP der Datenbank
- **Typ**: String
- **Standard**: `mariadb`
- **Docker**: Service-Name verwenden
- **Externe DB**: IP-Adresse oder FQDN
- **Beispiele**: 
  ```bash
  DB_HOST=mariadb                    # Docker-Compose
  DB_HOST=192.168.1.100             # Externe DB
  DB_HOST=db.meine-domain.de        # Externer Service
  ```

### **DB_USER, DB_PASSWORD, DB_NAME**
- **Beschreibung**: Identisch mit MYSQL_* Variablen
- **Zweck**: Verbindung von der Anwendung zur Datenbank
- **⚠️ Wichtig**: Müssen mit MYSQL_* Variablen übereinstimmen

---

## 🔐 **JWT CONFIGURATION**

### **JWT_SECRET_KEY**
- **Beschreibung**: Geheimer Schlüssel für JWT-Token-Signierung
- **Typ**: String (Base64 oder Hex)
- **Standard**: `DeRBC3FDeY8d9nw9WMBwNJ0LpVyvB5ty607r2PHdmQBpqn`
- **Sicherheit**: ⚠️ **KRITISCH** - Mindestens 32 Zeichen
- **Generierung**: `openssl rand -base64 32`
- **Beispiel**: `JWT_SECRET_KEY=meinSuperGeheimerlanger32ZeichenSchluessel123`

### **ACCESS_TOKEN_EXPIRE_MINUTES**
- **Beschreibung**: Gültigkeitsdauer der Zugriffs-Token in Minuten
- **Typ**: Integer
- **Standard**: `30`
- **Bereich**: 5-1440 (1 Tag)
- **Empfehlung**: 
  ```bash
  # Entwicklung:
  ACCESS_TOKEN_EXPIRE_MINUTES=60
  
  # Produktion (sicherer):
  ACCESS_TOKEN_EXPIRE_MINUTES=15
  
  # High-Security:
  ACCESS_TOKEN_EXPIRE_MINUTES=5
  ```

### **REFRESH_TOKEN_EXPIRE_HOURS**
- **Beschreibung**: Gültigkeitsdauer der Refresh-Token in Stunden
- **Typ**: Integer
- **Standard**: `24`
- **Bereich**: 1-720 (30 Tage)
- **Empfehlung**:
  ```bash
  # Standard:
  REFRESH_TOKEN_EXPIRE_HOURS=24
  
  # Längere Session:
  REFRESH_TOKEN_EXPIRE_HOURS=168    # 7 Tage
  
  # Kurze Session:
  REFRESH_TOKEN_EXPIRE_HOURS=8      # 8 Stunden
  ```

---

## 👤 **ADMIN CONFIGURATION**

### **ADMIN_USERNAME**
- **Beschreibung**: Benutzername des Administrator-Accounts
- **Typ**: String
- **Standard**: `admin`
- **Sicherheit**: ⚠️ Standard-Namen vermeiden
- **Beispiele**: `ADMIN_USERNAME=administrator`, `ADMIN_USERNAME=webmaster`

### **ADMIN_EMAIL**
- **Beschreibung**: E-Mail-Adresse des Administrators
- **Typ**: String (E-Mail-Format)
- **Standard**: `admin@gcng.de`
- **Validierung**: Muss gültige E-Mail sein
- **Beispiel**: `ADMIN_EMAIL=admin@meine-domain.de`

### **ADMIN_PASSWORD**
- **Beschreibung**: Passwort für den Administrator-Account
- **Typ**: String
- **Standard**: `whHBJveMvwjs5a6p`
- **Sicherheit**: ⚠️ **KRITISCH** - Starkes Passwort erforderlich
- **Anforderungen**: Min. 12 Zeichen, Sonderzeichen, Zahlen
- **Beispiel**: `ADMIN_PASSWORD=MeinSicheres!Admin2025#`

### **ADMIN_ROLE**
- **Beschreibung**: Rolle des Administrator-Accounts
- **Typ**: String (Enum)
- **Standard**: `superuser`
- **Mögliche Werte**: 
  ```bash
  ADMIN_ROLE=superuser    # Vollzugriff
  ADMIN_ROLE=admin        # Admin-Rechte
  ADMIN_ROLE=moderator    # Moderation
  ```

### **ADMIN_IS_SUPERUSER**
- **Beschreibung**: Superuser-Status für erweiterte Rechte
- **Typ**: Boolean
- **Standard**: `true`
- **Mögliche Werte**: `true`, `false`
- **Empfehlung**: `true` für Vollzugriff

---

## 🌐 **CORS & SECURITY CONFIGURATION**

### **CORS_ORIGINS**
- **Beschreibung**: Erlaubte Domains für Cross-Origin-Requests
- **Typ**: String (Komma-getrennte Liste)
- **Standard**: Spezifische Domains
- **Sicherheit**: ⚠️ **Niemals** `*` in Produktion verwenden
- **Format**: `https://domain1.com,https://domain2.com`
- **Beispiele**:
  ```bash
  # Entwicklung:
  CORS_ORIGINS=http://localhost:3000,http://localhost:8080
  
  # Produktion:
  CORS_ORIGINS=https://www.meine-seite.de,https://app.meine-seite.de
  
  # iFrame-Integration:
  CORS_ORIGINS=https://hauptseite.de,https://iframe-host.de
  ```

### **ALLOWED_HOSTS**
- **Beschreibung**: Erlaubte Host-Header für Requests
- **Typ**: String (Komma-getrennte Liste)
- **Standard**: Spezifische Hosts
- **Sicherheit**: Schutz vor Host-Header-Injection
- **Format**: `domain1.com,domain2.com,192.168.1.100`
- **Beispiele**:
  ```bash
  # Single Domain:
  ALLOWED_HOSTS=www.meine-seite.de
  
  # Multiple Domains:
  ALLOWED_HOSTS=meine-seite.de,www.meine-seite.de,app.meine-seite.de
  
  # Mit IP-Adressen:
  ALLOWED_HOSTS=meine-seite.de,192.168.1.100,localhost
  ```

---

## 🏭 **APPLICATION ENVIRONMENT**

### **ENVIRONMENT**
- **Beschreibung**: Ausführungsumgebung der Anwendung
- **Typ**: String (Enum)
- **Standard**: `production`
- **Mögliche Werte**:
  ```bash
  ENVIRONMENT=development    # Entwicklung
  ENVIRONMENT=testing       # Test-Umgebung
  ENVIRONMENT=staging       # Staging-Umgebung
  ENVIRONMENT=production    # Produktion
  ```
- **Auswirkungen**: Logging, Caching, Error-Handling

### **DEBUG**
- **Beschreibung**: Debug-Modus aktivieren/deaktivieren
- **Typ**: Boolean
- **Standard**: `false` (Produktion)
- **Mögliche Werte**: `true`, `false`
- **Sicherheit**: ⚠️ **NIE** `true` in Produktion
- **Verwendung**:
  ```bash
  # Entwicklung:
  DEBUG=true
  
  # Produktion (IMMER):
  DEBUG=false
  ```

### **LOG_LEVEL**
- **Beschreibung**: Minimaler Logging-Level
- **Typ**: String (Enum)
- **Standard**: `INFO`
- **Mögliche Werte**: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`
- **Hierarchie**: DEBUG < INFO < WARNING < ERROR < CRITICAL
- **Beispiele**:
  ```bash
  # Entwicklung (verbose):
  LOG_LEVEL=DEBUG
  
  # Produktion (standard):
  LOG_LEVEL=INFO
  
  # Produktion (minimal):
  LOG_LEVEL=WARNING
  ```

---

## 📝 **LOGGING CONFIGURATION**

### **UVICORN_LOG_LEVEL**
- **Beschreibung**: Log-Level für Uvicorn Web-Server
- **Typ**: String (Enum)
- **Standard**: `info`
- **Mögliche Werte**: `critical`, `error`, `warning`, `info`, `debug`, `trace`
- **Empfehlung**: `info` für Produktion, `debug` für Entwicklung

### **UVICORN_ACCESS_LOG**
- **Beschreibung**: HTTP-Access-Logs aktivieren
- **Typ**: Boolean
- **Standard**: `true`
- **Verwendung**: Überwachung von HTTP-Requests
- **Performance**: `false` für bessere Performance

### **SQLALCHEMY_ECHO**
- **Beschreibung**: SQL-Queries in Logs ausgeben
- **Typ**: Boolean
- **Standard**: `false`
- **Sicherheit**: ⚠️ **NIE** `true` in Produktion (SQL-Injection-Risiko)
- **Verwendung**:
  ```bash
  # Entwicklung (SQL-Debugging):
  SQLALCHEMY_ECHO=true
  
  # Produktion (IMMER):
  SQLALCHEMY_ECHO=false
  ```

### **ENABLE_SQL_LOGGING**
- **Beschreibung**: Erweiterte SQL-Logs aktivieren
- **Typ**: Boolean
- **Standard**: `false`
- **Sicherheit**: Gleiche Vorsicht wie SQLALCHEMY_ECHO

### **ENABLE_REQUEST_LOGGING**
- **Beschreibung**: Request-Details loggen
- **Typ**: Boolean
- **Standard**: `true`
- **Datenschutz**: ⚠️ Kann sensible Daten enthalten

### **ENABLE_ERROR_LOGGING**
- **Beschreibung**: Fehler-Details loggen
- **Typ**: Boolean
- **Standard**: `true`
- **Empfehlung**: Immer aktiviert für Debugging

### **ENABLE_VALIDATION_LOGGING**
- **Beschreibung**: Validierungsfehler detailliert loggen
- **Typ**: Boolean
- **Standard**: `false`
- **Verwendung**: Debugging von Input-Validation

### **LOG_FORMAT**
- **Beschreibung**: Format der Log-Ausgabe
- **Typ**: String (Enum)
- **Standard**: `json`
- **Mögliche Werte**:
  ```bash
  LOG_FORMAT=json        # Strukturierte JSON-Logs
  LOG_FORMAT=detailed    # Ausführliche Text-Logs
  LOG_FORMAT=simple      # Einfache Text-Logs
  LOG_FORMAT=compact     # Kompakte Logs
  ```

### **LOG_TO_CONSOLE**
- **Beschreibung**: Logs auf Konsole ausgeben
- **Typ**: Boolean
- **Standard**: `true`
- **Docker**: Wichtig für Container-Logs

### **LOG_TO_FILE**
- **Beschreibung**: Logs in Dateien speichern
- **Typ**: Boolean
- **Standard**: `true`
- **Pfad**: `/app/logs/` (Container)

---

## 🛡️ **SECURITY SETTINGS**

### **ENABLE_RATE_LIMITING**
- **Beschreibung**: Rate Limiting aktivieren
- **Typ**: Boolean
- **Standard**: `true`
- **Sicherheit**: ✅ **Empfohlen** für Produktion
- **Schutz**: DDoS, Brute-Force, API-Missbrauch

### **ENABLE_BRUTE_FORCE_PROTECTION**
- **Beschreibung**: Brute-Force-Schutz aktivieren
- **Typ**: Boolean
- **Standard**: `true`
- **Sicherheit**: ✅ **Kritisch** für Login-Sicherheit

### **MAX_LOGIN_ATTEMPTS**
- **Beschreibung**: Maximale Login-Versuche vor Sperrung
- **Typ**: Integer
- **Standard**: `5`
- **Bereich**: 3-50
- **Empfehlung**:
  ```bash
  # High-Security:
  MAX_LOGIN_ATTEMPTS=3
  
  # Standard:
  MAX_LOGIN_ATTEMPTS=5
  
  # Entwicklung:
  MAX_LOGIN_ATTEMPTS=10
  ```

### **LOGIN_BLOCK_DURATION**
- **Beschreibung**: Sperrdauer nach fehlgeschlagenen Logins (Sekunden)
- **Typ**: Integer
- **Standard**: `900` (15 Minuten)
- **Bereich**: 60-86400 (1 Tag)
- **Empfehlung**:
  ```bash
  # Kurz (1 Minute):
  LOGIN_BLOCK_DURATION=60
  
  # Standard (15 Minuten):
  LOGIN_BLOCK_DURATION=900
  
  # High-Security (1 Stunde):
  LOGIN_BLOCK_DURATION=3600
  ```

### **ENABLE_SECURITY_MONITORING**
- **Beschreibung**: Security-Events monitoren und loggen
- **Typ**: Boolean
- **Standard**: `true`
- **Funktionen**: Verdächtige Aktivitäten, Failed-Logins, Rate-Limit-Violations

---

## 🔒 **HTTP SECURITY HEADERS**

### **SECURITY_HEADERS_ENABLED**
- **Beschreibung**: Alle Security-Headers aktivieren
- **Typ**: Boolean
- **Standard**: `true`
- **Sicherheit**: ✅ **Immer** aktiviert lassen

### **X_FRAME_OPTIONS**
- **Beschreibung**: Clickjacking-Schutz
- **Typ**: String (Enum)
- **Standard**: `SAMEORIGIN`
- **Mögliche Werte**:
  ```bash
  X_FRAME_OPTIONS=DENY        # Keine iFrames erlaubt
  X_FRAME_OPTIONS=SAMEORIGIN  # Nur Same-Origin iFrames
  X_FRAME_OPTIONS=ALLOW-FROM  # Spezifische Domains (deprecated)
  ```

### **X_CONTENT_TYPE_OPTIONS**
- **Beschreibung**: MIME-Type-Sniffing verhindern
- **Typ**: String
- **Standard**: `nosniff`
- **Sicherheit**: ✅ **Immer** `nosniff`

### **X_XSS_PROTECTION**
- **Beschreibung**: XSS-Filter im Browser aktivieren
- **Typ**: String
- **Standard**: `1; mode=block`
- **Optionen**:
  ```bash
  X_XSS_PROTECTION=0                # Deaktiviert
  X_XSS_PROTECTION=1                # Aktiviert
  X_XSS_PROTECTION=1; mode=block    # Aktiviert mit Blockierung
  ```

### **REFERRER_POLICY**
- **Beschreibung**: Kontrolle über Referrer-Header
- **Typ**: String (Enum)
- **Standard**: `strict-origin-when-cross-origin`
- **Mögliche Werte**:
  ```bash
  REFERRER_POLICY=no-referrer
  REFERRER_POLICY=origin
  REFERRER_POLICY=strict-origin
  REFERRER_POLICY=strict-origin-when-cross-origin
  REFERRER_POLICY=same-origin
  ```

### **PERMISSIONS_POLICY**
- **Beschreibung**: Browser-Features einschränken
- **Typ**: String
- **Standard**: `geolocation=(), microphone=(), camera=()`
- **Format**: `feature=allowlist`
- **Beispiele**:
  ```bash
  # Minimal:
  PERMISSIONS_POLICY=geolocation=(), microphone=(), camera=()
  
  # Erweitert:
  PERMISSIONS_POLICY=geolocation=(), microphone=(), camera=(), payment=(), usb=()
  
  # Selektiv erlauben:
  PERMISSIONS_POLICY=camera=(self), microphone=(self "https://trusted.com")
  ```

### **CONTENT_SECURITY_POLICY**
- **Beschreibung**: XSS und Code-Injection verhindern
- **Typ**: String (CSP-Direktiven)
- **Standard**: Secure Default + iFrame-Support
- **Komplex**: ⚠️ Sorgfältige Konfiguration erforderlich
- **Beispiele**:
  ```bash
  # Streng (nur eigene Inhalte):
  CONTENT_SECURITY_POLICY=default-src 'self'; script-src 'self'; style-src 'self'
  
  # Mit externen Ressourcen:
  CONTENT_SECURITY_POLICY=default-src 'self'; script-src 'self' https://cdn.js.com; style-src 'self' 'unsafe-inline'
  
  # iFrame-Support:
  CONTENT_SECURITY_POLICY=default-src 'self'; frame-ancestors 'self' https://trusted-site.com
  ```

### **STRICT_TRANSPORT_SECURITY**
- **Beschreibung**: HTTPS erzwingen (HSTS)
- **Typ**: String
- **Standard**: `max-age=31536000; includeSubDomains; preload`
- **Format**: `max-age=SECONDS; [includeSubDomains]; [preload]`
- **Beispiele**:
  ```bash
  # 1 Jahr:
  STRICT_TRANSPORT_SECURITY=max-age=31536000
  
  # 1 Jahr mit Subdomains:
  STRICT_TRANSPORT_SECURITY=max-age=31536000; includeSubDomains
  
  # Production-ready:
  STRICT_TRANSPORT_SECURITY=max-age=31536000; includeSubDomains; preload
  ```

### **X_PERMITTED_CROSS_DOMAIN_POLICIES**
- **Beschreibung**: Cross-Domain-Policies verhindern
- **Typ**: String (Enum)
- **Standard**: `none`
- **Mögliche Werte**: `none`, `master-only`, `by-content-type`, `all`
- **Sicherheit**: ✅ **Immer** `none`

---

## 📁 **VOLUME PATHS**

### **DB_VOLUME_PATH**
- **Beschreibung**: Pfad für Datenbank-Dateien auf Host-System
- **Typ**: String (Absoluter Pfad)
- **Standard**: `/volume2/docker/guestbook/db`
- **Docker**: Host-Pfad für Bind-Mount
- **Beispiele**:
  ```bash
  # Linux:
  DB_VOLUME_PATH=/var/lib/docker/volumes/guestbook_db
  
  # NAS (Synology):
  DB_VOLUME_PATH=/volume1/docker/guestbook/database
  
  # Windows:
  DB_VOLUME_PATH=C:\Docker\guestbook\db
  ```

### **UPLOADS_VOLUME_PATH**
- **Beschreibung**: Pfad für Upload-Dateien auf Host-System
- **Typ**: String (Absoluter Pfad)
- **Standard**: `/volume2/docker/guestbook/uploads`
- **Berechtigungen**: ⚠️ Schreibzugriff für Container erforderlich
- **Beispiele**:
  ```bash
  # Linux:
  UPLOADS_VOLUME_PATH=/var/www/guestbook/uploads
  
  # Shared Storage:
  UPLOADS_VOLUME_PATH=/mnt/nfs/guestbook/uploads
  ```

---

## 🐳 **DOCKER CONFIGURATION**

### **GUESTBOOK_IMAGE**
- **Beschreibung**: Docker-Image für die Anwendung
- **Typ**: String (Image-Tag)
- **Standard**: `ghcr.io/baronblk/guestbook-project:4.0.0-secure`
- **Format**: `registry/namespace/image:tag`
- **Beispiele**:
  ```bash
  # Sichere Version:
  GUESTBOOK_IMAGE=ghcr.io/baronblk/guestbook-project:4.0.0-secure
  
  # Neueste Version:
  GUESTBOOK_IMAGE=ghcr.io/baronblk/guestbook-project:latest
  
  # Spezifische Version:
  GUESTBOOK_IMAGE=ghcr.io/baronblk/guestbook-project:3.0.5-uploads-fix
  
  # Lokales Build:
  GUESTBOOK_IMAGE=guestbook:local-dev
  ```

### **NETWORK_NAME**
- **Beschreibung**: Name des Docker-Netzwerks
- **Typ**: String
- **Standard**: `guestbook-network`
- **Docker-Compose**: Netzwerk für Service-Kommunikation

### **APP_PORT**
- **Beschreibung**: Externer Port für die Anwendung
- **Typ**: Integer
- **Standard**: `8080`
- **Bereich**: 1024-65535 (Non-privileged)
- **Beispiele**:
  ```bash
  # Standard HTTP:
  APP_PORT=80
  
  # Alternative:
  APP_PORT=8080
  
  # Entwicklung:
  APP_PORT=3000
  ```

---

## 🎛️ **KONFIGURATIONSPROFILE**

### **ENTWICKLUNG**
```bash
# Entwicklung (.env.development)
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=DEBUG
SQLALCHEMY_ECHO=true
ENABLE_SQL_LOGGING=true
CORS_ORIGINS=http://localhost:3000,http://localhost:8080
MAX_LOGIN_ATTEMPTS=10
LOGIN_BLOCK_DURATION=60
```

### **STAGING**
```bash
# Staging (.env.staging)
ENVIRONMENT=staging
DEBUG=false
LOG_LEVEL=INFO
SQLALCHEMY_ECHO=false
ENABLE_SQL_LOGGING=false
CORS_ORIGINS=https://staging.meine-seite.de
MAX_LOGIN_ATTEMPTS=5
LOGIN_BLOCK_DURATION=300
```

### **PRODUKTION**
```bash
# Produktion (.env.production)
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO
SQLALCHEMY_ECHO=false
ENABLE_SQL_LOGGING=false
ENABLE_RATE_LIMITING=true
ENABLE_BRUTE_FORCE_PROTECTION=true
MAX_LOGIN_ATTEMPTS=3
LOGIN_BLOCK_DURATION=900
SECURITY_HEADERS_ENABLED=true
```

---

## ⚠️ **SICHERHEITSRICHTLINIEN**

### **🔴 KRITISCHE VARIABLEN (Immer ändern):**
```bash
MYSQL_ROOT_PASSWORD=    # Starkes DB-Root-Passwort
MYSQL_PASSWORD=         # Starkes DB-App-Passwort  
ADMIN_PASSWORD=         # Starkes Admin-Passwort
JWT_SECRET_KEY=         # Kryptographisch starker Schlüssel
```

### **🟡 PRODUKTIONS-ANFORDERUNGEN:**
```bash
DEBUG=false                        # NIE true in Produktion
ENVIRONMENT=production             # Korrekte Umgebung
SQLALCHEMY_ECHO=false             # Keine SQL-Logs
ENABLE_RATE_LIMITING=true         # Rate Limiting aktiv
ENABLE_BRUTE_FORCE_PROTECTION=true # Brute-Force-Schutz
```

### **🟢 EMPFOHLENE SICHERHEITSEINSTELLUNGEN:**
```bash
MAX_LOGIN_ATTEMPTS=3-5            # Wenige Login-Versuche
LOGIN_BLOCK_DURATION=900-3600     # Längere Sperrzeiten
CORS_ORIGINS=spezifische-domains   # Keine Wildcards
X_FRAME_OPTIONS=SAMEORIGIN        # Clickjacking-Schutz
```

---

## 🔧 **TROUBLESHOOTING**

### **Häufige Probleme:**

#### **CORS-Fehler:**
```bash
# Lösung: Domain zu CORS_ORIGINS hinzufügen
CORS_ORIGINS=https://meine-domain.de,https://www.meine-domain.de
```

#### **iFrame funktioniert nicht:**
```bash
# Lösung: X-Frame-Options anpassen
X_FRAME_OPTIONS=SAMEORIGIN
# UND Domain zu CSP hinzufügen
CONTENT_SECURITY_POLICY=frame-ancestors 'self' https://iframe-host.de
```

#### **Login-Sperrung:**
```bash
# Temporäre Lösung: Werte erhöhen
MAX_LOGIN_ATTEMPTS=10
LOGIN_BLOCK_DURATION=60
```

#### **Datenbank-Verbindungsfehler:**
```bash
# Lösung: Korrekte Host-Konfiguration
DB_HOST=mariadb  # Service-Name in Docker
# ODER
DB_HOST=192.168.1.100  # IP-Adresse
```

---

**💡 Diese Dokumentation sollte als Referenz für alle Konfigurationsänderungen verwendet werden.**
