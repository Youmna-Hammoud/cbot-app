import streamlit as st
from telegram_bot import check_emergency
from bot import initialize_chat, generate_response
from emergency import detector

def init_session_state():
    defaults = {
        "page": "Home",
        "chat_sessions": {"Chat 1": []},
        "message_count": 0,
        "user_input": "",
        "mood_before": None,
        "mood_after": None,
        "emergency_contact": {},
        "selected_chat": "Chat 1",
        "logged_in": False,
        "current_user": None,
        "show_em_form": False
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    if "selected_chat" not in st.session_state or st.session_state["selected_chat"] not in st.session_state["chat_sessions"]:
        st.session_state["selected_chat"] = list(st.session_state["chat_sessions"].keys())[0]

def apply_styles():
    st.markdown("""
        <div style="position: fixed; top: 60px; right: 20px; z-index: 999; display: flex; gap: 10px; align-items: center;">
            <a href="tel:1564" target="_blank" style="
                padding: 10px;
                font-size: 18px;
                color: white;
                background-color: #8E44AD;
                border-radius: 50%;
                width: 50px;
                height: 50px;
                display: flex;
                justify-content: center;
                align-items: center;
                text-decoration: none;
                font-weight: bold;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            ">🚨</a>
        </div>

        <style>
            html, body, [data-testid="stAppViewContainer"] {
                background-color: #E8D9F9 !important;
                color: #4B3B5F !important;
                font-family: 'Roboto', sans-serif;
            }
            .chat-bubble-user {
                background-color: #9B59B6;
                color: white;
                padding: 6px 10px;
                border-radius: 18px;
                margin-bottom: 6px;
                text-align: right;
                max-width: 70%;
                margin-left: auto;
                font-size: 14px;
            }
            .chat-bubble-bot {
                background-color: #F4E1F1;
                color: #4B3B5F;
                padding: 6px 10px;
                border-radius: 18px;
                margin-bottom: 6px;
                text-align: left;
                max-width: 70%;
                font-size: 14px;
            }
            .chat-container {
                padding: 5px;
                margin-top: 5px;
                max-height: 400px;
                overflow-y: auto;
            }
        </style>
    """, unsafe_allow_html=True)

def display_chat_messages(chat_sessions, selected_chat):
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for sender, message in chat_sessions[selected_chat]:
        bubble_class = "chat-bubble-user" if sender == "You" else "chat-bubble-bot"
        st.markdown(f'<div class="{bubble_class}"><b>{sender}:</b> {message}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def display_chat_sidebar():
    with st.sidebar:
        if st.button("Emergency"):
            st.session_state.show_em_form = True

        if st.session_state.show_em_form:
            with st.form("emergency_form", clear_on_submit=True):
                name = st.text_input("Contact username (on telegram)", key="em_name")
                st.markdown(
                    "<h6>Make sure your contact started the chat with our <a href='https://t.me/cbot_emergency_bot'>bot on telegram</a> and have a telegram username</h6>",
                    unsafe_allow_html=True
                )
                submitted = st.form_submit_button("Save Contact")
                if submitted:
                    if name:
                        st.session_state.emergency_contact = {"name": name}
                        try:
                            check_emergency(name, st.session_state.current_user)
                            st.success("Emergency contact saved.")
                            st.session_state.show_em_form = False
                        except Exception:
                            st.error(f"Failed to register emergency contact")
                    else:
                        st.error("Please fill out all fields.")

        if st.session_state.emergency_contact:
            st.markdown("### 📞 Emergency Contact")
            contact = st.session_state.emergency_contact
            st.markdown(f"""
                <div style='
                    background-color: #FDEDEC;
                    padding: 12px;
                    border-radius: 10px;
                    box-shadow: 0 1px 5px rgba(0,0,0,0.1);
                    color: #5D3A3A;
                    margin-top: 10px;
                    margin-bottom: 10px;
                    display: flex;
                    align-items: center;
                    gap: 10px;
                '>
                    <img src='https://cdn-icons-png.flaticon.com/512/847/847969.png' width='40' style='border-radius: 50%;'>
                    <div>
                        <b>Name:</b> {contact.get('name', '')}<br>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        if st.button("Reset Chat"):
            st.session_state.chat_sessions = {"Chat 1": []}
            st.session_state.selected_chat = "Chat 1"
            st.session_state.message_count = 0
            st.write("Chat reset complete.")

        st.sidebar.markdown("## 💬 Chats")
        if not st.session_state.chat_sessions:
            st.session_state.chat_sessions["Chat 1"] = []

        chat_names = list(st.session_state.chat_sessions.keys())

        if st.session_state.selected_chat not in chat_names:
            st.session_state.selected_chat = chat_names[0]

        st.session_state.selected_chat = st.selectbox(
            "Select Chat", chat_names, index=chat_names.index(st.session_state.selected_chat)
        )

        if st.button("➕ New Chat"):
            new_chat_name = f"Chat {len(st.session_state.chat_sessions) + 1}"
            st.session_state.chat_sessions[new_chat_name] = []
            st.session_state.selected_chat = new_chat_name 
            st.rerun() 

        new_name = st.text_input("Rename selected chat", value=st.session_state.selected_chat)
        if st.button("Rename Chat") and new_name:
            if new_name not in st.session_state.chat_sessions:
                st.session_state.chat_sessions[new_name] = st.session_state.chat_sessions.pop(st.session_state.selected_chat)
                st.session_state.selected_chat = new_name 
            else:
                st.warning("Chat name already exists.")

        if st.button("Delete Chat"):
            if len(st.session_state.chat_sessions) > 1:
                st.session_state.chat_sessions.pop(st.session_state.selected_chat)
                st.session_state.selected_chat = list(st.session_state.chat_sessions.keys())[0]
            else:
                st.warning("You must have at least one chat.")

def get_mood_rating():
    if st.session_state.mood_before is None:
        st.session_state.mood_before = st.slider("How do you feel before chatting?", 1, 10, 5)
        st.write("Thank you. Let's start chatting now!")
        return st.session_state.mood_before
    return None

def check_mood_after():
    if st.session_state.message_count >= 10:
        if "mood_after" not in st.session_state or st.session_state.mood_after is None:
            st.session_state.mood_after = st.slider("How do you feel after chatting?", 1, 10, 5)
            st.session_state.show_mood_after = True
        elif st.session_state.get("show_mood_after", False):
            st.session_state.mood_after = st.slider("How do you feel after chatting?", 1, 10, st.session_state.mood_after)

        if st.session_state.mood_after is not None:
            if st.session_state.mood_after <= 3:
                if st.session_state.emergency_contact:
                    try:
                        check_emergency(st.session_state.emergency_contact["name"], st.session_state.current_user)
                        st.warning("Your emergency contact has been notified. You're not alone. 💜")
                    except Exception as e:
                        st.error(f"Failed to notify emergency contact: {e}")
                st.write("I'm still here for you. Let's keep talking 💬")
            elif st.session_state.mood_after >= 7:
                continue_chat = st.radio("You're feeling better! 😊 Do you want to keep chatting?", ["Yes", "No"])
                if continue_chat == "No":
                    st.write("Thank you for chatting with me today. Take care! 💜")
                    st.stop()
            else:
                st.write("I'm still here for you. Let's keep talking 💬")

def display_main_chat_interface():
    st.title("Welcome to C-Bot, your mental health Chat-Bot!!💜")

    # Get initial mood rating
    mood = get_mood_rating()
    if mood is not None:
        initialize_chat(st.session_state.current_user["_id"])

    st.write("Hello, I'm C-Bot. What's on your mind today? 😊")

    # Use the currently selected chat from the sidebar
    selected_chat = st.session_state.selected_chat

    # Display chat messages
    display_chat_messages(st.session_state.chat_sessions, selected_chat)

    # Create a form for chat input
    chat_form = st.form(key="chat_form", clear_on_submit=True)
    with chat_form:
        user_input = st.text_input("Tell me anything...", key="user_input", label_visibility="collapsed")
        submit_button = st.form_submit_button("Send")

    if submit_button and user_input:
        generate_response(user_input, st.session_state.chat_sessions, selected_chat, st.session_state.current_user)
        detector([user_input], st.session_state.current_user)
        st.session_state.message_count += 1
        st.rerun()

    # Check mood after conversation
    check_mood_after()
