from app.database import Base, engine
import app.models  # ensure models are imported and registered

def reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    reset_db()
    print("DB reset complete.")