import streamlit as st

from utils.database import (
    get_all_candidates,
    get_job,
    get_interview
)


def show():

    st.title("📩 Interview Invitation")

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
    # Interview Details
    # ==========================================

    interview = get_interview(candidate["id"])

    if interview is None:

        st.warning("Please schedule the interview first.")

        return

    st.subheader("📅 Interview Details")

    c1, c2 = st.columns(2)

    with c1:

        interview_types = [

            "🤖 AI Interview (Round 1)",

            "💻 Technical Interview (Round 2)",

            "👨‍💼 HR Interview (Round 3)",

            "🎯 Final Manager Interview (Round 4)"

        ]

        current_type = interview.get("interview_type", interview_types[0])

        if current_type not in interview_types:
            current_type = interview_types[0]

        interview_type = st.selectbox(

            "Interview Type",

            interview_types,

            index=interview_types.index(current_type)

        )
        
        st.write("**Date:**", interview["interview_date"])
        st.write("**Time:**", interview["interview_time"])

    with c2:

        st.write("**Mode:**", interview["interview_mode"])
        st.write("**Interviewer:**", interview["interviewer"])
        st.write("**Meeting Link:**", interview["meeting_link"])

    st.divider()



    # ==========================================
    # AI Interview Invitation
    # ==========================================

    st.subheader("🤖 AI Interview Invitation")

    if st.button(
        "Generate Invitation",
        use_container_width=True
    ):

        from models.interview_invitation_ai import (
            generate_interview_invitation
        )

        with st.spinner(
            "Generating Interview Invitation..."
        ):

            email = generate_interview_invitation(

                candidate["name"],

                job["job_title"],

                interview_type,

                interview["interview_date"],

                interview["interview_time"],

                interview["interview_mode"],

                interview["meeting_link"]

            )

        st.session_state["interview_email"] = email

        st.success(
            "✅ Interview Invitation Generated Successfully!"
        )

    st.divider()

    # ==========================================
    # Email Preview
    # ==========================================

    if "interview_email" in st.session_state:

        st.subheader("📧 Interview Invitation Preview")

        st.text_area(

            "Generated Email",

            st.session_state["interview_email"],

            height=350

        )

    st.divider()


    # ==========================================
    # Email Actions
    # ==========================================

    if "interview_email" in st.session_state:

        st.subheader("📨 Email Actions")

        c1, c2 = st.columns(2)

        with c1:

            if st.button(
                "📋 Copy Email",
                use_container_width=True
            ):

                st.code(
                    st.session_state["interview_email"],
                    language="text"
                )

                st.success("Email ready to copy.")

        with c2:

            if st.button(
                "📨 Send Email",
                use_container_width=True
            ):

                from utils.email_sender import send_email

                send_email(

                        candidate["email"],

                        "Interview Invitation",

                        st.session_state["interview_email"]

                )

                st.success(

                    f"Interview Invitation sent successfully to {candidate['email']}"

                )

                st.balloons()

    st.divider()


    # ==========================================
    # Invitation Summary
    # ==========================================

    if "interview_email" in st.session_state:

        st.subheader("📊 Invitation Summary")

        c1, c2 = st.columns(2)

        with c1:

            st.metric(
                "Candidate",
                candidate["name"]
            )

            st.metric(
                "Interview Type",
                interview["interview_type"]
            )

            st.metric(
                "Status",
                interview["status"]
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


    # ==========================================
    # Invitation Status
    # ==========================================

    st.subheader("📌 Invitation Status")

    invitation_status = st.selectbox(

        "Invitation Status",

        [

            "Draft",

            "Sent",

            "Accepted",

            "Declined"

        ]

    )

    recruiter_notes = st.text_area(

        "Recruiter Notes"

    )

    st.divider()


    # ==========================================
    # Save Invitation
    # ==========================================

    if st.button(

        "💾 Save Invitation",

        use_container_width=True

    ):

        from utils.database import save_invitation_status

        save_invitation_status(

            candidate["id"],

            interview["interview_type"],

            interview["interview_date"],

            interview["interview_time"],

            interview["interview_mode"],

            invitation_status,

            recruiter_notes

        )

        st.success(

            "✅ Invitation Saved Successfully!"

        )

        st.balloons()


        st.divider()

        st.subheader("📊 Invitation Dashboard")

        c1, c2 = st.columns(2)

        with c1:

            st.metric(
                "Candidate",
                candidate["name"]
            )

            st.metric(
                "Interview Type",
                interview["interview_type"]
            )

            st.metric(
                "Invitation Status",
                invitation_status
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

        if recruiter_notes.strip() == "":

            st.info("No recruiter notes added.")

        else:

            st.info(recruiter_notes)

        st.divider()

        st.success(
            "🎉 Interview Invitation Completed Successfully!"
        )

        st.info(
            "➡️ Next Module: Interview Reminder"
        )