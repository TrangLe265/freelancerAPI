from pydantic import BaseModel, EmailStr
from datetime import date
from enum import Enum
from typing import Optional
from .models import InvoiceStatus

class ClientCreate(BaseModel):
    name: str
    email: str
    phone: Optional[str]
    business_id: Optional[str]
    note: Optional[str]

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

class GigResponse(GigCreate):
    title: str
    wage: float
    location: Optional[str]
    description: Optional[str]
    class Config:
        from_attributes = True      

class InvoiceCreate(BaseModel):
    client_id: int
    issue_date: date
    due_date: date
    status: InvoiceStatus

class InvoiceResponse(InvoiceCreate):
    id: int
    issue_date: date
    due_date: date
    status: InvoiceStatus
    total_amount: float
    class Config:
        from_attributes = True