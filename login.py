import streamlit as st

def show_login():
    st.title("🔐 Recruiter Login")

    st.write("Please login to continue")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        # Temporary credentials
        if username == "admin" and password == "admin123":
            st.session_state.logged_in = True
            st.success("Login Successful")
            st.rerun()

        else:
            st.error("Invalid Username or Password")