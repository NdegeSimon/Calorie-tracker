from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Activity(Base):
    __tablename__ = "activities"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    activity_type = Column(String)
    quantity = Column(Float)
    emission = Column(Float)
    activity_date = Column(DateTime, default=datetime.utcnow)

class Goal(Base):
    __tablename__ = "goals"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    description = Column(String)
    target_emission = Column(Float)
    deadline = Column(DateTime)

engine = create_engine("sqlite:///ecotracker.db")
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)