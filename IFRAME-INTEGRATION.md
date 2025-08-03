# 🖼️ IFRAME INTEGRATION GUIDE
## Guestbook iFrame-Einbindung auf externen Domains

---

## ✅ **UNTERSTÜTZTE DOMAINS FÜR IFRAME-EINBINDUNG**

Das Gästebuch kann jetzt sicher auf folgenden Domains per iFrame eingebunden werden:

### **Produktions-Domains:**
```bash
✅ https://www.fhhc.de
✅ https://wasservilla-ostsee.de
✅ https://guestbook.gcng.de (Haupt-Domain)
```

### **Entwicklungs-/Test-Domains:**
```bash
✅ http://guestbook.gcng.de
✅ http://192.168.2.12:8080
✅ http://localhost:8080
```

---

## 🔧 **TECHNISCHE ANPASSUNGEN**

### **1. CORS-Konfiguration erweitert:**
```bash
# Vorher:
CORS_ORIGINS=https://guestbook.gcng.de,http://guestbook.gcng.de,http://192.168.2.12:8080,http://localhost:8080

# Nachher:
CORS_ORIGINS=https://guestbook.gcng.de,http://guestbook.gcng.de,http://192.168.2.12:8080,http://localhost:8080,https://www.fhhc.de,https://wasservilla-ostsee.de
```

### **2. X-Frame-Options angepasst:**
```bash
# Vorher (blockiert ALLE iFrames):
X_FRAME_OPTIONS=DENY

# Nachher (erlaubt iFrames von Same-Origin):
X_FRAME_OPTIONS=SAMEORIGIN
```

### **3. Content-Security-Policy erweitert:**
```bash
# frame-ancestors hinzugefügt für spezifische Domains:
frame-ancestors 'self' https://www.fhhc.de https://wasservilla-ostsee.de
```

---

## 📝 **IFRAME HTML-CODE**

### **Für www.fhhc.de:**
```html
<iframe 
    src="https://guestbook.gcng.de" 
    width="100%" 
    height="600" 
    frameborder="0"
    title="Gästebuch"
    style="border: 1px solid #ddd; border-radius: 8px;">
</iframe>
```

### **Für wasservilla-ostsee.de:**
```html
<iframe 
    src="https://guestbook.gcng.de" 
    width="100%" 
    height="600" 
    frameborder="0"
    title="Gästebuch"
    style="border: 1px solid #ddd; border-radius: 8px;">
</iframe>
```

### **Responsive iFrame (empfohlen):**
```html
<div style="position: relative; width: 100%; height: 0; padding-bottom: 75%;">
    <iframe 
        src="https://guestbook.gcng.de" 
        style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 1px solid #ddd; border-radius: 8px;"
        frameborder="0"
        title="Gästebuch">
    </iframe>
</div>
```

---

## 🔍 **TESTING & VERIFIKATION**

### **1. CORS-Test:**
```javascript
// Browser-Console auf www.fhhc.de öffnen und testen:
fetch('https://guestbook.gcng.de/api/reviews')
    .then(response => response.json())
    .then(data => console.log('CORS funktioniert:', data))
    .catch(error => console.error('CORS-Fehler:', error));
```

### **2. iFrame-Test:**
```html
<!-- Einfacher Test auf der Ziel-Domain: -->
<iframe src="https://guestbook.gcng.de" width="400" height="300"></iframe>
```

### **3. Erwartete Ergebnisse:**
```bash
✅ iFrame lädt vollständig
✅ Gästebuch-Funktionen funktionieren
✅ Keine CORS-Fehler in Browser-Console
✅ Keine Frame-blocking Fehler
```

---

## ⚠️ **SICHERHEITSHINWEISE**

### **Beibehaltene Sicherheit:**
```bash
✅ Rate Limiting weiterhin aktiv
✅ Brute Force Protection aktiv
✅ XSS-Schutz aktiviert
✅ HTTPS erzwungen (HSTS)
✅ Nur spezifische Domains erlaubt (nicht *)
```

### **Kompromisse für iFrame-Funktionalität:**
```bash
⚠️ X-Frame-Options: DENY → SAMEORIGIN
⚠️ CSP frame-ancestors erweitert für spezifische Domains
✅ Immer noch sicher, aber iFrame-kompatibel
```

---

## 🚀 **DEPLOYMENT-SCHRITTE**

### **1. Portainer aktualisieren:**
```bash
1. Portainer → Stacks → Guestbook
2. Environment Variables aktualisieren
3. Neue CORS_ORIGINS und X_FRAME_OPTIONS verwenden
4. Stack neu deployen
```

### **2. iFrame-Code implementieren:**
```bash
1. HTML-Code auf www.fhhc.de einfügen
2. HTML-Code auf wasservilla-ostsee.de einfügen
3. Funktionalität testen
```

### **3. Verifikation:**
```bash
1. Beide Domains öffnen
2. Gästebuch-Funktionen testen
3. Browser-Console auf Fehler prüfen
```

---

## 🔧 **TROUBLESHOOTING**

### **Falls iFrame nicht lädt:**
```bash
1. Browser-Console öffnen (F12)
2. Nach Fehlermeldungen suchen:
   - "Refused to display in a frame" → CSP-Problem
   - "CORS error" → CORS-Problem
   - "Mixed content" → HTTP/HTTPS-Problem
```

### **Häufige Probleme:**
```bash
# Problem: iFrame bleibt leer
Lösung: Browser-Cache leeren, neue Deployment warten

# Problem: CORS-Fehler trotz Konfiguration  
Lösung: Domain-Schreibweise prüfen (www. vs ohne www.)

# Problem: Mixed Content Warnings
Lösung: Sicherstellen, dass beide Domains HTTPS verwenden
```

---

## 📊 **PERFORMANCE-OPTIMIERUNG**

### **iFrame-Loading optimieren:**
```html
<iframe 
    src="https://guestbook.gcng.de" 
    loading="lazy"
    width="100%" 
    height="600">
</iframe>
```

### **Preload für bessere Performance:**
```html
<link rel="preconnect" href="https://guestbook.gcng.de">
<iframe src="https://guestbook.gcng.de" ...>
```

---

## ✅ **ZUSAMMENFASSUNG**

**Nach diesem Update funktioniert:**
- ✅ iFrame-Einbindung auf www.fhhc.de
- ✅ iFrame-Einbindung auf wasservilla-ostsee.de  
- ✅ Alle Gästebuch-Funktionen in iFrames
- ✅ Sichere CORS-Konfiguration
- ✅ Optimale Balance zwischen Sicherheit und Funktionalität

**Die Konfiguration ist bereit für Deployment!** 🎉
