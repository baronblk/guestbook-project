#!/usr/bin/env python3
"""
Direct database import from JSON file
"""
import json
import pymysql
from datetime import datetime
import re

# Database connection settings
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'guestuser',
    'password': 'whHBJveMvwjs5a6p',
    'database': 'guestbook',
    'charset': 'utf8mb4'
}

def clean_text(text):
    """Clean text content"""
    if not text:
        return text
    # Remove extra whitespace and normalize
    text = re.sub(r'\s+', ' ', text.strip())
    return text

def parse_date(date_str):
    """Parse date string to MySQL datetime format"""
    if not date_str:
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    try:
        # Try parsing ISO format first
        if 'T' in date_str:
            dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            return dt.strftime('%Y-%m-%d %H:%M:%S')
        
        # Try parsing DD.MM.YYYY format
        if '.' in date_str:
            day, month, year = date_str.split('.')
            dt = datetime(int(year), int(month), int(day))
            return dt.strftime('%Y-%m-%d %H:%M:%S')
            
    except Exception as e:
        print(f"Error parsing date '{date_str}': {e}")
    
    # Fallback to current date
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def import_reviews():
    """Import reviews from JSON file"""
    
    # Read JSON file
    with open('import_request_complete.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    reviews = data.get('reviews', [])
    print(f"🚀 Starting direct database import...")
    print(f"📝 Found {len(reviews)} reviews to import")
    
    # Connect to database
    try:
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor()
        print("✅ Database connection established")
        
        # Check existing reviews
        cursor.execute("SELECT COUNT(*) FROM reviews")
        existing_count = cursor.fetchone()[0]
        print(f"📊 Existing reviews in database: {existing_count}")
        
        successful_imports = 0
        failed_imports = 0
        
        for i, review in enumerate(reviews, 1):
            try:
                # Extract data
                name = clean_text(review.get('name', 'Anonymous'))[:100]
                email = review.get('email', '')[:255] if review.get('email') else None
                rating = min(max(int(review.get('rating', 5)), 1), 5)  # Ensure rating is 1-5
                title = clean_text(review.get('title', ''))[:200] if review.get('title') else None
                content = clean_text(review.get('content', ''))
                created_at = parse_date(review.get('created_at'))
                is_approved = True  # Import as approved
                is_featured = rating >= 5  # Feature 5-star reviews
                import_source = 'JSON Import'
                
                # Insert review
                sql = """
                INSERT INTO reviews 
                (name, email, rating, title, content, created_at, is_approved, is_featured, import_source)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                
                cursor.execute(sql, (
                    name, email, rating, title, content, 
                    created_at, is_approved, is_featured, import_source
                ))
                
                successful_imports += 1
                print(f"✅ Imported review {i}/{len(reviews)}: {name}")
                
            except Exception as e:
                failed_imports += 1
                print(f"❌ Failed to import review {i}: {name} - Error: {e}")
                continue
        
        # Commit changes
        connection.commit()
        
        # Final count
        cursor.execute("SELECT COUNT(*) FROM reviews")
        final_count = cursor.fetchone()[0]
        
        print(f"\n📊 Import Summary:")
        print(f"✅ Successfully imported: {successful_imports}")
        print(f"❌ Failed imports: {failed_imports}")
        print(f"📈 Total reviews in database: {final_count}")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        print("Make sure the database container is running and accessible")

if __name__ == "__main__":
    import_reviews()
