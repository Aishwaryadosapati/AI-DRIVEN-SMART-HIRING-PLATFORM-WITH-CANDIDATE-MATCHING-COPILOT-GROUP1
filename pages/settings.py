import streamlit as st

def show():

    st.title("⚙️ Settings")

    st.subheader("Application Settings")

    st.selectbox(
        "Theme",
        ["Light", "Dark", "System Default"]
    )

    st.selectbox(
        "AI Model",
        ["Llama 3", "Llama 3.1", "GPT-4 (Future)", "Gemma"]
    )

    st.selectbox(
        "Language",
        ["English", "Telugu", "Hindi"]
    )

    st.slider(
        "AI Match Threshold (%)",
        50,
        100,
        80
    )

    st.checkbox("Enable AI Resume Analysis", value=True)

    st.checkbox("Enable Skill Gap Analyzer", value=True)

    st.checkbox("Enable AI Email Generator", value=True)

    st.checkbox("Enable Resume Chat", value=True)

    st.checkbox("Enable Notifications", value=True)

    st.markdown("---")

    st.subheader("Email Settings")

    st.text_input(
        "Recruiter Email",
        "hr@company.com"
    )

    st.text_input(
        "Company Name",
        "ABC Technologies"
    )

    st.markdown("---")

    st.subheader("System Information")

    st.info("""
Version : 1.0

Framework : Streamlit

Backend : Python

AI Model : Llama (Milestone 2)

Database : SQLite / MySQL (Future)
""")

    st.button("💾 Save Settings")

    st.success("Settings Saved Successfully!")