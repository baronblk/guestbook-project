#!/usr/bin/env python3
"""
Import the remaining 10 missing reviews from the complete list of 46
"""
import requests
import time

# API base URL
API_BASE_URL = "http://localhost:8080/api"

# The 10 missing reviews based on the provided complete list
missing_reviews = [
    {
        "name": "Fam. Hirsch",
        "date": "05.04.2024",
        "id": "35",
        "content": "Jederzeit wieder. Für uns mit Hund die beste Unterkunft. Es fehlte an nichts. Alles sehr geschmackvoll und liebevoll eingerichtet. Besonders toll fanden wir die Sauna sowie das Massagebett mit Blick aufs Wasser um den Sonnenaufgang oder am Abend den Sternenhimmel beobachten zu können. Selbst bei Regenwetter wird s ein in diesem Domizil nicht langweilig. Wir sagen Danke für diese schöne Zeit die wir dort verbringen durften. Herzliche Grüße aus Berlin",
        "rating": 5,
        "title": "Übernommene Rezension von Hundeurlaub.de vom 05.04.24",
        "source": "Hundeurlaub.de"
    },
    {
        "name": "Irmgard",
        "date": "23.03.2024",
        "id": "34",
        "content": "Urlaub im August 2023 auf der Coco de Mer Super herzlicher Empfang und Betreuung durch Familie Hartwich! Ein wunderbares Hausboot, mit erstklassigem Ambiente, phantastische Einrichtung - mit Liebe ausgestattet und dekoriert - hier fehlt es an Nichts. Die Sauna ist ein Highlight. Absoluter Erholungsurlaub!",
        "rating": 5,
        "title": "Super herzlicher Empfang und Betreuung",
        "source": "Gästebuch"
    },
    {
        "name": "Christian u. Jana Z.",
        "date": "03.01.2024",
        "id": "33",
        "content": "Wir habe den Jahreswechsel als Gäste im Coco de Mer verbracht. Und es war zauberhaft. Schon der herzliche Empfang durch Familie H. ließ uns mit Entspannung in die freien Tage starten. Das Feriendomizil ist mit viel Liebe zum Detail eingerichtet, so hatten wir noch eine weihnachtliche Atmosphäre (ich bin ein kleiner Weihnachtsfreak). Auch unsere Hundedame Daisy war willkommen und fand Näpfe und ein Deckchen zum kuscheln vor. Es fehlte einem an nichts. Man kann von hier schöne Spaziergänge mit dem Hund unternehmen und auch das Zentrum ist zu Fuß zu erreichen. Zur Ostsee sind es nur wenige Minuten mit dem Auto. Alles in allem haben wir uns dort verdammt wohl gefühlt, ob entspannt in der eigenen Sauna oder bei Kaminfeuer auf der gemütlichen Couch den Abend ausklingen lassen. Es war einfach herrlich, so dass wir schon den nächsten Besuch im Coco de Mer planen.",
        "rating": 5,
        "title": "Zauberhafter Jahreswechsel im Coco de Mer",
        "source": "Gästebuch"
    },
    {
        "name": "Reinhold HANNBERGER",
        "date": "04.10.2023",
        "id": "32",
        "content": "Ein fantastischer Urlaub. So eine tolle Unterkunft für Mensch und Hund. Es fehlt an nichts! Vom orthopädischen Bett mit Massagefunktion, Sauna mit 3 verschiedenen Wellnessprogrammen, ob Infrarot oder Finnische Sauna, Sonnendeck, Waschmaschine und voll ausgestattete Küche, die keine Wünsche offen lässt. Das Ferienhaus auf dem Wasser ist einzigartig. Können es nur mit gutem Gewissen empfehlen. September 2023 Helga, Reinhold mit den Hunden Dotti und Alma",
        "rating": 5,
        "title": "Übernommene Google-Rezension vom 03.10.2023",
        "source": "Google"
    },
    {
        "name": "Jenny & René",
        "date": "11.09.2023",
        "id": "31",
        "content": "Wir hatten eine wunderschöne und entspannte Woche auf dem Hausboot. Uns hat es an nichts gefehlt und selbst für unsere Fellnasen war gesorgt. Jeden Tag diesen schönen Ausblick von der Terrasse oder vom Wasser aus zu genießen war einfach ein Traum. Wir kommen gerne wieder!!",
        "rating": 5,
        "title": "Wunderschöne und entspannte Woche",
        "source": "Gästebuch"
    },
    {
        "name": "Das Schmidtsche Rudel",
        "date": "29.08.2023",
        "id": "30",
        "content": "Wir waren im August 2023 für 2 Wochen auf dem tollen Coco und habe die Zeit wahnsinnig genossen. Bei Ankunft wird man von der lieben Familie Hartwich begrüßt und in all die technischen Wunder des Coco eingeführt. Und dann kann die Erholung auch sofort beginnen, denn es ist alles da, was man dafür braucht. Morgens Sonnenaufgang auf der Terrasse unten, Frühstück dort im Idealfall in der Morgensonne, eine Runde schwimmen im Bodden, chillen auf der gemütlich eingerichteten Dachterrasse, Sonnenuntergang dann auch auf der Dachterrasse. Wo bekommt man schon mal beides an einem Ort. Schön! Und wenn das Wetter mal nordisch steif ist, auch kein Problem. Die Sauna ist ein Traum. Die ganze Wohnung ist urgemütlich, große Couch, liebevolle Gestaltung von allem. Tolle Ausstattung in der Küche. Es gibt NICHTS zu meckern. Und auch unsere Hündin fand den Aufenthalt super. Für die standen zwei Napfe und ein Deckchen bereit als wir ankamen. Das war auch toll, Hundebett mit Boddenblick. Jens und Jens, die beiden lieben Eigentümer, haben da eine Oase der Erholung geschaffen, die man einfach nur lieben, loben und weiterempfehlen kann. Die beiden versorgen einen mit tollen Tipps zu Ausflügen und den besten Torten der Umgebung. Auch ein ganz besonderer Kontakt, so wie wir ihn noch nie erlebt haben bei anderen Objekten. Ihr macht das großartig!!! Wir werden auf alle Fälle sehr, sehr gerne einmal wiederkommen.",
        "rating": 5,
        "title": "Urlaub im Coco de Mer heißt Wohlfühlen ab der ersten Sekunde",
        "source": "Gästebuch"
    },
    {
        "name": "Ines",
        "date": "03.08.2023",
        "id": "29",
        "content": "Wir haben vom 15. -23. Juli diesen Jahres unserem Urlaub in Coco de Mer verbracht und sind vollkommen zufrieden. Das Haus war sehr schön eingerichtet, sodass man sich direkt sehr wohl gefühlt hat. Die großen Fenster im Wohnzimmer von denen man den Ausblick über den Bodden genießen konnte, haben diese heimelige Atmosphäre unterstützt. Der Platz war vollkommen ausreichend für 4 Personen, da es 2 Badezimmern gab, kam man sich nie ins Gehege. Ich würde allerdings nicht empfehlen mit mehr als 4 Personen anzureisen, da es dann doch etwas eng wird. Das Haus war zudem auch gut ausgestattet. In der Küche waren alle notwendigen Sachen vorhanden, um sich beispielsweise etwas Schönes zu Kochen. Auch verschiedene Gewürze standen zur Verfügung. Die Lage ist wie bereits erwähnt super. Man liegt jedoch etwas abgeschieden vom Zentrum der Stadt, daher der eine Stern Abzug. Das Zentrum ist aber dennoch gut zu Fuß oder mit dem Fahrrad erreichbar. Zusammenfassend war es ein rundum gelungener Urlaub und ich kann Coco de Mer weiterempfehlen.",
        "rating": 4,
        "title": "Übernommene Gelbesterne-Rezension vom 30.07.23",
        "source": "Gelbesterne"
    },
    {
        "name": "Ingenieur",
        "date": "03.08.2023",
        "id": "28",
        "content": "Sehr positiv. Im Sommer hatten wir kein Kamingas verbraucht, waren aber zur Zahlung verpflichtet. Bei nochmaliger Buchung hätten wir eine Gutschrift erhalten. Wir hätten bei den Tagespreisen von ca. Euro 400.-mehr Kulanz erwartet.",
        "rating": 4,
        "title": "Übernommene Gelbe-Sterne-Bewertung vom 20.07.22",
        "source": "Gelbe-Sterne"
    },
    {
        "name": "Annett",
        "date": "11.06.2023",
        "id": "27",
        "content": "Eine entspannte Woche im gemütlichen Coco de Mer.",
        "rating": 5,
        "title": "Übernommene Gelbesterne-Rezension vom 28.05.23",
        "source": "Gelbesterne"
    },
    {
        "name": "Barbara und Ricky",
        "date": "08.05.2023",
        "id": "26",
        "content": "Wir haben im April eine wunderschöne Urlaubswoche auf dem Coco de Mer verbracht,genossen die Aussichten, das Plätschern der Wellen, die Ruhe, das sehr geschmackvoll eingerichtete Floatinghaus... Sehr zu unserer Freude konnten wir sogar problemlos unseren Aufenthalt verlängern und wir sind uns sicher, dass wir mehr von diesem sehr entspannendem Urlaub wollen und auf jeden Fall wieder kommen!!! Liebe Grüße an Jens & Jens sowie die netten Hartwigs, die uns sehr freundlich empfangen und eingewiesen haben!!!",
        "rating": 5,
        "title": "Wunderschöne Urlaubswoche mit Verlängerung",
        "source": "Gästebuch"
    }
]

def import_review(review_data):
    """Import a single review"""
    api_data = {
        "name": review_data["name"],
        "email": f"import_{review_data['id']}@coco-de-mer.de",
        "rating": review_data["rating"],
        "title": review_data["title"],
        "content": review_data["content"]
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/reviews", json=api_data)
        if response.status_code == 200:
            review = response.json()
            print(f"✓ Imported: {review_data['name']} (ID: {review['id']})")
            return True
        else:
            print(f"✗ Failed to import {review_data['name']}: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Error importing {review_data['name']}: {str(e)}")
        return False

def main():
    print("🚀 Importing the final 10 missing reviews...")
    print(f"📝 Found {len(missing_reviews)} reviews to import")
    
    imported_count = 0
    failed_count = 0
    
    for i, review in enumerate(missing_reviews):
        print(f"\n[{i+1}/{len(missing_reviews)}] Processing {review['name']}...")
        
        if import_review(review):
            imported_count += 1
        else:
            failed_count += 1
        
        # Wait between requests to avoid rate limiting
        if i < len(missing_reviews) - 1:
            print("⏳ Waiting 4 seconds...")
            time.sleep(4)
    
    print(f"\n📊 Final Import Summary:")
    print(f"✅ Successfully imported: {imported_count}")
    print(f"❌ Failed imports: {failed_count}")
    print(f"📈 Total processed: {len(missing_reviews)}")
    
    # Check final count
    try:
        response = requests.get(f"{API_BASE_URL}/reviews")
        if response.status_code == 200:
            total = response.json().get("total", 0)
            print(f"🎯 Total reviews now in database: {total}")
            if total >= 46:
                print("🎉 All 46 reviews successfully imported!")
        else:
            print("❌ Could not verify final count")
    except Exception as e:
        print(f"❌ Error checking final count: {str(e)}")

if __name__ == "__main__":
    main()
