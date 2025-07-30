#!/usr/bin/env python3
"""
Import the last 2 missing reviews with original dates
"""
import requests
import time

# API base URL - using production container
API_BASE_URL = "http://192.168.2.12:3000/api"

# JWT Token for admin access
JWT_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTc1MzgwOTYwMH0.oDOYSfFEiGh6lhsI7_Vgvgl6wQvmzg7VNlNqhHhHrJ0"

# The 2 missing reviews with original dates
missing_reviews = [
    {
        "name": "Katharina S.",
        "content": "Als Architektin bin ich begeistert von dem durchdachten Design und der hochwertigen Ausstattung. Jeder Quadratmeter ist optimal genutzt, ohne dass es beengt wirkt. Die Materialauswahl ist exquisit und die technische Ausstattung auf höchstem Niveau. Ein Meisterwerk des Houseboats-Designs!",
        "import_source": "Gästebuch - 25.02.2024"
    },
    {
        "name": "Familie Schneider", 
        "content": "Unser Familienurlaub mit drei Kindern war perfekt organisiert! Das Hausboot bietet genug Platz für alle und die sichere Terrasse gab den Kindern Freiheit zum Spielen. Die Eltern konnten in der Sauna entspannen, während die Kinder sicher spielten. Familienurlaub deluxe!",
        "import_source": "Gästebuch - 12.02.2024"
    }
]

def import_review(review_data):
    """Import a single review using admin endpoint"""
    headers = {
        "Authorization": f"Bearer {JWT_TOKEN}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/admin/reviews/import", 
                               json=[review_data], 
                               headers=headers)
        if response.status_code == 200:
            result = response.json()
            print(f"✓ Imported: {review_data['name']} - {result.get('message', 'Success')}")
            return True
        else:
            print(f"✗ Failed to import {review_data['name']}: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Error importing {review_data['name']}: {str(e)}")
        return False

def main():
    print("🚀 Importing the last 2 missing reviews with original dates...")
    
    imported_count = 0
    for review in missing_reviews:
        print(f"Processing {review['name']}...")
        if import_review(review):
            imported_count += 1
        print("⏳ Waiting 2 seconds...")
        time.sleep(2)
    
    print(f"✅ Done! Successfully imported {imported_count} reviews with original dates!")

if __name__ == "__main__":
    main()
