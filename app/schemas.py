from pydantic import BaseModel, EmailStr
from datetime import date
from enum import Enum

class ClientCreate(BaseModel):
    name: str
    email: str
    phone: str | None = None
    business_id: str | None = None

class ClientResponse(ClientCreate):
    id: int
    name: str
    email: str
    phone: str | None = None
    business_id: str | None = None
    class Config:
        from_attributes = True


class GigCreate(BaseModel):
    client_id: int
    title: str
    wage: float
    location: str | None = None
    description: str | None = None

class GigResponse(GigCreate):
    title: str
    wage: float
    location: str | None = None
    description: str | None = None
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