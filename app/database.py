from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DB_URL = "sqlite:///freelancer.db"

#create an engine to hold the database connection
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})

#create a DB session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()