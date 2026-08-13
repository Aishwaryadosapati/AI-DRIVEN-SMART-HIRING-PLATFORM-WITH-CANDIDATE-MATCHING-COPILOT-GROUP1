import streamlit as st

from utils.database import (
    get_all_candidates,
    get_job,
    get_interview
)


def show():

    st.title("👨‍💼 Round 3 - HR Interview")

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
    # Technical Interview Result
    # ==========================================

    interview = get_interview(candidate["id"])

    if interview is None:

        st.error("Technical Interview not completed.")

        return

    st.subheader("💻 Round 2 Result")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Technical Score",
        interview["technical_score"]
    )

    c2.metric(
        "Status",
        interview["final_status"]
    )

    c3.metric(
        "Round",
        interview["round"]
    )

    st.divider()

    # ==========================================
    # Job Details
    # ==========================================

    job = get_job(candidate["job_id"])

    if job:

        st.subheader("💼 Applied Job")

        col1, col2 = st.columns(2)

        with col1:

            st.write("**Job Title:**", job["job_title"])
            st.write("**Department:**", job["department"])
            st.write("**Experience:**", job["experience"])

        with col2:

            st.write("**Employment Type:**", job["employment_type"])
            st.write("**Minimum ATS:**", job["minimum_ats_score"])
            st.write("**Openings:**", job["openings"])

        st.info(job["skills"])

    st.divider()

    # ==========================================
    # HR Interview Details
    # ==========================================

    st.subheader("👨‍💼 HR Interview Details")

    col1, col2 = st.columns(2)

    with col1:

        hr_interviewer = st.text_input(
            "HR Interviewer Name"
        )

        interview_date = st.date_input(
            "Interview Date"
        )

        mode = st.selectbox(
            "Interview Mode",
            [
                "Online",
                "Offline"
            ]
        )

    with col2:

        interview_time = st.time_input(
            "Interview Time"
        )

        meeting_link = st.text_input(
            "Meeting Link (Optional)"
        )

    st.divider()

    # ==========================================
    # Generate AI HR Questions
    # ==========================================

    st.subheader("🤖 AI HR Interview Questions")

    if st.button(
        "Generate HR Questions",
        use_container_width=True
    ):

        from models.hr_questions_ai import generate_hr_questions

        with st.spinner("Generating HR Questions..."):

            questions = generate_hr_questions(

                candidate["resume_text"],

                job["job_title"]

            )

            st.session_state["hr_questions"] = questions

    # ==========================================
    # Display HR Questions
    # ==========================================

    if "hr_questions" in st.session_state:

        st.success("✅ HR Questions Generated")

        st.subheader("📋 HR Interview Questions")

        questions = st.session_state["hr_questions"]

        if isinstance(questions, list):

            for i, question in enumerate(questions):

                st.write(f"**Q{i+1}. {question}**")

        else:

            st.write(questions)

    st.divider()


    # ==========================================
    # HR Evaluation
    # ==========================================

    st.subheader("⭐ HR Evaluation")

    col1, col2 = st.columns(2)

    with col1:

        communication = st.slider(
            "Communication Skills",
            0,
            10,
            7
        )

        confidence = st.slider(
            "Confidence",
            0,
            10,
            7
        )

        leadership = st.slider(
            "Leadership",
            0,
            10,
            7
        )

    with col2:

        teamwork = st.slider(
            "Teamwork",
            0,
            10,
            7
        )

        culture_fit = st.slider(
            "Culture Fit",
            0,
            10,
            7
        )

        adaptability = st.slider(
            "Adaptability",
            0,
            10,
            7
        )

    hr_remarks = st.text_area(
        "HR Remarks"
    )

    st.divider()

    # ==========================================
    # HR Score
    # ==========================================

    hr_score = round(

        (

            communication +

            confidence +

            leadership +

            teamwork +

            culture_fit +

            adaptability

        ) / 60 * 100

    )

    st.subheader("📊 HR Interview Score")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Communication",
        communication
    )

    c2.metric(
        "Confidence",
        confidence
    )

    c3.metric(
        "Leadership",
        leadership
    )

    c4, c5, c6 = st.columns(3)

    c4.metric(
        "Teamwork",
        teamwork
    )

    c5.metric(
        "Culture Fit",
        culture_fit
    )

    c6.metric(
        "Adaptability",
        adaptability
    )

    st.progress(hr_score / 100)

    st.metric(
        "Overall HR Score",
        f"{hr_score}%"
    )

    st.divider()

    # ==========================================
    # AI HR Recommendation
    # ==========================================

    st.subheader("🤖 HR Recommendation")

    if hr_score >= 85:

        recommendation = "Strongly Recommended"

        st.success(
            "🌟 Excellent HR Performance"
        )

    elif hr_score >= 70:

        recommendation = "Recommended"

        st.success(
            "✅ Good HR Performance"
        )

    elif hr_score >= 50:

        recommendation = "Needs Improvement"

        st.warning(
            "⚠ Average HR Performance"
        )

    else:

        recommendation = "Not Recommended"

        st.error(
            "❌ Poor HR Performance"
        )

    st.info(
        f"Recommendation : {recommendation}"
    )

    st.divider()


    # ==========================================
    # Save HR Interview
    # ==========================================

    if st.button(
        "💾 Save HR Interview",
        use_container_width=True
    ):

        if hr_interviewer == "":

            st.warning("Please enter HR Interviewer Name.")

        else:

            from utils.database import update_hr_interview

            update_hr_interview(

                candidate["id"],

                hr_interviewer,

                str(interview_date),

                str(interview_time),

                mode,

                meeting_link,

                hr_score,

                hr_remarks

            )

            st.success("✅ HR Interview Saved Successfully!")

            st.balloons()

            st.divider()

            st.subheader("📋 HR Interview Summary")

            c1, c2, c3 = st.columns(3)

            c1.metric(
                "Candidate",
                candidate["name"]
            )

            c2.metric(
                "HR Score",
                f"{hr_score}%"
            )

            c3.metric(
                "Recommendation",
                recommendation
            )

            st.progress(hr_score / 100)

            st.divider()

            if hr_score >= 70:

                st.success(
                    "🎉 Candidate Qualified for Round 4 - Final Manager Interview"
                )

            elif hr_score >= 50:

                st.warning(
                    "⚠ Candidate can proceed after HR approval."
                )

            else:

                st.error(
                    "❌ Candidate is not qualified for the Final Manager Interview."
                )

            st.info(
                "➡️ Next Module: Final Manager Interview"
            )