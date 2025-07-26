from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Entry(Base):
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    stars = Column(Integer, nullable=False)  # 1 bis 5
    comment = Column(String(5000), nullable=False)
    image_url = Column(String(255), nullable=True)
    visible = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
