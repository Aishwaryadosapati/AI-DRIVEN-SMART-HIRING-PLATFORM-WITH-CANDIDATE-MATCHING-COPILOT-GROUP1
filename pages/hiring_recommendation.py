import streamlit as st

from utils.database import (
    get_all_candidates,
    get_all_jobs
)

from models.hiring_recommendation_ai import generate_hiring_recommendation
from utils.hiring_parser import parse_hiring_recommendation


def show():

    st.title("🤖 AI Hiring Recommendation")

    # ==========================================
    # Select Candidate
    # ==========================================

    candidates = get_all_candidates()

    if len(candidates) == 0:
        st.warning("No candidates available.")
        return

    candidate_names = [
        candidate["name"]
        for candidate in candidates
    ]

    selected_name = st.selectbox(
        "👤 Select Candidate",
        candidate_names
    )

    candidate = next(
        c for c in candidates
        if c["name"] == selected_name
    )

    st.subheader("👤 Candidate Details")

    col1, col2 = st.columns(2)

    with col1:

        st.write("**Name:**", candidate["name"])
        st.write("**Email:**", candidate["email"])
        st.write("**Phone:**", candidate["phone"])

    with col2:

        st.write("**Location:**", candidate["location"])
        st.write("**ATS Score:**", candidate["resume_score"])
        st.write("**Status:**", candidate["candidate_status"])

    with st.expander("📄 Resume Preview"):

        st.text_area(
            "Resume",
            candidate["resume_text"],
            height=250,
            disabled=True
        )

    # ==========================================
    # Select Job
    # ==========================================

    st.divider()

    jobs = get_all_jobs()

    if len(jobs) == 0:
        st.warning("No jobs available.")
        return

    job_options = {
        f"{job['job_title']} ({job['department']})": job
        for job in jobs
    }

    selected_job = st.selectbox(
        "💼 Select Job",
        list(job_options.keys())
    )

    job = job_options[selected_job]

    st.subheader("📌 Job Details")

    col1, col2 = st.columns(2)

    with col1:

        st.write("**Job Title:**", job["job_title"])
        st.write("**Department:**", job["department"])
        st.write("**Experience:**", job["experience"])

    with col2:

        st.write("**Location:**", job["location"])
        st.write("**Minimum ATS:**", job["minimum_ats_score"])
        st.write("**Status:**", job["status"])

    st.write("### 🛠 Required Skills")

    st.info(job["skills"])

    st.divider()

    # ==========================================
    # Generate Recommendation
    # ==========================================

    if st.button(
        "🤖 Generate Recommendation",
        use_container_width=True
    ):

        with st.spinner("Generating AI Recommendation..."):

            response = generate_hiring_recommendation(
                candidate["resume_text"],
                job["description"]
            )

        parsed = parse_hiring_recommendation(response)

        st.success("✅ Recommendation Generated Successfully")

        st.divider()

        # ==========================================
        # Hiring Decision
        # ==========================================

        st.subheader("🎯 Hiring Decision")

        decision = parsed["decision"]

        if decision.lower() == "hire":

            st.success("✅ HIRE")

        elif decision.lower() == "hold":

            st.warning("⏳ HOLD")

        else:

            st.error("❌ REJECT")

        # ==========================================
        # Reason
        # ==========================================

        st.subheader("📝 Reason")

        st.info(parsed["reason"])

        # ==========================================
        # Strengths
        # ==========================================

        st.subheader("💪 Candidate Strengths")

        for skill in parsed["strengths"]:

            st.success(skill)

        # ==========================================
        # Weaknesses
        # ==========================================

        st.subheader("⚠ Areas to Improve")

        for skill in parsed["weaknesses"]:

            st.error(skill)

        # ==========================================
        # Interview Questions
        # ==========================================

        st.subheader("🎤 Suggested Interview Questions")

        for question in parsed["questions"]:

            st.write("•", question)

        # ==========================================
        # Final Summary
        # ==========================================

        st.divider()

        st.subheader("📊 Hiring Summary")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "ATS Score",
            f"{candidate['resume_score']}%"
        )

        col2.metric(
            "Decision",
            decision
        )

        col3.metric(
            "Strengths",
            len(parsed["strengths"])
        )

        st.divider()

        if decision.lower() == "hire":

            st.success(
                "🚀 Candidate is ready to move to Interview Management."
            )

        elif decision.lower() == "hold":

            st.warning(
                "📚 Candidate should improve missing skills before proceeding."
            )

        else:

            st.error(
                "❌ Candidate is not suitable for this position."
            )

        st.divider()

        st.success("🎉 Hiring Recommendation Completed Successfully!")