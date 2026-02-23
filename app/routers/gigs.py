from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, enums 
from typing import Optional

router = APIRouter(prefix="/gigs", tags=["Gigs"])

@router.get("/", response_model=list[schemas.GigResponse])
def get_all_gigs(db: Session = Depends(get_db)):
    db_gigs = db.query(models.Gig).all()
    if not db_gigs:
        raise HTTPException(status_code=404, detail="No gigs found")  
    return db_gigs

@router.get("/{gig_id}", response_model=schemas.GigResponse)
def get_gig(gig_id: int, db: Session = Depends(get_db)):
    db_gig = db.query(models.Gig).filter(models.Gig.id == gig_id).first()
    if not db_gig:
        raise HTTPException(status_code=404, detail="Gig not found")
    return db_gig   
    
@router.post("/", response_model=schemas.GigResponse)
def create_gig(gig: schemas.GigCreate, db: Session = Depends(get_db)):
    if (db.query(models.Client).filter(models.Client.id == gig.client_id).first() is None):
        raise HTTPException(status_code=400, detail="Client with the given id does not exist")

    if (gig.wage <= 0 or gig.wage is None):
        raise HTTPException(status_code=400, detail="Wage must be greater than 0")
        
    db_gig = models.Gig(**gig.dict())
    db.add(db_gig)
    db.commit()
    db.refresh(db_gig)
    return db_gig
    if db_gig is None:
        raise HTTPException(status_code=400, detail="Gig could not be created") 

#soft delete gig by setting its status to 'cancelled' and associated invoice to 'void'
@router.patch("/{gig_id}", response_model=schemas.GigResponse)
def deactivate_gig(gig_id: int, db: Session = Depends(get_db)):
    db_gig = db.query(models.Gig).filter(models.Gig.id == gig_id).first()
    if not db_gig:
        raise HTTPException(status_code=404, detail="Gig not found")

    db_gig.status = enums.GigStatus.cancelled
    
    db_invoice = db.query(models.Invoice).filter(models.Invoice.gig_id == gig_id).first()

    if db_invoice:
        db_invoice.status = enums.InvoiceStatus.void
    
    db.commit()
    db.refresh(db_gig)
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
    db.refresh(db_gig)
    return db_gig