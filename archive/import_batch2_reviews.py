#!/usr/bin/env python3
"""
Import aller historischen Bewertungen für Coco de Mer
Batch 2: Reviews 30-16 (nächste 15 Reviews)
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

def import_batch_2(token):
    """Importiere Batch 2: Reviews 30-16"""
    print("📦 Importiere Batch 2: Reviews 30-16...")
    
    reviews_batch_2 = [
        {
            "name": "Das Schmidtsche Rudel",
            "email": "imported.30@coco-de-mer.review",
            "rating": 5,
            "title": "Wohlfühlen ab der ersten Sekunde",
            "content": "Wir waren im August 2023 für 2 Wochen auf dem tollen Coco und habe die Zeit wahnsinnig genossen. Bei Ankunft wird man von der lieben Familie Hartwich begrüßt und in all die technischen Wunder des Coco eingeführt. Und dann kann die Erholung auch sofort beginnen, denn es ist alles da, was man dafür braucht. Morgens Sonnenaufgang auf der Terrasse unten, Frühstück dort im Idealfall in der Morgensonne, eine Runde schwimmen im Bodden, chillen auf der gemütlich eingerichteten Dachterrasse, Sonnenuntergang dann auch auf der Dachterrasse. Wo bekommt man schon mal beides an einem Ort. Und wenn das Wetter mal nordisch steif ist, auch kein Problem. Die Sauna ist ein Traum. Die ganze Wohnung ist urgemütlich, große Couch, liebevolle Gestaltung von allem. Tolle Ausstattung in der Küche. Es gibt NICHTS zu meckern. Und auch unsere Hündin fand den Aufenthalt super. Für die standen zwei Napfe und ein Deckchen bereit als wir ankamen. Das war auch toll, Hundebett mit Boddenblick. Jens und Jens, die beiden lieben Eigentümer, haben da eine Oase der Erholung geschaffen, die man einfach nur lieben, loben und weiterempfehlen kann.",
            "import_source": "Gästebuch"
        },
        {
            "name": "Ines",
            "email": "imported.29@coco-de-mer.review",
            "rating": 4,
            "title": "Vollkommen zufrieden - heimelige Atmosphäre",
            "content": "Wir haben vom 15. -23. Juli diesen Jahres unserem Urlaub in Coco de Mer verbracht und sind vollkommen zufrieden. Das Haus war sehr schön eingerichtet, sodass man sich direkt sehr wohl gefühlt hat. Die großen Fenster im Wohnzimmer von denen man den Ausblick über den Bodden genießen konnte, haben diese heimelige Atmosphäre unterstützt. Der Platz war vollkommen ausreichend für 4 Personen, da es 2 Badezimmern gab, kam man sich nie ins Gehege. Das Haus war zudem auch gut ausgestattet. In der Küche waren alle notwendigen Sachen vorhanden, um sich beispielsweise etwas Schönes zu Kochen. Auch verschiedene Gewürze standen zur Verfügung. Die Lage ist wie bereits erwähnt super. Zusammenfassend war es ein rundum gelungener Urlaub und ich kann Coco de Mer weiterempfehlen.",
            "import_source": "Gelbesterne"
        },
        {
            "name": "Ingenieur",
            "email": "imported.28@coco-de-mer.review",
            "rating": 4,
            "title": "Sehr positiv - mehr Kulanz erwartet",
            "content": "Sehr positiv. Im Sommer hatten wir kein Kamingas verbraucht, waren aber zur Zahlung verpflichtet. Bei nochmaliger Buchung hätten wir eine Gutschrift erhalten. Wir hätten bei den Tagespreisen von ca. Euro 400.- mehr Kulanz erwartet.",
            "import_source": "Gelbe-Sterne"
        },
        {
            "name": "Annett",
            "email": "imported.27@coco-de-mer.review",
            "rating": 5,
            "title": "Eine entspannte Woche im gemütlichen Coco de Mer",
            "content": "Eine entspannte Woche im gemütlichen Coco de Mer.",
            "import_source": "Gelbesterne"
        },
        {
            "name": "Barbara und Ricky",
            "email": "imported.26@coco-de-mer.review",
            "rating": 5,
            "title": "Wunderschöne Urlaubswoche - wir kommen wieder",
            "content": "Wir haben im April eine wunderschöne Urlaubswoche auf dem Coco de Mer verbracht, genossen die Aussichten, das Plätschern der Wellen, die Ruhe, das sehr geschmackvoll eingerichtete Floatinghaus... Sehr zu unserer Freude konnten wir sogar problemlos unseren Aufenthalt verlängern und wir sind uns sicher, dass wir mehr von diesem sehr entspannendem Urlaub wollen und auf jeden Fall wieder kommen!!! Liebe Grüße an Jens & Jens sowie die netten Hartwigs, die uns sehr freundlich empfangen und eingewiesen haben!!!",
            "import_source": "Gästebuch"
        },
        {
            "name": "Florian",
            "email": "imported.25@coco-de-mer.review",
            "rating": 5,
            "title": "Sehr schöner Kurzurlaub - perfekter Standort",
            "content": "Wir waren sehr begeistert von der Ausstattung, den liebevollen Details sowie der schönen Lage. Gerade als Ausgangspunkt für Radtouren entlang des Boddens bis hin zur Ostsee, ist es ein perfekter Standort. Zum entspannen lädt die schöne Dachterrasse und der Kamin, aber vor allem die schöne Sauna, ein. Es war ein rundum schöner Aufenthalt in einem wunderschönem Haus.",
            "import_source": "Gelbesterne"
        },
        {
            "name": "Anonym",
            "email": "imported.24@coco-de-mer.review",
            "rating": 5,
            "title": "Hausboot im Winter - Balsam für die Seele",
            "content": "Ein Hausboot im Winter ist Balsam für die Seele - besonders, wenn es so schön und gemütlich UND dann auch noch so komfortabel und praktisch ausgestattet ist wie das Coco de Mer!!",
            "import_source": "Gelbesterne"
        },
        {
            "name": "Tilo Weidig",
            "email": "imported.23@coco-de-mer.review",
            "rating": 5,
            "title": "Ein Traum - Selbstversorgerurlaub auf höchstem Niveau",
            "content": "Ein Traum! - hier ist ein Selbstversorgerurlaub auf allerhöchstem Niveau möglich. Bei der Ausstattung des Coco de mer fehlt es wahrlich an nichts. Hier wurde mit viel Liebe ein wunderschönes und kuscheliges Wohlfühlambiente geschaffen. Die Freundlichkeit der Vermieter, sowie die Umgebung mit der Nähe zur Ostsee umrahmen diese Entspannungsoase. Ein ganz großes Plus: Unsere beiden Vierbeiner waren ebenfalls herzlich willkommen und haben sich pudelwohl gefühlt. Was will man mehr?.... Wiederkommen!",
            "import_source": "Google"
        },
        {
            "name": "Familie Anger",
            "email": "imported.22@coco-de-mer.review",
            "rating": 5,
            "title": "Da muss man hin!",
            "content": "Dieses liebe- und geschmackvoll eingerichtete Haus lädt zum wiederkommen ein. Sowohl Aktiv- als auch Wellnessurlauber und Hundebesitzer können in diesem Haus und dieser herrlichen Gegend einen unvergesslichen Urlaub in Deutschland verleben. Sauberkeit und Service sind Top und die netten Vermieter lassen sich immer etwas einfallen, um die Gäste zu beeindrucken. Also auf bald !",
            "import_source": "Gelbesterne/Floatinghouses"
        },
        {
            "name": "Anja und Gerd",
            "email": "imported.21@coco-de-mer.review",
            "rating": 5,
            "title": "Traumhafte Auszeit - ein Geheimtipp",
            "content": "Das Coco de Mer ist ein Geheimtipp aus drei Gründen: 1. Ein schwimmendes Haus in romantischer Umgebung und Top Lage 2. Im liebevoll und mit vielen romantischen Überraschungen ausgestatteten Haus fehlt es an nichts 3. Und die Wellnessbehandlung neben der Sauna und Infrarotkabine im Haus durch Herrn Müller ist das Sahnehäubchen obendrauf ... besonders die Kräuterstempelmassage ein Traum... der Mann versteht sein Handwerk.",
            "import_source": "Gelbesterne/Floatinghouses"
        },
        {
            "name": "Karl-Uwe und Katrin",
            "email": "imported.20@coco-de-mer.review",
            "rating": 5,
            "title": "Das schwimmende Ferienhaus ist der Knaller",
            "content": "Das schwimmende Ferienhaus ist der Knaller. Die Liebe zum Detail ist bei der Ausstattung überall zu erkennen. Ob man einen Urlaub zum relaxen (vorhandene Sauna, 2 wunderschöne Terrassen und eine sehr gemütliche Wohnlandschaft) oder lieber aktiv sein möchte (direkter Zugang von der Terrasse in den Bodden, Fahrradweg vor dem Bootssteg). Wir waren nur zu einem Kurztrip in diesem herrlichen Urlaubsdomizil. Man fühlt sich garantiert wohl, egal welche Jahreszeit.",
            "import_source": "Gästebuch"
        },
        {
            "name": "Konstanze, Sigrid, Ralf und Heiko",
            "email": "imported.19@coco-de-mer.review",
            "rating": 5,
            "title": "Super schöne Winterwoche - perfektes Silvester",
            "content": "Wir haben eine super schöne Winterwoche im liebevoll eingerichteten und voll ausgestatteten Luxus Hausboot verbracht. Das weihnachtliche Ambiente und der Blick von der Dachterrasse auf das Silvester Feuerwerk haben den Aufenthalt perfekt gemacht. Coco de Mer wir kommen wieder.",
            "import_source": "Gästebuch"
        },
        {
            "name": "Hutzenohmd",
            "email": "imported.18@coco-de-mer.review",
            "rating": 5,
            "title": "Kunstwerk mit Herz - mehr als gelungen",
            "content": "Es war uns schon lange ein Bedürfnis das Kunstwerk mit Herz zu besichtigen. Ich kann nur sagen, es ist mehr als gelungen, ich war überrascht und begeistert und komme aus dem Schwärmen gar nicht raus.",
            "import_source": "Gästebuch"
        },
        {
            "name": "Gabriele S.",
            "email": "imported.17@coco-de-mer.review",
            "rating": 5,
            "title": "Traumurlaub mit Punktevieh",
            "content": "Es war für uns alle ein Traumurlaub. Dass wir unser Punktevieh dann auch noch mitbringen durften, war einfach toll. Vielen Dank an den Service. Wir wissen, dass Reinigen nach Hundebesuch schon sehr aufwendig ist. Wir haben uns täglich nach den Aktivitäten auf die Rückankunft im Hausboot gefreut. Dort hat der Tag immer den krönenden Abschluss erhalten. Es hat an nichts gefehlt.",
            "import_source": "Hundehotel.info"
        },
        {
            "name": "Susanne Freiberg",
            "email": "imported.16@coco-de-mer.review",
            "rating": 5,
            "title": "Super schön zum 88. Geburtstag der Schwiegermutter",
            "content": "Wir waren im September für 1 Woche anlässlich Geburtstag meiner Schwiegermutter (88Jahre) da. Ich kann nur sagen das Haus ist super schön, sauber, liebevoll eingerichtet und Herr Flagel ein super netter Mann der uns viele Hinweise zum Ort geben hat! Dieses Hausboot kann ich nur weiterempfehlen und würde auch sofort wenn die Zeit es zulassen würde wieder hin fahren! Wir haben uns sehr wohl gefühlt und nette Gespräche mit Jens waren einfach nur schön. Dankeschön nochmal für den wunderschönen Blumenstrauß für meine Schwiegermutter. Ach ja hab ich fast vergessen: Meine zwei süßen Hunden haben sich auch dort pudelwohl gefühlt! Körbchen und frisches Wasser war bei Ankunft schon bereitgestellt! Sogar Kotbeutel für die Hunde waren vorhanden! Einfach klasse Service und ganz nette Liebe Vermieter + Herr Flagel! Wir kommen wieder.",
            "import_source": "Gästebuch"
        }
    ]
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    import_data = {
        "source": "historical_batch_2",
        "reviews": reviews_batch_2
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
            print(f"✅ Batch 2: {result.get('imported_count', 0)} Reviews erfolgreich importiert!")
            return True
        else:
            print("❌ Batch 2 Import fehlgeschlagen")
            return False
            
    except Exception as e:
        print(f"❌ Fehler beim Import von Batch 2: {e}")
        return False

def main():
    print("🚀 Coco de Mer Reviews Import - Batch 2")
    print("=" * 60)
    print(f"Target: {BASE_URL}")
    print()
    
    # Admin login
    token = admin_login()
    if token is None:
        print("Cannot proceed without admin login")
        return
    
    print()
    
    # Import Batch 2
    import_batch_2(token)
    
    print("\n🎉 Batch 2 Import abgeschlossen!")
    print("💡 Nächste Schritte:")
    print("   - Prüfe die importierten Reviews auf der Website")
    print("   - Führe dann Batch 3 (Reviews 15-1) aus")

if __name__ == "__main__":
    main()
