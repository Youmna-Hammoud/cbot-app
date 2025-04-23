import streamlit as st
from mainui import init_session_state, apply_styles, display_chat_sidebar, display_main_chat_interface
from authui import signup_ui, login_ui

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
        display_main_chat_interface()

if __name__ == "__main__":
    main() 