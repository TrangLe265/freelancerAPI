import enum

class ClientStatus(str, enum.Enum):
    active = "active"
    inactive = "inactive"
    archived = "archived"

class InvoiceStatus(str, enum.Enum):
    draft = "draft"
    created = "created"
    sent = "sent"
    paid = "paid"
    void = "void"

class GigStatus(str, enum.Enum):
    pending = "pending"
    completed = "completed"
    cancelled = "cancelled"
