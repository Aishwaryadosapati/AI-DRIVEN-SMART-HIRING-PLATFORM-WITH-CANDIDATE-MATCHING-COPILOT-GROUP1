import streamlit as st

from utils.database import (
    get_all_candidates,
    get_all_jobs
)

from models.skill_gap_ai import analyze_skill_gap
from utils.skill_gap_parser import parse_skill_gap


def show():

    st.title("📚 Skill Gap Analysis")

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

    resume_text = candidate["resume_text"]

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
            resume_text,
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

    with st.expander("📄 Job Description"):

        st.write(job["description"])

    st.divider()

    # ==========================================
    # Skill Gap Analysis
    # ==========================================

    if st.button(
        "📚 Analyze Skill Gap",
        use_container_width=True
    ):

        with st.spinner("Analyzing Skill Gap..."):

            result = analyze_skill_gap(
                resume_text,
                job["description"]
            )

        parsed = parse_skill_gap(result)

        st.success("✅ Skill Gap Analysis Completed")

        # ==========================================
        # Missing Skills
        # ==========================================

        st.subheader("❌ Missing Skills")

        missing = parsed["missing_skills"]

        if len(missing) > 0:

            cols = st.columns(3)

            for i, skill in enumerate(missing):

                cols[i % 3].error(skill)

        else:

            st.success("No missing skills found.")

        st.divider()

        # ==========================================
        # Existing Skills
        # ==========================================

        st.subheader("✅ Existing Skills")

        existing = parsed["existing_skills"]

        if len(existing) > 0:

            cols = st.columns(3)

            for i, skill in enumerate(existing):

                cols[i % 3].success(skill)

        else:

            st.info("No skills identified.")

        st.divider()

        # ==========================================
        # Recommended Courses
        # ==========================================

        st.subheader("🎓 Recommended Learning")

        st.info(parsed["courses"])

        st.divider()

        # ==========================================
        # Improvement Tips
        # ==========================================

        st.subheader("💡 Improvement Suggestions")

        st.info(parsed["suggestions"])

        st.divider()

        # ==========================================
        # Skill Gap Summary
        # ==========================================

        st.subheader("📊 Skill Gap Summary")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Existing Skills",
            len(existing)
        )

        col2.metric(
            "Missing Skills",
            len(missing)
        )

        completion = 0

        if len(existing) + len(missing) > 0:

            completion = round(
                len(existing)
                /
                (len(existing) + len(missing))
                * 100
            )

        col3.metric(
            "Skill Match",
            f"{completion}%"
        )

        st.progress(completion / 100)

        st.divider()

        # ==========================================
        # AI Recommendation
        # ==========================================

        st.subheader("🤖 AI Recommendation")

        if completion >= 90:

            st.success("🌟 Candidate is job-ready.")

        elif completion >= 75:

            st.success("✅ Candidate needs minor upskilling.")

        elif completion >= 60:

            st.warning("⚠ Candidate requires moderate upskilling.")

        else:

            st.error("❌ Candidate requires significant skill development.")

        st.divider()

        # ==========================================
        # Next Steps
        # ==========================================

        st.subheader("🚀 Next Steps")

        if completion >= 75:

            st.success(
                "Candidate can proceed to Hiring Recommendation."
            )

        else:

            st.info(
                "Complete recommended courses before proceeding."
            )

        st.divider()

        st.success("🎉 Skill Gap Analysis Completed Successfully!")