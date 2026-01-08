from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas  

router = APIRouter(prefix="/gigs", tags=["Gigs"])

@router.get("/", response_model=list[schemas.GigResponse])
def get_all_gigs(db: Session = Depends(get_db)):
    db_gigs = db.query(models.Gig).all()
    return db_gigs
    if db_gigs is None:
        raise HTTPException(status_code=404, detail="No gigs found")    

@router.post("/", response_model=schemas.GigResponse)
def create_gig(gig: schemas.GigCreate, db: Session = Depends(get_db)):
    db_gig = models.Gig(**gig.dict())
    db.add(db_gig)
    db.commit()
    db.refresh(db_gig)
    return db_gig
    if db_gig is None:
        raise HTTPException(status_code=400, detail="Gig could not be created") 

@router.get("/{gig_id}", response_model=schemas.GigResponse)
def get_gig(gig_id: int, db: Session = Depends(get_db)):
    db_gig = db.query(models.Gig).filter(models.Gig.id == gig_id).first()
    if not db_gig:
        raise HTTPException(status_code=404, detail="Gig not found")
    return db_gig   

@router.delete("/{gig_id}", response_model=schemas.GigResponse)
def delete_gig(gig_id: int, db: Session = Depends(get_db)):
    db_gig = db.query(models.Gig).filter(models.Gig.id == gig_id).first()
    if not db_gig:
        raise HTTPException(status_code=404, detail="Gig not found")
    db.delete(db_gig)
    db.commit()
    return db_gig

@router.put("/{gig_id}", response_model=schemas.GigResponse)
def update_gig(
    gig_id: int, 
    gig: schemas.GigUpdate, 
    db: Session = Depends(get_db)
    ):
    db_gig = db.query(models.Gig).filter(models.Gig.id == gig_id).first()
    if not db_gig:
        raise HTTPException(status_code=404, detail="Gig with the given id not found")
    for key, value in gig.dict(exclude_unset=True).items():
        setattr(db_gig, key, value)
    db.commit()

    if db_gig.gig_status == 'cancelled':
        if db_gig.invoice:
            db.delete(db_gig.invoice)
            db.commit()
    db.refresh(db_gig)
    return db_gig