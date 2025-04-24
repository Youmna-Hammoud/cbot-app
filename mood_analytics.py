from pymongo import MongoClient
from datetime import datetime, timedelta
from collections import Counter
import streamlit as st
import cohere

COHERE_API_KEY = st.secrets["COHERE_API_KEY"]
MOOD1 = st.secrets["MOOD1"]

co = cohere.ClientV2(api_key=COHERE_API_KEY)

MONGO_URI = st.secrets["MONGO_URI"]

client = MongoClient(MONGO_URI)
authdb = client.get_database("cbotauth")
users = authdb.get_collection("users")
mood_logs = authdb.get_collection("mood_logs")
mood_summary = authdb.get_collection("mood_summary")

# Mood classification labels to numeric scores
mood_scores = {
    "sad": -2,
    "angry": -2,
    "anxious": -1,
    "happy": 2,
    "neutral": 0
}

def convert_mood(mood):
    if 1<=mood<=2:
        return -2
    elif 3<=mood<=4:
        return -1
    elif mood == 5:
        return 0
    elif mood > 5:
        return 2

def mood_detector(input, current_user):
    response = co.classify(
        model = MOOD1,
        inputs=input
    )
    prediction = response.classifications[0].prediction
    save_user_mood(prediction, current_user)

def save_user_mood_score(mood_score, current_user):
    mood_logs.insert_one({
        "user_id": current_user["_id"],
        "mood": next(key for key, value in mood_scores.items() if value == mood_score),
        "timestamp": datetime.utcnow()
    })

def save_user_mood(mood, current_user):
    mood_logs.insert_one({
        "user_id": current_user["_id"],
        "mood": mood,
        "timestamp": datetime.utcnow()
    })

def get_user_mood_logs(user_id, days=7):
    now = datetime.utcnow()
    start_date = now - timedelta(days=days)
    logs = list(mood_logs.find({"user_id": user_id, "timestamp": {"$gte": start_date}}))
    return logs


def calculate_mood_distribution(logs):
    """
    Count the occurrence of each mood in the user's logs and return a distribution (count).
    """
    mood_count = Counter()
    total_score = 0
    for log in logs:
        mood = log["mood"]
        if mood in mood_scores:
            mood_count[mood] += 1
            total_score += mood_scores[mood]
    
    # Calculate average mood score
    avg_mood_score = total_score / len(logs) if logs else 0
    return mood_count, avg_mood_score


def calculate_improvement(user_id, current_avg_score):
    """
    Compare current average mood score with previous week's data and calculate the improvement.
    """
    prev = mood_summary.find_one({"user_id": user_id})
    prev_avg_score = prev["avg_mood_score"] if prev else 0

    # Improvement is calculated based on the difference in average scores
    improvement = current_avg_score - prev_avg_score
    improvement_percent = ((improvement /abs(prev_avg_score)) * 100 ) if prev_avg_score != 0 else improvement

    return improvement_percent


def update_mood_summary(user_id, mood_distribution, avg_mood_score, improvement_percent):
    """
    Update or insert the user's mood summary in the mood_summary collection.
    """
    mood_summary.update_one(
        {"user_id": user_id},
        {"$set": {
            "mood_distribution": dict(mood_distribution),
            "avg_mood_score": round(avg_mood_score, 2),
            "mood_improvement_percent": round(improvement_percent, 2),
            "last_checked": datetime.utcnow()
        }},
        upsert=True
    )


def calculate_user_mood_summary(user_id, days=7):
    """
    Main function to calculate and update mood summary for a user.
    """
    logs = get_user_mood_logs(user_id, days)
    
    if not logs:
        raise ValueError("No logs yet, start chatting with the bot first!")
    
    # Calculate mood distribution and average mood score
    mood_distribution, avg_mood_score = calculate_mood_distribution(logs)
    
    # Calculate mood improvement percentage
    improvement_percent = calculate_improvement(user_id, avg_mood_score)
    
    # Update the mood summary in the database
    update_mood_summary(user_id, mood_distribution, avg_mood_score, improvement_percent)
    
    return avg_mood_score, improvement_percent

