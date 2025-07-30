from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional, List
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

class CommentListResponse(BaseModel):
    """Paginierte Liste von Kommentaren"""
    comments: List[CommentResponse]
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

class AdminUserResponse(AdminUserBase):
    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime
    last_login: Optional[datetime]
    
    class Config:
        from_attributes = True

# Auth Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

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
