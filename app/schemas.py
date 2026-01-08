from pydantic import BaseModel, EmailStr
from datetime import date
from enum import Enum
from typing import Optional
from .models import InvoiceStatus, GigStatus

class ClientCreate(BaseModel):
    name: str
    email: str
    phone: Optional[str]
    business_id: Optional[str]
    note: Optional[str]

class ClientUpdate(BaseModel):
    name: Optional[str]=None
    email: Optional[EmailStr]=None
    phone: Optional[str]=None
    business_id: Optional[str]=None
    note: Optional[str]=None
    
class ClientResponse(ClientCreate):
    id: int
    name: str
    email: str
    phone: Optional[str]
    business_id: Optional[str]
    note: Optional[str]
    class Config:
        from_attributes = True


class GigCreate(BaseModel):
    client_id: int
    title: str
    wage: float
    location: Optional[str]
    description: Optional[str]

class GigUpdate(BaseModel):
    title: Optional[str]=None
    wage: Optional[float]=None
    location: Optional[str] =None
    description: Optional[str]=None
    gig_status: Optional[GigStatus]=None

class GigResponse(GigCreate):
    client_id: int
    title: str
    wage: float
    location: Optional[str]
    description: Optional[str]
    gig_status: GigStatus
    class Config:
        from_attributes = True   

class InvoiceCreate(BaseModel):
    client_id: int
    gig_id: int
    issue_date: date
    due_date: date
    status: InvoiceStatus

class InvoiceUpdate(BaseModel):
    issue_date: Optional[date]=None
    due_date: Optional[date]=None
    status: Optional[InvoiceStatus]=None

class InvoiceResponse(InvoiceCreate):
    id: int
    issue_date: date
    due_date: date
    status: InvoiceStatus
    total_amount: float
    class Config:
        from_attributes = True