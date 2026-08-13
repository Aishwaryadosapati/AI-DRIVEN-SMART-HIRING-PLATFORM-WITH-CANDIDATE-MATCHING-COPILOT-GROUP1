import streamlit as st

from models.job_description_ai import generate_job_description

from utils.database import (
    add_job,
    get_all_jobs,
    delete_job,
    get_candidates_by_job
)


def show():

    st.title("💼 Job Management")

    tab1, tab2 = st.tabs([
        "➕ Create Job",
        "📋 Job Applications"
    ])

    # =====================================================
    # TAB 1 - CREATE JOB
    # =====================================================

    with tab1:

        st.subheader("➕ Create New Job")

        job_title = st.text_input("Job Title")

        department = st.text_input("Department")

        location = st.text_input("Location")

        experience = st.selectbox(
            "Experience",
            [
                "Fresher",
                "1-2 Years",
                "3-5 Years",
                "5+ Years"
            ]
        )

        employment_type = st.selectbox(
            "Employment Type",
            [
                "Full Time",
                "Part Time",
                "Internship",
                "Contract"
            ]
        )

        salary = st.text_input("Salary")

        minimum_ats_score = st.slider(
            "Minimum ATS Score",
            min_value=0,
            max_value=100,
            value=80
        )

        openings = st.number_input(
            "Number of Openings",
            min_value=1,
            value=1
        )

        skills = st.text_area(
            "Required Skills"
        )

        if "generated_description" not in st.session_state:
            st.session_state.generated_description = ""

        if st.button("🤖 Generate Job Description"):

            if job_title == "":
                st.warning("Please enter Job Title.")

            elif skills == "":
                st.warning("Please enter Required Skills.")

            else:

                with st.spinner("Generating Job Description..."):

                    st.session_state.generated_description = generate_job_description(
                        job_title,
                        department,
                        experience,
                        skills
                    )

        description = st.text_area(
            "Job Description",
            value=st.session_state.generated_description,
            height=300
        )

        if st.session_state.generated_description:

            st.subheader("📄 AI Generated Preview")

            st.info(
                st.session_state.generated_description
            )

        status = st.selectbox(
            "Status",
            [
                "Open",
                "Closed"
            ]
        )

        # ==========================================
        # Create Job
        # ==========================================

        if st.button("💾 Create Job"):

            if job_title == "":
                st.warning("Please enter Job Title.")

            elif skills == "":
                st.warning("Please enter Required Skills.")

            elif description == "":
                st.warning("Please generate or enter Job Description.")

            else:

                add_job(
                    job_title,
                    department,
                    location,
                    experience,
                    employment_type,
                    salary,
                    skills,
                    description,
                    minimum_ats_score,
                    openings,
                    status
                )

                st.success("✅ Job Created Successfully")

                st.balloons()

                st.session_state.generated_description = ""

                st.rerun()

    # =====================================================
    # TAB 2 - JOB APPLICATIONS
    # =====================================================

    with tab2:

        st.subheader("📋 Job Applications")

        jobs = get_all_jobs()


        unique_jobs = len({job["job_title"] for job in jobs})

        st.metric("📊 Total Jobs", unique_jobs)

        if len(jobs) == 0:
            st.info("No Jobs Available")
            return

        job_options = {
            f"{job['job_title']} ({job['department']})": job
            for job in jobs
        }

        selected_job = st.selectbox(
            "Select Job",
            list(job_options.keys())
        )

        job = job_options[selected_job]

        # ==========================================
        # Job Details
        # ==========================================

        st.divider()

        st.subheader("📌 Job Details")

        col1, col2 = st.columns(2)

        with col1:
            st.write(f"**Department:** {job['department']}")
            st.write(f"**Location:** {job['location']}")
            st.write(f"**Experience:** {job['experience']}")
            st.write(f"**Employment Type:** {job['employment_type']}")

        with col2:
            st.write(f"**Salary:** {job['salary']}")
            st.write(f"**Minimum ATS Score:** {job['minimum_ats_score']}")
            st.write(f"**Openings:** {job['openings']}")
            st.write(f"**Status:** {job['status']}")

        st.write("### 🛠 Required Skills")
        st.info(job["skills"])

        st.write("### 📄 Job Description")
        st.write(job["description"])

        # ==========================================
        # Candidate Statistics
        # ==========================================

        st.divider()

        candidates = get_candidates_by_job(job["id"])

        applications = len(candidates)

        shortlisted = len([
            c for c in candidates
            if c["candidate_status"] == "Shortlisted"
        ])

        rejected = len([
            c for c in candidates
            if c["candidate_status"] == "Rejected"
        ])

        interview = len([
            c for c in candidates
            if c["candidate_status"] == "Interview Scheduled"
        ])

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("📄 Applications", applications)
        c2.metric("✅ Shortlisted", shortlisted)
        c3.metric("❌ Rejected", rejected)
        c4.metric("📅 Interview", interview)

        # ==========================================
        # Applicants
        # ==========================================

        st.divider()

        st.subheader("👥 Applicants")

        if len(candidates) == 0:

            st.info("No applications received for this job.")

        else:

            h1, h2, h3, h4 = st.columns([3, 2, 2, 3])

            h1.markdown("**Candidate**")
            h2.markdown("**ATS Score**")
            h3.markdown("**Status**")
            h4.markdown("**Email**")

            st.markdown("---")

            for candidate in candidates:

                c1, c2, c3, c4 = st.columns([3, 2, 2, 3])

                c1.write(candidate["name"])
                c2.write(candidate["resume_score"])
                c3.write(candidate["candidate_status"])
                c4.write(candidate["email"])

                b1, b2 = st.columns(2)

                with b1:

                    if st.button(
                        "👤 View Profile",
                        key=f"profile_{candidate['id']}"
                    ):

                        st.session_state.selected_candidate = candidate["id"]

                        st.success(
                            f"{candidate['name']} profile selected."
                        )

                with b2:

                    if st.button(
                        "📅 Schedule Interview",
                        key=f"interview_{candidate['id']}"
                    ):

                        st.session_state.selected_candidate = candidate["id"]

                        st.success(
                            f"Interview selected for {candidate['name']}."
                        )

                st.markdown("---")

        # ==========================================
        # Delete Job
        # ==========================================

        st.divider()

        col1, col2 = st.columns([1, 2])

        with col1:

            if st.button(
                "🗑 Delete Job",
                key=f"delete_{job['id']}"
            ):

                if applications > 0:

                    st.warning(
                        "This job has applications. Delete only if you are sure."
                    )

                else:

                    delete_job(job["id"])

                    st.success("✅ Job deleted successfully.")

                    st.rerun()

        with col2:

            st.info(f"Job ID : {job['id']}")