C-BoT

C-BoT is an AI-powered cognitive behavioral therapy (CBT) chatbot designed to support users through mood tracking, therapeutic exercises, and conversation. Built using Streamlit, it offers an intuitive interface and connects to external APIs and databases for a seamless experience.

Live App: cbot-app.streamlit.app


---

Features

Mood classification and tracking

CBT-based chatbot interactions

Telegram integration for messaging

Secure handling of credentials via Streamlit secrets

Uses Cohere models for text classification and generation



---

Getting Started

1. Clone the repository

git clone https://github.com/Youmna-Hammoud/cbot.git
cd cbot

2. Install dependencies

Make sure Python 3.8+ is installed. Then run:

pip install -r requirements.txt

3. Set up secrets

Create a file at .streamlit/secrets.toml with the following structure:

COHERE_API_KEY = "your_cohere_api_key"
MONGO_URI = "your_mongodb_connection_uri"
TOKEN = "your_telegram_bot_token"

EMERGENCY1 = "emergency_model_id"
MOOD1 = "mood_classification_model_id"



> Note: These secrets are securely read by Streamlit and not exposed in the frontend.



4. Run the app

Launch the app locally using Streamlit:

streamlit run app.py


---

Deployment

The app is live and accessible at:
https://cbot-app.streamlit.app


---