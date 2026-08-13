import streamlit as st
import os
import re

from utils.pdf_parser import extract_text
from utils.database import (
    add_candidate,
    get_all_jobs
)


def show():

    st.title("📄 Resume Upload")

    # ==========================================
    # Select Job
    # ==========================================

    jobs = get_all_jobs()

    if len(jobs) == 0:

        st.warning(
            "⚠ Please create a Job first in Job Management."
        )

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

    job_id = job["id"]

    st.success(f"Selected Job : {job['job_title']}")

    st.subheader("📌 Job Details")

    col1, col2 = st.columns(2)

    with col1:

        st.write("**Department:**", job["department"])
        st.write("**Location:**", job["location"])
        st.write("**Experience:**", job["experience"])

    with col2:

        st.write(
            "**Employment Type:**",
            job["employment_type"]
        )

        st.write(
            "**Minimum ATS:**",
            job["minimum_ats_score"]
        )

        st.write(
            "**Openings:**",
            job["openings"]
        )

    st.write("### 🛠 Required Skills")

    st.info(job["skills"])

    with st.expander("📄 Job Description"):

        st.write(job["description"])

    st.divider()

    # ==========================================
    # Upload Resume
    # ==========================================

    uploaded_file = st.file_uploader(
        "📤 Upload Resume",
        type=["pdf"]
    )

    if uploaded_file is not None:

        os.makedirs(
            "data/resumes",
            exist_ok=True
        )

        file_path = os.path.join(
            "data/resumes",
            uploaded_file.name
        )

        with open(file_path, "wb") as f:

            f.write(
                uploaded_file.getbuffer()
            )

        st.success(
            f"📁 File Uploaded : {uploaded_file.name}"
        )

        st.session_state["resume_path"] = file_path

        resume_text = extract_text(file_path)

        st.session_state["resume_text"] = resume_text


        # ==========================================
        # Extract Email
        # ==========================================

        email = ""

        email_match = re.search(
            r'[\w\.-]+@[\w\.-]+\.\w+',
            resume_text
        )

        if email_match:

            email = email_match.group()

        # ==========================================
        # Extract Phone
        # ==========================================

        phone = ""

        phone_match = re.search(
            r'(\+91[- ]?)?[6-9]\d{9}',
            resume_text
        )

        if phone_match:

            phone = phone_match.group()

        # ==========================================
        # Extract Name
        # ==========================================

        name = "Unknown"

        lines = resume_text.split("\n")

        for line in lines[:10]:

            line = line.strip()

            if (
                len(line) > 3
                and
                len(line.split()) <= 4
                and
                "resume" not in line.lower()
            ):

                name = line
                break

        # ==========================================
        # Location
        # ==========================================

        location = "Not Available"

        # ==========================================
        # Candidate Information
        # ==========================================

        st.subheader("👤 Candidate Information")

        col1, col2 = st.columns(2)

        with col1:

            st.write("**Name:**", name)
            st.write("**Email:**", email)

        with col2:

            st.write("**Phone:**", phone)
            st.write("**Location:**", location)

        st.divider()

        # ==========================================
        # Resume Statistics
        # ==========================================

        word_count = len(resume_text.split())

        character_count = len(resume_text)

        col1, col2 = st.columns(2)

        col1.metric(
            "Words",
            word_count
        )

        col2.metric(
            "Characters",
            character_count
        )

        st.progress(0.25)

        st.success("✅ Step 1 of 4 Completed")

        # ==========================================
        # Save Candidate
        # ==========================================

        candidate_id = add_candidate(
            job_id=job_id,
            name=name,
            email=email,
            phone=phone,
            location=location,
            resume_path=file_path,
            resume_text=resume_text
        )

        st.session_state["candidate_id"] = candidate_id

        # ==========================================
        # Upload Summary
        # ==========================================

        st.divider()

        st.subheader("📊 Upload Summary")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Candidate ID",
            candidate_id
        )

        col2.metric(
            "Applied Job",
            job["job_title"]
        )

        col3.metric(
            "Status",
            "Applied"
        )

        st.success("✅ Resume Uploaded Successfully")

        st.success("✅ Candidate Saved Successfully")

        st.progress(0.50)

        st.success("✅ Step 2 of 4 Completed")

        # ==========================================
        # Next Step
        # ==========================================

        st.info(
            "➡️ Next Step: Resume Analysis"
        )

        st.divider()

        # ==========================================
        # Resume Preview
        # ==========================================

        st.subheader("📄 Resume Preview")

        st.text_area(
            "Extracted Resume",
            resume_text,
            height=350,
            disabled=True
        )

        # ==========================================
        # Download Resume
        # ==========================================

        st.divider()

        st.subheader("⬇ Download Resume")

        with open(file_path, "rb") as file:

            st.download_button(
                label="⬇ Download Uploaded Resume",
                data=file,
                file_name=uploaded_file.name,
                mime="application/pdf",
                use_container_width=True
            )

        # ==========================================
        # Final Summary
        # ==========================================

        st.divider()

        st.subheader("📋 Upload Summary")

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Resume File",
                uploaded_file.name
            )

            st.metric(
                "Applied Job",
                job["job_title"]
            )

        with col2:

            st.metric(
                "Candidate ID",
                candidate_id
            )

            st.metric(
                "Application Status",
                "Applied"
            )

        st.progress(1.0)

        st.success("✅ Step 4 of 4 Completed")

        st.balloons()

        st.success("🎉 Resume Upload Completed Successfully!")

        st.info(
            "➡️ Continue to the Resume Analysis module to analyze the uploaded resume and calculate the ATS score."
        )