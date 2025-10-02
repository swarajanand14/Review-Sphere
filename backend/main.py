from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
import models, schemas, crud
from database import SessionLocal, engine

# Initialize the database
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/ingest", response_model=list[schemas.Review])
def ingest_reviews(reviews: list[schemas.ReviewCreate], db: Session = Depends(get_db)):
    """
    Ingest a list of reviews into the database.
    """
    created_reviews = []
    for review in reviews:
        created_review = crud.create_review(db, review)
        created_reviews.append(created_review)
    return created_reviews

@app.get("/reviews", response_model=list[schemas.Review])
def get_reviews(
    location: Optional[str] = Query(None),
    q: Optional[str] = Query(None),
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Retrieve reviews with optional filters and pagination.
    - `location`: Filter by location.
    - `q`: Search for text in reviews.
    - `skip`: Number of records to skip (for pagination).
    - `limit`: Maximum number of records to return.
    """
    reviews = crud.get_reviews(db, location=location, q=q, skip=skip, limit=limit)
    return reviews

@app.get("/analytics")
def get_analytics(db: Session = Depends(get_db)):
    """
    Get analytics data: counts by sentiment and topic.
    """
    analytics = crud.analyze_reviews(db)
    return analytics

@app.post("/reviews/{id}/suggest-reply")
def suggest_reply(id: int, db: Session = Depends(get_db)):
    """
    Generate a suggested reply for a review using OpenAI API.
    """
    # Fetch the review from the database
    review = db.query(models.Review).filter(models.Review.id == id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    # Generate the reply
    result = crud.generate_reply_with_openai(review.text)
    return result

@app.get("/search")
def search_similar_reviews(q: str, k: int = 5, db: Session = Depends(get_db)):
    """
    Search for similar reviews using TF-IDF and cosine similarity.
    - `q`: The query string to search for.
    - `k`: The number of similar reviews to return.
    """
    similar_reviews = crud.find_similar_reviews(db, query=q, top_k=k)
    return {"query": q, "results": similar_reviews}