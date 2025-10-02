from sqlalchemy import Column, Integer, String, Date
from database import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    location = Column(String, index=True)
    rating = Column(Integer)
    text = Column(String)
    date = Column(Date)