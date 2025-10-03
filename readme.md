ReviewSphere
============

ReviewSphere is an AI-powered review management platform designed to help businesses analyze customer feedback, generate AI-suggested replies, and gain actionable insights. With features like sentiment analysis, topic tagging, and similar review recommendations, ReviewSphere makes it easy to manage and respond to customer reviews.

---

Features
--------

1. Inbox:
   - View all customer reviews in a table format.
   - Filter reviews by location or search by keywords.
   - View detailed information about each review.
   - Generate AI-suggested replies for reviews.

2. Analytics:
   - Visualize sentiment analysis (positive, neutral, negative) as bar charts.
   - Analyze topics (e.g., service, cleanliness, price) based on review content.

3. Search Similar Reviews:
   - Use TF-IDF and cosine similarity to find reviews similar to a given query.
   - Display the top-k most similar reviews with similarity scores.

---

Tech Stack
----------

Backend:
- FastAPI: For building RESTful APIs.
- SQLite: For storing reviews.
- OpenAI API: For generating AI-suggested replies.
- Scikit-learn: For implementing TF-IDF and cosine similarity.

Frontend:
- Streamlit: For building an interactive and user-friendly interface.
- Altair: For creating analytics visualizations.

---

Project Structure
-----------------

ReviewSphere/
├── backend/
│   ├── main.py          # FastAPI entry point
│   ├── crud.py          # Database operations
│   ├── models.py        # Database models
│   ├── database.py      # Database connection
│   ├── schemas.py       # Pydantic schemas
│   ├── requirements.txt # Backend dependencies
├── app.py               # Streamlit frontend
├── requirements.txt     # Frontend dependencies

---

Installation
------------

1. Clone the Repository:
   git clone https://github.com/your-username/ReviewSphere.git
   cd ReviewSphere

2. Set Up the Backend:
   - Navigate to the `backend` directory:
     cd backend
   - Create a virtual environment and activate it:
     python -m venv venv
     source venv/bin/activate  # On Windows: venv\Scripts\activate
   - Install dependencies:
     pip install -r requirements.txt
   - Run the backend:
     uvicorn main:app --reload

3. Set Up the Frontend:
   - Navigate back to the root directory:
     cd ..
   - Install frontend dependencies:
     pip install -r requirements.txt
   - Run the Streamlit app:
     streamlit run app.py

---

Deployment
----------

Backend Deployment:
- Deploy the backend on Render or Railway.
- Use the following commands for deployment:
  Build Command: pip install -r requirements.txt
  Start Command: uvicorn main:app --host 0.0.0.0 --port 8000

Frontend Deployment:
- Deploy the frontend on Render or Streamlit Community Cloud.
- Use the following commands for deployment:
  Build Command: pip install -r requirements.txt
  Start Command: streamlit run app.py --server.port 8501 --server.address 0.0.0.0

---

API Endpoints
-------------

1. Ingest Reviews:
   - Endpoint: POST /ingest
   - Description: Add a list of reviews to the database.
   - Request Body:
     [
       {
         "location": "NYC",
         "rating": 5,
         "text": "Amazing service!",
         "date": "2025-10-01"
       }
     ]

2. Get Reviews:
   - Endpoint: GET /reviews
   - Description: Retrieve reviews with optional filters and pagination.
   - Query Parameters:
     - location: Filter by location.
     - q: Search by text.
     - skip: Number of records to skip.
     - limit: Number of records to return.

3. Analytics:
   - Endpoint: GET /analytics
   - Description: Get sentiment and topic analytics.

4. Search Similar Reviews:
   - Endpoint: GET /search
   - Description: Find similar reviews using TF-IDF and cosine similarity.
   - Query Parameters:
     - q: Query string.
     - k: Number of similar reviews to return.

5. Suggest Reply:
   - Endpoint: POST /reviews/{id}/suggest-reply
   - Description: Generate an AI-suggested reply for a review.

---

Future Enhancements
-------------------
- Add user authentication for secure access.
- Support for multiple languages in reviews.
- Advanced analytics with time-series visualizations.
- Deploy as a single Dockerized application.


---

Acknowledgments
---------------
- FastAPI: https://fastapi.tiangolo.com/
- Streamlit: https://streamlit.io/
- OpenAI: https://openai.com/
- Render: https://render.com/