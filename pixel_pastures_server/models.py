from sqlalchemy import Column, Integer, String, Float, Sequence
from sqlalchemy.ext.declarative import declarative_base

# Basic Model Class for using SQLAlchemy
Base = declarative_base()

class Player(Base):
    # DB Table name
    __tablename__ = "players"
    
    id = Column(Integer, Sequence('player_id_seq'), primary_key=True, index=True)
    player_id = Column(String, unique=True, index=True)

    # Player Location
    x = Column(Float, default=0.0)
    y = Column(Float, default=0.0)
    
    farm_level = Column(Integer, default=1)