import streamlit as st
from models.llama import ask_llama

def show():

    st.title("🤖 AI Assistant")

    st.write("Ask me anything about the Recruitment System.")

    question = st.text_input(
        "Ask your question",
        placeholder="Example: How do I upload a resume?"
    )

    if st.button("💬 Ask Assistant"):

        if question.strip() == "":
            st.warning("Please enter a question.")
            return

        prompt = f"""
You are an AI Assistant for an AI Recruitment & Talent Management System.

Help users understand and use the application.

The application has these modules:
- Dashboard
- Resume Upload
- Resume Analysis
- Candidate Profile
- Job Management
- Resume Matching
- Candidate Ranking
- Skill Gap Analyzer
- Interview Questions
- Hiring Recommendation
- AI Email Generator
- Analytics
- Resume Chat
- Interview Management
- Interview Invitation
- Resume Repository
- AI Recruitment Copilot

User Question:
{question}

Answer in a simple, professional, and helpful way.
"""

        with st.spinner("Thinking..."):
            answer = ask_llama(prompt)

        st.subheader("🤖 Assistant Response")

        st.write(answer)