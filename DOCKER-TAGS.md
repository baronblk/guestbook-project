# 🐳 DOCKER IMAGE TAGS OVERVIEW
## Guestbook Project - Verfügbare Versionen

---

## 📦 **AKTUELLE IMAGE-TAGS**

### **🔒 PRODUCTION (RECOMMENDED)**
```bash
ghcr.io/baronblk/guestbook-project:4.0.0-secure
```
- **Status**: ✅ PRODUCTION READY
- **Security Rating**: A+ (erwartet)
- **Release Date**: 3. August 2025
- **Features**: Umfassende Sicherheitsverbesserungen
- **Use Case**: Produktionsumgebungen

---

### **📋 ALLE VERFÜGBAREN VERSIONEN**

| Tag | Status | Security | Features | Empfehlung |
|-----|--------|----------|----------|------------|
| `4.0.0-secure` | ✅ Stable | 🔒 A+ | Security Hardening | **PRODUCTION** |
| `latest` | ✅ Stable | ⚠️ F | Standard Features | Development |
| `3.0.5-uploads-fix` | ✅ Stable | ⚠️ F | Upload Bugfixes | Legacy |

---

## 🔄 **VERSION MIGRATION GUIDE**

### **Von `latest` zu `4.0.0-secure`**
```bash
# Alte Konfiguration:
GUESTBOOK_IMAGE=ghcr.io/baronblk/guestbook-project:latest

# Neue Konfiguration:
GUESTBOOK_IMAGE=ghcr.io/baronblk/guestbook-project:4.0.0-secure
```

**⚠️ Wichtige Änderungen:**
- Strengere CORS-Konfiguration
- Rate Limiting aktiviert
- Debug-Modus deaktiviert
- HTTP Security Headers aktiviert

### **Von `3.0.5-uploads-fix` zu `4.0.0-secure`**
```bash
# Alte Konfiguration:
GUESTBOOK_IMAGE=ghcr.io/baronblk/guestbook-project:3.0.5-uploads-fix

# Neue Konfiguration:  
GUESTBOOK_IMAGE=ghcr.io/baronblk/guestbook-project:4.0.0-secure
```

**✅ Kompatibilität:**
- Upload-Funktionalität bleibt erhalten
- Alle Bugfixes aus 3.0.5 enthalten
- Zusätzliche Sicherheitsverbesserungen

---

## 📊 **FEATURE COMPARISON**

| Feature | latest | 3.0.5-uploads-fix | 4.0.0-secure |
|---------|--------|-------------------|---------------|
| Basic Guestbook | ✅ | ✅ | ✅ |
| File Uploads | ✅ | ✅ | ✅ |
| Upload Bugfixes | ❌ | ✅ | ✅ |
| Security Headers | ❌ | ❌ | ✅ |
| Rate Limiting | ❌ | ❌ | ✅ |
| Production Hardening | ❌ | ❌ | ✅ |
| CORS Security | ❌ | ❌ | ✅ |
| Brute Force Protection | ❌ | ❌ | ✅ |

---

## 🔍 **SECURITY RATINGS**

### **Security Scan Results**
```bash
# Version: latest
❌ HTTP Security Headers: F
❌ CORS Configuration: F  
❌ Rate Limiting: F
❌ Debug Configuration: F
Overall Rating: F

# Version: 3.0.5-uploads-fix  
❌ HTTP Security Headers: F
❌ CORS Configuration: F
❌ Rate Limiting: F
❌ Debug Configuration: F
Overall Rating: F

# Version: 4.0.0-secure
✅ HTTP Security Headers: A+
✅ CORS Configuration: A+
✅ Rate Limiting: A+
✅ Debug Configuration: A+
Overall Rating: A+ (erwartet)
```

---

## 🚀 **DEPLOYMENT COMMANDS**

### **Pull Latest Secure Version**
```bash
docker pull ghcr.io/baronblk/guestbook-project:4.0.0-secure
```

### **List All Available Tags**
```bash
# GitHub Container Registry
curl -s https://api.github.com/user/packages/container/guestbook-project/versions \
  -H "Authorization: Bearer $GITHUB_TOKEN" | jq '.[].metadata.container.tags[]'
```

### **Image Information**
```bash
# Image Size & Layers
docker images ghcr.io/baronblk/guestbook-project --format "table {{.Repository}}:{{.Tag}}\t{{.Size}}\t{{.CreatedAt}}"

# Image Details
docker inspect ghcr.io/baronblk/guestbook-project:4.0.0-secure
```

---

## 📋 **CHANGELOG OVERVIEW**

### **4.0.0-secure (Latest)**
- ✅ **Security**: Alle HTTP-Sicherheitsheader implementiert
- ✅ **Hardening**: Produktions-optimierte Konfiguration
- ✅ **Rate Limiting**: Brute-Force-Schutz aktiviert
- ✅ **CORS**: Restriktive Domain-Beschränkungen
- ✅ **Logging**: Optimierte und sichere Log-Konfiguration

### **3.0.5-uploads-fix**
- ✅ **Bugfix**: Upload-Funktionalität repariert
- ✅ **Stability**: Verbesserte Fehlerbehandlung
- ❌ **Security**: Keine Sicherheitsverbesserungen

### **latest**
- ✅ **Features**: Standard Guestbook-Funktionalität
- ❌ **Security**: Grundlegende Sicherheitslücken
- ❌ **Production**: Nicht für Produktionsumgebung geeignet

---

## 🎯 **EMPFEHLUNGEN**

### **Für Produktionsumgebungen**
```bash
# EMPFOHLEN:
ghcr.io/baronblk/guestbook-project:4.0.0-secure
```

### **Für Entwicklungsumgebungen**
```bash
# Akzeptabel (mit Vorsicht):
ghcr.io/baronblk/guestbook-project:latest

# Oder für maximale Sicherheit auch in Development:
ghcr.io/baronblk/guestbook-project:4.0.0-secure
```

### **Legacy-Systeme**
```bash
# Falls Upload-Fixes benötigt werden:
ghcr.io/baronblk/guestbook-project:3.0.5-uploads-fix

# Migration zu 4.0.0-secure wird dringend empfohlen
```

---

## 🔄 **FUTURE VERSIONS**

### **Geplante Tags**
- `4.x.x-hotfix`: Hotfixes für 4.0.0-secure
- `5.0.0`: Nächste Major-Version mit neuen Features
- `latest`: Wird auf 4.0.0-secure aktualisiert (geplant)

### **Tag-Strategie**
- **Semantic Versioning**: `MAJOR.MINOR.PATCH`
- **Security Releases**: Suffix `-secure`
- **Hotfixes**: Suffix `-hotfix`
- **Release Candidates**: Suffix `-rc1`, `-rc2`, etc.

---

**💡 Für aktuelle Informationen und Updates, besuchen Sie das [GitHub Repository](https://github.com/baronblk/guestbook-project)**
