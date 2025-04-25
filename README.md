# C-BoT

**C-BoT** is an AI-powered cognitive behavioral therapy (CBT) chatbot designed to support users through mood tracking, therapeutic exercises, and guided conversations. Built with Streamlit, it integrates with Cohere, MongoDB, and Telegram for a seamless experience.

**Live App:** [https://cbot-app.streamlit.app](https://cbot-app.streamlit.app)

---

## Features

- Mood classification and tracking  
- Structured CBT-style chatbot conversations  
- Telegram integration  
- Cohere-powered NLP (generation + classification)  
- Secure credential handling via Streamlit secrets

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Youmna-Hammoud/cbot.git
cd cbot
```

### 2. Install dependencies

Make sure you have Python 3.8 or higher installed.

```bash
pip install -r requirements.txt
```

### 3. Configure secrets

Create a file at .streamlit/secrets.toml with the following content:

```bash
COHERE_API_KEY = "your_cohere_api_key"
MONGO_URI = "your_mongodb_connection_uri"
TOKEN = "your_telegram_bot_token"

EMERGENCY1 = "emergency_model_id"
MOOD1 = "mood_classification_model_id"
```


> These secrets are securely accessed by Streamlit during runtime.



### 4. Run the app

```bash
streamlit run app.py
```


---

## Deployment

The app is live at:
https://cbot-app.streamlit.app


