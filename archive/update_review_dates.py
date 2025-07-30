#!/usr/bin/env python3
"""
Update existing reviews with original dates
"""
import requests
import time
from datetime import datetime

# API base URL - using production container
API_BASE_URL = "http://192.168.2.12:3000/api"

def get_admin_token():
    """Get admin JWT token"""
    try:
        response = requests.post(f"{API_BASE_URL}/admin/login?username=admin&password=whHBJveMvwjs5a6p")
        if response.status_code == 200:
            return response.json()["access_token"]
        else:
            print(f"❌ Login failed: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Login error: {str(e)}")
        return None

def parse_date(date_str):
    """Parse date string DD.MM.YYYY to datetime"""
    try:
        return datetime.strptime(date_str, "%d.%m.%Y")
    except ValueError:
        print(f"⚠️ Invalid date format: {date_str}")
        return None

def get_existing_reviews(token):
    """Get all existing reviews"""
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{API_BASE_URL}/admin/reviews", headers=headers)
        if response.status_code == 200:
            return response.json().get("reviews", [])
        else:
            print(f"❌ Failed to fetch reviews: {response.text}")
            return []
    except Exception as e:
        print(f"❌ Error fetching reviews: {str(e)}")
        return []

def update_review_date(token, review_id, new_date):
    """Update a review's created_at date"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.put(f"{API_BASE_URL}/admin/reviews/{review_id}", 
                              json={"created_at": new_date.isoformat()}, 
                              headers=headers)
        return response.status_code in [200, 201]
    except Exception as e:
        print(f"❌ Error updating review {review_id}: {str(e)}")
        return False

# Name to date mapping from the original data
NAME_TO_DATE = {
    "Marcus & Sarah": "15.12.2024",
    "Familie Weber": "08.12.2024",
    "Thomas K.": "01.12.2024",
    "Lisa & Michael": "24.11.2024",
    "Andreas Schmidt": "17.11.2024",
    "Familie Müller": "10.11.2024",
    "Julia & Stefan": "03.11.2024",
    "Rentnergruppe Seeadler": "27.10.2024",
    "Markus B.": "20.10.2024",
    "Freundesgruppe Hamburg": "13.10.2024"
}

def main():
    print("🔄 Coco de Mer Reviews - Date Update")
    print("=" * 50)
    print(f"Target: {API_BASE_URL}")
    print()
    
    # Get admin token
    print("🔐 Admin-Anmeldung...")
    token = get_admin_token()
    if not token:
        return
    
    print("✅ Admin-Anmeldung erfolgreich")
    print()
    
    # Get existing reviews
    print("📋 Lade bestehende Reviews...")
    reviews = get_existing_reviews(token)
    print(f"✅ {len(reviews)} Reviews gefunden")
    print()
    
    # Update dates
    updated_count = 0
    for review in reviews:
        name = review["name"]
        review_id = review["id"]
        
        if name in NAME_TO_DATE:
            original_date = parse_date(NAME_TO_DATE[name])
            if original_date:
                if update_review_date(token, review_id, original_date):
                    updated_count += 1
                    print(f"✅ Review {review_id:2d}: {name[:30]:30} → {NAME_TO_DATE[name]}")
                else:
                    print(f"❌ Review {review_id:2d}: {name[:30]:30} - Update fehlgeschlagen")
            else:
                print(f"⚠️ Review {review_id:2d}: {name[:30]:30} - Ungültiges Datum")
        else:
            print(f"⚠️ Review {review_id:2d}: {name[:30]:30} - Kein Datum gefunden")
        
        time.sleep(0.2)  # Kurze Pause zwischen Updates
    
    print(f"\n📊 Update-Zusammenfassung:")
    print(f"   ✅ Aktualisiert: {updated_count}")
    print(f"   📋 Gesamt Reviews: {len(reviews)}")
    
    if updated_count > 0:
        print(f"\n🎉 {updated_count} Reviews erfolgreich mit Original-Datumsangaben aktualisiert!")
        print("🌐 Prüfe die Updates unter: http://192.168.2.12:3000")
    else:
        print("\n❌ Keine Reviews aktualisiert!")

if __name__ == "__main__":
    main()
