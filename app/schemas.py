from pydantic import BaseModel, Field
from datetime import date, timedelta
from enum import Enum
from typing import Optional
from .enums import ClientStatus, GigStatus, InvoiceStatus
from datetime import date, timedelta

#create Pydantic schemas, what got sent and received via API
class ClientCreate(BaseModel):
    name: str
    email: str
    phone: Optional[str]
    business_id: Optional[str]
    note: Optional[str]

class ClientUpdate(BaseModel):
    name: Optional[str]=None
    email: Optional[str]=None
    status: Optional[ClientStatus]=None
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
    status: Optional[GigStatus]=None

class GigResponse(GigCreate):
    id: int
    client_id: Optional[int] = None
    title: str
    wage: float
    location: Optional[str]
    description: Optional[str]
    status: GigStatus
    class Config:
        from_attributes = True   

class InvoiceBase(BaseModel):
    client_id: int
    gig_id: int
    issue_date: date
    due_date: date
    status: InvoiceStatus

class InvoiceCreate(InvoiceBase):
    issue_date: date = Field(default_factory= date.today)
    due_date: date = Field(default_factory=lambda: date.today() + timedelta(days=15))

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