from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import time
import logging
from sqlalchemy import text

# Logging konfigurieren
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DB_USER = os.getenv("DB_USER", "guestuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "guestpw")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "guestbook")

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

def create_engine_with_retry(max_retries=10, retry_delay=5):
    """Erstellt eine Engine mit Retry-Logik für die Datenbankverbindung"""
    for attempt in range(max_retries):
        try:
            logger.info(f"Versuch {attempt + 1}/{max_retries}: Verbindung zur Datenbank herstellen...")
            engine = create_engine(
                SQLALCHEMY_DATABASE_URL, 
                echo=True,
                pool_pre_ping=True,
                pool_recycle=300,
                pool_size=10,
                max_overflow=20
            )
            # Test der Verbindung mit moderner SQLAlchemy Syntax
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            logger.info("Datenbankverbindung erfolgreich hergestellt!")
            return engine
        except Exception as e:
            logger.warning(f"Verbindungsversuch {attempt + 1} fehlgeschlagen: {e}")
            if attempt < max_retries - 1:
                logger.info(f"Warte {retry_delay} Sekunden vor nächstem Versuch...")
                time.sleep(retry_delay)
            else:
                logger.error("Maximale Anzahl von Verbindungsversuchen erreicht!")
                raise

engine = create_engine_with_retry()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency für FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
