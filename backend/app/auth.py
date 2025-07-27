from datetime import datetime, timedelta
from typing import Optional
import jwt
from fastapi import Depends, HTTPException, status, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import os

from .database import get_db
from .crud import admin_user_crud
from . import models

# JWT Konfiguration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-super-secret-jwt-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

security = HTTPBearer()

class AuthManager:
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
        """JWT Access Token erstellen"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def verify_token(token: str) -> Optional[str]:
        """JWT Token verifizieren"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                return None
            return username
        except jwt.PyJWTError:
            return None

def get_current_admin_user(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db)
) -> models.AdminUser:
    """Aktueller Admin-Benutzer aus JWT Token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    username = AuthManager.verify_token(credentials.credentials)
    if username is None:
        raise credentials_exception
    
    user = admin_user_crud.get_admin_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    return user

def get_current_active_admin_user(
    current_user: models.AdminUser = Depends(get_current_admin_user)
) -> models.AdminUser:
    """Aktiver Admin-Benutzer"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# Rate Limiting (einfache IP-basierte Implementierung)
from collections import defaultdict
from time import time

class RateLimiter:
    def __init__(self):
        self.requests = defaultdict(list)
        self.max_requests = 10  # Max Requests pro Zeitfenster
        self.time_window = 60   # Zeitfenster in Sekunden
    
    def is_allowed(self, ip_address: str) -> bool:
        """Prüft ob Request erlaubt ist"""
        now = time()
        # Alte Requests entfernen
        self.requests[ip_address] = [
            req_time for req_time in self.requests[ip_address]
            if now - req_time < self.time_window
        ]
        
        # Prüfen ob Limit erreicht
        if len(self.requests[ip_address]) >= self.max_requests:
            return False
        
        # Request hinzufügen
        self.requests[ip_address].append(now)
        return True

rate_limiter = RateLimiter()
