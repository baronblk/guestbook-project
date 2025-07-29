#!/usr/bin/env python3
"""
Script to extract dates from import_source and update the created_at field of existing reviews
"""
import requests
import re
from datetime import datetime

# API base URL - using production container
API_BASE_URL = "http://192.168.2.12:3000/api"

def get_admin_token():
    """Get admin JWT token"""
    try:
        response = requests.post(f"{API_BASE_URL}/admin/login", 
                               params={"username": "admin", "password": "admin123"})
        if response.status_code == 200:
            return response.json()["access_token"]
        else:
            print(f"❌ Login failed: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Login error: {str(e)}")
        return None

def parse_date_from_import_source(import_source):
    """Extract date from import_source string"""
    if not import_source:
        return None
    
    # Look for dates in format DD.MM.YYYY
    date_pattern = r'(\d{1,2})\.(\d{1,2})\.(\d{4})'
    match = re.search(date_pattern, import_source)
    
    if match:
        day, month, year = match.groups()
        try:
            # Create datetime object
            return datetime(int(year), int(month), int(day))
        except ValueError:
            print(f"⚠️ Invalid date in import_source: {import_source}")
            return None
    
    return None

def get_all_reviews(token):
    """Get all reviews from the API"""
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{API_BASE_URL}/admin/reviews?per_page=100", headers=headers)
        if response.status_code == 200:
            return response.json()["reviews"]
        else:
            print(f"❌ Failed to get reviews: {response.text}")
            return []
    except Exception as e:
        print(f"❌ Error getting reviews: {str(e)}")
        return []

def update_review_date(token, review_id, new_date):
    """Update a review's created_at date"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    data = {"created_at": new_date.isoformat()}
    
    try:
        response = requests.put(f"{API_BASE_URL}/admin/reviews/{review_id}", 
                              json=data, headers=headers)
        if response.status_code == 200:
            return True
        else:
            print(f"❌ Failed to update review {review_id}: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error updating review {review_id}: {str(e)}")
        return False

def main():
    print("🚀 Fixing review dates from import_source...")
    
    # Get admin token
    token = get_admin_token()
    if not token:
        return
    
    print("✅ Admin login successful")
    
    # Get all reviews
    reviews = get_all_reviews(token)
    if not reviews:
        print("❌ No reviews found")
        return
    
    print(f"📚 Found {len(reviews)} reviews")
    
    fixed_count = 0
    skipped_count = 0
    
    for review in reviews:
        import_source = review.get("import_source")
        if not import_source:
            skipped_count += 1
            continue
        
        # Extract date from import_source
        original_date = parse_date_from_import_source(import_source)
        if not original_date:
            print(f"⚠️ No date found in import_source for review {review['id']}: {import_source}")
            skipped_count += 1
            continue
        
        # Update the review
        print(f"🔄 Updating review {review['id']} ({review['name']}) to date {original_date.strftime('%d.%m.%Y')}")
        if update_review_date(token, review["id"], original_date):
            fixed_count += 1
            print(f"✅ Updated review {review['id']}")
        else:
            print(f"❌ Failed to update review {review['id']}")
    
    print(f"\n🎉 Date fixing completed!")
    print(f"✅ Fixed: {fixed_count} reviews")
    print(f"⏭️ Skipped: {skipped_count} reviews")

if __name__ == "__main__":
    main()
