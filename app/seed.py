from datetime import date, timedelta
from app.database import SessionLocal, engine
from app import models
from app.enums import ClientStatus, GigStatus, InvoiceStatus

def seed():
    db = SessionLocal()

    # --- Clients ---
    clients = [
        models.Client(
            name="Nordic Web Studio",
            email="contact@nordicweb.fi",
            phone="+358401234567",
            business_id="FI12345678",
            note="Long-term client, monthly contracts",
            status=ClientStatus.active
        ),
        models.Client(
            name="Helsinki Fitness Club",
            email="admin@helsinkifit.fi",
            phone="+358409876543",
            business_id="FI87654321",
            note="Event-based gigs",
            status=ClientStatus.active
        ),
        models.Client(
            name="Solo Startup Oy",
            email="founder@solostartup.io",
            note="Early-stage startup",
            status=ClientStatus.inactive
        )
    ]

    db.add_all(clients)
    db.commit()

    # --- Gigs ---
    gigs = [
        models.Gig(
            client_id=clients[0].id,
            title="Company Website Redesign",
            wage=4500.00,
            location="Remote",
            date=date.today() - timedelta(days=30),
            description="Full redesign using React and Tailwind",
            status=GigStatus.completed
        ),
        models.Gig(
            client_id=clients[0].id,
            title="Landing Page SEO Optimization",
            wage=1200.00,
            location="Remote",
            date=date.today() - timedelta(days=20),
            description="SEO and performance improvements",
            status=GigStatus.completed
        ),
        models.Gig(
            client_id=clients[1].id,
            title="Hyrox Event Media Coverage",
            wage=1800.00,
            location="Helsinki",
            date=date.today() - timedelta(days=30),
            description="Photography and video editing",
            status=GigStatus.pending
        )
    ]

    db.add_all(gigs)
    db.commit()

    # --- Invoices ---
    invoices = [
        models.Invoice(
            client_id=clients[0].id,
            gig_id=gigs[0].id,
            issue_date=date.today() - timedelta(days=10),
            due_date=date.today() + timedelta(days=5),
            status=InvoiceStatus.sent
        ),
        models.Invoice(
            client_id=clients[0].id,
            gig_id=gigs[1].id,
            issue_date=date.today() - timedelta(days=20),
            due_date=date.today() - timedelta(days=5),
            status=InvoiceStatus.paid
        ),
        models.Invoice(
            client_id=clients[1].id,
            gig_id=gigs[2].id,
            issue_date=date.today(),
            due_date=date.today() + timedelta(days=15),
            status=InvoiceStatus.draft
        )
    ]

    db.add_all(invoices)
    db.commit()
    db.close()

if __name__ == "__main__":
    seed()
