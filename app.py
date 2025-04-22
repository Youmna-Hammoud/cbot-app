import streamlit as st
from mainui import init_session_state, apply_styles, display_chat_messages, display_chat_sidebar, get_mood_rating, check_mood_after
from bot import initialize_chat, generate_response
from authui import signup_ui, login_ui
from emergency import detector

def main():
    # Initialize session state and apply styles
    init_session_state()
    apply_styles()

    # Check if user is logged in
    if not st.session_state.get("logged_in", False):
        # Check if user wants to sign up
        if st.session_state.get("page", "login") == "signup":
            signup_ui()
            if st.button("Already have an account? Login", key="back_to_login"):
                st.session_state.page = "login"
                st.rerun()
        else:
            # Show login form
            login_ui()
    else:
        # User is logged in, show chat interface
        display_chat_sidebar()

        # Main content
        st.title("Welcome to C-Bot, your mental health Chat-Bot!!💜")

        # Get initial mood rating
        mood = get_mood_rating()
        if mood is not None:
            initialize_chat(st.session_state.current_user["_id"])

        st.write("Hello, I'm C-Bot. What's on your mind today? 😊")

        # Get selected chat
        selected_chat = list(st.session_state.chat_sessions.keys())[0]

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
            st.rerun()

        # Check mood after conversation
        check_mood_after()

if __name__ == "__main__":
    main() 