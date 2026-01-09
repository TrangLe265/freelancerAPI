from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from .models import Base
from .routers import clients, gigs, invoices

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Freelancer API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
app.include_router(clients.router)  
app.include_router(gigs.router)
app.include_router(invoices.router)
