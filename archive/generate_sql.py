#!/usr/bin/env python3
"""
Generate SQL INSERT statements from JSON data
"""
import json
import re
from datetime import datetime

def clean_text(text):
    """Clean and escape text for SQL"""
    if not text:
        return 'NULL'
    # Clean whitespace
    text = re.sub(r'\s+', ' ', text.strip())
    # Escape single quotes for SQL
    text = text.replace("'", "''")
    return f"'{text}'"

def parse_date(date_str):
    """Parse date string to MySQL datetime format"""
    if not date_str:
        return "'2025-07-20 10:00:00'"
    
    try:
        # Try parsing ISO format first
        if 'T' in date_str:
            dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            return f"'{dt.strftime('%Y-%m-%d %H:%M:%S')}'"
        
        # Try parsing DD.MM.YYYY format
        if '.' in date_str:
            day, month, year = date_str.split('.')
            dt = datetime(int(year), int(month), int(day), 10, 0, 0)
            return f"'{dt.strftime('%Y-%m-%d %H:%M:%S')}'"
            
    except Exception:
        pass
    
    # Fallback to current date
    return "'2025-07-20 10:00:00'"

def generate_sql():
    """Generate SQL INSERT statements"""
    
    # Read JSON file
    with open('import_request_complete.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    reviews = data.get('reviews', [])
    print(f"-- Generating SQL for {len(reviews)} reviews")
    print("-- Created on:", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print()
    
    sql_statements = []
    
    for i, review in enumerate(reviews, 1):
        try:
            # Extract and clean data
            name = clean_text(review.get('name', 'Anonymous'))
            if len(review.get('name', '')) > 100:
                name = clean_text(review.get('name', '')[:97] + '...')
            
            email = review.get('email', '')
            if email:
                email = f"'{email[:255]}'"
            else:
                email = 'NULL'
            
            rating = min(max(int(review.get('rating', 5)), 1), 5)
            
            title = review.get('title', '')
            if title:
                title = clean_text(title[:197] + '...' if len(title) > 200 else title)
            else:
                title = 'NULL'
            
            content = clean_text(review.get('content', ''))
            created_at = parse_date(review.get('created_at'))
            is_approved = 1  # Import as approved
            is_featured = 1 if rating >= 5 else 0
            import_source = "'JSON Import'"
            
            # Generate SQL statement
            sql = f"""INSERT INTO reviews (name, email, rating, title, content, created_at, is_approved, is_featured, import_source) VALUES ({name}, {email}, {rating}, {title}, {content}, {created_at}, {is_approved}, {is_featured}, {import_source});"""
            
            sql_statements.append(sql)
            
        except Exception as e:
            print(f"-- Error processing review {i}: {e}", file=sys.stderr)
            continue
    
    # Output all SQL statements
    for sql in sql_statements:
        print(sql)
    
    print(f"\n-- Generated {len(sql_statements)} INSERT statements")

if __name__ == "__main__":
    import sys
    generate_sql()
