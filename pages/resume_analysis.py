import streamlit as st

from models.ai_resume_parser import ai_parse_resume
from utils.ai_response_parser import parse_ai_response
from utils.resume_parser import calculate_score, recommendation

from utils.database import (
    update_candidate_analysis,
    update_candidate_ats,
    get_candidate
)


def show():

    st.title("📄 Resume Analysis")

    if "resume_text" not in st.session_state:
        st.warning("Please upload a resume first.")
        return

    text = st.session_state["resume_text"]

    with st.spinner("🤖 AI is analyzing the resume..."):
        ai_response = ai_parse_resume(text)

    parsed = parse_ai_response(ai_response)

    # Save analysis
    st.session_state["resume_analysis"] = parsed

    # Calculate Resume Score
    score = calculate_score(
        parsed["skills"],
        parsed["education"],
        parsed["projects"],
        parsed["certifications"],
        parsed["experience"]
    )

    recommend = recommendation(score)

    # Candidate ID
    candidate_id = st.session_state.get("candidate_id")

    if candidate_id is None:
        st.error("Candidate not found. Please upload the resume again.")
        return

    # Save Resume Analysis
    rows = update_candidate_analysis(
        candidate_id,
        ",".join(parsed["skills"]),
        parsed["experience"],
        ",".join(parsed["education"]),
        ",".join(parsed["projects"]),
        ",".join(parsed["certifications"]),
        score,
        recommend
    )

    # Automatic ATS Screening
    update_candidate_ats(
        candidate_id,
        score
    )

    # Get updated candidate details
    candidate = get_candidate(candidate_id)

    if rows > 0:

        st.success("✅ Resume Analysis Completed Successfully")

        if candidate["candidate_status"] == "Shortlisted":
            st.success("🎉 Candidate Automatically Shortlisted")
        else:
            st.error("❌ Candidate Rejected (ATS Score below Job Cutoff)")

        st.info(
            "➡️ Next Step: Proceed to Interview Management."
        )

    else:
        st.error("❌ Candidate could not be updated.")

    st.divider()

    # ==========================
    # Candidate Details
    # ==========================

    col1, col2 = st.columns([2, 1])

    with col1:

        st.subheader("👤 Candidate Details")

        st.write("**Name:**", parsed["name"] or "Not Found")
        st.write("**Email:**", parsed["email"] or "Not Found")
        st.write("**Phone:**", parsed["phone"] or "Not Found")
        st.write("**Location:**", parsed["location"] or "Not Found")

    with col2:

        st.metric("Resume Score", f"{score}%")

        st.metric(
            "Candidate Status",
            candidate["candidate_status"]
        )

    st.divider()

    # ==========================
    # Skills
    # ==========================

    st.subheader("🛠 Technical Skills")

    if parsed["skills"]:

        cols = st.columns(3)

        for i, skill in enumerate(parsed["skills"]):
            cols[i % 3].success(skill)

    else:
        st.info("No skills detected.")

    st.divider()

    # ==========================
    # Education
    # ==========================

    st.subheader("🎓 Education")

    if parsed["education"]:

        for edu in parsed["education"]:
            st.write("•", edu)

    else:
        st.info("No education found.")

    st.divider()

    # ==========================
    # Experience
    # ==========================

    st.subheader("💼 Experience")

    if parsed["experience"]:
        st.info(parsed["experience"])
    else:
        st.info("No experience found.")

    st.divider()

    # ==========================
    # Projects
    # ==========================

    st.subheader("🚀 Projects")

    if parsed["projects"]:

        for project in parsed["projects"]:
            st.write("•", project)

    else:
        st.info("No projects found.")

    st.divider()

    # ==========================
    # Certifications
    # ==========================

    st.subheader("📜 Certifications")

    if parsed["certifications"]:

        for cert in parsed["certifications"]:
            st.write("•", cert)

    else:
        st.info("No certifications found.")

    st.divider()

    # ==========================
    # AI Summary
    # ==========================

    st.subheader("📝 AI Resume Summary")

    st.info(
        parsed["summary"]
        if parsed["summary"]
        else "Summary not available."
    )

    st.divider()

    # ==========================
    # Resume Preview
    # ==========================

    st.subheader("📄 Resume Preview")

    st.text_area(
        "Extracted Resume",
        text,
        height=300
    )

    import streamlit as st

from models.ai_resume_parser import ai_parse_resume
from utils.ai_response_parser import parse_ai_response
from utils.resume_parser import calculate_score, recommendation

from utils.database import (
    update_candidate_analysis,
    update_candidate_ats,
    get_candidate
)


def show():

    st.title("📄 Resume Analysis")

    if "resume_text" not in st.session_state:
        st.warning("Please upload a resume first.")
        return

    text = st.session_state["resume_text"]

    with st.spinner("🤖 AI is analyzing the resume..."):
        ai_response = ai_parse_resume(text)

    parsed = parse_ai_response(ai_response)

    # Save analysis
    st.session_state["resume_analysis"] = parsed

    # Calculate Resume Score
    score = calculate_score(
        parsed["skills"],
        parsed["education"],
        parsed["projects"],
        parsed["certifications"],
        parsed["experience"]
    )

    recommend = recommendation(score)

    # Candidate ID
    candidate_id = st.session_state.get("candidate_id")

    if candidate_id is None:
        st.error("Candidate not found. Please upload the resume again.")
        return

    # Save Resume Analysis
    rows = update_candidate_analysis(
        candidate_id,
        ",".join(parsed["skills"]),
        parsed["experience"],
        ",".join(parsed["education"]),
        ",".join(parsed["projects"]),
        ",".join(parsed["certifications"]),
        score,
        recommend
    )

    # Automatic ATS Screening
    update_candidate_ats(
        candidate_id,
        score
    )

    # Get updated candidate details
    candidate = get_candidate(candidate_id)

    if rows > 0:

        st.success("✅ Resume Analysis Completed Successfully")

        if candidate["candidate_status"] == "Shortlisted":
            st.success("🎉 Candidate Automatically Shortlisted")
        else:
            st.error("❌ Candidate Rejected (ATS Score below Job Cutoff)")

        st.info(
            "➡️ Next Step: Proceed to Interview Management."
        )

    else:
        st.error("❌ Candidate could not be updated.")

    st.divider()

    # ==========================
    # Candidate Details
    # ==========================

    col1, col2 = st.columns([2, 1])

    with col1:

        st.subheader("👤 Candidate Details")

        st.write("**Name:**", parsed["name"] or "Not Found")
        st.write("**Email:**", parsed["email"] or "Not Found")
        st.write("**Phone:**", parsed["phone"] or "Not Found")
        st.write("**Location:**", parsed["location"] or "Not Found")

    with col2:

        st.metric("Resume Score", f"{score}%")

        st.metric(
            "Candidate Status",
            candidate["candidate_status"]
        )

    st.divider()

    # ==========================
    # Skills
    # ==========================

    st.subheader("🛠 Technical Skills")

    if parsed["skills"]:

        cols = st.columns(3)

        for i, skill in enumerate(parsed["skills"]):
            cols[i % 3].success(skill)

    else:
        st.info("No skills detected.")

    st.divider()

    # ==========================
    # Education
    # ==========================

    st.subheader("🎓 Education")

    if parsed["education"]:

        for edu in parsed["education"]:
            st.write("•", edu)

    else:
        st.info("No education found.")

    st.divider()

    # ==========================
    # Experience
    # ==========================

    st.subheader("💼 Experience")

    if parsed["experience"]:
        st.info(parsed["experience"])
    else:
        st.info("No experience found.")

    st.divider()

    # ==========================
    # Projects
    # ==========================

    st.subheader("🚀 Projects")

    if parsed["projects"]:

        for project in parsed["projects"]:
            st.write("•", project)

    else:
        st.info("No projects found.")

    st.divider()

    # ==========================
    # Certifications
    # ==========================

    st.subheader("📜 Certifications")

    if parsed["certifications"]:

        for cert in parsed["certifications"]:
            st.write("•", cert)

    else:
        st.info("No certifications found.")

    st.divider()

    # ==========================
    # AI Summary
    # ==========================

    st.subheader("📝 AI Resume Summary")

    st.info(
        parsed["summary"]
        if parsed["summary"]
        else "Summary not available."
    )

    st.divider()

    # ==========================
    # Resume Preview
    # ==========================

    st.subheader("📄 Resume Preview")

    st.text_area(
        "Extracted Resume",
        text,
        height=300
    )

    st.subheader("Raw AI Response")
    st.code(ai_response)