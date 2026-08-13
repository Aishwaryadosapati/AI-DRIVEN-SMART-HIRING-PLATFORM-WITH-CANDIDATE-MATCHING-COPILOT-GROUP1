import streamlit as st

from utils.database import (
    get_all_candidates,
    get_all_jobs
)

from models.resume_matching_ai import match_resume
from utils.matching_parser import parse_matching


def show():

    st.title("🎯 Resume Matching")

    # ==========================================
    # Resume Source
    # ==========================================

    option = st.radio(
        "Choose Resume Source",
        [
            "📤 Upload New Resume",
            "👤 Existing Candidate"
        ],
        horizontal=True
    )

    resume_text = ""
    selected_candidate = None

    # ==========================================
    # Uploaded Resume
    # ==========================================

    if option == "📤 Upload New Resume":

        if "resume_text" not in st.session_state:
            st.warning("Please upload a resume first.")
            return

        resume_text = st.session_state["resume_text"]

        st.success("✅ Resume loaded from Resume Upload.")

    # ==========================================
    # Existing Candidate
    # ==========================================

    else:

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

        selected_candidate = next(
            candidate
            for candidate in candidates
            if candidate["name"] == selected_name
        )

        resume_text = selected_candidate["resume_text"]

        st.subheader("👤 Candidate Details")

        col1, col2 = st.columns(2)

        with col1:

            st.write("**Name:**", selected_candidate["name"])
            st.write("**Email:**", selected_candidate["email"])
            st.write("**Phone:**", selected_candidate["phone"])

        with col2:

            st.write("**Location:**", selected_candidate["location"])
            st.write("**ATS Score:**", selected_candidate["resume_score"])
            st.write("**Status:**", selected_candidate["candidate_status"])

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

    st.subheader("💼 Select Job")

    jobs = get_all_jobs()

    if len(jobs) == 0:
        st.warning("No jobs available.")
        return

    job_options = {
        f"{job['job_title']} ({job['department']})": job
        for job in jobs
    }

    selected_job = st.selectbox(
        "Choose Job",
        list(job_options.keys())
    )

    job = job_options[selected_job]

    st.subheader("📌 Job Details")

    col1, col2 = st.columns(2)

    with col1:

        st.write("**Job Title:**", job["job_title"])
        st.write("**Department:**", job["department"])
        st.write("**Location:**", job["location"])
        st.write("**Experience:**", job["experience"])

    with col2:

        st.write("**Employment Type:**", job["employment_type"])
        st.write("**Minimum ATS:**", job["minimum_ats_score"])
        st.write("**Openings:**", job["openings"])
        st.write("**Salary:**", job["salary"])
        st.write("**Status:**", job["status"])

    st.write("### 🛠 Required Skills")
    st.info(job["skills"])

    with st.expander("📄 Job Description"):

        st.write(job["description"])

    st.divider()

    # ==========================================
    # Resume Matching
    # ==========================================

    if st.button(
        "🎯 Match Resume",
        use_container_width=True
    ):

        with st.spinner("Matching Resume with Job Description..."):

            result = match_resume(
                resume_text,
                job["description"]
            )

        parsed = parse_matching(result)

        st.success("✅ Resume Matching Completed Successfully")

        match_score = parsed["score"]

        st.metric(
            "🎯 Match Score",
            f"{match_score}%"
        )

        # ==========================================
        # Match Progress
        # ==========================================

        st.progress(match_score / 100)

        st.divider()

        # ==========================================
        # Matched Skills
        # ==========================================

        st.subheader("✅ Matched Skills")

        matched = parsed["matched"]

        if len(matched) > 0:

            cols = st.columns(3)

            for i, skill in enumerate(matched):

                cols[i % 3].success(skill)

        else:

            st.info("No matched skills found.")

        st.divider()

        # ==========================================
        # Missing Skills
        # ==========================================

        st.subheader("❌ Missing Skills")

        missing = parsed["missing"]

        if len(missing) > 0:

            cols = st.columns(3)

            for i, skill in enumerate(missing):

                cols[i % 3].error(skill)

        else:

            st.success("No missing skills found.")

        st.divider()

        # ==========================================
        # AI Suggestions
        # ==========================================

        st.subheader("💡 AI Suggestions")

        st.info(parsed["suggestions"])

        st.divider()

        # ==========================================
        # Match Summary
        # ==========================================

        st.subheader("📊 Match Summary")

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Matched Skills",
            len(matched)
        )

        c2.metric(
            "Missing Skills",
            len(missing)
        )

        c3.metric(
            "Match Score",
            f"{match_score}%"
        )


        # ==========================================
        # Hiring Decision
        # ==========================================

        st.divider()

        st.subheader("🤖 AI Hiring Decision")

        if match_score >= 90:

            st.success("🌟 Excellent Match")
            st.success("Recommendation: Strongly Recommended")

        elif match_score >= 75:

            st.success("✅ Good Match")
            st.info("Recommendation: Recommended")

        elif match_score >= 60:

            st.warning("⚠ Average Match")
            st.warning("Recommendation: Consider After Upskilling")

        else:

            st.error("❌ Poor Match")
            st.error("Recommendation: Not Recommended")

        # ==========================================
        # Match Statistics
        # ==========================================

        st.divider()

        st.subheader("📈 Match Statistics")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Match Score",
            f"{match_score}%"
        )

        if match_score >= job["minimum_ats_score"]:

            st.success(
                f"✅ Candidate cleared ATS Cutoff ({job['minimum_ats_score']}%)"
            )

        else:

            st.error(
                f"❌ Candidate failed ATS Cutoff ({job['minimum_ats_score']}%)"
            )

        
        col2.metric(
            "Matched Skills",
            len(matched)
        )

        col3.metric(
            "Missing Skills",
            len(missing)
        )

        col4.metric(
            "Required Skills",
            len(matched) + len(missing)
        )

        # ==========================================
        # Next Steps
        # ==========================================

        st.divider()

        st.subheader("🚀 Next Steps")

        if match_score >= job["minimum_ats_score"]:

            st.success(
                "✅ Candidate meets the minimum ATS requirement."
            )

            st.info(
    "➡️ Next Step: Candidate Ranking → Hiring Recommendation → Interview Management"
)

        else:

            st.error(
                "❌ Candidate does not meet the minimum ATS requirement."
            )

            st.info(
    "➡️ Review Skill Gap Analysis and improve missing skills before continuing."
)
        # ==========================================
        # Resume Matching Completed
        # ==========================================

        st.divider()

        st.success("🎉 Resume Matching Completed Successfully!")

        st.divider()

        st.subheader("📋 Final Summary")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Match Score",
            f"{match_score}%"
        )

        col2.metric(
            "Matched Skills",
            len(matched)
        )

        col3.metric(
            "Missing Skills",
            len(missing)
        )

        col4.metric(
            "Qualification",
            "Qualified"
            if match_score >= job["minimum_ats_score"]
            else "Not Qualified"
        )