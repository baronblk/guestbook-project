#!/usr/bin/env python3
"""
Script to approve all existing reviews in the database
Run this on your NAS to make all reviews visible again
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Database configuration - adjust these values if needed
DB_HOST = "db"  # Docker service name
DB_USER = "guestuser"
DB_PASSWORD = "whHBJveMvwjs5a6p"
DB_NAME = "guestbook"

# Create database URL
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:3306/{DB_NAME}"

def approve_all_reviews():
    """Set all reviews to approved=True"""
    try:
        # Create engine and session
        engine = create_engine(DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        session = SessionLocal()
        
        # Update all reviews to be approved
        result = session.execute(
            text("UPDATE reviews SET is_approved = TRUE WHERE is_approved = FALSE")
        )
        session.commit()
        
        print(f"✅ Successfully approved {result.rowcount} reviews")
        
        # Show current status
        result = session.execute(text("SELECT COUNT(*) as total FROM reviews"))
        total = result.fetchone()[0]
        
        result = session.execute(text("SELECT COUNT(*) as approved FROM reviews WHERE is_approved = TRUE"))
        approved = result.fetchone()[0]
        
        print(f"📊 Database status: {approved}/{total} reviews are now visible")
        
        session.close()
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
def show_reviews():
    """Show all reviews in the database"""
    try:
        engine = create_engine(DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        session = SessionLocal()
        
        result = session.execute(
            text("SELECT id, name, rating, title, is_approved, created_at FROM reviews ORDER BY created_at DESC")
        )
        
        reviews = result.fetchall()
        
        if not reviews:
            print("🔍 No reviews found in database")
            return
            
        print(f"\n📋 Found {len(reviews)} reviews:")
        print("ID | Name | Rating | Title | Approved | Created")
        print("-" * 70)
        
        for review in reviews:
            approved_icon = "✅" if review.is_approved else "❌"
            print(f"{review.id:2} | {review.name[:15]:15} | {review.rating} ⭐ | {(review.title or '')[:20]:20} | {approved_icon} | {review.created_at}")
        
        session.close()
        
    except Exception as e:
        print(f"❌ Error showing reviews: {e}")

if __name__ == "__main__":
    print("🔧 Guestbook Database Repair Tool")
    print("=" * 50)
    
    if len(sys.argv) > 1 and sys.argv[1] == "show":
        show_reviews()
    else:
        print("🔍 Checking current reviews...")
        show_reviews()
        
        print("\n🔧 Approving all reviews...")
        if approve_all_reviews():
            print("\n✅ Done! All reviews should now be visible on your guestbook.")
            print("💡 Refresh your browser to see the changes.")
        else:
            print("\n❌ Failed to update reviews. Check the database connection.")
