import streamlit as st
from models.llama import ask_llama
from utils.email_sender import send_email
from utils.database import get_all_candidates
from utils.database import update_candidate_status

def show():

    st.title("📧 AI Email Generator")

    # ===============================
    # Load Candidates from Database
    # ===============================

    candidates = get_all_candidates()

    if len(candidates) == 0:
        st.warning("⚠ No candidates found. Please upload a resume first.")
        return

    candidate_names = []

    for candidate in candidates:
        candidate_names.append(
            f"{candidate['name']} ({candidate['email']})"
        )

    selected = st.selectbox(
        "Select Candidate",
        candidate_names
    )

    selected_candidate = None

    for candidate in candidates:

        if f"{candidate['name']} ({candidate['email']})" == selected:

            selected_candidate = candidate

            break

    candidate = selected_candidate["name"]
    candidate_email = selected_candidate["email"]

    st.subheader("📊 Candidate Evaluation")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Resume Score",
            selected_candidate["resume_score"]
        )

    with col2:

        recommendation = selected_candidate["recommendation"]

        if recommendation == "Hire":
            st.success("✅ Hire")

        elif recommendation == "Hold":
            st.warning("🟡 Hold")

        else:
            st.error("❌ Reject")

    # ===============================
    # Candidate Details
    # ===============================

    st.subheader("Candidate Details")

    st.text_input(
        "Candidate Name",
        candidate,
        disabled=True
    )

    st.text_input(
        "Candidate Email",
        candidate_email,
        disabled=True
    )

    position = st.text_input(
        "Job Position",
        "Software Engineer"
    )

    email_type = st.selectbox(
        "Email Type",
        [
            "Interview Invitation",
            "Offer Letter",
            "Rejection",
            "Follow-up"
        ]
    )

    # ===============================
    # Interview Details
    # ===============================

    if email_type == "Interview Invitation":

        st.subheader("Interview Details")

        interview_date = st.date_input("Interview Date")
        interview_time = st.time_input("Interview Time")
        duration = st.text_input("Duration", "45 Minutes")
        meeting_link = st.text_input(
            "Meeting Link",
            "https://meet.google.com/abc-defg-hij"
        )

    else:   

        interview_date = ""
        interview_time = ""
        duration = ""
        meeting_link = ""

    subject = st.text_input(
        "Email Subject",
        f"{email_type} - {position}"
    )

    # ===============================
    # Generate Email
    # ===============================

    if st.button("📨 Generate Email"):

        with st.spinner("Generating Email..."):

            prompt = f"""
You are an experienced HR Recruiter.

Generate a professional {email_type} email.

Candidate Name: {candidate}

Job Position: {position}

Interview Details:

Date: {interview_date}

Time: {interview_time}

Duration: {duration}

Mode: Online

Meeting Link:
{meeting_link}

Instructions:

1. Write a professional subject.
2. Address the candidate by name.
3. Mention the selected job position.
4. Mention the interview schedule.
5. Mention the meeting link.
6. Tell the candidate to join 10 minutes early.
7. End with:

Best Regards,
HR Team

Return only the email.
"""

            st.session_state["generated_email"] = ask_llama(prompt)

    # ===============================
    # Display Email
    # ===============================

    if "generated_email" in st.session_state:

        st.success("✅ Email Generated Successfully")
        st.info("➡️ Recruitment communication completed successfully.")

        st.text_area(
            "Generated Email",
            st.session_state["generated_email"],
            height=450
        )

        st.download_button(
            "⬇ Download Email",
            st.session_state["generated_email"],
            "Interview_Email.txt",
            mime="text/plain"
        )

        if st.button("📤 Send Email"):

            result = send_email(
                candidate_email,
                subject,
                st.session_state["generated_email"]
            )

            if result is True:

                if email_type == "Offer Letter":
                    update_candidate_status(
                    selected_candidate["id"],
                    "Offer Sent"
                )

                elif email_type == "Interview Invitation":
                    update_candidate_status(
                    selected_candidate["id"],
                "Interview Scheduled"
                )

                elif email_type == "Rejection":
                    update_candidate_status(
                    selected_candidate["id"],
                    "Rejected"
                )

                st.success("✅ Email Sent Successfully!")

            else:

                st.error(result)

    # Update candidate status
    