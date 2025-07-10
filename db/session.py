from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Base

engine = create_engine("sqlite:///memory.db")
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
