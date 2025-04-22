from pymongo import MongoClient
from datetime import datetime
import streamlit as st

MONGO_URI = st.secrets["MONGO_URI"]

client = MongoClient(MONGO_URI)

authdb = client.get_database("cbotauth")
history = authdb.get_collection("history")

def get_user_messages(user_id):
    messages = []
    for message in list(history.find({'user_id': str(user_id)})):
        messages.append({"role": message["role"], "content": message["content"]})
    return messages

def save_user_message(message, current_user):
    message["user_id"] = current_user["_id"]
    message["timestamp"] = datetime.utcnow()
    history.insert_one(message)




