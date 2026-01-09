from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/clients", tags=["Clients"])

#Respone Models hide sensitive info like business_id and note
@router.get("/", response_model=list[schemas.ClientResponse])
def get_all_clients(db: Session = Depends(get_db)): #db is a session depends on get_db from database.py
    db_clients = db.query(models.Client).all()
    if db_clients is None:
        raise HTTPException(status_code=404, detail="No clients found")
    return db_clients

@router.get("/{client_id}", response_model=schemas.ClientResponse)
def get_client(client_id: int, db: Session = Depends(get_db)):
    db_client = db.query(models.Client).filter(models.Client.id == client_id).first()
    if not db_client:
        raise HTTPException(status_code=404, detail="Client not found")
    return db_client

@router.post("/", response_model=schemas.ClientResponse)
def create_client(client: schemas.ClientCreate, db: Session = Depends(get_db)):
    #check if email already exists
    if db.query(models.Client).filter(models.Client.email == client.email).first():
        raise HTTPException(status_code=400, detail="Client with this email already exists")
    #create new client
    db_client = models.Client(**client.dict())
    db.add(db_client)
    #always commit when making changes to the db
    db.commit()
    db.refresh(db_client)
    return db_client
    if db_client is None:
        raise HTTPException(status_code=400, detail="Client could not be created")

@router.delete("/{client_id}", response_model=schemas.ClientResponse)
def delete_client(client_id: int, db: Session = Depends(get_db)):
    db_client = db.query(models.Client).filter(models.Client.id == client_id).first()
    if not db_client:
        raise HTTPException(status_code=404, detail="Client not found")
    db.delete(db_client)
    db.commit()
    return db_client
