#!/usr/bin/env python3
"""
Import the last 2 missing reviews
"""
import requests
import time

# API base URL
API_BASE_URL = "http://localhost:8080/api"

# The 2 missing reviews
missing_reviews = [
    {
        "name": "Katharina S.",
        "date": "25.02.2024",
        "id": "6",
        "content": "Als Architektin bin ich begeistert von dem durchdachten Design und der hochwertigen Ausstattung. Jeder Quadratmeter ist optimal genutzt, ohne dass es beengt wirkt. Die Materialauswahl ist exquisit und die technische Ausstattung auf höchstem Niveau. Ein Meisterwerk des Houseboats-Designs!",
        "rating": 5,
        "title": "Design-Meisterwerk auf dem Wasser",
        "source": "Gästebuch"
    },
    {
        "name": "Familie Schneider",
        "date": "12.02.2024",
        "id": "5",
        "content": "Unser Familienurlaub mit drei Kindern war perfekt organisiert! Das Hausboot bietet genug Platz für alle und die sichere Terrasse gab den Kindern Freiheit zum Spielen. Die Eltern konnten in der Sauna entspannen, während die Kinder sicher spielten. Familienurlaub deluxe!",
        "rating": 5,
        "title": "Perfekter Familienurlaub mit drei Kindern",
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
    print("🚀 Importing the last 2 missing reviews...")
    
    for review in missing_reviews:
        print(f"Processing {review['name']}...")
        import_review(review)
        print("⏳ Waiting 5 seconds...")
        time.sleep(5)
    
    print("✅ Done!")

if __name__ == "__main__":
    main()
