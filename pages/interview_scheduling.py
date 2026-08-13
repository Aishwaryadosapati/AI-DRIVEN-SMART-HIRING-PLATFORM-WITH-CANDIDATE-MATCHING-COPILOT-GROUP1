import streamlit as st

from utils.database import (
    get_all_candidates,
    get_job
)


def show():

    st.title("📅 Interview Scheduling")

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
    # Candidate Details
    # ==========================================

    st.subheader("👤 Candidate Information")

    col1, col2 = st.columns(2)

    with col1:

        st.write("**Name:**", candidate["name"])
        st.write("**Email:**", candidate["email"])
        st.write("**Phone:**", candidate["phone"])

    with col2:

        st.write("**ATS Score:**", candidate["resume_score"])
        st.write("**Status:**", candidate["candidate_status"])

    st.progress(candidate["resume_score"] / 100)

    st.divider()

    # ==========================================
    # Job Details
    # ==========================================

    job = get_job(candidate["job_id"])

    if job is None:

        st.error("Job details not found.")

        return

    st.subheader("💼 Job Details")

    col1, col2 = st.columns(2)

    with col1:

        st.write("**Job Title:**", job["job_title"])
        st.write("**Department:**", job["department"])
        st.write("**Experience:**", job["experience"])

    with col2:

        st.write("**Employment Type:**", job["employment_type"])
        st.write("**Location:**", job["location"])
        st.write("**Openings:**", job["openings"])

    st.write("### 🛠 Required Skills")

    st.info(job["skills"])

    st.divider()

    # ==========================================
    # Interview Type
    # ==========================================

    st.subheader("🎯 Interview Type")

    interview_type = st.selectbox(

        "Select Interview Round",

        [

            "🤖 AI Interview (Round 1)",

            "💻 Technical Interview (Round 2)",

            "👨‍💼 HR Interview (Round 3)",

            "🎯 Final Manager Interview (Round 4)"

        ]

    )

    st.divider()


    # ==========================================
    # Interview Details
    # ==========================================

    st.subheader("📅 Interview Details")

    col1, col2 = st.columns(2)

    with col1:

        interviewer = st.text_input(
            "Interviewer Name"
        )

        interview_date = st.date_input(
            "Interview Date"
        )

        duration = st.selectbox(

            "Interview Duration",

            [

                "30 Minutes",

                "45 Minutes",

                "60 Minutes",

                "90 Minutes"

            ]

        )

    with col2:

        interview_time = st.time_input(
            "Interview Time"
        )

        mode = st.selectbox(

            "Interview Mode",

            [

                "Online",

                "Offline"

            ]

        )

        meeting_link = st.text_input(
            "Meeting Link / Venue"
        )

    st.divider()

    # ==========================================
    # Round-wise Configuration
    # ==========================================

    st.subheader("⚙ Interview Configuration")

    # ------------------------------------------
    # AI Interview
    # ------------------------------------------

    if interview_type == "🤖 AI Interview (Round 1)":

        difficulty = st.selectbox(

            "Difficulty",

            [

                "Easy",

                "Medium",

                "Hard"

            ]

        )

        question_count = st.selectbox(

            "Number of Questions",

            [

                5,

                10,

                15,

                20

            ],

            index=1

        )

        st.info(
            "AI Screening Test will be generated automatically."
        )

    # ------------------------------------------
    # Technical Interview
    # ------------------------------------------

    elif interview_type == "💻 Technical Interview (Round 2)":

        language = st.selectbox(

            "Programming Language",

            [

                "Python",

                "Java",

                "C++",

                "JavaScript",

                "SQL"

            ]

        )

        experience = st.text_input(
            "Required Experience"
        )

        skills = st.text_area(
            "Required Technical Skills",
            value=job["skills"]
        )

    # ------------------------------------------
    # HR Interview
    # ------------------------------------------

    elif interview_type == "👨‍💼 HR Interview (Round 3)":

        interview_focus = st.multiselect(

            "Interview Focus",

            [

                "Communication",

                "Behaviour",

                "Leadership",

                "Teamwork",

                "Salary Discussion",

                "Culture Fit"

            ]

        )

    # ------------------------------------------
    # Final Manager Interview
    # ------------------------------------------

    else:

        discussion_topics = st.multiselect(

            "Discussion Topics",

            [

                "Project Discussion",

                "Technical Review",

                "Business Understanding",

                "Leadership",

                "Culture Fit",

                "Final Decision"

            ]

        )

    st.divider()



    # ==========================================
    # Interview Status
    # ==========================================

    st.subheader("📌 Interview Status")

    status = st.selectbox(

        "Status",

        [

            "Scheduled",

            "Rescheduled",

            "Completed",

            "Cancelled"

        ]

    )

    remarks = st.text_area(

        "Remarks"

    )

    st.divider()

    # ==========================================
    # Schedule Interview
    # ==========================================

    if st.button(

        "📅 Schedule Interview",

        use_container_width=True

    ):

        from utils.database import schedule_interview

        schedule_interview(

            candidate["id"],

            job["id"],

            interview_type,

            interviewer,

            str(interview_date),

            str(interview_time),

            duration,

            mode,

            meeting_link,

            status,

            remarks

        )

        st.success("✅ Interview Scheduled Successfully!")

        st.balloons()

        st.divider()

        # ==========================================
        # Interview Summary
        # ==========================================

        st.subheader("📋 Interview Summary")

        c1, c2 = st.columns(2)

        with c1:

            st.metric(
                "Candidate",
                candidate["name"]
            )

            st.metric(
                "Interview Type",
                interview_type
            )

            st.metric(
                "Interviewer",
                interviewer
            )

            st.metric(
                "Status",
                status
            )

        with c2:

            st.metric(
                "Interview Date",
                str(interview_date)
            )

            st.metric(
                "Interview Time",
                str(interview_time)
            )

            st.metric(
                "Mode",
                mode
            )

            st.metric(
                "Duration",
                duration
            )

        st.divider()

        if mode == "Online":

            st.info(f"🔗 Meeting Link: {meeting_link}")

        else:

            st.info(f"📍 Venue: {meeting_link}")

        st.divider()

        st.subheader("📝 Remarks")

        if remarks.strip() == "":

            st.info("No remarks added.")

        else:

            st.info(remarks)

        st.divider()

        st.success("🎉 Interview Scheduled Successfully!")


    # ==========================================
    # Scheduled Interviews
    # ==========================================

    st.divider()

    st.subheader("📋 Scheduled Interviews")

    from utils.database import get_all_interviews

    interviews = get_all_interviews()

    if len(interviews) == 0:

        st.info("No interviews scheduled.")

    else:

        for interview in interviews:

            with st.expander(

                f"{interview.get('interview_type', 'Interview')} | Candidate ID: {interview.get('candidate_id', '-')}"

            ):

                c1, c2 = st.columns(2)

                with c1:

                    st.write("**Candidate:**", interview.get("candidate_name", "-"))
                st.write("**Interviewer:**", interview.get("interviewer", "-"))
                st.write("**Date:**", interview.get("interview_date", "-"))
                st.write("**Time:**", interview.get("interview_time", "-"))
                st.write("**Duration:**", interview.get("duration", "-"))

                with c2:

                    st.write("**Mode:**", interview.get("interview_mode", "-"))
                st.write("**Status:**", interview.get("status", "-"))
                st.write("**Meeting Link:**", interview.get("meeting_link", "-"))

            st.write("**Feedback:**", interview.get("feedback", "No feedback available"))

    st.divider()

    # ==========================================
    # Interview Analytics
    # ==========================================

    st.subheader("📊 Interview Analytics")

    total = len(interviews)

    scheduled = len(
        [i for i in interviews if i["status"] == "Scheduled"]
    )

    completed = len(
        [i for i in interviews if i["status"] == "Completed"]
    )

    cancelled = len(
        [i for i in interviews if i["status"] == "Cancelled"]
    )

    rescheduled = len(
        [i for i in interviews if i["status"] == "Rescheduled"]
    )

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric(
        "Total",
        total
    )

    c2.metric(
        "Scheduled",
        scheduled
    )

    c3.metric(
        "Completed",
        completed
    )

    c4.metric(
        "Cancelled",
        cancelled
    )

    c5.metric(
        "Rescheduled",
        rescheduled
    )

    st.divider()

    st.success("🎉 Interview Scheduling Module Completed Successfully!")