import streamlit as st
from models.llama import ask_llama
from utils.database import get_all_candidates


def show():

    st.title("💬 Resume Chat")

    # ==================================
    # Resume Source
    # ==================================

    option = st.radio(
        "Choose Resume Source",
        [
            "📤 Upload New Resume",
            "👤 Existing Candidate Profile"
        ],
        horizontal=True
    )

    resume_text = ""

    # ==================================
    # Upload Resume
    # ==================================

    if option == "📤 Upload New Resume":

        if "resume_text" not in st.session_state:
            st.warning("⚠ Please upload a resume first.")
            return

        resume_text = st.session_state["resume_text"]

    # ==================================
    # Existing Candidate
    # ==================================

    else:

        candidates = get_all_candidates()

        if len(candidates) == 0:
            st.warning("No candidate profiles available.")
            return

        candidate_names = [
            candidate["name"]
            for candidate in candidates
        ]

        selected_name = st.selectbox(
            "👤 Select Candidate",
            candidate_names
        )

        selected_candidate = next(
            candidate
            for candidate in candidates
            if candidate["name"] == selected_name
        )

        st.subheader("📄 Candidate Details")

        col1, col2 = st.columns(2)

        with col1:
            st.write("**Name:**", selected_candidate["name"])
            st.write("**Email:**", selected_candidate["email"])
            st.write("**Location:**", selected_candidate["location"])

        with col2:
            st.write("**Resume Score:**", selected_candidate["resume_score"])
            st.write("**Recommendation:**", selected_candidate["recommendation"])
            st.write("**Status:**", selected_candidate["candidate_status"])

        with st.expander("📄 Resume Preview"):

            st.text_area(
                "Resume",
                selected_candidate["resume_text"],
                height=250,
                disabled=True
            )

        resume_text = selected_candidate["resume_text"]

    # ==================================
    # Resume Chat
    # ==================================

    st.info("💡 Ask anything about the selected resume.")

    question = st.text_input(
        "Ask a Question"
    )

    if st.button("🤖 Ask AI", use_container_width=True):

        if question.strip() == "":
            st.warning("Please enter a question.")
            return

        prompt = f"""
You are an AI Recruitment Assistant.

Resume:

{resume_text}

Question:

{question}

Answer ONLY using the resume.

If the answer is not available in the resume, reply:

'Not mentioned in the resume.'
"""

        with st.spinner("Thinking..."):

            answer = ask_llama(prompt)

        st.success("Answer Generated Successfully")

        st.subheader("🤖 AI Answer")

        st.write(answer)

    # ==================================
    # Example Questions
    # ==================================

    st.divider()

    st.subheader("💡 Example Questions")

    st.markdown("""
- What are the candidate's technical skills?
- What projects has the candidate completed?
- What certifications does the candidate have?
- What is the candidate's education?
- How many years of experience does the candidate have?
- Summarize the resume.
- Is the candidate suitable for a Python Developer role?
- What programming languages does the candidate know?
- What are the candidate's strengths?
- Is the candidate a good fit for this job?
""")