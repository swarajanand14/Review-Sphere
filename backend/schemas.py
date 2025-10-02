from pydantic import BaseModel
from datetime import date

class ReviewBase(BaseModel):
    location: str
    rating: int
    text: str
    date: date

class ReviewCreate(ReviewBase):
    pass

class Review(ReviewBase):
    id: int

    class Config:
        from_attributes = True  # Updated for Pydantic v2