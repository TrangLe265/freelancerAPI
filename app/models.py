from sqlalchemy import Column, Integer, String, Float, Date, Enum, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from .database import Base
from .enums import ClientStatus, GigStatus, InvoiceStatus

#database models
class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    status= Column(Enum(ClientStatus), default=ClientStatus.active)
    phone = Column(String(20))
    business_id = Column(String(50))
    note = Column(String(500))

    gigs = relationship("Gig", back_populates="client")
    invoices = relationship("Invoice", back_populates="client")

class Gig(Base):
    __tablename__ = "gigs"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    client_id = Column(Integer, ForeignKey("clients.id"))
    title = Column(String(200))
    wage = Column(Numeric(10, 2), nullable=False)
    location = Column(String(100))
    date= Column(Date, nullable=False)
    description = Column(String(500))
    status = Column(Enum(GigStatus), default=GigStatus.pending)

    client = relationship("Client", back_populates="gigs")
    invoice = relationship("Invoice", back_populates="gig", uselist=False)

class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    gig_id = Column(Integer, ForeignKey("gigs.id"), nullable=False)
    issue_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False)
    status = Column(Enum(InvoiceStatus), default=InvoiceStatus.draft)
    
    client = relationship("Client", back_populates="invoices")
    gig = relationship("Gig", back_populates="invoice")

    @property
    def total_amount(self):
        return self.gig.wage 