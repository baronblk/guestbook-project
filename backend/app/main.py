from fastapi import FastAPI, Depends, HTTPException, status, File, UploadFile, Request, Query
from fastapi.security import HTTPBearer
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import math
from datetime import timedelta

from . import models, schemas, crud, auth, database, utils

# App initialisieren
app = FastAPI(
    title="Gästebuch API",
    description="Vollständiges Gästebuch-System mit Admin-Panel",
    version="1.0.0"
)

# CORS konfigurieren
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In Produktion spezifische Origins setzen
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static Files für Uploads
app.mount("/uploads", StaticFiles(directory="/app/uploads"), name="uploads")

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

@app.get("/", response_class=HTMLResponse)
async def root():
    """Basis-Endpunkt"""
    return """
    <html>
        <head>
            <title>Gästebuch API</title>
        </head>
        <body>
            <h1>Gästebuch API</h1>
            <p>API läuft erfolgreich!</p>
            <ul>
                <li><a href="/docs">API Dokumentation</a></li>
                <li><a href="/api/reviews">Bewertungen anzeigen</a></li>
                <li><a href="/api/stats">Statistiken</a></li>
            </ul>
        </body>
    </html>
    """

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
    featured_only: Optional[bool] = Query(None),
    search: Optional[str] = Query(None),
    sort_by: str = Query("created_at", pattern="^(created_at|rating|name)$"),
    sort_order: str = Query("desc", pattern="^(asc|desc)$"),
    db: Session = Depends(database.get_db)
):
    """Bewertungen abrufen (öffentlich)"""
    skip = (page - 1) * per_page
    
    # Filter erstellen
    filters = schemas.ReviewFilters(
        rating=rating,
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
    return db_review

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
    username: str,
    password: str,
    db: Session = Depends(database.get_db)
):
    """Admin-Login"""
    user = crud.admin_user_crud.authenticate_admin_user(db, username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Ungültige Anmeldedaten"
        )
    
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.AuthManager.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
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
        approved_only=approved_only if approved_only is not None else False
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

# Error Handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail, "status_code": exc.status_code}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
