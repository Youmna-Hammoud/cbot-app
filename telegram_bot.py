import requests
from auth import get_user
from pymongo import MongoClient
import streamlit as st

TOKEN = st.secrets["TOKEN"]
MONGO_URI = st.secrets["MONGO_URI"]

client = MongoClient(MONGO_URI)
authdb = client.get_database("cbotauth")
contacts = authdb.get_collection("contacts")
emergency = authdb.get_collection("emergency_contacts")

bot_token = TOKEN


def add_contacts():
    url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
    response = requests.get(url).json()

    if response["ok"] == True:
        for message in response.get("result", []):
            user_info = message.get("message", {}).get("from", {})
            chat_id = user_info.get("id")
            first_name = user_info.get("first_name")
            last_name = user_info.get("last_name")
            username = user_info.get("username")

            if not all([chat_id, first_name, last_name]):
                continue 
            if not username:
                send_message(chat_id, "Please make sure your account has a username, then send a message to be added as an emergency contact.")
                continue
            ids=[]
            for contact in contacts.find({"chat_id" : {"$exists" : True}}):
                ids.append(contact["chat_id"])
            if chat_id not in ids:
                contacts.insert_one({"chat_id" : chat_id, "first_name" : first_name, "last_name" : last_name, "username": username})

def set_contact_emergency(current_user, contact):
    contact["for"] = current_user["_id"]
    if contact not in emergency.find({"_id" : contact["_id"]}):
        emergency.insert_one(contact)


def find_contact(username):
    contact = contacts.find_one({"username" : username})
    if contact:
        return contact
    raise ValueError("Contact not found.")

def emergency_contacts(current_user):
    emergency_contacts_list = emergency.find({"for" : current_user["_id"]})
    return [contact for contact in emergency_contacts_list]

def send_verification(contacts, current_user):

    url2 = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    for contact in contacts:
        chat_id = contact["chat_id"]
        data = {
            "chat_id": chat_id,
            "text": f"Your contact is set as emergency contact for {current_user["username"]} "
        }

    
        res = requests.post(url2, data=data)

        '''if res.status_code == 200:
            st.success("Message sent successfully!")
        else:
            st.error("Failed to send message")'''

def check_emergency(username, current_user):
    add_contacts()
    set_contact_emergency(current_user, find_contact(username))
    send_verification(emergency_contacts(current_user), current_user)

def send_emergency(contacts, current_user, user_message):

    url2 = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    for contact in contacts:
        chat_id = contact["chat_id"]
        data = {
            "chat_id": chat_id,
            "text": f"EMERGENCY DETECTED for {current_user["username"]}, message: {str(user_message)}  "
        }

    
        res = requests.post(url2, data=data)

        '''if res.status_code == 200:
            st.success("Message sent successfully!")
        else:
            st.error("Failed to send message")'''
def send_message(chat_id, message):

    url2 = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    data = {
        "chat_id": chat_id,
        "text": message
    }

    
    requests.post(url2, data=data)