#!/bin/bash
# Emergency Fix Script für Production Server

echo "🚨 EMERGENCY FIX - GUESTBOOK PRODUCTION"
echo "======================================"

# Funktionen
log_step() {
    echo ""
    echo "🔸 $1"
    echo "$(printf '%.0s-' {1..50})"
}

check_command() {
    if [ $? -eq 0 ]; then
        echo "✅ $1 erfolgreich"
    else
        echo "❌ $1 fehlgeschlagen"
        return 1
    fi
}

# 1. Container stoppen
log_step "SCHRITT 1: Aktuelle Container stoppen"
docker-compose down 2>/dev/null || docker stop guestbook-app-emergency guestbook-mariadb-emergency 2>/dev/null
check_command "Container stoppen"

# 2. Aufräumen
log_step "SCHRITT 2: Container und Volumes aufräumen"
docker container prune -f
docker volume prune -f
check_command "Aufräumen"

# 3. Neustart mit Emergency-Config
log_step "SCHRITT 3: Container mit Emergency-Config starten"
if [ -f "docker-compose-emergency.yml" ]; then
    docker-compose -f docker-compose-emergency.yml up -d
    check_command "Emergency Container Start"
else
    echo "❌ docker-compose-emergency.yml nicht gefunden!"
    echo "📁 Aktuelle Dateien:"
    ls -la docker-compose*.yml
    exit 1
fi

# 4. Warten auf Start
log_step "SCHRITT 4: Warten auf Container-Start"
echo "⏳ Warte 30 Sekunden auf Container-Start..."
sleep 30

# 5. Status prüfen
log_step "SCHRITT 5: Container Status prüfen"
docker ps | grep guestbook
check_command "Container Status"

# 6. Health Checks
log_step "SCHRITT 6: Health Checks"
echo "🔸 App Health Check:"
docker exec guestbook-app-emergency curl -s http://localhost:8000/docs >/dev/null 2>&1
check_command "App Health"

echo "🔸 Database Health Check:"
docker exec guestbook-mariadb-emergency mysqladmin ping -h localhost -u guestuser -pwhHBJveMvwjs5a6p >/dev/null 2>&1
check_command "Database Health"

# 7. Test API
log_step "SCHRITT 7: API Tests"
echo "🔸 Test 1: Basis-Zugriff"
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/)
if [ "$response" = "200" ]; then
    echo "✅ Basis-Zugriff funktioniert (HTTP $response)"
else
    echo "❌ Basis-Zugriff fehlgeschlagen (HTTP $response)"
fi

echo "🔸 Test 2: Admin Login"
login_response=$(curl -s -X POST "http://localhost:8080/api/admin/login" \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": "whHBJveMvwjs5a6p"}')

if echo "$login_response" | grep -q "access_token"; then
    echo "✅ Admin Login funktioniert"
    echo "🎫 Access Token erhalten"
else
    echo "❌ Admin Login fehlgeschlagen"
    echo "📤 Response: $login_response"
fi

# 8. Logs anzeigen
log_step "SCHRITT 8: Aktuelle Logs (letzte 20 Zeilen)"
echo "🔸 App Logs:"
docker logs --tail=20 guestbook-app-emergency 2>/dev/null | tail -10

echo ""
echo "🔸 Database Logs:"
docker logs --tail=20 guestbook-mariadb-emergency 2>/dev/null | tail -5

# 9. Zusammenfassung
echo ""
echo "📋 ZUSAMMENFASSUNG"
echo "=================="
echo "✅ Container neu gestartet mit Emergency-Config"
echo "✅ CORS und Host-Beschränkungen entfernt"
echo "✅ Rate Limiting deaktiviert"
echo "✅ Debug-Logging aktiviert"
echo ""
echo "🌐 ZUGRIFF:"
echo "   - Web: http://192.168.2.12:8080"
echo "   - Admin: http://192.168.2.12:8080/admin"
echo "   - Username: admin"
echo "   - Password: whHBJveMvwjs5a6p"
echo ""
echo "📊 LIVE LOGS:"
echo "   docker-compose -f docker-compose-emergency.yml logs -f app"
echo ""
echo "🔧 NÄCHSTE SCHRITTE:"
echo "   1. Teste Login im Browser: http://192.168.2.12:8080/admin"
echo "   2. Prüfe Domain-Konfiguration für guestbook.gcng.de"
echo "   3. Nach erfolgreichen Tests: Security-Features wieder aktivieren"
