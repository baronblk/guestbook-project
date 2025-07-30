from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional, List, Union
from datetime import datetime
from enum import IntEnum

class RatingEnum(IntEnum):
    """Bewertungs-Sterne (1-5)"""
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5

# Review Schemas
class ReviewBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Name des Bewerters")
    email: Optional[EmailStr] = Field(None, description="Optional: E-Mail für Benachrichtigungen")
    rating: RatingEnum = Field(..., description="Bewertung von 1-5 Sternen")
    title: Optional[str] = Field(None, max_length=200, description="Optionaler Titel")
    content: str = Field(..., min_length=10, max_length=5000, description="Bewertungstext")

    @validator('content')
    def validate_content(cls, v):
        if len(v.strip()) < 10:
            raise ValueError('Bewertungstext muss mindestens 10 Zeichen haben')
        return v.strip()

class ReviewCreate(ReviewBase):
    """Schema für neue Bewertung"""
    pass

class ReviewUpdate(BaseModel):
    """Schema für Bewertung-Updates (Admin)"""
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    rating: Optional[RatingEnum] = None
    title: Optional[str] = Field(None, max_length=200)
    content: Optional[str] = Field(None, min_length=10, max_length=5000)
    image_path: Optional[str] = None
    created_at: Optional[datetime] = None
    is_approved: Optional[bool] = None
    is_featured: Optional[bool] = None
    admin_notes: Optional[str] = None

class ReviewResponse(ReviewBase):
    """Schema für Bewertung-Response"""
    id: int
    image_path: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    is_approved: bool
    is_featured: bool
    comment_count: Optional[int] = 0  # Anzahl genehmigter Kommentare

    class Config:
        from_attributes = True

class ReviewAdminResponse(ReviewResponse):
    """Erweiterte Response für Admin"""
    admin_notes: Optional[str]
    import_source: Optional[str]
    external_id: Optional[str]
    ip_address: Optional[str]

# Pagination
class ReviewListResponse(BaseModel):
    """Paginierte Liste von Bewertungen"""
    reviews: List[ReviewResponse]
    total: int
    page: int
    per_page: int
    total_pages: int

# Comment Schemas
class CommentBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Name des Kommentators")
    email: Optional[EmailStr] = Field(None, description="Optional: E-Mail für Benachrichtigungen")
    content: str = Field(..., min_length=5, max_length=2000, description="Kommentartext")

    @validator('content')
    def validate_content(cls, v):
        if len(v.strip()) < 5:
            raise ValueError('Kommentar muss mindestens 5 Zeichen haben')
        return v.strip()

class CommentCreate(CommentBase):
    """Schema für neuen Kommentar"""
    pass

class CommentUpdate(BaseModel):
    """Schema für Kommentar-Updates (Admin)"""
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    content: Optional[str] = Field(None, min_length=5, max_length=2000)
    is_approved: Optional[bool] = None
    admin_notes: Optional[str] = None

class CommentResponse(CommentBase):
    """Schema für Kommentar-Response"""
    id: int
    review_id: int
    created_at: datetime
    updated_at: Optional[datetime]
    is_approved: bool

    class Config:
        from_attributes = True

class CommentAdminResponse(CommentResponse):
    """Erweiterte Response für Admin"""
    admin_notes: Optional[str]
    ip_address: Optional[str]

class CommentWithReviewInfo(CommentAdminResponse):
    """Kommentar mit zugehörigen Review-Informationen für Admin"""
    review_author: str
    review_title: Optional[str] = None
    review_rating: int

class CommentListResponse(BaseModel):
    """Paginierte Liste von Kommentaren"""
    comments: List[CommentResponse]
    total: int
    page: int
    per_page: int
    total_pages: int

class CommentAdminListResponse(BaseModel):
    """Paginierte Liste von Admin-Kommentaren mit Review-Info"""
    comments: List[CommentWithReviewInfo]
    total: int
    page: int
    per_page: int
    total_pages: int

# Admin Schemas
class AdminUserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr

class AdminUserCreate(AdminUserBase):
    password: str = Field(..., min_length=8)

class AdminUserUpdate(BaseModel):
    """Schema für Admin-Benutzer Updates"""
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8)
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None

class AdminUserResponse(AdminUserBase):
    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime
    last_login: Optional[datetime]

    class Config:
        from_attributes = True

class AdminUserListResponse(BaseModel):
    """Paginierte Liste von Admin-Benutzern"""
    users: List[AdminUserResponse]
    total: int
    page: int
    per_page: int
    total_pages: int

class PasswordChangeRequest(BaseModel):
    """Schema für Passwort-Änderung"""
    old_password: str = Field(..., min_length=1)
    new_password: str = Field(..., min_length=8)

# Auth Schemas
class AdminLogin(BaseModel):
    """Schema für Admin-Login"""
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=1)

class RefreshToken(BaseModel):
    """Schema für Token-Refresh"""
    refresh_token: str

class Token(BaseModel):
    """Schema für Authentication Token"""
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"
    expires_in: Optional[int] = None

class TokenData(BaseModel):
    username: Optional[str] = None
    token_id: Optional[str] = None

# Import Schemas
class ImportReview(BaseModel):
    """Schema für Import von externen Bewertungen"""
    name: str
    rating: int = Field(..., ge=1, le=5)
    content: str
    title: Optional[str] = None
    email: Optional[str] = None
    created_at: Optional[datetime] = None
    import_source: str = "manual"
    external_id: Optional[str] = None

class ImportRequest(BaseModel):
    """Schema für Bulk-Import"""
    reviews: List[ImportReview]
    source: str = "manual"

# Erweiterte Export/Import Schemas für vollständige Datenwiederherstellung
class ExportComment(BaseModel):
    """Schema für Kommentar-Export"""
    id: int
    name: str
    email: Optional[str] = None
    content: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    is_approved: bool
    admin_notes: Optional[str] = None
    ip_address: Optional[str] = None

class ExportReview(BaseModel):
    """Schema für Review-Export mit Kommentaren"""
    id: int
    name: str
    email: Optional[str] = None
    rating: int
    title: Optional[str] = None
    content: str
    image_path: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    is_approved: bool
    is_featured: bool
    admin_notes: Optional[str] = None
    import_source: Optional[str] = None
    external_id: Optional[str] = None
    ip_address: Optional[str] = None
    comments: List[ExportComment] = []

class FullExportData(BaseModel):
    """Schema für vollständigen Datenexport"""
    exported_at: datetime
    export_version: str = "2.0"
    total_reviews: int
    total_comments: int
    reviews: List[ExportReview]

class ImportComment(BaseModel):
    """Schema für Kommentar-Import"""
    name: str
    email: Optional[str] = None
    content: str
    created_at: Optional[datetime] = None
    is_approved: bool = True
    admin_notes: Optional[str] = None

class ImportReviewWithComments(BaseModel):
    """Schema für Review-Import mit Kommentaren"""
    name: str
    email: Optional[str] = None
    rating: int = Field(..., ge=1, le=5)
    title: Optional[str] = None
    content: str
    created_at: Optional[datetime] = None
    is_approved: bool = True
    is_featured: bool = False
    admin_notes: Optional[str] = None
    import_source: str = "restore"
    external_id: Optional[str] = None
    comments: List[ImportComment] = []

class FullImportData(BaseModel):
    """Schema für vollständigen Datenimport - akzeptiert sowohl Export- als auch Import-Format"""
    export_version: Optional[str] = "2.0"
    exported_at: Optional[datetime] = None  # Vom Export-Format
    total_reviews: Optional[int] = None     # Vom Export-Format
    total_comments: Optional[int] = None    # Vom Export-Format
    reviews: List[Union[ExportReview, ImportReviewWithComments]]

# Filter/Sort Schemas
class ReviewFilters(BaseModel):
    """Filter-Parameter für Bewertungen"""
    rating: Optional[int] = Field(None, ge=1, le=5)
    is_featured: Optional[bool] = None
    search: Optional[str] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None

class SortOptions(BaseModel):
    """Sortier-Optionen"""
    sort_by: str = Field("created_at", pattern="^(created_at|rating|name)$")
    sort_order: str = Field("desc", pattern="^(asc|desc)$")
