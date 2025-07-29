#!/usr/bin/env python3
"""
Wait for database to be ready before starting the application.
"""
import sys
import time
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
import os

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def wait_for_database(max_retries: int = 30, retry_delay: int = 2):
    """
    Wait for database to be ready.
    
    Args:
        max_retries: Maximum number of retry attempts
        retry_delay: Delay between retries in seconds
    """
    # Database connection parameters
    db_host = os.getenv('DB_HOST', 'localhost')
    db_user = os.getenv('DB_USER', 'guestuser')
    db_password = os.getenv('DB_PASSWORD', 'guestpw')
    db_name = os.getenv('DB_NAME', 'guestbook')
    
    database_url = f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"
    
    for attempt in range(1, max_retries + 1):
        try:
            logger.info(f"Attempt {attempt}/{max_retries}: Connecting to database...")
            
            # Create engine and test connection
            engine = create_engine(database_url)
            with engine.connect() as connection:
                # Test with a simple query
                result = connection.execute(text("SELECT 1"))
                result.fetchone()
                
            logger.info("✅ Database is ready!")
            return True
            
        except OperationalError as e:
            logger.warning(f"❌ Database not ready (attempt {attempt}/{max_retries}): {e}")
            
            if attempt == max_retries:
                logger.error("🚨 Database connection failed after all retries!")
                return False
                
            logger.info(f"⏳ Waiting {retry_delay} seconds before next attempt...")
            time.sleep(retry_delay)
            
        except Exception as e:
            logger.error(f"🚨 Unexpected error: {e}")
            return False
    
    return False

if __name__ == "__main__":
    success = wait_for_database()
    sys.exit(0 if success else 1)
