from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas  

router = APIRouter(prefix="/invoices", tags=["Invoices"])