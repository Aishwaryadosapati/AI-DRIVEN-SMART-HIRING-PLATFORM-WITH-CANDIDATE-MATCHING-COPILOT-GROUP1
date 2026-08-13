import os
import streamlit as st

from utils.database import (
    get_all_candidates,
    get_job
)


def show():

    st.title("👤 Candidate Profile")

    candidates = get_all_candidates()

    if len(candidates) == 0:

        st.warning("No candidates found.")

        return

    # ==========================================
    # Select Candidate
    # ==========================================

    candidate_options = {

        f"{c['name']} ({c['email']})": c

        for c in candidates

    }

    selected = st.selectbox(

        "Select Candidate",

        list(candidate_options.keys())

    )

    candidate = candidate_options[selected]

    st.divider()

    # ==========================================
    # Profile Header
    # ==========================================

    col1, col2 = st.columns([1, 3])

    with col1:

        st.image(

            "https://placehold.co/150x150?text=Profile",

            width=130

        )

    with col2:

        st.subheader(candidate["name"])

        st.write("📧 Email :", candidate["email"])

        st.write("📞 Phone :", candidate["phone"])

        st.write("📍 Location :", candidate["location"])

        st.write("🆔 Candidate ID :", candidate["id"])

    st.divider()

    # ==========================================
    # Resume Evaluation
    # ==========================================

    st.subheader("📊 Resume Evaluation")

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(

            "ATS Score",

            f"{candidate['resume_score']}%"

        )

    with c2:

        st.metric(

            "Status",

            candidate["candidate_status"]

        )

    with c3:

        recommendation = candidate.get(
            "recommendation",
            ""
        )

        if recommendation == "Shortlisted":

            st.success("✅ Shortlisted")

        elif recommendation == "Rejected":

            st.error("❌ Rejected")

        else:

            st.info(recommendation)

    st.progress(candidate["resume_score"] / 100)

    st.divider()
    # ==========================================
    # Job Applied
    # ==========================================

    st.subheader("💼 Job Applied")

    job = get_job(candidate["job_id"])

    if job:

        col1, col2 = st.columns(2)

        with col1:

            st.write("**Job Title:**", job["job_title"])
            st.write("**Department:**", job["department"])
            st.write("**Location:**", job["location"])

        with col2:

            st.write("**Experience:**", job["experience"])
            st.write("**Employment Type:**", job["employment_type"])
            st.write("**Minimum ATS:**", job["minimum_ats_score"])

    else:

        st.warning("Job not found.")

    # ==========================================
    # Education
    # ==========================================

    st.subheader("🎓 Education")

    if candidate["education"]:

        education = [
            e.strip()
            for e in candidate["education"].split(",")
            if e.strip()
        ]

        for edu in education:

            st.write("•", edu)

    else:

        st.info("Education details not available.")

    st.divider()

    # ==========================================
    # Experience
    # ==========================================

    st.subheader("💼 Experience")

    if candidate["experience"]:

        st.info(candidate["experience"])

    else:

        st.info("Fresher")

    st.divider()

    # ==========================================
    # Technical Skills
    # ==========================================

    st.subheader("🛠 Technical Skills")

    if candidate["skills"]:

        skills = [
            s.strip()
            for s in candidate["skills"].split(",")
            if s.strip()
        ]

        cols = st.columns(3)

        for i, skill in enumerate(skills):

            cols[i % 3].success(skill)

    else:

        st.info("No technical skills available.")

    st.divider()

    # ==========================================
    # Projects
    # ==========================================

    st.subheader("🚀 Projects")

    if candidate["projects"]:

        projects = [
            p.strip()
            for p in candidate["projects"].split(",")
            if p.strip()
        ]

        for project in projects:

            st.write("•", project)

    else:

        st.info("No projects available.")

    st.divider()

    # ==========================================
    # Certifications
    # ==========================================

    st.subheader("📜 Certifications")

    if candidate["certifications"]:

        certifications = [
            c.strip()
            for c in candidate["certifications"].split(",")
            if c.strip()
        ]

        for cert in certifications:

            st.success(cert)

    else:

        st.info("No certifications available.")

    st.divider()

    # ==========================================
    # AI Resume Summary
    # ==========================================

    st.subheader("📝 AI Resume Summary")

    if "resume_analysis" in st.session_state:

        summary = st.session_state["resume_analysis"].get(
            "summary",
            "Summary Not Available"
        )

        st.info(summary)

    else:

        st.info("Resume summary not available.")

    st.divider()

    # ==========================================
    # Resume Preview
    # ==========================================

    st.subheader("📄 Resume Preview")

    if candidate["resume_text"]:

        st.text_area(
            "Resume Content",
            candidate["resume_text"],
            height=300,
            disabled=True
        )

    else:

        st.info("Resume not available.")

    st.divider()

    # ==========================================
    # Candidate Statistics
    # ==========================================

    st.subheader("📊 Candidate Statistics")

    word_count = len(candidate["resume_text"].split()) \
        if candidate["resume_text"] else 0

    skill_count = len([
        s for s in candidate["skills"].split(",")
        if s.strip()
    ]) if candidate["skills"] else 0

    project_count = len([
        p for p in candidate["projects"].split(",")
        if p.strip()
    ]) if candidate["projects"] else 0

    cert_count = len([
        c for c in candidate["certifications"].split(",")
        if c.strip()
    ]) if candidate["certifications"] else 0

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Resume Words",
        word_count
    )

    c2.metric(
        "Skills",
        skill_count
    )

    c3.metric(
        "Projects",
        project_count
    )

    c4.metric(
        "Certificates",
        cert_count
    )

    st.divider()

    # ==========================================
    # Recruitment Timeline
    # ==========================================

    st.subheader("📅 Recruitment Timeline")

    st.success("✅ Resume Uploaded")

    if candidate["resume_score"]:

        st.success("✅ Resume Analyzed")

    if candidate["candidate_status"] == "Shortlisted":

        st.success("✅ ATS Shortlisted")

    elif candidate["candidate_status"] == "Interview Scheduled":

        st.success("✅ ATS Shortlisted")
        st.success("📅 Interview Scheduled")

    elif candidate["candidate_status"] == "Rejected":

        st.error("❌ Rejected")

    st.divider()

    # ==========================================
    # Recruiter Insights
    # ==========================================

    st.subheader("🤖 Recruiter Insights")

    if candidate["resume_score"] >= 90:

        st.success(
            "🌟 Excellent candidate with a very strong profile."
        )

    elif candidate["resume_score"] >= 80:

        st.success(
            "✅ Strong candidate recommended for interview."
        )

    elif candidate["resume_score"] >= 70:

        st.warning(
            "⚠ Candidate has potential but may need additional evaluation."
        )

    else:

        st.error(
            "❌ Candidate does not currently meet the preferred criteria."
        )

    st.divider()

    # ==========================================
    # Recruiter Actions
    # ==========================================

    st.subheader("⚡ Recruiter Actions")

    col1, col2, col3 = st.columns(3)

    with col1:

        if st.button(
            "📅 Schedule Interview",
            use_container_width=True
        ):

            st.session_state.selected_candidate = candidate["id"]

            st.success(
                "Candidate selected. Open Interview Management."
            )

    with col2:

        if st.button(
            "📧 Send Interview Email",
            use_container_width=True
        ):

            st.session_state.selected_candidate = candidate["id"]

            st.success(
                "Candidate selected. Open AI Communication."
            )

    with col3:

        if st.button(
            "🏆 View Ranking",
            use_container_width=True
        ):

            st.success(
                "Open Candidate Ranking module."
            )

    st.divider()

    # ==========================================
    # Download Resume
    # ==========================================

    st.subheader("⬇ Resume Download")

    if candidate["resume_path"] and os.path.exists(candidate["resume_path"]):

        with open(candidate["resume_path"], "rb") as file:

            st.download_button(

                "⬇ Download Resume",

                data=file,

                file_name=os.path.basename(
                    candidate["resume_path"]
                ),

                mime="application/pdf",

                use_container_width=True

            )

    else:

        st.warning("Resume file not found.")

    st.divider()

    # ==========================================
    # Final Profile Summary
    # ==========================================

    st.subheader("📋 Candidate Summary")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "ATS Score",
        f"{candidate['resume_score']}%"
    )

    c2.metric(
        "Status",
        candidate["candidate_status"]
    )

    c3.metric(
        "Candidate ID",
        candidate["id"]
    )

    st.progress(candidate["resume_score"] / 100)

    if candidate["candidate_status"] == "Shortlisted":

        st.success(
            "✅ Candidate is ready for the interview stage."
        )

    elif candidate["candidate_status"] == "Interview Scheduled":

        st.success(
            "📅 Interview has been scheduled."
        )

    elif candidate["candidate_status"] == "Rejected":

        st.error(
            "❌ Candidate was not shortlisted."
        )

    else:

        st.info(
            "Candidate is currently under review."
        )

    st.divider()

    st.success("🎉 Candidate Profile Loaded Successfully!")