#!/bin/bash
# Script to fix missing reviews by setting all reviews to approved
# Run this on your NAS where the guestbook container is running

echo "🔧 Guestbook Review Fix Script"
echo "==============================="

# Find the running guestbook container
CONTAINER_ID=$(docker ps --filter "ancestor=ghcr.io/baronblk/guestbook-project/combined:latest" --format "{{.ID}}" | head -1)

if [ -z "$CONTAINER_ID" ]; then
    echo "❌ No running guestbook container found!"
    echo "💡 Make sure your guestbook stack is running in Portainer"
    exit 1
fi

echo "✅ Found guestbook container: $CONTAINER_ID"

# Execute SQL command to approve all reviews
echo "🔧 Approving all reviews..."

docker exec $CONTAINER_ID python3 -c "
import pymysql
import sys

try:
    # Connect to database
    connection = pymysql.connect(
        host='db',
        user='guestuser',
        password='whHBJveMvwjs5a6p',
        database='guestbook',
        charset='utf8mb4'
    )
    
    with connection.cursor() as cursor:
        # Show current status
        cursor.execute('SELECT COUNT(*) FROM reviews')
        total = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM reviews WHERE is_approved = 1')
        approved_before = cursor.fetchone()[0]
        
        print(f'📊 Before: {approved_before}/{total} reviews approved')
        
        # Approve all reviews
        cursor.execute('UPDATE reviews SET is_approved = 1 WHERE is_approved = 0')
        updated = cursor.rowcount
        
        # Show updated status
        cursor.execute('SELECT COUNT(*) FROM reviews WHERE is_approved = 1')
        approved_after = cursor.fetchone()[0]
        
        print(f'✅ Updated {updated} reviews')
        print(f'📊 After: {approved_after}/{total} reviews approved')
        
    connection.commit()
    connection.close()
    
    print('🎉 All reviews are now visible!')
    print('💡 Refresh your browser: http://192.168.2.12:3000/')
    
except Exception as e:
    print(f'❌ Error: {e}')
    sys.exit(1)
"

echo ""
echo "✅ Done! Check your guestbook at http://192.168.2.12:3000/"
