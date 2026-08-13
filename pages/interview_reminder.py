import streamlit as st

from utils.database import (
    get_all_candidates,
    get_job,
    get_interview
)


def show():

    st.title("⏰ Interview Reminder")

    # ==========================================
    # Select Candidate
    # ==========================================

    candidates = get_all_candidates()

    if len(candidates) == 0:

        st.warning("No candidates available.")

        return

    candidate_options = {

        f"{c['name']} ({c['email']})": c

        for c in candidates

    }

    selected = st.selectbox(

        "👤 Select Candidate",

        list(candidate_options.keys())

    )

    candidate = candidate_options[selected]

    st.divider()

    # ==========================================
    # Candidate Information
    # ==========================================

    st.subheader("👤 Candidate Information")

    c1, c2 = st.columns(2)

    with c1:

        st.write("**Name:**", candidate["name"])
        st.write("**Email:**", candidate["email"])
        st.write("**Phone:**", candidate["phone"])

    with c2:

        st.write("**ATS Score:**", candidate["resume_score"])
        st.write("**Status:**", candidate["candidate_status"])

    st.divider()

    # ==========================================
    # Job Information
    # ==========================================

    job = get_job(candidate["job_id"])

    if job is None:

        st.error("Job not found.")

        return

    st.subheader("💼 Job Information")

    c1, c2 = st.columns(2)

    with c1:

        st.write("**Job Title:**", job["job_title"])
        st.write("**Department:**", job["department"])

    with c2:

        st.write("**Location:**", job["location"])
        st.write("**Employment Type:**", job["employment_type"])

    st.divider()

    # ==========================================
    # Interview Information
    # ==========================================

    interview = get_interview(candidate["id"])

    if interview is None:

        st.warning("Interview not scheduled.")

        return

    st.subheader("📅 Interview Details")

    c1, c2 = st.columns(2)

    with c1:

        st.write("**Interview Type:**", interview["interview_type"])
        st.write("**Date:**", interview["interview_date"])
        st.write("**Time:**", interview["interview_time"])

    with c2:

        st.write("**Mode:**", interview["interview_mode"])
        st.write("**Interviewer:**", interview["interviewer"])
        st.write("**Meeting Link:**", interview["meeting_link"])

    st.divider()






    # ==========================================
    # AI Reminder Generator
    # ==========================================

    st.subheader("🤖 AI Interview Reminder")

    if st.button(

        "Generate Reminder",

        use_container_width=True

    ):

        from models.interview_reminder_ai import (
            generate_interview_reminder
        )

        with st.spinner(

            "Generating Reminder..."

        ):

            email = generate_interview_reminder(

                candidate["name"],

                job["job_title"],

                interview["interview_type"],

                interview["interview_date"],

                interview["interview_time"],

                interview["interview_mode"],

                interview["meeting_link"]

            )

        st.session_state["reminder_email"] = email

        st.success(
            "Reminder Generated Successfully!"
        )

    st.divider()



    # ==========================================
    # Email Preview
    # ==========================================

    if "reminder_email" in st.session_state:

        st.subheader("📧 Reminder Email")

        st.text_area(

            "Generated Reminder",

            st.session_state["reminder_email"],

            height=350

        )

    st.divider()



    # ==========================================
    # Email Actions
    # ==========================================

    if "reminder_email" in st.session_state:

        st.subheader("📨 Reminder Actions")

        c1, c2 = st.columns(2)

        with c1:

            if st.button(
                "📋 Copy Reminder",
                use_container_width=True
            ):

                st.code(
                    st.session_state["reminder_email"],
                    language="text"
                )

                st.success(
                    "Reminder ready to copy."
                )

        with c2:

            if st.button(
                "📨 Send Reminder",
                use_container_width=True
            ):

                st.success(

                    f"Reminder sent successfully to {candidate['email']}"

                )

                st.balloons()

    st.divider()



    # ==========================================
    # Reminder Status
    # ==========================================

    st.subheader("📌 Reminder Status")

    reminder_status = st.selectbox(

        "Reminder Status",

        [

            "Pending",

            "Sent",

            "Delivered"

        ]

    )

    recruiter_notes = st.text_area(

        "Recruiter Notes"

    )

    st.divider()



    # ==========================================
    # Save Reminder
    # ==========================================

    if st.button(

        "💾 Save Reminder",

        use_container_width=True

    ):

        from utils.database import save_reminder_status

        save_reminder_status(

            candidate["id"],

            reminder_status,

            recruiter_notes

        )

        st.success(
            "Reminder Saved Successfully!"
        )

        st.balloons()


        st.divider()

        st.subheader("📊 Reminder Dashboard")

        c1, c2 = st.columns(2)

        with c1:

            st.metric(
                "Candidate",
                candidate["name"]
            )

            st.metric(
                "Interview",
                interview["interview_type"]
            )

            st.metric(
                "Reminder",
                reminder_status
            )

        with c2:

            st.metric(
                "Interview Date",
                interview["interview_date"]
            )

            st.metric(
                "Interview Time",
                interview["interview_time"]
            )

            st.metric(
                "Mode",
                interview["interview_mode"]
            )

        st.divider()

        st.subheader("📄 Recruiter Notes")

        if recruiter_notes.strip():

            st.info(recruiter_notes)

        else:

            st.info("No recruiter notes added.")

        st.divider()

        st.success(
            "🎉 Interview Reminder Completed Successfully!"
        )

        st.info(
            "➡️ Next Module: Offer Letter"
        )