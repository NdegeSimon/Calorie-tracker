from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime

Base = declarative_base()
engine = create_engine('sqlite:///ecotracker.db')
SessionLocal = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    activities = relationship("Activity", back_populates="user", cascade="all, delete-orphan")
    
    
class Activity(Base):
    __tablename__ = 'activities'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    activity_type = Column(String(50), nullable=False)
    quantity = Column(Float, nullable=False)
    emission = Column(Float, nullable=False)
    activity_date = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="activities")
    
class Goal(Base):
    __tablename__ = 'goals'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    description = Column(String(100), nullable=False)
    target_emission = Column(Float, nullable=False)
    deadline = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="goals")

User.goals = relationship("Goal", back_populates="user", cascade="all, delete-orphan")



Base.metadata.create_all(engine)



