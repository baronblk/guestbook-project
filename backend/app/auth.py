from datetime import datetime, timedelta
from typing import Optional
import jwt
import hashlib
import secrets
import bcrypt
from fastapi import Depends, HTTPException, status, Security, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import os
import logging
from collections import defaultdict
from time import time

from .database import get_db
from .crud import admin_user_crud
from . import models
from .security_monitor import security_monitor, log_failed_login, log_successful_login, log_rate_limit_violation

# Security Configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-super-secret-jwt-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))  # Kürzere Session für bessere Sicherheit
REFRESH_TOKEN_EXPIRE_HOURS = int(os.getenv("REFRESH_TOKEN_EXPIRE_HOURS", "24"))

# Logging für Security Events
security_logger = logging.getLogger("security")
security_logger.setLevel(logging.INFO)

security = HTTPBearer()

class SecurityUtils:
    """Security-Hilfsfunktionen"""

    @staticmethod
    def hash_password(password: str) -> str:
        """Password mit bcrypt hashen"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """Password verifizieren"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

    @staticmethod
    def generate_session_id() -> str:
        """Sichere Session-ID generieren"""
        return secrets.token_urlsafe(32)

    @staticmethod
    def hash_token(token: str) -> str:
        """Token hashen für sicheren Vergleich"""
        return hashlib.sha256(token.encode()).hexdigest()

    @staticmethod
    def get_client_ip(request: Request) -> str:
        """Client-IP ermitteln (auch hinter Proxy)"""
        # Prüfe verschiedene Headers für echte Client-IP
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()

        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip

        return request.client.host if request.client else "unknown"

class LoginAttemptTracker:
    """Login-Versuche tracken für Brute-Force-Schutz"""

    def __init__(self):
        self.failed_attempts = defaultdict(list)
        self.blocked_ips = defaultdict(float)
        self.max_attempts = 5  # Max fehlgeschlagene Versuche
        self.block_duration = 900  # 15 Minuten Block
        self.attempt_window = 300  # 5 Minuten Zeitfenster

    def record_failed_attempt(self, ip_address: str, username: str):
        """Fehlgeschlagenen Login-Versuch aufzeichnen"""
        now = time()
        key = f"{ip_address}:{username}"

        # Alte Versuche entfernen
        self.failed_attempts[key] = [
            attempt_time for attempt_time in self.failed_attempts[key]
            if now - attempt_time < self.attempt_window
        ]

        # Neuen Versuch hinzufügen
        self.failed_attempts[key].append(now)

        # IP blockieren wenn zu viele Versuche
        if len(self.failed_attempts[key]) >= self.max_attempts:
            self.blocked_ips[ip_address] = now + self.block_duration
            security_logger.warning(f"IP {ip_address} blocked for {self.block_duration} seconds after {self.max_attempts} failed login attempts for user {username}")

    def is_blocked(self, ip_address: str) -> bool:
        """Prüfen ob IP blockiert ist"""
        now = time()
        if ip_address in self.blocked_ips:
            if now < self.blocked_ips[ip_address]:
                return True
            else:
                # Block abgelaufen
                del self.blocked_ips[ip_address]
        return False

    def clear_attempts(self, ip_address: str, username: str):
        """Erfolgreiche Anmeldung - Versuche löschen"""
        key = f"{ip_address}:{username}"
        if key in self.failed_attempts:
            del self.failed_attempts[key]
        if ip_address in self.blocked_ips:
            del self.blocked_ips[ip_address]

class RateLimiter:
    """Erweiterte Rate-Limiting-Implementierung"""

    def __init__(self):
        self.requests = defaultdict(list)
        self.max_requests = 60  # Max Requests pro Minute
        self.time_window = 60   # 1 Minute
        self.strict_endpoints = {
            "/api/admin/login": {"max": 5, "window": 300},  # 5 Login-Versuche pro 5 Minuten
            "/api/admin/refresh": {"max": 10, "window": 60}  # 10 Refresh-Versuche pro Minute
        }

    def is_allowed(self, ip_address: str, endpoint: str = None) -> bool:
        """Prüft ob Request erlaubt ist"""
        now = time()

        # Endpoint-spezifische Limits
        if endpoint and endpoint in self.strict_endpoints:
            config = self.strict_endpoints[endpoint]
            max_requests = config["max"]
            time_window = config["window"]
            key = f"{ip_address}:{endpoint}"
        else:
            max_requests = self.max_requests
            time_window = self.time_window
            key = ip_address

        # Alte Requests entfernen
        self.requests[key] = [
            req_time for req_time in self.requests[key]
            if now - req_time < time_window
        ]

        # Prüfen ob Limit erreicht
        if len(self.requests[key]) >= max_requests:
            security_logger.warning(f"Rate limit exceeded for IP {ip_address} on endpoint {endpoint}")
            return False

        # Request hinzufügen
        self.requests[key].append(now)
        return True

# Globale Instanzen
rate_limiter = RateLimiter()
login_tracker = LoginAttemptTracker()

class AuthManager:
    """Erweiterte Authentifizierungs- und Autorisierungsmanagement"""

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
        """Access Token erstellen mit erweiterten Security-Features"""
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        # Zusätzliche Security-Claims
        to_encode.update({
            "exp": expire,
            "iat": datetime.utcnow(),
            "jti": SecurityUtils.generate_session_id(),  # JWT ID für Token-Invalidierung
            "type": "access"
        })

        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def create_refresh_token(data: dict):
        """Refresh Token erstellen"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(hours=REFRESH_TOKEN_EXPIRE_HOURS)

        to_encode.update({
            "exp": expire,
            "iat": datetime.utcnow(),
            "jti": SecurityUtils.generate_session_id(),
            "type": "refresh"
        })

        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def verify_token(token: str, token_type: str = "access") -> Optional[str]:
        """Token verifizieren mit erweiterten Sicherheitsprüfungen"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

            # Token-Typ prüfen
            if payload.get("type") != token_type:
                return None

            username: str = payload.get("sub")
            if username is None:
                return None

            return username

        except jwt.ExpiredSignatureError:
            security_logger.info("Token expired")
            return None
        except jwt.InvalidTokenError:
            security_logger.info("Invalid token")
            return None
        except Exception as e:
            security_logger.error(f"Token verification error: {str(e)}")
            return None

    @staticmethod
    def authenticate_user(username: str, password: str, db: Session, ip_address: str, user_agent: str = None) -> Optional[models.AdminUser]:
        """User authentifizieren mit Brute-Force-Schutz und Security-Monitoring"""

        # IP-Block prüfen (sowohl Login-Tracker als auch Security-Monitor)
        if login_tracker.is_blocked(ip_address) or security_monitor.is_ip_blocked(ip_address):
            log_failed_login(ip_address, username, user_agent)
            security_logger.warning(f"Login attempt from blocked IP {ip_address}")
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many failed login attempts. Please try again later."
            )

        # User laden
        user = admin_user_crud.get_admin_user_by_username(db, username=username)
        if not user:
            login_tracker.record_failed_attempt(ip_address, username)
            log_failed_login(ip_address, username, user_agent)
            security_logger.warning(f"Login attempt for non-existent user {username} from IP {ip_address}")
            return None

        # Password prüfen - verwende SecurityUtils
        if not SecurityUtils.verify_password(password, user.hashed_password):
            login_tracker.record_failed_attempt(ip_address, username)
            log_failed_login(ip_address, username, user_agent)
            security_logger.warning(f"Failed login attempt for user {username} from IP {ip_address}")
            return None

        # User aktiv?
        if not user.is_active:
            login_tracker.record_failed_attempt(ip_address, username)
            log_failed_login(ip_address, username, user_agent)
            security_logger.warning(f"Login attempt for inactive user {username} from IP {ip_address}")
            return None

        # Erfolgreiche Anmeldung
        login_tracker.clear_attempts(ip_address, username)
        log_successful_login(ip_address, username, user_agent)
        security_logger.info(f"Successful login for user {username} from IP {ip_address}")
        return user

# Security Middleware und Dependencies
async def check_rate_limit(request: Request, endpoint: str = None):
    """Rate Limiting prüfen mit Security-Monitoring"""
    ip_address = SecurityUtils.get_client_ip(request)
    user_agent = request.headers.get("User-Agent", "Unknown")

    if not rate_limiter.is_allowed(ip_address, endpoint):
        # Rate Limit Verletzung protokollieren
        log_rate_limit_violation(ip_address, endpoint or str(request.url), user_agent)
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Please try again later."
        )

async def get_current_admin_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db)
) -> models.AdminUser:
    """Aktuellen Admin-User ermitteln mit erweiterten Security-Checks"""

    # Rate Limiting
    await check_rate_limit(request)

    # Token verifizieren
    username = AuthManager.verify_token(credentials.credentials)
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # User laden und validieren
    user = admin_user_crud.get_admin_user_by_username(db, username=username)
    if user is None or not user.is_active:
        security_logger.warning(f"Access attempt with invalid/inactive user {username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user

def get_current_active_admin_user(
    current_user: models.AdminUser = Depends(get_current_admin_user)
) -> models.AdminUser:
    """Aktiver Admin-Benutzer mit zusätzlicher Aktivitätsprüfung"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user

# Role-based Authorization
class RolePermissions:
    """Rollen-basierte Berechtigungen"""

    @staticmethod
    def require_role(*allowed_roles):
        """Decorator für rollenbasierte Zugriffskontrolle"""
        def decorator(func):
            def wrapper(current_user = Depends(get_current_active_admin_user), *args, **kwargs):
                from app.models import AdminRole

                # Convert string roles to enum
                role_enums = []
                for role in allowed_roles:
                    if isinstance(role, str):
                        role_enums.append(AdminRole(role))
                    else:
                        role_enums.append(role)

                if current_user.role not in role_enums:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Insufficient permissions for this operation"
                    )
                return func(current_user=current_user, *args, **kwargs)
            return wrapper
        return decorator

    @staticmethod
    def can_manage_users(user) -> bool:
        """Kann Benutzer verwalten"""
        from app.models import AdminRole
        return user.role in [AdminRole.ADMIN, AdminRole.SUPERUSER]

    @staticmethod
    def can_create_superusers(user) -> bool:
        """Kann Superuser erstellen"""
        from app.models import AdminRole
        return user.role == AdminRole.SUPERUSER

    @staticmethod
    def can_moderate(user) -> bool:
        """Kann moderieren"""
        return True  # Alle Rollen können moderieren

    @staticmethod
    def can_import_export(user) -> bool:
        """Kann Import/Export"""
        return True  # Alle Rollen können Import/Export
