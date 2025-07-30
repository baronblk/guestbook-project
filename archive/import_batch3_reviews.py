#!/usr/bin/env python3
"""
Import aller historischen Bewertungen für Coco de Mer
Batch 3: Reviews 15-1 (nächste 15 Reviews)
"""
import requests
import json
import time

# API Konfiguration
BASE_URL = "http://192.168.2.12:3000"
ADMIN_USER = "admin"
ADMIN_PASS = "whHBJveMvwjs5a6p"

def admin_login():
    """Admin login und JWT Token erhalten"""
    print("🔐 Admin-Anmeldung...")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/admin/login",
            params={
                "username": ADMIN_USER,
                "password": ADMIN_PASS
            }
        )
        
        if response.status_code == 200:
            print("✅ Admin-Anmeldung erfolgreich")
            result = response.json()
            token = result.get("access_token")
            if token:
                return token
            else:
                print("❌ Kein JWT Token erhalten")
                return None
        else:
            print(f"❌ Admin-Anmeldung fehlgeschlagen: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Verbindungsfehler: {e}")
        return None

def import_batch_3(token):
    """Importiere Batch 3: Reviews 15-1"""
    print("📦 Importiere Batch 3: Reviews 15-1...")
    
    reviews_batch_3 = [
        {
            "name": "Cornelia W.",
            "email": "imported.15@coco-de-mer.review",
            "rating": 5,
            "title": "Gemeinsame Familienauszeit - rundum perfekt",
            "content": "Wir buchten das Coco de Mer für eine gemeinsame Familienauszeit und konnten diese dank hervorragender Vorbereitungen seitens der Gastgeber in vollen Zügen genießen. Angefangen bei den tollen und unkomplizierten Buchungs-und Rechnungsmodalitäten, über die erhaltenen wichtigen Informationen vorab in Form einer digitalen Infomappe (so war die Möglichkeit gegeben, sich im Vorfeld über das Haus selbst sowie über Ausflugsziele, vorhandene Einkaufsmöglichkeiten bis hin zu Ärzten in der Umgebung zu informieren) bis natürlich zu dem sehr liebevoll eingerichtetem und sehr sauberem Haus selbst.... rundum perfekt! In diesem Haus wurde wirklich an alles gedacht und man konnte spüren, dass hier alles zur Zufriedenheit des Gastes vorbereitet wurde. Vielen Dank an die Gastgeber und auch den Objektbetreuer vor Ort für den tollen Service!!!!",
            "import_source": "Floatingdays"
        },
        {
            "name": "K_ Illing",
            "email": "imported.14@coco-de-mer.review",
            "rating": 5,
            "title": "Das Haus ist Bombe - alles drin was das Herz begehrt",
            "content": "Wir waren da zu viert für 11 Tage Und was soll ich Sagen? Das Haus ist Bombe! Es hat alles drin was das Herz begehrt. Massage-Betten, Sauna, Kamin, Dachterrasse... Alles Modern eingerichtet, und auch kleine Annehmlichkeiten (Getränke) oder andere Alltäglichen Sachen wie z.B einige Gewürze Tees etc sind ebenfalls vorhanden. Vermieter sind sehr nett und gehen auf die Wünsche anderer ein.",
            "import_source": "Google"
        },
        {
            "name": "Denise",
            "email": "imported.13@coco-de-mer.review",
            "rating": 5,
            "title": "Zwei traumhafte Wochen mit tollen Erlebnissen",
            "content": "Es waren zwei traumhafte Wochen mit tollen Erlebnissen. Egal ob SUP, Wanderungen, Städtetrips, ein Tag am Meer und und und. Ein besonderes Highlight war die Wellnessoase mit Sauna mit anschließender Abkühlung im Bodden oder auf der Terrasse, wobei man auch seinen Blick weitläufig über das Wasser schweifen lassen kann. Für Frühaufsteher ist zudem der Sonnenaufgang ein tolles Erlebnis, welchen man direkt aus dem Schlafzimmerfenster sehen und genießen kann. In Familie haben wir die tollen Frühstücke auf der Terrasse bei besten Blick und Sonne genossen. Es ist auf jeden Fall für jeden Geschmack etwas dabei.",
            "import_source": "Floatingdays"
        },
        {
            "name": "Jana Klässig",
            "email": "imported.12@coco-de-mer.review",
            "rating": 5,
            "title": "Sehr luxuriöses Haus - spitzenmäßiger Blick",
            "content": "Sehr luxuriöses Haus mit allen Annehmlichkeiten. Der Blick auf das Wasser ist spitzenmäßig. Da schmeckt das Frühstück richtig gut. Auch die SUPs machen riesigen Spaß. Nach der Sauna rein ins Wasser. Wo gibt es das schon. Schwimmen ist auch möglich aber bitte die Beine hoch nehmen. Mit dem Fahrrad kann man schöne Touren unternehmen, z.B. nach Dierhagen zum Strand. Wir haben uns sehr wohl gefühlt. Juli 2022",
            "import_source": "Google"
        },
        {
            "name": "R L F",
            "email": "imported.11@coco-de-mer.review",
            "rating": 5,
            "title": "Tolles Hausboot mit allem Luxus",
            "content": "Ein wirklich tolles Hausboot mit allem an Luxus, was man sich für einen gelungenen Urlaub so vorstellt. Es war geschmackvoll eingerichtet und sehr gut ausgestattet... es fehlte uns an nichts. Die Sauna war eine gelungene Abwechslung. Unser Highlight war aber der schöne Ausblick aufs Wasser beim Aufwachen, Entspannen auf der Couch oder Kochen. Wir haben es genossen auf der Bugterrasse zu frühstücken und auf der Dachterrase den Sonnenuntergang zu beobachten. Netter und unkomplizierter Kontakt zu den Besitzern und dem Verwalter. Nur zu empfehlen!!!",
            "import_source": "Google"
        },
        {
            "name": "Marcel Müller VissionSpa",
            "email": "imported.10@coco-de-mer.review",
            "rating": 5,
            "title": "Der Traum eines jeden Besuchers",
            "content": "Der Traum eines jeden Besuchers, mit einem unvergesslichen Ambiente. Massage und Wellness kann in jeglicher Form dazu gebucht werden, ein vollendeter Entspannungsmodus kann erfüllt werden, egal ob bei warmen Sonnenstrahlen auf dem Oberdeck oder mit schönster Aussicht und den Bodden mit dem Blick auf das Idyllische Ribnitz Damgarten. Wir heißen Sie herzlich Willkommen. Mit freundlichem Gruß Marcel Müller Vission Spa und Team",
            "import_source": "Gästebuch"
        },
        {
            "name": "Uli Münch",
            "email": "imported.9@coco-de-mer.review",
            "rating": 5,
            "title": "Teil des Einrichterteams - außergewöhnliches Haus",
            "content": "Wir waren als Teil des Einrichterteams auf dem Hausboot und können sagen, dass sich die Strapatzen mehr als gelohnt haben. Die Vermieter haben mit viel Aufwand, tolle Ideen für Luxus und vor allem Komfort umgesetzt. Seien es die übergroßen Betten, der Schiebetürenschrank im Schlafzimmer mit Einbautresor, die elektrisch verbreiterbare Sitzfläche der Couch bis hin zur Sauna und noch so vieles mehr. Sicher werde ich das außergewöhnliche Haus im Bodden in einem meiner nächsten Urlaube selbst einmal richtig genießen.",
            "import_source": "Google"
        },
        {
            "name": "Britt Anger",
            "email": "imported.8@coco-de-mer.review",
            "rating": 5,
            "title": "Liebevoll und luxuriös für alle Altersklassen",
            "content": "Ein liebevoll und luxuriös ausgestattetes Urlaubsdomizil für alle Altersklassen! Das schwimmende Haus Coco de Mer bietet alles für erholsame Urlaubstage: eine Terrasse mit Morgensonne zum Frühstücken, eine Sonnenterasse zum chillen und für kühle Tage einen Kamin und Sauna. Freizeitmöglichkeiten, wie z. B. Baden, Segeln Paddeln und Radfahren oder einfach im Lesecafe schmökern, gibt es reichlich. Wir kommen gerne wieder !",
            "import_source": "Google"
        },
        {
            "name": "Jan Meiwald",
            "email": "imported.7@coco-de-mer.review",
            "rating": 5,
            "title": "Sehr schön und liebevoll eingerichtet",
            "content": "Sehr schön und liebevoll eingerichtet. Die Schlüssel Übergabe lief problemlos. Haben eine Stunde vorher angerufen. Als wir ankamen war der Verwalter vor Ort und ließ uns ins Haus. Dabei gab er einen kurzen Abriß über die Technischen Einrichtungen. Es giebt online gute Erklärviedeos, zur Nutzung der Sauna und auch der Nutzung der Terrassenmöbel Handtuchheizer und zur Klimaanlage. Es ist empfehlenswert diese anzuschauen. Bis jetzt fühlen wir uns sehr Wohl in diesem Haus. Die Sauna ist sehr gemütlich. Die Küche ist modern eingerichtet. Küchenmesser sehr scharf. Meine Mädels haben sich den Empfohlenen Physiotherapeuten ins Haus bestellt und waren von der Behandlung hier im Haus sehr begeistert. Ist nur zu empfehlen.",
            "import_source": "Google"
        },
        {
            "name": "Sebastian Müller",
            "email": "imported.6@coco-de-mer.review",
            "rating": 5,
            "title": "Schönes Hausboot lädt zum entspannen ein",
            "content": "Schönes Hausboot, liebevoll eingerichtet, lädt zum entspannen ein. Für alle die das erste Mal auf einem Hausboot sind: es liegt sehr ruhig im Wasser.",
            "import_source": "Google"
        },
        {
            "name": "Daniela",
            "email": "imported.5@coco-de-mer.review",
            "rating": 5,
            "title": "Wunderschönes Hausboot - dem Alltagsstress entfliehen",
            "content": "Ein wunderschönes Hausboot, an einem tollen Ort lädt zu ruhigen entspannten Ferien ein. Hier kann man dem Alltagsstress für ein paar Tage entfliehen. Vielen Dank",
            "import_source": "Google"
        },
        {
            "name": "Philipp G",
            "email": "imported.4@coco-de-mer.review",
            "rating": 5,
            "title": "Sehr angenehmer Aufenthalt - Highlights Sauna und Wasserblick",
            "content": "Wir möchten uns hier auch nochmal ganz offiziell für den sehr angenehmen Aufenthalt bedanken. Wer einmal dem Alltagsstress entfliehen möchte ist hier gut aufgehoben. Die Einrichtung ist sehr modern. Meine persönlichen Highlights waren sowohl die Sauna, als auch das Aufwachen am Morgen mit direktem Blick aufs Wasser. Bis zum nächsten Mal!",
            "import_source": "Google"
        },
        {
            "name": "Klein Lisa",
            "email": "imported.3@coco-de-mer.review",
            "rating": 5,
            "title": "Wunderschönes Hausboot - super entspannt",
            "content": "Ein wunderschönes Hausboot, mit allem was das Herz begehrt. Ich konnte mich dort super entspannen und habe meine Zeit dort sehr genossen. Sehr zu empfehlen",
            "import_source": "Google"
        },
        {
            "name": "Marcel Müller VissionSpa (Duplicate)",
            "email": "imported.2@coco-de-mer.review",
            "rating": 5,
            "title": "Unvergessliches Ambiente - Massage und Wellness",
            "content": "Der Traum eines jeden Besuchers, mit einem unvergesslichen Ambiente. Massage und Wellness kann in jeglicher Form dazu gebucht werden, ein vollendeter Entspannungsmodus kann erfüllt werden, egal ob bei warmen Sonnenstrahlen auf dem Oberdeck oder mit schönster Aussicht und den Bodden mit dem Blick auf das Idyllische Ribnitz Damgarten. Wir heißen Sie herzlich Willkommen. Mit freundlichem Gruß Marcel Müller Vission Spa und Team",
            "import_source": "Gästebuch"
        },
        {
            "name": "René",
            "email": "imported.1@coco-de-mer.review",
            "rating": 5,
            "title": "Sehr schönes Domizil - hoffen dass es bald losgeht",
            "content": "Sehr schönes Domizil wollen wir hoffen dass es bald losgehen kann. Viele Grüße",
            "import_source": "Gästebuch"
        }
    ]
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    import_data = {
        "source": "historical_batch_3",
        "reviews": reviews_batch_3
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/admin/reviews/import",
            json=import_data,
            headers=headers
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Batch 3: {result.get('imported_count', 0)} Reviews erfolgreich importiert!")
            return True
        else:
            print("❌ Batch 3 Import fehlgeschlagen")
            return False
            
    except Exception as e:
        print(f"❌ Fehler beim Import von Batch 3: {e}")
        return False

def main():
    print("🚀 Coco de Mer Reviews Import - Batch 3")
    print("=" * 60)
    print(f"Target: {BASE_URL}")
    print()
    
    # Admin login
    token = admin_login()
    if token is None:
        print("Cannot proceed without admin login")
        return
    
    print()
    
    # Import Batch 3
    import_batch_3(token)
    
    print("\n🎉 Batch 3 Import abgeschlossen!")
    print("💡 Nächste Schritte:")
    print("   - Prüfe die importierten Reviews auf der Website")
    print("   - Führe dann Batch 4 (Review 0) aus")

if __name__ == "__main__":
    main()
