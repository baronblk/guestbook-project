from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, database, schemas, crud

app = FastAPI()

# Datenbank initialisieren
models.Base.metadata.create_all(bind=database.engine)

# Dependency Injection
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/entries", response_model=schemas.EntryOut)
def create_guestbook_entry(entry: schemas.EntryCreate, db: Session = Depends(get_db)):
    return crud.create_entry(db, entry)

@app.get("/entries", response_model=list[schemas.EntryOut])
def list_entries(db: Session = Depends(get_db)):
    return crud.get_visible_entries(db)

@app.put("/entries/{entry_id}/publish", response_model=schemas.EntryOut)
def set_visibility(entry_id: int, visible: bool, db: Session = Depends(get_db)):
    entry = crud.set_entry_visibility(db, entry_id, visible)
    if not entry:
        raise HTTPException(status_code=404, detail="Eintrag nicht gefunden")
    return entry

@app.delete("/entries/{entry_id}")
def delete_entry(entry_id: int, db: Session = Depends(get_db)):
    entry = crud.delete_entry(db, entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Eintrag nicht gefunden")
    return {"detail": "Eintrag gelöscht"}
