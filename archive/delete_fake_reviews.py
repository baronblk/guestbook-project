#!/usr/bin/env python3
"""
Delete all fake reviews and import REAL guest reviews
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

def delete_all_reviews(token):
    """Delete all existing reviews"""
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        # Get all reviews
        response = requests.get(f"{API_BASE_URL}/admin/reviews?per_page=100", headers=headers)
        if response.status_code == 200:
            reviews = response.json().get("reviews", [])
            print(f"🗑️ Lösche {len(reviews)} falsche Reviews...")
            
            deleted_count = 0
            for review in reviews:
                delete_response = requests.delete(f"{API_BASE_URL}/admin/reviews/{review['id']}", headers=headers)
                if delete_response.status_code == 200:
                    deleted_count += 1
                    print(f"   ✅ Gelöscht: {review['name']} (ID: {review['id']})")
                else:
                    print(f"   ❌ Fehler beim Löschen: {review['name']} (ID: {review['id']})")
                time.sleep(0.2)  # Kurze Pause
            
            return deleted_count
        else:
            print(f"❌ Failed to get reviews: {response.text}")
            return 0
    except Exception as e:
        print(f"❌ Error deleting reviews: {str(e)}")
        return 0

def main():
    print("🔄 KORREKTUR: Lösche falsche Reviews")
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
    
    # Delete all fake reviews
    deleted_count = delete_all_reviews(token)
    
    print(f"\n📊 Lösch-Zusammenfassung:")
    print(f"   🗑️ Gelöscht: {deleted_count} falsche Reviews")
    
    if deleted_count > 0:
        print(f"✅ {deleted_count} falsche Reviews erfolgreich gelöscht!")
        print("🎯 Bereit für Import der echten Gästebewertungen")
    else:
        print("❌ Keine Reviews gelöscht!")

if __name__ == "__main__":
    main()
