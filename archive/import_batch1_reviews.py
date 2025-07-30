#!/usr/bin/env python3
"""
Import aller historischen Bewertungen für Coco de Mer
Batch 1: Reviews 45-31 (erste 15 Reviews)
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

def import_batch_1(token):
    """Importiere Batch 1: Reviews 45-31"""
    print("📦 Importiere Batch 1: Reviews 45-31...")
    
    reviews_batch_1 = [
        {
            "name": "Andrea Ackermann",
            "email": "imported.45@coco-de-mer.review",
            "rating": 5,
            "title": "Bequemes Bett mit Massagefunktion - alles perfekt!",
            "content": "Ein so bequemes Bett mit Massagefunktion hatten wir noch nie! Das Coco de Mer bietet einem alles, nein - es bietet noch mehr als man sich wünscht. Super sauber, liebevoll eingerichtet, sehr ruhig, aller mögliche technische Schnickschnack, den es heute so braucht, Sauna, Kamin und sogar 2 Hausengel, die einem willkommen heissen - sehr persönlich. Wenn man Erholung sucht, gerne gut isst, sich sportlich betätigen möchte, die Natur liebt, dann ist man hier richtig. Für uns am Schönsten war, dass wir unseren Pudel mitnehmen konnten. Solch hochwertige Unterkünfte sind für Hündler meist tabu. Für Badefans ist eher die nahe gelegene Ostsee, als der Bodden zu empfehlen. Alles ist genau so, wie in den Unterlagen beschrieben & auf die Tipps und Empfehlungen der Eigentümer ist Verlass. Mängel wären zu suchen! Wir kommen gerne wieder, trotz der langen Anreise.",
            "import_source": "Google"
        },
        {
            "name": "Falkenseeer",
            "email": "imported.44@coco-de-mer.review",
            "rating": 5,
            "title": "Sehr schönes Hausboot mit Wellness Oase!",
            "content": "Sehr schönes Hausboot mit Wellness Oase! Wir haben einen super Urlaub auf einem traumhaften Hausboot verbracht. Alles lief reibungslos und ist so wie in der Anzeige beschrieben.",
            "import_source": "Google"
        },
        {
            "name": "Gitta Fischer",
            "email": "imported.43@coco-de-mer.review",
            "rating": 5,
            "title": "Wiederholungsurlauber - perfekte Auszeit",
            "content": "Wir sind als Wiederholungurlauber im sonnigen, aber kalten März 2025 im wunderschönen Coco de Mer gewesen. Nach ausgiebigen Boddenwanderungen gibt es fast nicht schöneres, als in das warme Seychellenflair (Sauna) einzutauchen. Wie beim letzten Besuch war einfach alles wieder perfekt und nach unserem damaligen Hinweis, dass doch ein gemütlicher Lesesessel mit Blick auf das Wasser toll wäre, haben die Vermieter diesen Tipp prompt umgesetzt. Danke und bis bald.",
            "import_source": "Google"
        },
        {
            "name": "Meiwald Jan",
            "email": "imported.42@coco-de-mer.review",
            "rating": 5,
            "title": "Bereits zum 2. Mal - Erwartungen mehr als erfüllt",
            "content": "Bereits zum 2. Mal haben wir einen Kurzurlaub auf dem Coco de Mer verbracht. Wieder wurden unsere Erwartungen mehr als erfüllt. Wir haben die bequemen Betten, die frische Luft um die Nase auf den großzügigen Terrassen, die entspannende Sauna im kleinen Wellnessbereich und auch auch den neuen Lesestuhl vor den riesigen Fenstern sehr genossen. Durch die ebenerdigkeit fast aller Einrichtungen war der Aufenthalt auch für unseren sehbeeinträchtigten Bruder eine echte Erholung. Sehr gerne kommen wir wieder zu Euch.",
            "import_source": "Gästebuch"
        },
        {
            "name": "Heiko Wolf",
            "email": "imported.41@coco-de-mer.review",
            "rating": 5,
            "title": "Schönes Silvester am Kaminfeuer",
            "content": "Wie immer hatten wir, trotz schlechtem Wetter, einen schönen und gemütlichen Aufenthalt am Kaminfeuer. Wir haben das Silvester Feuerwerk von der Dachterrasse perfekt genossen.",
            "import_source": "Google"
        },
        {
            "name": "Gudrun, Manfred, Helga und Jürgen",
            "email": "imported.40@coco-de-mer.review",
            "rating": 5,
            "title": "320 Jahre Jubiläumsgeburtstage auf den Seychellen",
            "content": "Coco de Meer funktional und äußerst geschmackvoll, mit viel Liebe zum Detail, eingerichtete Bleibe - hier steckt echt Herzblut drin. Wer hätte gedacht, dass wir unsere Jubiläumsgeburtstage (320 Jahre) 3 Tage auf den Seychellen verbringen können! Wir haben die Zeit und die Annehmlichkeiten hier in vollen Umfang genossen. Sogar der Seegang wird, sonst nicht bemerkbar, mit den Lampen über dem Esstisch angezeigt. Das Wetter glich zwar nicht dem Indischen Ozean, aber wir haben eine tolle Darssrundfahrt gemacht u. waren sogar auf dem Leuchtturm. Den beiden Jensén danken wir herzlich, wünschen alles gute, beste Gesundheit und Erholung bei den eigenen Auszeiten sowie weiterhin viele neugierige Gäste.",
            "import_source": "Gästebuch"
        },
        {
            "name": "Abendstern",
            "email": "imported.39@coco-de-mer.review",
            "rating": 5,
            "title": "Rundum wohl gefühlt",
            "content": "Wir haben uns rundum wohl gefühlt! Das Hausboot ist liebevoll eingerichtet und bietet alles was man im Urlaub braucht!",
            "import_source": "Google"
        },
        {
            "name": "M., Yvonne",
            "email": "imported.38@coco-de-mer.review",
            "rating": 5,
            "title": "13 Übernachtungen - super schöne Zeit",
            "content": "Wir (mein Partner, ich und unser Hund) waren Anfang Juli 2024 für 13 Übernachtungen im Coco de Mer. Wir hatten eine super schöne Zeit auf dem Hausboot und werden es def. nochmal buchen. Die von den Vermietern eingestellten Bilder stimmen wirklich mit der Realität überein. Alles ist mit sehr viel Liebe eingerichtet. Der Kontakt mit den Vermietern war klasse, die sind supernett. Vor Ort ist ein liebes Pärchen als Objektverwalter, die uns herzlich empfangen und alles auf dem Hausboot erklärt haben. Für unseren Hund war ein kleines Körbchen/Hundekissen vorhanden, Näpfe für Futter und Wasser waren vorhanden, sogar eine Taschenlampe mit Hundekotbeutel wurde uns gestellt. Die Schlafzimmer waren mit Bett (und mit nicht durchgelegenen Matratzen), Schrank, Nachttischen, USB-Stecker ausgestattet. Beim Masterschlafzimmer hat man einen traumhaften Blick aufs Wasser. Die Küche ist auch mit allem ausgestattet, was man benötigt. Auf der unteren Terrasse kann man morgens schon in der Sonne frühstücken. Eine Sauna ist ebenfalls vorhanden, die haben wir aber nicht getestet, da wir wirklich top Wetter hatten. Vom Sonnendeck kann man superschöne Sonnenuntergänge erleben. Auch tagsüber kann man sich dort gut entspannen und sonnen. Die Innenstadt ist in wenigen Minuten fußläufig zu erreichen. Wir können das Coco de Mer sehr empfehlen, gleich vom ersten Tag war es Erholung pur.",
            "import_source": "Hundehotel.info"
        },
        {
            "name": "Kleene Maus",
            "email": "imported.37@coco-de-mer.review",
            "rating": 5,
            "title": "Erster Hausboot-Urlaub - sofort wie zu Hause gefühlt",
            "content": "Für uns war es der erste Urlaub auf einem Hausboot und wir haben uns sofort wie zu Hause gefühlt. Alles ist so liebevoll und bis ins kleinste Detail eingerichtet, so dass es einem an nichts fehlt. Das Hausboot ist perfekt geschnitten, somit finden hier bis zu 6 Personen bequem Platz. Auch unsere Vierbeiner waren herzlich willkommen und Sie haben sich sehr wohl gefühlt. Dank der Sauna und der großen Außenterrasse, mit einem wunderschönen Blick auf den Bodden, kann man das Hausboot zu jeder Jahreszeit genießen. Vielen lieben Dank für die tolle Auszeit und den herzlichen Empfang.",
            "import_source": "Google"
        },
        {
            "name": "Traumhafter Sonnenuntergang",
            "email": "imported.36@coco-de-mer.review",
            "rating": 5,
            "title": "Wunderschöne Unterkunft in traumhafter Lage",
            "content": "Eine wunderschöne Unterkunft in absolut ruhiger und traumhafter Lage! Ideal, um vom Alltag abzuschalten und ein romantisches Nest für Paare.",
            "import_source": "Traumferienwohnungen.de"
        },
        {
            "name": "Fam. Hirsch",
            "email": "imported.35@coco-de-mer.review",
            "rating": 5,
            "title": "Jederzeit wieder - beste Unterkunft mit Hund",
            "content": "Jederzeit wieder. Für uns mit Hund die beste Unterkunft. Es fehlte an nichts. Alles sehr geschmackvoll und liebevoll eingerichtet. Besonders toll fanden wir die Sauna sowie das Massagebett mit Blick aufs Wasser um den Sonnenaufgang oder am Abend den Sternenhimmel beobachten zu können. Selbst bei Regenwetter wird s ein in diesem Domizil nicht langweilig. Wir sagen Danke für diese schöne Zeit die wir dort verbringen durften.",
            "import_source": "Hundeurlaub.de"
        },
        {
            "name": "Irmgard",
            "email": "imported.34@coco-de-mer.review",
            "rating": 5,
            "title": "Erstklassiges Ambiente - absoluter Erholungsurlaub",
            "content": "Urlaub im August 2023 auf der Coco de Mer. Super herzlicher Empfang und Betreuung durch Familie Hartwich! Ein wunderbares Hausboot, mit erstklassigem Ambiente, phantastische Einrichtung - mit Liebe ausgestattet und dekoriert - hier fehlt es an Nichts. Die Sauna ist ein Highlight. Absoluter Erholungsurlaub!",
            "import_source": "Gästebuch"
        },
        {
            "name": "Christian u. Jana Z.",
            "email": "imported.33@coco-de-mer.review",
            "rating": 5,
            "title": "Zauberhafte Jahreswende im Coco de Mer",
            "content": "Wir habe den Jahreswechsel als Gäste im Coco de Mer verbracht. Und es war zauberhaft. Schon der herzliche Empfang durch Familie H. ließ uns mit Entspannung in die freien Tage starten. Das Feriendomizil ist mit viel Liebe zum Detail eingerichtet, so hatten wir noch eine weihnachtliche Atmosphäre. Auch unsere Hundedame Daisy war willkommen und fand Näpfe und ein Deckchen zum kuscheln vor. Es fehlte einem an nichts. Man kann von hier schöne Spaziergänge mit dem Hund unternehmen und auch das Zentrum ist zu Fuß zu erreichen. Zur Ostsee sind es nur wenige Minuten mit dem Auto. Alles in allem haben wir uns dort verdammt wohl gefühlt, ob entspannt in der eigenen Sauna oder bei Kaminfeuer auf der gemütlichen Couch den Abend ausklingen lassen. Es war einfach herrlich, so dass wir schon den nächsten Besuch im Coco de Mer planen.",
            "import_source": "Gästebuch"
        },
        {
            "name": "Reinhold HANNBERGER",
            "email": "imported.32@coco-de-mer.review",
            "rating": 5,
            "title": "Fantastischer Urlaub - tolle Unterkunft für Mensch und Hund",
            "content": "Ein fantastischer Urlaub. So eine tolle Unterkunft für Mensch und Hund. Es fehlt an nichts! Vom orthopädischen Bett mit Massagefunktion, Sauna mit 3 verschiedenen Wellnessprogrammen, ob Infrarot oder Finnische Sauna, Sonnendeck, Waschmaschine und voll ausgestattete Küche, die keine Wünsche offen lässt. Das Ferienhaus auf dem Wasser ist einzigartig. Können es nur mit gutem Gewissen empfehlen. September 2023 Helga, Reinhold mit den Hunden Dotti und Alma.",
            "import_source": "Google"
        },
        {
            "name": "Jenny & René",
            "email": "imported.31@coco-de-mer.review",
            "rating": 5,
            "title": "Wunderschöne und entspannte Woche",
            "content": "Wir hatten eine wunderschöne und entspannte Woche auf dem Hausboot. Uns hat es an nichts gefehlt und selbst für unsere Fellnasen war gesorgt. Jeden Tag diesen schönen Ausblick von der Terrasse oder vom Wasser aus zu genießen war einfach ein Traum. Wir kommen gerne wieder!!",
            "import_source": "Gästebuch"
        }
    ]
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    import_data = {
        "source": "historical_batch_1",
        "reviews": reviews_batch_1
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
            print(f"✅ Batch 1: {result.get('imported_count', 0)} Reviews erfolgreich importiert!")
            return True
        else:
            print("❌ Batch 1 Import fehlgeschlagen")
            return False
            
    except Exception as e:
        print(f"❌ Fehler beim Import von Batch 1: {e}")
        return False

def main():
    print("🚀 Coco de Mer Reviews Import - Batch 1")
    print("=" * 60)
    print(f"Target: {BASE_URL}")
    print()
    
    # Admin login
    token = admin_login()
    if token is None:
        print("Cannot proceed without admin login")
        return
    
    print()
    
    # Import Batch 1
    import_batch_1(token)
    
    print("\n🎉 Batch 1 Import abgeschlossen!")
    print("💡 Nächste Schritte:")
    print("   - Prüfe die importierten Reviews auf der Website")
    print("   - Führe dann Batch 2 (Reviews 30-16) aus")

if __name__ == "__main__":
    main()
