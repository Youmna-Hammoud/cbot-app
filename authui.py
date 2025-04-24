from auth import login, signup, get_user
import streamlit as st

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

def login_ui():
    st.title("Login")
    with st.form(key="login"):
        email = st.text_input("Email").strip()
        password = st.text_input("Password", type="password").strip()
        submit_button = st.form_submit_button("Login")

    if submit_button:
        try:
            if login(email, password):
                st.session_state.logged_in = True
                st.session_state.current_user = get_user(email)
                st.success(f"Logged in as {st.session_state.current_user['username']}!")
                st.rerun()
        except ValueError as e:
            st.error(str(e))

    if not st.session_state.logged_in:
        st.button("Don't have an account? Sign up", on_click=lambda: st.session_state.update(page="signup"))

def signup_ui():
    st.title("Sign Up")
    with st.form(key="signup"):
        username = st.text_input("Username").strip()
        email = st.text_input("Email").strip()
        password1 = st.text_input("Password", type="password").strip()
        password2 = st.text_input("Verify Password", type="password").strip()
        submit_button = st.form_submit_button("Sign Up")

    if submit_button:
        try:
            signup(username, email, password1, password2)
            st.success(f"Successfully registered as {username}!")
            st.session_state.page = "login"
            st.rerun()
        except ValueError as e:
            st.error(str(e))


def logout_ui():
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.success("Successfully logged out!")
        st.rerun()

def main():
    # Navigation
    if 'page' not in st.session_state:
        st.session_state.page = "login"
    
    # Show appropriate page based on login state
    if st.session_state.logged_in:
        st.sidebar.title(f"Welcome, {st.session_state.current_user['username']}!")
        logout_ui()
        # Add your main app content here
        st.title("Main Application")
        st.write("You are logged in!")
    else:
        if st.session_state.page == "login":
            login_ui()
        else:
            signup_ui()

if __name__ == "__main__":
    main()