import streamlit as st

from utils.database import (
    get_all_candidates,
    get_job
)


def show():

    st.title("🎉 Offer Letter")

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
    # Job Details
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
    # Offer Details
    # ==========================================

    st.subheader("📄 Offer Details")

    c1, c2 = st.columns(2)

    with c1:

        employee_id = st.text_input(
            "Employee ID",
            value="EMP1001"
        )

        designation = st.text_input(
            "Designation",
            value=job["job_title"]
        )

        salary = st.text_input(
            "Annual Salary",
            value="₹8,00,000"
        )

    with c2:

        joining_date = st.date_input(
            "Joining Date"
        )

        department = st.text_input(
            "Department",
            value=job["department"]
        )

        work_location = st.text_input(
            "Work Location",
            value=job["location"]
        )

    employment_type = st.selectbox(

        "Employment Type",

        [

            "Full-Time",

            "Intern",

            "Contract"

        ]

    )

    st.divider()



    # ==========================================
    # AI Offer Letter
    # ==========================================

    st.subheader("🤖 AI Offer Letter")

    if st.button(
        "Generate Offer Letter",
        use_container_width=True
    ):

        from models.offer_letter_ai import generate_offer_letter

        with st.spinner("Generating Offer Letter..."):

            offer = generate_offer_letter(

                candidate["name"],
                designation,
                employee_id,
                salary,
                joining_date,
                department,
                work_location,
                employment_type

            )

        st.session_state["offer_letter"] = offer

        st.success("Offer Letter Generated Successfully!")

    if "offer_letter" in st.session_state:

        st.text_area(

            "Offer Letter",

            st.session_state["offer_letter"],

            height=400

        )



    # ==========================================
    # Offer Status
    # ==========================================

    offer_status = st.selectbox(

        "Offer Status",

        [

            "Draft",

            "Sent",

            "Accepted",

            "Rejected"

        ]

    )

    hr_notes = st.text_area(
        "HR Notes"
    )

    if st.button(
        "💾 Save Offer",
        use_container_width=True
    ):

        from utils.database import save_offer_status

        save_offer_status(

            candidate["id"],

            employee_id,

            designation,

            salary,

            str(joining_date),

            department,

            work_location,

            employment_type,

            offer_status,

            hr_notes

        )

        st.success("✅ Offer Letter Saved Successfully!")

        st.balloons()