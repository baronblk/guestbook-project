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
    title="Guestbook API",
    description="Professional Guestbook System with Admin Panel",
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

@app.get("/health")
async def health_check():
    """Health Check für Container"""
    try:
        # Datenbankverbindung testen
        db = database.SessionLocal()
        db.execute("SELECT 1")
        db.close()
        
        return {"status": "healthy", "service": "guestbook-api", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Health check failed: {str(e)}")

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
                <li><a href="/health">Health Check</a></li>
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
    """Create new review"""
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
    """Upload image for review"""
    # Review prüfen
    db_review = crud.review_crud.get_review(db, review_id)
    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")
    
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
    """Get reviews (public)"""
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
    """Get single review"""
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
        <title>Guestbook Widget</title>
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
            <h3>Customer Reviews</h3>
            <div id="reviews-container">Loading...</div>
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
                    document.getElementById('reviews-container').innerHTML = 'Error loading reviews.';
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
    """Bewertungen importieren (Admin) mit optionalen Kommentaren"""
    created_reviews = crud.review_crud.bulk_import_reviews(
        db, 
        import_request.reviews, 
        import_request.source, 
        auto_approve=True, 
        include_comments=import_request.include_comments
    )
    
    comments_info = ""
    if import_request.include_comments:
        total_comments = sum(len(review.comments) for review in import_request.reviews)
        comments_info = f" mit {total_comments} Kommentaren"
    
    return {
        "message": f"{len(created_reviews)} Bewertungen{comments_info} erfolgreich importiert",
        "imported_count": len(created_reviews),
        "include_comments": import_request.include_comments
    }

@app.post("/api/admin/reviews/import-export")
async def admin_import_from_export(
    export_data: dict,
    import_source: str = Query("export_reimport", description="Source identifier for imported reviews"),
    current_user: models.AdminUser = Depends(auth.get_current_active_admin_user),
    db: Session = Depends(database.get_db)
):
    """Export-Datei direkt importieren (Admin) mit Kommentar-Support"""
    try:
        # Export-Format zu Import-Format konvertieren
        import_data = utils.ImportExportUtils.convert_export_to_import_format(
            export_data, import_source
        )
        
        # Import durchführen
        created_reviews = crud.review_crud.bulk_import_reviews(
            db, 
            [schemas.ImportReview(**review) for review in import_data['reviews']], 
            import_data['source'],
            auto_approve=True,
            include_comments=import_data.get('include_comments', False)
        )
        
        comments_info = ""
        if import_data.get('include_comments', False):
            total_comments = sum(len(review.get('comments', [])) for review in import_data['reviews'])
            comments_info = f" mit {total_comments} Kommentaren"
        
        return {
            "message": f"{len(created_reviews)} Bewertungen aus Export-Datei{comments_info} erfolgreich importiert",
            "imported_count": len(created_reviews),
            "source": import_data['source'],
            "include_comments": import_data.get('include_comments', False)
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Fehler beim Importieren der Daten")

@app.post("/api/admin/import")
async def admin_import_export_data(
    import_data: dict,
    current_user: models.AdminUser = Depends(auth.get_current_active_admin_user),
    db: Session = Depends(database.get_db)
):
    """Legacy Import-Endpunkt für Admin-Dashboard (Export-Daten importieren)"""
    try:
        # Prüfen ob es Export-Format ist (hat "reviews" und "exported_at")
        if 'reviews' in import_data and 'exported_at' in import_data:
            # Export-Format zu Import-Format konvertieren
            converted_data = utils.ImportExportUtils.convert_export_to_import_format(
                import_data, "admin_dashboard_import"
            )
            
            # Import durchführen
            created_reviews = crud.review_crud.bulk_import_reviews(
                db, 
                [schemas.ImportReview(**review) for review in converted_data['reviews']], 
                converted_data['source'],
                auto_approve=True,
                include_comments=converted_data.get('include_comments', False)
            )
            
            comments_info = ""
            if converted_data.get('include_comments', False):
                total_comments = sum(len(review.get('comments', [])) for review in converted_data['reviews'])
                comments_info = f" mit {total_comments} Kommentaren"
            
            return {
                "message": f"{len(created_reviews)} Bewertungen{comments_info} erfolgreich importiert",
                "imported_count": len(created_reviews),
                "include_comments": converted_data.get('include_comments', False)
            }
        else:
            # Legacy Format handling
            raise HTTPException(status_code=400, detail="Unsupported import format")
            
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Fehler beim Importieren der Daten")

@app.get("/api/admin/stats")
async def admin_get_stats(
    current_user: models.AdminUser = Depends(auth.get_current_active_admin_user),
    db: Session = Depends(database.get_db)
):
    """Vollständige Statistiken (Admin)"""
    return crud.review_crud.get_review_stats(db)

@app.get("/api/admin/stats/comments")
async def admin_get_comments_stats(
    current_user: models.AdminUser = Depends(auth.get_current_active_admin_user),
    db: Session = Depends(database.get_db)
):
    """Kommentar-Statistiken für Dashboard (Admin)"""
    return crud.comment_crud.get_comment_stats(db)

@app.get("/api/admin/export")
async def admin_export_reviews(
    include_comments: bool = Query(True, description="Include comments in export"),
    current_user: models.AdminUser = Depends(auth.get_current_active_admin_user),
    db: Session = Depends(database.get_db)
):
    """Bewertungen exportieren (Admin) mit optionalen Kommentaren"""
    # Reviews mit Kommentaren laden falls gewünscht
    if include_comments:
        from sqlalchemy.orm import joinedload
        reviews = db.query(models.Review).options(joinedload(models.Review.comments)).limit(10000).all()
    else:
        reviews, _ = crud.review_crud.get_reviews(db, approved_only=None, limit=10000)
    
    export_data = utils.ImportExportUtils.export_reviews_json(reviews, include_comments)
    
    filename = f"reviews_export{'_with_comments' if include_comments else ''}.json"
    return JSONResponse(
        content=export_data,
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

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

@app.get("/api/admin/comments", response_model=schemas.CommentListResponse)
async def admin_get_comments(
    page: int = Query(1, ge=1, description="Seitennummer"),
    per_page: int = Query(10, ge=1, le=100, description="Einträge pro Seite"),
    current_user: models.AdminUser = Depends(auth.get_current_active_admin_user),
    db: Session = Depends(database.get_db)
):
    """Alle Kommentare abrufen (Admin)"""
    skip = (page - 1) * per_page
    comments, total = crud.comment_crud.get_comments(
        db, skip=skip, limit=per_page, approved_only=False
    )
    
    total_pages = math.ceil(total / per_page)
    
    # Tab-Statistiken für korrekte Anzeige
    comment_stats = crud.comment_crud.get_comment_stats(db)
    
    return {
        "comments": comments,
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": total_pages,
        "tab_stats": {
            "all_comments": comment_stats["total_comments"],
            "pending_comments": comment_stats["pending_comments"],
            "approved_comments": comment_stats["approved_comments"]
        }
    }

@app.get("/api/admin/comments/pending", response_model=schemas.CommentListResponse)
async def admin_get_pending_comments(
    page: int = Query(1, ge=1, description="Seitennummer"),
    per_page: int = Query(10, ge=1, le=100, description="Einträge pro Seite"),
    current_user: models.AdminUser = Depends(auth.get_current_active_admin_user),
    db: Session = Depends(database.get_db)
):
    """Pending Kommentare abrufen (Admin)"""
    skip = (page - 1) * per_page
    comments, total = crud.comment_crud.get_pending_comments(
        db, skip=skip, limit=per_page
    )
    
    total_pages = math.ceil(total / per_page)
    
    # Tab-Statistiken für korrekte Anzeige
    comment_stats = crud.comment_crud.get_comment_stats(db)
    
    return {
        "comments": comments,
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": total_pages,
        "tab_stats": {
            "all_comments": comment_stats["total_comments"],
            "pending_comments": comment_stats["pending_comments"],
            "approved_comments": comment_stats["approved_comments"]
        }
    }
    
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
