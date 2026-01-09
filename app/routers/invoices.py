from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas 
from typing import Optional

router = APIRouter(prefix="/invoices", tags=["Invoices"])

@router.get("/", response_model=list[schemas.InvoiceResponse])
def get_invoice( 
        client_id: Optional[int] = Query(None), 
        gig_id: Optional[int] = Query(None),
        status: Optional[schemas.InvoiceStatus] = Query(None),
        db: Session = Depends(get_db)
    ):
    query = db.query(models.Invoice)

    if client_id is not None: 
        query = query.filter(models.Invoice.client_id == client_id) 
    if gig_id is not None: 
        query = query.filter(models.Invoice.gig_id == gig_id) 
    if status is not None:
        query = query.filter(models.Invoice.status == status)
    
    print(str(query.statement.compile(compile_kwargs={"literal_binds": True})))
    results = query.all()
    

    if not results:
        raise HTTPException(status_code=404, detail="No invoices found matching the criteria")
    return results
  
@router.get("/{invoice_id}", response_model=schemas.InvoiceResponse)
def get_invoice(invoice_id, db: Session = Depends(get_db)):
    db_invoice = db.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()
    if not db_invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return db_invoice

@router.post("/", response_model=schemas.InvoiceResponse)
def create_invoice(invoice: schemas.InvoiceCreate, db: Session = Depends(get_db)):
    #check if client_id and gig_id exist
    if db.query(models.Client).filter(models.Client.id == invoice.client_id).first() is None:
        raise HTTPException(status_code=400, detail="Client with the given id does not exist")
    if db.query(models.Gig).filter(models.Gig.id == invoice.gig_id).first() is None:
        raise HTTPException(status_code=400, detail="Gig with the given id does not exist")
    
    #check if gig_id already has an invoice
    if db.query(models.Invoice).filter(models.Invoice.gig_id == invoice.gig_id).first() is not None:
        raise HTTPException(status_code=400, detail="An invoice for the given gig_id already exists")

    #check if gig's sttatus is not 'cancelled'
    db_gig = db.query(models.Gig).filter(models.Gig.id == invoice.gig_id).first()
    if db_gig.status == schemas.GigStatus.cancelled:
        raise HTTPException(status_code=400, detail="Cannot create invoice for a cancelled gig")
        
    #check if the gig belongs to the client
    if db_gig.client_id != invoice.client_id:
        raise HTTPException(status_code=400, detail="The gig does not belong to the specified client")

    new_invoice = models.Invoice(**invoice.dict())
    db.add(new_invoice)
    db.commit()
    db.refresh(new_invoice)
    return new_invoice

@router.put("/{invoice_id}", response_model=schemas.InvoiceResponse)
def update_invoice(invoice_id: int, invoice: schemas.InvoiceUpdate, db: Session = Depends(get_db)):
    db_invoice = db.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()
    if not db_invoice:
        raise HTTPException(status_code=404, detail="Invoice with the given id not found")
    for key, value in invoice.dict(exclude_unset=True).items():
        setattr(db_invoice, key, value)
    db.commit()
    db.refresh(db_invoice)
    return db_invoice