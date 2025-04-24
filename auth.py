import hashlib
from pymongo import MongoClient
import streamlit as st
from pymongo.errors import DuplicateKeyError

MONGO_URI = st.secrets["MONGO_URI"]

client = MongoClient(MONGO_URI)
authdb = client.get_database("cbotauth")
users = authdb.get_collection("users")

# Create unique index for email
#users.create_index("email", unique=True)

def hash_password(password):
    """Hashes the password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(password, hashed):
    return hash_password(password) == hashed

def signup(username, email, password1, password2):
    if password1 != password2:
        raise ValueError("Password confirmation declined!")
    if users.find_one({"email": email}):
        raise ValueError("Email already registered.")
    if users.find_one({"username": username}):
        raise ValueError("Username already taken.")

    try:
        users.insert_one({
            "username": username,
            "email": email,
            "password": hash_password(password1)
        })
    except DuplicateKeyError:
        raise ValueError("Duplicate email or username detected.")

def login(email, password):
    user = users.find_one({"email": email})
    if user:
        if check_password(password, user["password"]):
            return True
        raise ValueError("Invalid credentials.")
    raise ValueError("User not found.")

def get_user(email):
    user = users.find_one({"email": email})
    if user:
        return {
            "username": user["username"],
            "email": user["email"],
            "_id": str(user["_id"])  # Convert ObjectId to string
        }
    return None
