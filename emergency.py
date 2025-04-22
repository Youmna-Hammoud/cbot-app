import cohere
from telegram_bot import send_emergency, emergency_contacts
import streamlit as st

COHERE_API_KEY = st.secrets["COHERE_API_KEY"]
EMERGENCY1 = st.secrets["EMERGENCY1"]

co = cohere.ClientV2(api_key=COHERE_API_KEY)

def detector(input, current_user):
    response = co.classify(
        model=EMERGENCY1,
        inputs=input
    )
    prediction = response.classifications[0].prediction
    if prediction == "emergency":
        handle_emergency(current_user, input)

def handle_emergency(current_user, user_message):
    send_emergency(emergency_contacts(current_user), current_user, user_message)