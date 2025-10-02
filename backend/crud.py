from sqlalchemy.orm import Session
from sqlalchemy import or_
from collections import Counter
import openai
from openai import OpenAIError
import re
import models
import os
from dotenv import load_dotenv
load_dotenv()
# Load OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def find_similar_reviews(db: Session, query: str, top_k: int = 5):
    """
    Find similar reviews using TF-IDF and cosine similarity.
    """
    # Fetch all reviews from the database
    reviews = db.query(models.Review).all()
    review_texts = [review.text for review in reviews]

    # Add the query to the list of reviews
    all_texts = [query] + review_texts

    # Compute TF-IDF vectors
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(all_texts)

    # Compute cosine similarity between the query and all reviews
    query_vector = tfidf_matrix[0]  # The first vector corresponds to the query
    similarities = cosine_similarity(query_vector, tfidf_matrix[1:]).flatten()

    # Get the indices of the top-k most similar reviews
    top_indices = np.argsort(similarities)[::-1][:top_k]

    # Return the top-k similar reviews
    similar_reviews = [{"id": reviews[i].id, "text": reviews[i].text, "similarity": similarities[i]} for i in top_indices]
    return similar_reviews

def create_review(db: Session, review):
    """
    Create a new review in the database.
    """
    db_review = models.Review(**review.dict())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

def get_reviews(db: Session, location: str = None, q: str = None, skip: int = 0, limit: int = 10):
    """
    Retrieve reviews with optional filters and pagination.
    """
    query = db.query(models.Review)

    # Apply filters
    if location:
        query = query.filter(models.Review.location == location)
    if q:
        query = query.filter(
            or_(
                models.Review.text.ilike(f"%{q}%"),  # Case-insensitive text search
            )
        )

    # Apply pagination
    return query.offset(skip).limit(limit).all()

def analyze_reviews(db: Session):
    """
    Analyze reviews to calculate counts by sentiment and topic.
    """
    reviews = db.query(models.Review).all()

    # Sentiment analysis
    sentiment_counts = {"positive": 0, "neutral": 0, "negative": 0}
    for review in reviews:
        if review.rating >= 4:
            sentiment_counts["positive"] += 1
        elif review.rating == 3:
            sentiment_counts["neutral"] += 1
        else:
            sentiment_counts["negative"] += 1

    # Topic tagging (rule-based)
    topic_keywords = {
        "service": ["service", "staff", "wait"],
        "cleanliness": ["clean", "hygiene"],
        "price": ["price", "cost", "expensive", "cheap"]
    }
    topic_counts = Counter()
    for review in reviews:
        for topic, keywords in topic_keywords.items():
            if any(keyword in review.text.lower() for keyword in keywords):
                topic_counts[topic] += 1

    return {
        "sentiment": sentiment_counts,
        "topics": topic_counts
    }

def redact_sensitive_info(text: str) -> str:
    """
    Redact sensitive information like emails and phone numbers from the text.
    """
    # Redact emails
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[REDACTED EMAIL]', text)
    # Redact phone numbers
    text = re.sub(r'\b\d{10}\b', '[REDACTED PHONE]', text)
    return text
 # Correct import for OpenAIError
def generate_reply_with_openai(review_text: str):
    """
    Generate a reply for the given review text using OpenAI API.
    """
    # Redact sensitive information
    clean_text = redact_sensitive_info(review_text)

    # Call OpenAI API to analyze sentiment and generate a reply
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Use "gpt-3.5-turbo" if you don't have access to GPT-4
            messages=[
                {"role": "system", "content": "You are a helpful assistant that analyzes customer reviews."},
                {"role": "user", "content": f"Analyze the sentiment of this review and summarize it: {clean_text}"}
            ],
            temperature=0.7
        )

        # Extract the reply and sentiment from the response
        reply_content = response["choices"][0]["message"]["content"]
        sentiment = "positive" if "positive" in reply_content.lower() else \
                    "neutral" if "neutral" in reply_content.lower() else "negative"

        # Generate reasoning log
        reasoning_log = {
            "sentiment": sentiment,
            "summary": reply_content
        }

        # Generate a reply
        reply = f"We appreciate your feedback. Based on your review, we understand that: {reply_content}. Please let us know if we can assist further."

        return {
            "reply": reply,
            "tags": {"sentiment": sentiment},
            "reasoning_log": reasoning_log
        }

    except openai.OpenAIError as e:  # Updated error handling
        raise Exception(f"OpenAI API error: {e}")