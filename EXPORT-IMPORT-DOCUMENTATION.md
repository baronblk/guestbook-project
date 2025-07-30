# 📥📤 Vollständige Export/Import-Funktionalität

## Übersicht

Das Gästebuch-System verfügt jetzt über eine umfassende Export/Import-Funktionalität, die eine vollständige Datensicherung und -wiederherstellung ermöglicht.

## ✨ Features

### 🔸 Vollständiger Export
- **Alle Gästebucheinträge** mit sämtlichen Metadaten
- **Alle zugehörigen Kommentare** pro Eintrag
- **Moderationsstatus** (genehmigt/ausstehend)
- **Admin-Notizen** und interne Vermerke
- **Bewertungen, Titel und Inhalte**
- **Zeitstempel** (Erstellung, letzte Änderung)
- **Import-Quellen** und externe IDs

### 🔸 Intelligenter Import
- **Vollständige Datenwiederherstellung** aus Export-Dateien
- **Wahlweise Ersetzung** oder Ergänzung bestehender Daten
- **Fehlerbehandlung** mit detailliertem Bericht
- **Duplikatserkennung** und -vermeidung
- **Batch-Verarbeitung** für große Datenmengen

## 🚀 Verwendung

### Export erstellen

1. **Admin-Dashboard** aufrufen (`http://localhost:3000/admin`)
2. **"Daten Import/Export"** Tab wählen
3. **"Vollständigen Export erstellen"** klicken
4. **JSON-Datei** wird automatisch heruntergeladen

### Import durchführen

1. **Admin-Dashboard** aufrufen
2. **"Daten Import/Export"** Tab wählen
3. **JSON-Datei auswählen** (nur Export-Dateien)
4. **Bestätigen**, ob bestehende Daten ersetzt werden sollen
5. **Import-Bericht** wird angezeigt

## 📊 Export-Datenformat (JSON)

```json
{
  "exported_at": "2025-07-30T10:15:30Z",
  "export_version": "2.0",
  "total_reviews": 25,
  "total_comments": 47,
  "reviews": [
    {
      "id": 1,
      "name": "Max Mustermann",
      "email": "max@example.com",
      "rating": 5,
      "title": "Ausgezeichneter Service!",
      "content": "Sehr zufrieden mit der Qualität...",
      "image_path": null,
      "created_at": "2025-07-30T08:30:00Z",
      "updated_at": null,
      "is_approved": true,
      "is_featured": false,
      "admin_notes": null,
      "import_source": null,
      "external_id": null,
      "ip_address": "192.168.1.100",
      "comments": [
        {
          "id": 1,
          "name": "Admin",
          "email": "admin@guestbook.com",
          "content": "Vielen Dank für das Feedback!",
          "created_at": "2025-07-30T09:00:00Z",
          "updated_at": null,
          "is_approved": true,
          "admin_notes": null,
          "ip_address": "10.0.0.1"
        }
      ]
    }
  ]
}
```

## 🔧 Technische Details

### Backend API-Endpoints

#### Vollständiger Export
```http
GET /api/admin/export/full
Authorization: Bearer <admin_token>
```

#### Vollständiger Import  
```http
POST /api/admin/import/full?replace_existing=false
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "export_version": "2.0",
  "reviews": [...]
}
```

### Import-Optionen

| Parameter | Typ | Beschreibung |
|-----------|-----|--------------|
| `replace_existing` | Boolean | `true`: Alle bestehenden Daten löschen<br>`false`: Daten ergänzen (Standard) |

### Import-Antwort

```json
{
  "message": "Import abgeschlossen: 25 Reviews und 47 Kommentare importiert",
  "imported_reviews": 25,
  "imported_comments": 47,
  "skipped_reviews": 0,
  "errors": []
}
```

## ⚠️ Wichtige Hinweise

### Sicherheit
- **Export** benötigt Admin-Berechtigung
- **Import** benötigt Admin-Berechtigung
- **Datenersetzung** ist irreversibel!

### Best Practices
1. **Regelmäßige Backups** vor größeren Änderungen
2. **Test-Import** in Entwicklungsumgebung
3. **Backup vor Import** mit `replace_existing=true`
4. **Dateiformat prüfen** vor Import

### Datenschutz
- Export enthält **alle Benutzerdaten** (Namen, E-Mails, IP-Adressen)
- **Sichere Aufbewahrung** der Export-Dateien erforderlich
- **DSGVO-konforme Behandlung** bei Löschungsanfragen

## 🛠️ Entwicklung

### Neue Schema-Definitionen
- `FullExportData`: Vollständige Export-Struktur
- `ImportReviewWithComments`: Review mit Kommentaren für Import
- `FullImportData`: Import-Request-Format

### Erweiterte CRUD-Funktionen
- `full_export_data()`: Kompletter Export mit Relations
- `full_import_data()`: Intelligenter Batch-Import
- Optimierte Datenbankabfragen mit `selectinload`

### Frontend-Verbesserungen
- Erweiterte Admin-Dashboard-Komponente
- Benutzerfreundliche Drag&Drop-Dateiauswahl
- Fortschrittsanzeigen und Fehlermeldungen
- Responsive Design für mobile Geräte

## 📈 Vorteile gegenüber v1.0

| Feature | v1.0 | v2.0 |
|---------|------|------|
| **Kommentare** | ❌ | ✅ Vollständig |
| **Metadaten** | ⚠️ Teilweise | ✅ Komplett |
| **Fehlerbehandlung** | ❌ Basic | ✅ Detailliert |
| **Datenvalidierung** | ❌ | ✅ Umfassend |
| **Batch-Import** | ❌ | ✅ Optimiert |
| **Progress-Feedback** | ❌ | ✅ Real-time |

## 🔄 Migration von v1.0

Alte Export-Dateien (v1.0) sind **nicht kompatibel** mit dem neuen System. 
Für Migration:

1. Alte Daten über v1.0-System exportieren
2. Manuell in v2.0-Format konvertieren
3. Über neue Import-Funktion einlesen

## 🐛 Troubleshooting

### Häufige Probleme

**Import schlägt fehl:**
- Dateiformat prüfen (muss v2.0 Export sein)
- Dateigröße unter 100MB halten
- Browser-Console auf JavaScript-Fehler prüfen

**Langsamer Export:**
- Bei >1000 Einträgen kann Export 30+ Sekunden dauern
- Nicht mehrfach klicken während Export läuft

**Speicherprobleme:**
- Große Exports (>10MB) können Browser verlangsamen
- Bei Bedarf Export-Größe über Backend-Parameter limitieren

### Support-Kontakt

Bei Problemen mit Export/Import:
1. Browser-Console-Logs sammeln
2. Fehlermeldungen dokumentieren  
3. Beispiel-Export-Datei bereitstellen
4. Support kontaktieren

---

*Letzte Aktualisierung: 30. Juli 2025*
*Version: 2.0.0*
