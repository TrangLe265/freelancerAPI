from fastapi import FastAPI
from .database import engine
from .models import Base
from .routers import clients

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Freelancer API", version="1.0.0")

app.include_router(clients.router)  