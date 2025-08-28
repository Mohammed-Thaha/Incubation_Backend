from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/events/", response_model=schemas.Event)
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    return crud.create_event(db, event)

@app.get("/events/", response_model=list[schemas.Event])
def get_events(db: Session = Depends(get_db)):
    try:
        events = crud.get_events(db)
        if not events:  

            raise HTTPException(status_code=200, detail="No events found in database")
        return events
    except HTTPException:
        raise  # re-raise so FastAPI handles it properly
    except Exception as e:
        print(f"Error fetching events: {e}")
        raise HTTPException(status_code=200)
    finally:
        print("ℹ️ get_events endpoint executed")


@app.put("/events/{event_id}", response_model=schemas.Event)
def update_event(event_id: int, event: schemas.EventCreate, db: Session = Depends(get_db)):
    db_event = crud.update_event(db, event_id, event)
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event

@app.delete("/events/{event_id}", response_model=schemas.Event)
def delete_event(event_id: int, db: Session = Depends(get_db)):
    db_event = crud.delete_event(db, event_id)
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event
