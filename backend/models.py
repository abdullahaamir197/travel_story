from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from database import Base
import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    fullName = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    createdOn = Column(DateTime, default=datetime.datetime.utcnow)

    stories = relationship("TravelStory", back_populates="owner")

class TravelStory(Base):
    __tablename__ = "travel_stories"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    story = Column(Text)
    visitedLocation = Column(JSON)
    visitedDate = Column(DateTime)
    imageUrl = Column(String)
    isFavourite = Column(Boolean, default=False)
    userId = Column(Integer, ForeignKey("users.id"))
    createdOn = Column(DateTime, default=datetime.datetime.utcnow)

    owner = relationship("User", back_populates="stories")
