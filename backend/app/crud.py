from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, asc, func
from typing import List, Optional
from datetime import datetime
import hashlib
from passlib.context import CryptContext

from . import models, schemas

# Passwort-Hashing Kontext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """Password hashen"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Password verifizieren"""
    return pwd_context.verify(plain_password, hashed_password)

# Review CRUD
class ReviewCRUD:

    @staticmethod
    def create_review(db: Session, review: schemas.ReviewCreate, ip_address: Optional[str] = None) -> models.Review:
        """Neue Bewertung erstellen"""
        db_review = models.Review(
            name=review.name,
            email=review.email,
            rating=review.rating,
            title=review.title,
            content=review.content,
            ip_address=ip_address
            # is_approved wird vom Modell-Default (False) gesetzt
        )
        db.add(db_review)
        db.commit()
        db.refresh(db_review)
        return db_review

    @staticmethod
    def get_review(db: Session, review_id: int) -> Optional[models.Review]:
        """Einzelne Bewertung abrufen"""
        return db.query(models.Review).filter(models.Review.id == review_id).first()

    @staticmethod
    def get_reviews(
        db: Session,
        skip: int = 0,
        limit: int = 10,
        approved_only: bool = True,
        filters: Optional[schemas.ReviewFilters] = None,
        sort_by: str = "created_at",
        sort_order: str = "desc"
    ) -> tuple[List[models.Review], int]:
        """Bewertungen mit Filterung und Pagination abrufen"""
        query = db.query(models.Review)

        # Basis-Filter für Genehmigungsstatus
        if approved_only is True:
            query = query.filter(models.Review.is_approved == True)
        elif approved_only is False:
            query = query.filter(models.Review.is_approved == False)
        # Wenn approved_only None ist, werden alle Reviews angezeigt

        # Erweiterte Filter
        if filters:
            if filters.rating:
                query = query.filter(models.Review.rating >= filters.rating)
            if filters.is_featured is not None:
                query = query.filter(models.Review.is_featured == filters.is_featured)
            if filters.search:
                search_term = f"%{filters.search}%"
                query = query.filter(
                    or_(
                        models.Review.name.ilike(search_term),
                        models.Review.title.ilike(search_term),
                        models.Review.content.ilike(search_term)
                    )
                )
            if filters.date_from:
                query = query.filter(models.Review.created_at >= filters.date_from)
            if filters.date_to:
                query = query.filter(models.Review.created_at <= filters.date_to)

        # Sortierung - Neueste zuerst, Featured Reviews werden hervorgehoben aber nicht priorisiert
        sort_column = getattr(models.Review, sort_by, models.Review.created_at)
        if sort_order == "desc":
            query = query.order_by(desc(sort_column))
        else:
            query = query.order_by(asc(sort_column))

        total = query.count()
        reviews = query.offset(skip).limit(limit).all()

        return reviews, total

    @staticmethod
    def update_review(db: Session, review_id: int, review_update: schemas.ReviewUpdate) -> Optional[models.Review]:
        """Bewertung aktualisieren (Admin)"""
        db_review = db.query(models.Review).filter(models.Review.id == review_id).first()
        if not db_review:
            return None

        update_data = review_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_review, field, value)

        db_review.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_review)
        return db_review

    @staticmethod
    def delete_review(db: Session, review_id: int) -> bool:
        """Bewertung löschen"""
        db_review = db.query(models.Review).filter(models.Review.id == review_id).first()
        if not db_review:
            return False

        db.delete(db_review)
        db.commit()
        return True

    @staticmethod
    def get_review_stats(db: Session) -> dict:
        """Statistiken für Dashboard"""
        total_reviews = db.query(models.Review).count()
        approved_reviews = db.query(models.Review).filter(models.Review.is_approved == True).count()
        avg_rating = db.query(func.avg(models.Review.rating)).filter(models.Review.is_approved == True).scalar() or 0

        rating_distribution = db.query(
            models.Review.rating,
            func.count(models.Review.id).label('count')
        ).filter(models.Review.is_approved == True).group_by(models.Review.rating).all()

        return {
            "total_reviews": total_reviews,
            "approved_reviews": approved_reviews,
            "pending_reviews": total_reviews - approved_reviews,
            "average_rating": round(float(avg_rating), 2),
            "rating_distribution": {str(rating): count for rating, count in rating_distribution}
        }

    @staticmethod
    def bulk_import_reviews(db: Session, reviews: List[schemas.ImportReview], source: str, auto_approve: bool = True) -> List[models.Review]:
        """Bulk-Import von Bewertungen"""
        created_reviews = []

        for review_data in reviews:
            # Check für Duplikate basierend auf external_id
            if review_data.external_id:
                existing = db.query(models.Review).filter(
                    models.Review.external_id == review_data.external_id,
                    models.Review.import_source == source
                ).first()
                if existing:
                    continue  # Skip Duplikat

            db_review = models.Review(
                name=review_data.name,
                email=review_data.email,
                rating=review_data.rating,
                title=review_data.title,
                content=review_data.content,
                created_at=review_data.created_at or datetime.utcnow(),
                import_source=source,
                external_id=review_data.external_id,
                is_approved=auto_approve  # Kann beim Import konfiguriert werden
            )
            db.add(db_review)
            created_reviews.append(db_review)

        db.commit()
        for review in created_reviews:
            db.refresh(review)

        return created_reviews

    @staticmethod
    def approve_review(db: Session, review_id: int) -> Optional[models.Review]:
        """Bewertung genehmigen"""
        db_review = db.query(models.Review).filter(models.Review.id == review_id).first()
        if not db_review:
            return None

        db_review.is_approved = True
        db_review.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_review)
        return db_review

    @staticmethod
    def reject_review(db: Session, review_id: int) -> Optional[models.Review]:
        """Bewertung ablehnen (verstecken)"""
        db_review = db.query(models.Review).filter(models.Review.id == review_id).first()
        if not db_review:
            return None

        db_review.is_approved = False
        db_review.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_review)
        return db_review

    @staticmethod
    def get_reviews_with_comments_for_export(db: Session) -> List[models.Review]:
        """Alle Reviews mit Kommentaren für Export abrufen"""
        from sqlalchemy.orm import selectinload
        return db.query(models.Review).options(
            selectinload(models.Review.comments)
        ).all()

    @staticmethod
    def full_export_data(db: Session) -> dict:
        """Vollständiger Datenexport mit Reviews und Kommentaren"""
        from sqlalchemy.orm import selectinload

        # Reviews mit allen Kommentaren laden
        reviews = db.query(models.Review).options(
            selectinload(models.Review.comments)
        ).all()

        total_comments = sum(len(review.comments) for review in reviews)

        export_data = {
            "exported_at": datetime.utcnow(),
            "export_version": "2.0",
            "total_reviews": len(reviews),
            "total_comments": total_comments,
            "reviews": []
        }

        for review in reviews:
            review_data = {
                "id": review.id,
                "name": review.name,
                "email": review.email,
                "rating": review.rating,
                "title": review.title,
                "content": review.content,
                "image_path": review.image_path,
                "created_at": review.created_at,
                "updated_at": review.updated_at,
                "is_approved": review.is_approved,
                "is_featured": review.is_featured,
                "admin_notes": review.admin_notes,
                "import_source": review.import_source,
                "external_id": review.external_id,
                "ip_address": review.ip_address,
                "comments": []
            }

            # Kommentare hinzufügen
            for comment in review.comments:
                comment_data = {
                    "id": comment.id,
                    "name": comment.name,
                    "email": comment.email,
                    "content": comment.content,
                    "created_at": comment.created_at,
                    "updated_at": comment.updated_at,
                    "is_approved": comment.is_approved,
                    "admin_notes": comment.admin_notes,
                    "ip_address": comment.ip_address
                }
                review_data["comments"].append(comment_data)

            export_data["reviews"].append(review_data)

        return export_data

    @staticmethod
    def full_import_data(db: Session, import_data: schemas.FullImportData, replace_existing: bool = False) -> dict:
        """Vollständiger Datenimport mit Reviews und Kommentaren"""
        if replace_existing:
            # Alle bestehenden Daten löschen (VORSICHT!)
            db.query(models.Comment).delete()
            db.query(models.Review).delete()
            db.commit()

        imported_reviews = 0
        imported_comments = 0
        skipped_reviews = 0
        errors = []

        for review_data in import_data.reviews:
            try:
                # Review erstellen - kompatibel mit Export- und Import-Format
                review_dict = {
                    "name": review_data.name,
                    "email": review_data.email,
                    "rating": review_data.rating,
                    "title": review_data.title,
                    "content": review_data.content,
                    "created_at": getattr(review_data, 'created_at', datetime.utcnow()) or datetime.utcnow(),
                    "is_approved": getattr(review_data, 'is_approved', True),
                    "is_featured": getattr(review_data, 'is_featured', False),
                    "admin_notes": getattr(review_data, 'admin_notes', None),
                    "import_source": getattr(review_data, 'import_source', 'restore'),
                    "external_id": getattr(review_data, 'external_id', None)
                }

                # Image-Path nur setzen wenn es existiert (aus Export-Format)
                if hasattr(review_data, 'image_path') and review_data.image_path:
                    review_dict["image_path"] = review_data.image_path

                # IP-Adresse nur setzen wenn es existiert (aus Export-Format)
                if hasattr(review_data, 'ip_address') and review_data.ip_address:
                    review_dict["ip_address"] = review_data.ip_address

                db_review = models.Review(**review_dict)
                db.add(db_review)
                db.flush()  # Flush um ID zu bekommen

                # Kommentare hinzufügen - kompatibel mit Export- und Import-Format
                for comment_data in review_data.comments:
                    comment_dict = {
                        "review_id": db_review.id,
                        "name": comment_data.name,
                        "email": getattr(comment_data, 'email', None),
                        "content": comment_data.content,
                        "created_at": getattr(comment_data, 'created_at', datetime.utcnow()) or datetime.utcnow(),
                        "is_approved": getattr(comment_data, 'is_approved', True),
                        "admin_notes": getattr(comment_data, 'admin_notes', None)
                    }

                    # IP-Adresse nur setzen wenn es existiert (aus Export-Format)
                    if hasattr(comment_data, 'ip_address') and comment_data.ip_address:
                        comment_dict["ip_address"] = comment_data.ip_address

                    db_comment = models.Comment(**comment_dict)
                    db.add(db_comment)
                    imported_comments += 1

                imported_reviews += 1

            except Exception as e:
                errors.append(f"Error importing review '{review_data.name}': {str(e)}")
                skipped_reviews += 1
                db.rollback()
                continue

        db.commit()

        return {
            "imported_reviews": imported_reviews,
            "imported_comments": imported_comments,
            "skipped_reviews": skipped_reviews,
            "errors": errors
        }

    @staticmethod
    def get_pending_reviews(db: Session, skip: int = 0, limit: int = 10) -> tuple[List[models.Review], int]:
        """Ausstehende Bewertungen für Moderation abrufen"""
        query = db.query(models.Review).filter(models.Review.is_approved == False)
        query = query.order_by(desc(models.Review.created_at))

        total = query.count()
        reviews = query.offset(skip).limit(limit).all()

        return reviews, total

# Admin User CRUD
class AdminUserCRUD:

    @staticmethod
    def create_admin_user(db: Session, user: schemas.AdminUserCreate) -> models.AdminUser:
        """Admin-Benutzer erstellen"""
        hashed_password = get_password_hash(user.password)
        db_user = models.AdminUser(
            username=user.username,
            email=user.email,
            hashed_password=hashed_password
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def get_admin_user(db: Session, user_id: int) -> Optional[models.AdminUser]:
        """Admin-Benutzer abrufen"""
        return db.query(models.AdminUser).filter(models.AdminUser.id == user_id).first()

    @staticmethod
    def get_admin_user_by_username(db: Session, username: str) -> Optional[models.AdminUser]:
        """Admin-Benutzer nach Username abrufen"""
        return db.query(models.AdminUser).filter(models.AdminUser.username == username).first()

    @staticmethod
    def authenticate_admin_user(db: Session, username: str, password: str) -> Optional[models.AdminUser]:
        """Admin-Benutzer authentifizieren"""
        user = AdminUserCRUD.get_admin_user_by_username(db, username)
        if not user or not verify_password(password, user.hashed_password):
            return None

        # Update last_login
        user.last_login = datetime.utcnow()
        db.commit()
        return user

# Comment CRUD
class CommentCRUD:

    @staticmethod
    def create_comment(db: Session, comment: schemas.CommentCreate, ip_address: Optional[str] = None, review_id: int = None) -> models.Comment:
        """Neuen Kommentar erstellen"""
        db_comment = models.Comment(
            review_id=review_id,
            name=comment.name,
            email=comment.email,
            content=comment.content,
            ip_address=ip_address
            # is_approved wird vom Modell-Default (False) gesetzt
        )
        db.add(db_comment)
        db.commit()
        db.refresh(db_comment)
        return db_comment

    @staticmethod
    def get_comment(db: Session, comment_id: int) -> Optional[models.Comment]:
        """Einzelnen Kommentar abrufen"""
        return db.query(models.Comment).filter(models.Comment.id == comment_id).first()

    @staticmethod
    def get_comments_by_review(
        db: Session,
        review_id: int,
        skip: int = 0,
        limit: int = 10,
        approved_only: bool = True
    ) -> tuple[List[models.Comment], int]:
        """Kommentare für eine bestimmte Bewertung abrufen"""
        query = db.query(models.Comment).filter(models.Comment.review_id == review_id)

        if approved_only:
            query = query.filter(models.Comment.is_approved == True)

        total = query.count()
        comments = query.order_by(desc(models.Comment.created_at)).offset(skip).limit(limit).all()
        return comments, total

    @staticmethod
    def get_comments(
        db: Session,
        skip: int = 0,
        limit: int = 10,
        approved_only: bool = True
    ) -> tuple[List[models.Comment], int]:
        """Alle Kommentare abrufen"""
        query = db.query(models.Comment)

        if approved_only:
            query = query.filter(models.Comment.is_approved == True)

        total = query.count()
        comments = query.order_by(desc(models.Comment.created_at)).offset(skip).limit(limit).all()
        return comments, total

    @staticmethod
    def get_pending_comments(
        db: Session,
        skip: int = 0,
        limit: int = 10
    ) -> tuple[List[models.Comment], int]:
        """Pending Kommentare für Admin abrufen"""
        query = db.query(models.Comment).filter(models.Comment.is_approved == False)
        total = query.count()
        comments = query.order_by(desc(models.Comment.created_at)).offset(skip).limit(limit).all()
        return comments, total

    @staticmethod
    def update_comment(db: Session, comment_id: int, comment_update: schemas.CommentUpdate) -> Optional[models.Comment]:
        """Kommentar aktualisieren"""
        db_comment = CommentCRUD.get_comment(db, comment_id)
        if not db_comment:
            return None

        update_data = comment_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_comment, field, value)

        db_comment.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_comment)
        return db_comment

    @staticmethod
    def approve_comment(db: Session, comment_id: int) -> Optional[models.Comment]:
        """Kommentar genehmigen"""
        db_comment = CommentCRUD.get_comment(db, comment_id)
        if not db_comment:
            return None

        db_comment.is_approved = True
        db_comment.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_comment)
        return db_comment

    @staticmethod
    def reject_comment(db: Session, comment_id: int) -> Optional[models.Comment]:
        """Kommentar ablehnen (löschen)"""
        db_comment = CommentCRUD.get_comment(db, comment_id)
        if not db_comment:
            return None

        db.delete(db_comment)
        db.commit()
        return db_comment

    @staticmethod
    def delete_comment(db: Session, comment_id: int) -> bool:
        """Kommentar löschen"""
        db_comment = CommentCRUD.get_comment(db, comment_id)
        if not db_comment:
            return False

        db.delete(db_comment)
        db.commit()
        return True

    @staticmethod
    def count_approved_comments_by_review(db: Session, review_id: int) -> int:
        """Anzahl genehmigter Kommentare für eine Bewertung"""
        return db.query(models.Comment).filter(
            and_(models.Comment.review_id == review_id, models.Comment.is_approved == True)
        ).count()

    @staticmethod
    def get_comments_with_review_info(
        db: Session,
        skip: int = 0,
        limit: int = 10,
        approved_only: bool = True
    ) -> tuple[List[dict], int]:
        """Alle Kommentare mit Review-Informationen abrufen (für Admin)"""
        from sqlalchemy.orm import join

        query = db.query(
            models.Comment.id,
            models.Comment.review_id,
            models.Comment.name,
            models.Comment.email,
            models.Comment.content,
            models.Comment.created_at,
            models.Comment.updated_at,
            models.Comment.is_approved,
            models.Comment.admin_notes,
            models.Comment.ip_address,
            models.Review.name.label('review_author'),
            models.Review.title.label('review_title'),
            models.Review.rating.label('review_rating')
        ).join(models.Review, models.Comment.review_id == models.Review.id)

        if approved_only:
            query = query.filter(models.Comment.is_approved == True)

        total = query.count()
        results = query.order_by(desc(models.Comment.created_at)).offset(skip).limit(limit).all()

        # Konvertiere zu Dictionary-Format
        comments = []
        for result in results:
            comment_dict = {
                'id': result.id,
                'review_id': result.review_id,
                'name': result.name,
                'email': result.email,
                'content': result.content,
                'created_at': result.created_at,
                'updated_at': result.updated_at,
                'is_approved': result.is_approved,
                'admin_notes': result.admin_notes,
                'ip_address': result.ip_address,
                'review_author': result.review_author,
                'review_title': result.review_title,
                'review_rating': result.review_rating
            }
            comments.append(comment_dict)

        return comments, total

    @staticmethod
    def get_pending_comments_with_review_info(
        db: Session,
        skip: int = 0,
        limit: int = 10
    ) -> tuple[List[dict], int]:
        """Pending Kommentare mit Review-Informationen abrufen (für Admin)"""
        from sqlalchemy.orm import join

        query = db.query(
            models.Comment.id,
            models.Comment.review_id,
            models.Comment.name,
            models.Comment.email,
            models.Comment.content,
            models.Comment.created_at,
            models.Comment.updated_at,
            models.Comment.is_approved,
            models.Comment.admin_notes,
            models.Comment.ip_address,
            models.Review.name.label('review_author'),
            models.Review.title.label('review_title'),
            models.Review.rating.label('review_rating')
        ).join(models.Review, models.Comment.review_id == models.Review.id).filter(
            models.Comment.is_approved == False
        )

        total = query.count()
        results = query.order_by(desc(models.Comment.created_at)).offset(skip).limit(limit).all()

        # Konvertiere zu Dictionary-Format
        comments = []
        for result in results:
            comment_dict = {
                'id': result.id,
                'review_id': result.review_id,
                'name': result.name,
                'email': result.email,
                'content': result.content,
                'created_at': result.created_at,
                'updated_at': result.updated_at,
                'is_approved': result.is_approved,
                'admin_notes': result.admin_notes,
                'ip_address': result.ip_address,
                'review_author': result.review_author,
                'review_title': result.review_title,
                'review_rating': result.review_rating
            }
            comments.append(comment_dict)

        return comments, total

# Instanzen für Import
review_crud = ReviewCRUD()
admin_user_crud = AdminUserCRUD()
comment_crud = CommentCRUD()
