from fastapi import FastAPI, Depends, HTTPException, status, File, UploadFile, Request, Query, Response
from fastapi.security import HTTPBearer
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import math
from datetime import timedelta, datetime

from . import models, schemas, crud, auth, database, utils

# App initialisieren
app = FastAPI(
    title="Gästebuch API",
    description="Vollständiges Gästebuch-System mit Admin-Panel",
    version="1.0.0"
)

# Security Headers Middleware
@app.middleware("http")
async def security_headers_middleware(request: Request, call_next):
    """Sichere HTTP-Headers hinzufügen"""
    response = await call_next(request)

    # Security Headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"

    # HSTS Header für HTTPS
    if request.url.scheme == "https":
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

    # CSP Header
    csp = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: blob:; "
        "font-src 'self'; "
        "connect-src 'self'; "
        "media-src 'self'; "
        "object-src 'none'; "
        "child-src 'none'; "
        "worker-src 'none'; "
        "frame-ancestors 'none'; "
        "form-action 'self'; "
        "base-uri 'self';"
    )
    response.headers["Content-Security-Policy"] = csp

    return response

# CORS konfigurieren - restriktiver für Produktion
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8080"],  # Spezifische Origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
)

# Trusted Host Middleware für zusätzliche Sicherheit
# ERWEITERT für externe Domain-Zugriffe
import os
allowed_hosts = ["localhost", "127.0.0.1", "*.localhost"]

# Zusätzliche Hosts aus Umgebungsvariable
allowed_hosts_env = os.getenv("ALLOWED_HOSTS", "")
if allowed_hosts_env:
    if allowed_hosts_env == "*":
        # Alle Hosts erlauben (für Debugging)
        allowed_hosts = ["*"]
    else:
        # Spezifische Hosts hinzufügen
        additional_hosts = [host.strip() for host in allowed_hosts_env.split(",")]
        allowed_hosts.extend(additional_hosts)

print(f"🔧 Allowed hosts: {allowed_hosts}")

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=allowed_hosts
)

# Static Files für Uploads
app.mount("/uploads", StaticFiles(directory="/app/uploads"), name="uploads")

# Static Files für Frontend (React Build)
import os
if os.path.exists("/app/backend/static"):
    app.mount("/static", StaticFiles(directory="/app/backend/static/static"), name="static")

# Database Tables erstellen und Admin-User initialisieren
@app.on_event("startup")
async def create_tables():
    models.Base.metadata.create_all(bind=database.engine)

    # Admin-User erstellen, falls keiner existiert
    import os
    db = database.SessionLocal()
    try:
        existing_admin = crud.admin_user_crud.get_admin_user_by_username(db, "admin")
        if not existing_admin:
            admin_user = schemas.AdminUserCreate(
                username=os.getenv("ADMIN_USERNAME", "admin"),
                email=os.getenv("ADMIN_EMAIL", "admin@example.com"),  # Verwendet Umgebungsvariable aus docker-compose.yml
                password=os.getenv("ADMIN_PASSWORD", "admin123")
            )
            try:
                crud.admin_user_crud.create_admin_user(db, admin_user)
                print(f"✅ Admin-User '{admin_user.username}' wurde erstellt")
            except Exception as e:
                print(f"❌ Fehler beim Erstellen des Admin-Users: {e}")
        else:
            print(f"ℹ️  Admin-User '{existing_admin.username}' existiert bereits")
    except Exception as e:
        print(f"❌ Fehler beim Erstellen des Admin-Users: {e}")
    finally:
        db.close()

# Hilfsfunktionen
def get_client_ip(request: Request) -> str:
    """Client IP-Adresse ermitteln"""
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host

# Public API Endpoints

@app.get("/health")
async def health_check():
    """Health Check für Container"""
    try:
        # Datenbankverbindung testen
        from sqlalchemy import text
        db = database.SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()

        return {"status": "healthy", "service": "guestbook-api", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Health check failed: {str(e)}")

@app.post("/api/reviews", response_model=schemas.ReviewResponse)
async def create_review(
    review: schemas.ReviewCreate,
    request: Request,
    db: Session = Depends(database.get_db)
):
    """Neue Bewertung erstellen"""
    client_ip = get_client_ip(request)

    # Rate Limiting
    if not auth.rate_limiter.is_allowed(client_ip):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Zu viele Anfragen. Bitte warten Sie eine Minute."
        )

    # Review erstellen
    db_review = crud.review_crud.create_review(db, review, client_ip)
    return db_review

@app.post("/api/reviews/{review_id}/image")
async def upload_review_image(
    review_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(database.get_db)
):
    """Bild zu Bewertung hochladen"""
    # Review prüfen
    db_review = crud.review_crud.get_review(db, review_id)
    if not db_review:
        raise HTTPException(status_code=404, detail="Bewertung nicht gefunden")

    # Altes Bild löschen falls vorhanden
    if db_review.image_path:
        utils.FileManager.delete_image(db_review.image_path)

    # Neues Bild speichern
    image_path = await utils.FileManager.save_image(file)

    # Review aktualisieren
    update_data = schemas.ReviewUpdate(image_path=image_path)
    updated_review = crud.review_crud.update_review(db, review_id, update_data)

    return {"image_path": image_path}

@app.get("/api/reviews", response_model=schemas.ReviewListResponse)
async def get_reviews(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=50),
    rating: Optional[int] = Query(None, ge=1, le=5),
    min_rating: Optional[int] = Query(None, ge=1, le=5),
    featured_only: Optional[bool] = Query(None),
    search: Optional[str] = Query(None),
    sort_by: str = Query("created_at", pattern="^(created_at|rating|name)$"),
    sort_order: str = Query("desc", pattern="^(asc|desc)$"),
    db: Session = Depends(database.get_db)
):
    """Bewertungen abrufen (öffentlich)"""
    skip = (page - 1) * per_page

    # min_rating und rating sind dasselbe - min_rating hat Vorrang
    effective_rating = min_rating or rating

    # Filter erstellen
    filters = schemas.ReviewFilters(
        rating=effective_rating,
        is_featured=featured_only,
        search=search
    )

    # Reviews abrufen
    reviews, total = crud.review_crud.get_reviews(
        db,
        skip=skip,
        limit=per_page,
        approved_only=True,
        filters=filters,
        sort_by=sort_by,
        sort_order=sort_order
    )

    total_pages = math.ceil(total / per_page)

    return schemas.ReviewListResponse(
        reviews=reviews,
        total=total,
        page=page,
        per_page=per_page,
        total_pages=total_pages
    )

@app.get("/api/reviews/{review_id}", response_model=schemas.ReviewResponse)
async def get_review(review_id: int, db: Session = Depends(database.get_db)):
    """Einzelne Bewertung abrufen"""
    db_review = crud.review_crud.get_review(db, review_id)
    if not db_review or not db_review.is_approved:
        raise HTTPException(status_code=404, detail="Bewertung nicht gefunden")

    # Kommentar-Anzahl hinzufügen
    comment_count = crud.comment_crud.count_approved_comments_by_review(db, review_id)
    db_review.comment_count = comment_count

    return db_review

# === COMMENT ENDPOINTS ===

@app.post("/api/reviews/{review_id}/comments", response_model=schemas.CommentResponse)
async def create_comment(
    review_id: int,
    comment: schemas.CommentCreate,
    request: Request,
    db: Session = Depends(database.get_db)
):
    """Neuen Kommentar zu einer Bewertung erstellen"""
    # Prüfen ob Review existiert und genehmigt ist
    db_review = crud.review_crud.get_review(db, review_id)
    if not db_review or not db_review.is_approved:
        raise HTTPException(status_code=404, detail="Bewertung nicht gefunden")

    # IP-Adresse für Anti-Spam speichern
    client_ip = utils.get_client_ip(request)

    try:
        db_comment = crud.comment_crud.create_comment(db, comment, client_ip, review_id)
        return db_comment
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Fehler beim Erstellen des Kommentars: {str(e)}")

@app.get("/api/reviews/{review_id}/comments", response_model=schemas.CommentListResponse)
async def get_comments_by_review(
    review_id: int,
    page: int = Query(1, ge=1, description="Seitennummer"),
    per_page: int = Query(10, ge=1, le=50, description="Einträge pro Seite"),
    db: Session = Depends(database.get_db)
):
    """Kommentare für eine bestimmte Bewertung abrufen"""
    # Prüfen ob Review existiert und genehmigt ist
    db_review = crud.review_crud.get_review(db, review_id)
    if not db_review or not db_review.is_approved:
        raise HTTPException(status_code=404, detail="Bewertung nicht gefunden")

    skip = (page - 1) * per_page
    comments, total = crud.comment_crud.get_comments_by_review(
        db, review_id, skip=skip, limit=per_page, approved_only=True
    )

    total_pages = math.ceil(total / per_page)

    return {
        "comments": comments,
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": total_pages
    }

@app.get("/api/stats")
async def get_stats(db: Session = Depends(database.get_db)):
    """Öffentliche Statistiken"""
    stats = crud.review_crud.get_review_stats(db)
    # Nur öffentliche Statistiken zurückgeben
    return {
        "total_reviews": stats["approved_reviews"],
        "average_rating": stats["average_rating"],
        "rating_distribution": stats["rating_distribution"]
    }

# Embed-Endpunkt für iFrame
@app.get("/embed", response_class=HTMLResponse)
async def embed_guestbook():
    """Einbettbarer Guestbook-Widget"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Gästebuch Widget</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 10px; }
            .review { border: 1px solid #ddd; margin: 10px 0; padding: 15px; border-radius: 5px; }
            .rating { color: #ffc107; }
            .name { font-weight: bold; }
            .date { color: #666; font-size: 0.9em; }
        </style>
    </head>
    <body>
        <div id="guestbook">
            <h3>Kundenbewertungen</h3>
            <div id="reviews-container">Laden...</div>
        </div>

        <script>
            async function loadReviews() {
                try {
                    const response = await fetch('/api/reviews?per_page=5');
                    const data = await response.json();

                    const container = document.getElementById('reviews-container');
                    container.innerHTML = '';

                    data.reviews.forEach(review => {
                        const reviewDiv = document.createElement('div');
                        reviewDiv.className = 'review';
                        reviewDiv.innerHTML = `
                            <div class="rating">${'★'.repeat(review.rating)}${'☆'.repeat(5-review.rating)}</div>
                            <div class="name">${review.name}</div>
                            <div class="content">${review.content}</div>
                            <div class="date">${new Date(review.created_at).toLocaleDateString()}</div>
                        `;
                        container.appendChild(reviewDiv);
                    });
                } catch (error) {
                    document.getElementById('reviews-container').innerHTML = 'Fehler beim Laden der Bewertungen.';
                }
            }

            loadReviews();
        </script>
    </body>
    </html>
    """

# Admin API Endpoints

@app.post("/api/admin/login", response_model=schemas.Token)
async def admin_login(
    request: Request,
    login_data: schemas.AdminLogin,
    db: Session = Depends(database.get_db)
):
    """Admin-Login mit erweiterten Sicherheitsfeatures"""
    client_ip = auth.SecurityUtils.get_client_ip(request)
    user_agent = request.headers.get("User-Agent", "Unknown")

    # Rate Limiting für Login-Versuche
    await auth.check_rate_limit(request, "/api/admin/login")

    # User authentifizieren mit Brute-Force-Schutz
    user = auth.AuthManager.authenticate_user(
        login_data.username,
        login_data.password,
        db,
        client_ip,
        user_agent
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Access und Refresh Token erstellen
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.AuthManager.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    refresh_token = auth.AuthManager.create_refresh_token(
        data={"sub": user.username}
    )

    # Login-Zeit aktualisieren
    user.last_login = datetime.utcnow()
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": auth.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }

@app.get("/api/admin/me", response_model=schemas.AdminUserResponse)
async def get_current_admin_user_info(
    current_user: models.AdminUser = Depends(auth.get_current_active_admin_user)
):
    """Aktuelle Benutzerinformationen mit Rollen-Details abrufen"""
    return current_user

@app.post("/api/admin/refresh", response_model=schemas.Token)
async def admin_refresh_token(
    request: Request,
    refresh_data: schemas.RefreshToken,
    db: Session = Depends(database.get_db)
):
    """Token erneuern mit Refresh Token"""

    # Rate Limiting für Refresh-Versuche
    await auth.check_rate_limit(request, "/api/admin/refresh")

    # Refresh Token verifizieren
    username = auth.AuthManager.verify_token(refresh_data.refresh_token, "refresh")
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # User laden und validieren
    user = crud.admin_user_crud.get_admin_user_by_username(db, username)
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Neuen Access Token erstellen
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.AuthManager.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    # Neuen Refresh Token erstellen
    new_refresh_token = auth.AuthManager.create_refresh_token(
        data={"sub": user.username}
    )

    # Login-Zeit aktualisieren
    user.last_login = datetime.utcnow()
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
        "expires_in": auth.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }

@app.get("/api/admin/security/dashboard")
async def security_dashboard(
    request: Request,
    current_user: models.AdminUser = Depends(auth.get_current_active_admin_user),
    db: Session = Depends(database.get_db)
):
    """Security Dashboard - Sicherheitsübersicht für Admins"""
    from .security_monitor import security_monitor

    return {
        "summary": security_monitor.get_security_summary(24),
        "recent_events": security_monitor.get_recent_events(20),
        "blocked_ips": list(security_monitor.blocked_ips.keys()),
        "active_threats": len(security_monitor.active_threats)
    }

@app.post("/api/admin/security/unblock-ip")
async def unblock_ip(
    request: Request,
    ip_data: dict,
    current_user: models.AdminUser = Depends(auth.get_current_active_admin_user),
    db: Session = Depends(database.get_db)
):
    """IP-Adresse manuell entsperren"""
    from .security_monitor import security_monitor

    ip_address = ip_data.get("ip_address")
    if not ip_address:
        raise HTTPException(status_code=400, detail="IP address required")

    # IP entsperren
    if ip_address in security_monitor.blocked_ips:
        del security_monitor.blocked_ips[ip_address]

    if ip_address in auth.login_tracker.blocked_ips:
        del auth.login_tracker.blocked_ips[ip_address]

    # Log the action
    security_monitor.log_event(
        event_type="admin_action",
        severity="LOW",
        source_ip=auth.SecurityUtils.get_client_ip(request),
        username=current_user.username,
        details={"action": "unblock_ip", "target_ip": ip_address}
    )

    return {"message": f"IP {ip_address} has been unblocked"}

    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/admin/reviews", response_model=schemas.ReviewListResponse)
async def admin_get_reviews(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    approved_only: Optional[bool] = Query(None),
    current_user: models.AdminUser = Depends(auth.get_current_active_admin_user),
    db: Session = Depends(database.get_db)
):
    """Alle Bewertungen abrufen (Admin)"""
    skip = (page - 1) * per_page

    reviews, total = crud.review_crud.get_reviews(
        db,
        skip=skip,
        limit=per_page,
        approved_only=approved_only
    )

    total_pages = math.ceil(total / per_page)

    return schemas.ReviewListResponse(
        reviews=reviews,
        total=total,
        page=page,
        per_page=per_page,
        total_pages=total_pages
    )

@app.put("/api/admin/reviews/{review_id}", response_model=schemas.ReviewAdminResponse)
async def admin_update_review(
    review_id: int,
    review_update: schemas.ReviewUpdate,
    current_user: models.AdminUser = Depends(auth.get_current_active_admin_user),
    db: Session = Depends(database.get_db)
):
    """Bewertung bearbeiten (Admin)"""
    updated_review = crud.review_crud.update_review(db, review_id, review_update)
    if not updated_review:
        raise HTTPException(status_code=404, detail="Bewertung nicht gefunden")
    return updated_review

@app.delete("/api/admin/reviews/{review_id}")
async def admin_delete_review(
    review_id: int,
    current_user: models.AdminUser = Depends(auth.get_current_active_admin_user),
    db: Session = Depends(database.get_db)
):
    """Bewertung löschen (Admin)"""
    success = crud.review_crud.delete_review(db, review_id)
    if not success:
        raise HTTPException(status_code=404, detail="Bewertung nicht gefunden")
    return {"message": "Bewertung erfolgreich gelöscht"}

@app.post("/api/admin/reviews/import")
async def admin_import_reviews(
    import_request: schemas.ImportRequest,
    current_user: models.AdminUser = Depends(auth.get_current_active_admin_user),
    db: Session = Depends(database.get_db)
):
    """Bewertungen importieren (Admin)"""
    created_reviews = crud.review_crud.bulk_import_reviews(
        db, import_request.reviews, import_request.source
    )

    return {
        "message": f"{len(created_reviews)} Bewertungen erfolgreich importiert",
        "imported_count": len(created_reviews)
    }

@app.get("/api/admin/stats")
async def admin_get_stats(
    current_user: models.AdminUser = Depends(auth.get_current_active_admin_user),
    db: Session = Depends(database.get_db)
):
    """Vollständige Statistiken (Admin)"""
    return crud.review_crud.get_review_stats(db)

@app.get("/api/admin/export")
async def admin_export_reviews(
    current_user: models.AdminUser = Depends(auth.get_current_active_admin_user),
    db: Session = Depends(database.get_db)
):
    """Bewertungen exportieren (Admin)"""
    reviews, _ = crud.review_crud.get_reviews(db, approved_only=False, limit=10000)
    export_data = utils.ImportExportUtils.export_reviews_json(reviews)

    return JSONResponse(
        content=export_data,
        headers={"Content-Disposition": "attachment; filename=reviews_export.json"}
    )

@app.get("/api/admin/export/full")
async def admin_export_full_data(
    current_user: models.AdminUser = Depends(auth.get_current_active_admin_user),
    db: Session = Depends(database.get_db)
):
    """Vollständigen Datenexport mit Reviews und Kommentaren (Admin)"""
    export_data = crud.review_crud.full_export_data(db)

    # JSON serializable machen
    serializable_data = utils.ImportExportUtils.make_json_serializable(export_data)

    return JSONResponse(
        content=serializable_data,
        headers={"Content-Disposition": "attachment; filename=guestbook_full_export.json"}
    )

@app.post("/api/admin/import/full")
async def admin_import_full_data(
    import_data: schemas.FullImportData,
    replace_existing: bool = False,
    current_user: models.AdminUser = Depends(auth.get_current_active_admin_user),
    db: Session = Depends(database.get_db)
):
    """Vollständigen Datenimport mit Reviews und Kommentaren (Admin)"""
    result = crud.review_crud.full_import_data(db, import_data, replace_existing)

    return {
        "message": f"Import abgeschlossen: {result['imported_reviews']} Reviews und {result['imported_comments']} Kommentare importiert",
        "imported_reviews": result["imported_reviews"],
        "imported_comments": result["imported_comments"],
        "skipped_reviews": result["skipped_reviews"],
        "errors": result["errors"]
    }

# Moderation Endpoints

@app.get("/api/admin/reviews/pending", response_model=schemas.ReviewListResponse)
async def admin_get_pending_reviews(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    current_user: models.AdminUser = Depends(auth.get_current_active_admin_user),
    db: Session = Depends(database.get_db)
):
    """Ausstehende Bewertungen für Moderation abrufen (Admin)"""
    skip = (page - 1) * per_page

    reviews, total = crud.review_crud.get_pending_reviews(
        db,
        skip=skip,
        limit=per_page
    )

    total_pages = math.ceil(total / per_page)

    return schemas.ReviewListResponse(
        reviews=reviews,
        total=total,
        page=page,
        per_page=per_page,
        total_pages=total_pages
    )

@app.post("/api/admin/reviews/{review_id}/approve", response_model=schemas.ReviewAdminResponse)
async def admin_approve_review(
    review_id: int,
    current_user: models.AdminUser = Depends(auth.get_current_active_admin_user),
    db: Session = Depends(database.get_db)
):
    """Bewertung genehmigen (Admin)"""
    approved_review = crud.review_crud.approve_review(db, review_id)
    if not approved_review:
        raise HTTPException(status_code=404, detail="Bewertung nicht gefunden")
    return approved_review

@app.post("/api/admin/reviews/{review_id}/reject", response_model=schemas.ReviewAdminResponse)
async def admin_reject_review(
    review_id: int,
    current_user: models.AdminUser = Depends(auth.get_current_active_admin_user),
    db: Session = Depends(database.get_db)
):
    """Bewertung ablehnen (Admin)"""
    rejected_review = crud.review_crud.reject_review(db, review_id)
    if not rejected_review:
        raise HTTPException(status_code=404, detail="Bewertung nicht gefunden")
    return rejected_review

# === ADMIN COMMENT ENDPOINTS ===

@app.get("/api/admin/comments", response_model=schemas.CommentAdminListResponse)
async def admin_get_comments(
    page: int = Query(1, ge=1, description="Seitennummer"),
    per_page: int = Query(10, ge=1, le=100, description="Einträge pro Seite"),
    current_user: models.AdminUser = Depends(auth.get_current_active_admin_user),
    db: Session = Depends(database.get_db)
):
    """Alle Kommentare mit Review-Informationen abrufen (Admin)"""
    skip = (page - 1) * per_page
    comments, total = crud.comment_crud.get_comments_with_review_info(
        db, skip=skip, limit=per_page, approved_only=False
    )

    total_pages = math.ceil(total / per_page)

    return {
        "comments": comments,
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": total_pages
    }

@app.get("/api/admin/comments/pending", response_model=schemas.CommentAdminListResponse)
async def admin_get_pending_comments(
    page: int = Query(1, ge=1, description="Seitennummer"),
    per_page: int = Query(10, ge=1, le=100, description="Einträge pro Seite"),
    current_user: models.AdminUser = Depends(auth.get_current_active_admin_user),
    db: Session = Depends(database.get_db)
):
    """Pending Kommentare mit Review-Informationen abrufen (Admin)"""
    skip = (page - 1) * per_page
    comments, total = crud.comment_crud.get_pending_comments_with_review_info(
        db, skip=skip, limit=per_page
    )

    total_pages = math.ceil(total / per_page)

    return {
        "comments": comments,
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": total_pages
    }

@app.put("/api/admin/comments/{comment_id}", response_model=schemas.CommentAdminResponse)
async def admin_update_comment(
    comment_id: int,
    comment_update: schemas.CommentUpdate,
    current_user: models.AdminUser = Depends(auth.get_current_active_admin_user),
    db: Session = Depends(database.get_db)
):
    """Kommentar aktualisieren (Admin)"""
    updated_comment = crud.comment_crud.update_comment(db, comment_id, comment_update)
    if not updated_comment:
        raise HTTPException(status_code=404, detail="Kommentar nicht gefunden")
    return updated_comment

@app.post("/api/admin/comments/{comment_id}/approve", response_model=schemas.CommentAdminResponse)
async def admin_approve_comment(
    comment_id: int,
    current_user: models.AdminUser = Depends(auth.get_current_active_admin_user),
    db: Session = Depends(database.get_db)
):
    """Kommentar genehmigen (Admin)"""
    approved_comment = crud.comment_crud.approve_comment(db, comment_id)
    if not approved_comment:
        raise HTTPException(status_code=404, detail="Kommentar nicht gefunden")
    return approved_comment

@app.delete("/api/admin/comments/{comment_id}")
async def admin_delete_comment(
    comment_id: int,
    current_user: models.AdminUser = Depends(auth.get_current_active_admin_user),
    db: Session = Depends(database.get_db)
):
    """Kommentar löschen (Admin)"""
    deleted = crud.comment_crud.delete_comment(db, comment_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Kommentar nicht gefunden")
    return {"message": "Kommentar erfolgreich gelöscht"}

# === ADMIN USER MANAGEMENT ENDPOINTS ===

@app.post("/api/admin/users", response_model=schemas.AdminUserResponse)
async def create_admin_user(
    user_data: schemas.AdminUserCreate,
    current_user: models.AdminUser = Depends(auth.get_current_active_admin_user),
    db: Session = Depends(database.get_db)
):
    """Neuen Admin-Benutzer erstellen (Admin/Superuser)"""
    from app.auth import RolePermissions

    # Rollenbasierte Berechtigungsprüfung
    if not RolePermissions.can_manage_users(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Keine Berechtigung zur Benutzerverwaltung"
        )

    # Nur Superuser können Superuser erstellen
    if user_data.role == models.AdminRole.SUPERUSER and not RolePermissions.can_create_superusers(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Nur Superuser können Superuser-Benutzer erstellen"
        )

    # Admins können keine höheren oder gleichen Rollen erstellen
    if current_user.role == models.AdminRole.ADMIN:
        if user_data.role in [models.AdminRole.ADMIN, models.AdminRole.SUPERUSER]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admins können nur Moderatoren erstellen"
            )

    # Prüfen ob Username bereits existiert
    existing_user = crud.admin_user_crud.get_admin_user_by_username(db, user_data.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Benutzername bereits vergeben"
        )

    # Prüfen ob E-Mail bereits existiert
    existing_email = crud.admin_user_crud.get_admin_user_by_email(db, user_data.email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="E-Mail-Adresse bereits vergeben"
        )

    return crud.admin_user_crud.create_admin_user(db, user_data)

@app.get("/api/admin/users", response_model=schemas.AdminUserListResponse)
async def get_admin_users(
    page: int = Query(1, ge=1, description="Seitennummer"),
    per_page: int = Query(10, ge=1, le=100, description="Einträge pro Seite"),
    current_user: models.AdminUser = Depends(auth.get_current_active_admin_user),
    db: Session = Depends(database.get_db)
):
    """Alle Admin-Benutzer abrufen (Admin/Superuser)"""
    from app.auth import RolePermissions

    # Rollenbasierte Berechtigungsprüfung
    if not RolePermissions.can_manage_users(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Keine Berechtigung zur Benutzerverwaltung"
        )

    skip = (page - 1) * per_page
    users = crud.admin_user_crud.get_all_admin_users(db, skip=skip, limit=per_page)
    total_users = db.query(models.AdminUser).count()
    total_pages = (total_users + per_page - 1) // per_page

    return schemas.AdminUserListResponse(
        users=users,
        total=total_users,
        page=page,
        per_page=per_page,
        total_pages=total_pages
    )

@app.get("/api/admin/users/{user_id}", response_model=schemas.AdminUserResponse)
async def get_admin_user(
    user_id: int,
    current_user: models.AdminUser = Depends(auth.get_current_active_admin_user),
    db: Session = Depends(database.get_db)
):
    """Einzelnen Admin-Benutzer abrufen"""
    user = crud.admin_user_crud.get_admin_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Admin-Benutzer nicht gefunden")
    return user

@app.put("/api/admin/users/{user_id}", response_model=schemas.AdminUserResponse)
async def update_admin_user(
    user_id: int,
    user_update: schemas.AdminUserUpdate,
    current_user: models.AdminUser = Depends(auth.get_current_active_admin_user),
    db: Session = Depends(database.get_db)
):
    """Admin-Benutzer aktualisieren"""
    from app.auth import RolePermissions

    # Prüfen ob User existiert
    target_user = crud.admin_user_crud.get_admin_user(db, user_id)
    if not target_user:
        raise HTTPException(status_code=404, detail="Admin-Benutzer nicht gefunden")

    # Berechtigung prüfen: Admin/Superuser für andere User oder User selbst
    is_self_update = current_user.id == user_id
    can_manage = RolePermissions.can_manage_users(current_user)

    if not (is_self_update or can_manage):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Keine Berechtigung"
        )

    # Rollenänderungen handhaben
    if user_update.role is not None and user_update.role != target_user.role:
        # Nur Admins/Superuser können Rollen ändern
        if not can_manage:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Keine Berechtigung zur Rollenänderung"
            )

        # Admins können keine höheren oder gleichen Rollen vergeben
        if current_user.role == models.AdminRole.ADMIN:
            if user_update.role in [models.AdminRole.ADMIN, models.AdminRole.SUPERUSER]:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Admins können nur Moderator-Rollen vergeben"
                )

        # Nur Superuser können Superuser-Rollen vergeben/entziehen
        if user_update.role == models.AdminRole.SUPERUSER and not RolePermissions.can_create_superusers(current_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Nur Superuser können Superuser-Rollen vergeben"
            )

        # Verhindere, dass sich der letzte Superuser selbst degradiert
        if (current_user.id == user_id and
            target_user.role == models.AdminRole.SUPERUSER and
            user_update.role != models.AdminRole.SUPERUSER):

            other_superusers = db.query(models.AdminUser).filter(
                models.AdminUser.id != user_id,
                models.AdminUser.role == models.AdminRole.SUPERUSER,
                models.AdminUser.is_active == True
            ).count()

            if other_superusers == 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Sie können sich nicht selbst degradieren, da Sie der einzige aktive Superuser sind"
                )

    # Legacy Superuser-Status-Änderungen handhaben (Rückwärtskompatibilität)
    if user_update.is_superuser is not None:
        # Nur Superuser können Superuser-Status ändern
        if not RolePermissions.can_create_superusers(current_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Nur Superuser können Superuser-Status ändern"
            )

        # Verhindere, dass sich ein Superuser selbst den Superuser-Status entzieht
        if current_user.id == user_id and target_user.is_superuser and not user_update.is_superuser:
            # Prüfe, ob es andere aktive Superuser gibt
            other_superusers = db.query(models.AdminUser).filter(
                models.AdminUser.id != user_id,
                models.AdminUser.is_superuser == True,
                models.AdminUser.is_active == True
            ).count()

            if other_superusers == 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Sie können sich nicht selbst den Superuser-Status entziehen, da Sie der einzige aktive Superuser sind"
                )

    # Username-Eindeutigkeit prüfen
    if user_update.username and user_update.username != target_user.username:
        existing_user = crud.admin_user_crud.get_admin_user_by_username(db, user_update.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Benutzername bereits vergeben"
            )

    # E-Mail-Eindeutigkeit prüfen
    if user_update.email and user_update.email != target_user.email:
        existing_email = crud.admin_user_crud.get_admin_user_by_email(db, user_update.email)
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="E-Mail-Adresse bereits vergeben"
            )

    updated_user = crud.admin_user_crud.update_admin_user(db, user_id, user_update)
    return updated_user

@app.delete("/api/admin/users/{user_id}")
async def delete_admin_user(
    user_id: int,
    current_user: models.AdminUser = Depends(auth.get_current_active_admin_user),
    db: Session = Depends(database.get_db)
):
    """Admin-Benutzer löschen (nur für Superuser)"""
    from app.auth import RolePermissions

    if not RolePermissions.can_create_superusers(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Nur Superuser können Admin-Benutzer löschen"
        )

    # Sich selbst nicht löschen
    if current_user.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Sie können sich nicht selbst löschen"
        )

    # Prüfen ob User existiert
    target_user = crud.admin_user_crud.get_admin_user(db, user_id)
    if not target_user:
        raise HTTPException(status_code=404, detail="Admin-Benutzer nicht gefunden")

    deleted = crud.admin_user_crud.delete_admin_user(db, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Admin-Benutzer nicht gefunden")

    return {"message": "Admin-Benutzer erfolgreich gelöscht"}

@app.post("/api/admin/users/{user_id}/deactivate", response_model=schemas.AdminUserResponse)
async def deactivate_admin_user(
    user_id: int,
    current_user: models.AdminUser = Depends(auth.get_current_active_admin_user),
    db: Session = Depends(database.get_db)
):
    """Admin-Benutzer deaktivieren (nur für Superuser)"""
    from app.auth import RolePermissions

    if not RolePermissions.can_create_superusers(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Nur Superuser können Admin-Benutzer deaktivieren"
        )

    # Sich selbst nicht deaktivieren
    if current_user.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Sie können sich nicht selbst deaktivieren"
        )

    user = crud.admin_user_crud.deactivate_admin_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Admin-Benutzer nicht gefunden")
    return user

@app.post("/api/admin/users/{user_id}/activate", response_model=schemas.AdminUserResponse)
async def activate_admin_user(
    user_id: int,
    current_user: models.AdminUser = Depends(auth.get_current_active_admin_user),
    db: Session = Depends(database.get_db)
):
    """Admin-Benutzer aktivieren (nur für Superuser)"""
    from app.auth import RolePermissions

    if not RolePermissions.can_create_superusers(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Nur Superuser können Admin-Benutzer aktivieren"
        )

    user = crud.admin_user_crud.activate_admin_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Admin-Benutzer nicht gefunden")
    return user

@app.post("/api/admin/change-password")
async def change_admin_password(
    password_data: schemas.PasswordChangeRequest,
    current_user: models.AdminUser = Depends(auth.get_current_active_admin_user),
    db: Session = Depends(database.get_db)
):
    """Eigenes Passwort ändern"""
    success = crud.admin_user_crud.change_password(
        db,
        current_user.id,
        password_data.old_password,
        password_data.new_password
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Altes Passwort ist falsch"
        )

    return {"message": "Passwort erfolgreich geändert"}

# Error Handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail, "status_code": exc.status_code}
    )

# Catch-All Route für React Frontend (muss als letztes definiert werden)
if os.path.exists("/app/backend/static"):
    @app.get("/{full_path:path}")
    async def catch_all(full_path: str):
        """Serve React App für alle nicht-API Routen"""
        # API-Routen nicht abfangen
        if full_path.startswith("api/") or full_path.startswith("docs") or full_path.startswith("redoc") or full_path.startswith("uploads") or full_path == "health":
            raise HTTPException(status_code=404, detail="Not found")

        # React index.html für alle anderen Routen
        return FileResponse("/app/backend/static/index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
