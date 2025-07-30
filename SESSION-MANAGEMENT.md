# 🔐 Session Management Dokumentation

## Überblick

Das verbesserte Session-Management-System bietet robuste Authentifizierung mit automatischer Weiterleitung, Session-Verlängerung und intelligenten Warnungen.

## ✨ Neue Features

### 1. **Session-Refresh-Endpoint**
- **Endpoint**: `POST /api/admin/refresh`
- **Funktion**: Verlängert die aktuelle Session um weitere 60 Minuten
- **Authentifizierung**: Benötigt gültigen JWT-Token
- **Response**: Neuer JWT-Token mit verlängerter Gültigkeitsdauer

### 2. **10-Minuten-Warnung**
- Warnung erscheint **10 Minuten** vor Session-Ablauf
- Gelbe Warnung: "Session läuft in weniger als 10 Minuten ab!"
- **5-Minuten-Warnung**: Kritische rote Warnung mit Handlungsaufforderung

### 3. **Session-Verlängerung Button**
- Erscheint automatisch wenn Session in **≤ 10 Minuten** abläuft
- Ein-Klick-Verlängerung der Session um weitere 60 Minuten
- Erfolgs-/Fehlermeldungen mit Toast-Notifications

### 4. **Automatische Weiterleitung**
- **Sofortige Weiterleitung** bei abgelaufenen Sessions
- Session-Expired-Banner auf Login-Seite
- Schutz vor "hängenden" Sessions

## 🔧 Technische Implementation

### Backend-Änderungen

```python
@app.post("/api/admin/refresh", response_model=schemas.Token)
async def admin_refresh_token(
    current_user: models.AdminUser = Depends(auth.get_current_active_admin_user),
    db: Session = Depends(database.get_db)
):
    """Session/Token verlängern (Admin)"""
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.AuthManager.create_access_token(
        data={"sub": current_user.username}, expires_delta=access_token_expires
    )
    
    current_user.last_login = datetime.utcnow()
    db.commit()
    
    return {"access_token": access_token, "token_type": "bearer"}
```

### Frontend-Verbesserungen

#### AuthStore Enhancement
```typescript
// Neue Funktionen
refreshSession: async () => Promise<boolean>
validateSession: async () => Promise<boolean>
```

#### Session Timer Hook
```typescript
// 10-Minuten-Warnung statt 5-Minuten
isExpiringSoon: timeLeft > 0 && timeLeft <= 600 // 10 Minuten
```

#### Session Monitor Hook
```typescript
// Gestufte Warnungen
- 10 Minuten: Gelbe Warnung
- 5 Minuten: Rote kritische Warnung
- 0 Minuten: Automatischer Logout
```

## 🎯 Benutzerexperience

### Admin-Dashboard Header
```
┌─────────────────────────────────────────────────┐
│ Admin Dashboard              Session: 51:23 🟢  │
│ Willkommen, admin           [Session verlängern] │
│                                      [Abmelden] │
└─────────────────────────────────────────────────┘
```

### Warnsystem
1. **Normal (grün)**: Session aktiv: 51:23
2. **Warnung (gelb)**: Session läuft bald ab: 09:15 ⚠️
3. **Kritisch (rot)**: Session abgelaufen: 00:00 ❌

### Toast-Benachrichtigungen
- 🟡 **10 Minuten**: "Session läuft in weniger als 10 Minuten ab!"
- 🔴 **5 Minuten**: "Session läuft in weniger als 5 Minuten ab! Bitte verlängern Sie Ihre Session."
- ✅ **Verlängert**: "Session wurde erfolgreich verlängert!"
- ❌ **Abgelaufen**: "Session abgelaufen. Sie werden zur Anmeldung weitergeleitet..."

## 📱 Responsive Design

### Desktop
- Session-Timer im Header sichtbar
- Session-Button bei Warnung sichtbar

### Mobile
- Separate Session-Info-Leiste
- Kompakte Timer-Anzeige
- Touch-optimierte Buttons

## 🔒 Sicherheitsfeatures

### Auto-Logout
- **Sofortiger Logout** bei abgelaufenen Token
- Weiterleitung zur Login-Seite
- Session-Expired-Banner

### Token-Validation
- **Regelmäßige Validierung** alle 3 Minuten
- **Tab-Wechsel-Validation**
- **API-Call-basierte Prüfung**

### Secure Headers
- JWT-Token in Authorization Header
- Automatische Token-Refresh
- localStorage-Management

## 🧪 Testing

### Backend-Test
```bash
# Login
TOKEN=$(curl -s -X POST "http://localhost:8000/api/admin/login?username=admin&password=whHBJveMvwjs5a6p" | jq -r '.access_token')

# Session refreshen
curl -H "Authorization: Bearer $TOKEN" -s -X POST http://localhost:8000/api/admin/refresh
```

### Frontend-Test
1. Login im Admin-Bereich
2. Warten auf 10-Minuten-Warnung
3. Session-Verlängerung-Button klicken
4. Erfolgreiche Toast-Meldung bestätigen

## 📊 Session-Zeitlinie

```
60 Min ──────► 10 Min ──────► 5 Min ──────► 0 Min
  🟢             🟡             🔴           ❌
Normal        Warnung      Kritisch     Logout
```

## 🚀 Vorteile

### Für Benutzer
- **Nahtlose Experience**: Keine unerwarteten Logouts
- **Proaktive Warnungen**: Rechtzeitige Benachrichtigungen
- **Ein-Klick-Verlängerung**: Einfache Session-Verlängerung

### Für Administratoren
- **Sicherheit**: Automatischer Schutz vor Session-Hijacking
- **Usability**: Benutzerfreundliche Session-Verwaltung
- **Monitoring**: Klare Session-Status-Anzeige

Das verbesserte Session-Management bietet jetzt eine professionelle, sichere und benutzerfreundliche Authentifizierungserfahrung! 🎉
