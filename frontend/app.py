import streamlit as st
import requests
import pandas as pd
import altair as alt

# Backend API URL
API_BASE_URL = "http://127.0.0.1:8000"  # Replace with your backend URL if deployed

# Helper functions to interact with the backend
def fetch_reviews(location=None, q=None):
    params = {}
    if location:
        params["location"] = location
    if q:
        params["q"] = q
    response = requests.get(f"{API_BASE_URL}/reviews", params=params)
    return response.json()

def fetch_analytics():
    response = requests.get(f"{API_BASE_URL}/analytics")
    return response.json()

def fetch_similar_reviews(query, k=5):
    response = requests.get(f"{API_BASE_URL}/search", params={"q": query, "k": k})
    return response.json()

def suggest_reply(review_id):
    response = requests.post(f"{API_BASE_URL}/reviews/{review_id}/suggest-reply")
    return response.json()

# Streamlit App
st.title("Customer Review Management")

# Sidebar Navigation
menu = st.sidebar.selectbox("Menu", ["Inbox", "Analytics", "Search Similar Reviews"])

# Inbox Page
if menu == "Inbox":
    st.header("Inbox")
    location = st.text_input("Filter by Location")
    query = st.text_input("Search Reviews")
    reviews = fetch_reviews(location=location, q=query)

    if reviews:
        df = pd.DataFrame(reviews)
        st.dataframe(df)

        # Select a review to view details
        selected_review = st.selectbox("Select a Review", reviews, format_func=lambda x: f"ID: {x['id']} - {x['text'][:50]}...")
        if selected_review:
            st.subheader("Review Details")
            st.write(f"**ID:** {selected_review['id']}")
            st.write(f"**Location:** {selected_review['location']}")
            st.write(f"**Rating:** {selected_review['rating']}")
            st.write(f"**Text:** {selected_review['text']}")

            # Suggest a reply
            if st.button("Suggest Reply"):
                reply = suggest_reply(selected_review["id"])
                st.subheader("Suggested Reply")
                st.write(reply["reply"])

# Analytics Page
elif menu == "Analytics":
    st.header("Analytics")
    analytics = fetch_analytics()

    # Sentiment Analysis
    st.subheader("Sentiment Analysis")
    sentiment_data = pd.DataFrame(
        [{"Sentiment": k, "Count": v} for k, v in analytics["sentiment"].items()]
    )
    chart = alt.Chart(sentiment_data).mark_bar().encode(
        x="Sentiment",
        y="Count",
        color="Sentiment"
    )
    st.altair_chart(chart, use_container_width=True)

    # Topic Analysis
    st.subheader("Topic Analysis")
    topic_data = pd.DataFrame(
        [{"Topic": k, "Count": v} for k, v in analytics["topics"].items()]
    )
    chart = alt.Chart(topic_data).mark_bar().encode(
        x="Topic",
        y="Count",
        color="Topic"
    )
    st.altair_chart(chart, use_container_width=True)

# Search Similar Reviews Page
elif menu == "Search Similar Reviews":
    st.header("Search Similar Reviews")
    query = st.text_input("Enter a Query")
    k = st.slider("Number of Similar Reviews", 1, 10, 5)

    if st.button("Search"):
        similar_reviews = fetch_similar_reviews(query, k)
        st.subheader("Results")
        for review in similar_reviews["results"]:
            st.write(f"**ID:** {review['id']}")
            st.write(f"**Text:** {review['text']}")
            st.write(f"**Similarity:** {review['similarity']:.2f}")
            st.write("---")