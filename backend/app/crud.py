from sqlalchemy.orm import Session
from . import models, schemas

def create_entry(db: Session, entry: schemas.EntryCreate):
    db_entry = models.Entry(**entry.dict())
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

def get_visible_entries(db: Session):
    return db.query(models.Entry).filter(models.Entry.visible == True).order_by(models.Entry.created_at.desc()).all()

def set_entry_visibility(db: Session, entry_id: int, visible: bool):
    entry = db.query(models.Entry).filter(models.Entry.id == entry_id).first()
    if entry:
        entry.visible = visible
        db.commit()
    return entry

def delete_entry(db: Session, entry_id: int):
    entry = db.query(models.Entry).filter(models.Entry.id == entry_id).first()
    if entry:
        db.delete(entry)
        db.commit()
    return entry
