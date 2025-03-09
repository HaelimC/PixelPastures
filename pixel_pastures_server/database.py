from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

DATABASE_URL = "postgresql://admin:admin@localhost:5432/pixel_pastures"

# PostgreSQL Connection Setting
engine = create_engine(DATABASE_URL)
# DB Session creation
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# create DB Table from model.py
def init_db():
    Base.metadata.create_all(bind=engine)