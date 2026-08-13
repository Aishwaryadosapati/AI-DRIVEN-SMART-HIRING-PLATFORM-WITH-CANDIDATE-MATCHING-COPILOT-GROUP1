import streamlit as st

from utils.database import (
    get_all_candidates,
    get_job
)


def show():

    st.title("👋 Welcome Email")

    # ==========================================
    # Select Employee
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

        "👤 Select Employee",

        list(candidate_options.keys())

    )

    candidate = candidate_options[selected]

    st.divider()

    # ==========================================
    # Candidate Details
    # ==========================================

    st.subheader("👤 Employee Information")

    c1, c2 = st.columns(2)

    with c1:

        st.write("**Name:**", candidate["name"])
        st.write("**Email:**", candidate["email"])
        st.write("**Phone:**", candidate["phone"])

    with c2:

        st.write("**ATS Score:**", candidate["resume_score"])
        st.write("**Status:**", candidate["candidate_status"])

    st.divider()

    job = get_job(candidate["job_id"])

    st.subheader("💼 Job Details")

    c1, c2 = st.columns(2)

    with c1:

        st.write("**Designation:**", job["job_title"])
        st.write("**Department:**", job["department"])

    with c2:

        st.write("**Location:**", job["location"])
        st.write("**Employment Type:**", job["employment_type"])

    st.divider()



    # ==========================================
    # Welcome Details
    # ==========================================

    st.subheader("🎉 Welcome Details")

    c1, c2 = st.columns(2)

    with c1:

        employee_id = st.text_input(
            "Employee ID",
            value="EMP1001"
        )

        joining_date = st.date_input(
            "Joining Date"
        )

        reporting_manager = st.text_input(
            "Reporting Manager"
        )

    with c2:

        work_location = st.text_input(
            "Work Location",
            value=job["location"]
        )

        reporting_time = st.time_input(
            "Reporting Time"
        )

        dress_code = st.selectbox(

            "Dress Code",

            [

                "Business Formal",

                "Business Casual",

                "Smart Casual"

            ]

        )

    documents = st.multiselect(

        "Documents to Carry",

        [

            "Aadhaar",

            "PAN",

            "Passport",

            "Educational Certificates",

            "Offer Letter",

            "Bank Passbook",

            "Passport Size Photos"

        ]

    )

    st.divider()


    # ==========================================
    # AI Welcome Email
    # ==========================================

    st.subheader("🤖 AI Welcome Email")

    if st.button(

        "Generate Welcome Email",

        use_container_width=True

    ):

        from models.welcome_email_ai import generate_welcome_email

        with st.spinner("Generating Welcome Email..."):

            email = generate_welcome_email(

                candidate["name"],

                employee_id,

                job["job_title"],

                joining_date,

                reporting_manager,

                reporting_time,

                work_location,

                ", ".join(documents)

            )

        st.session_state["welcome_email"] = email

        st.success("Welcome Email Generated Successfully!")

    if "welcome_email" in st.session_state:

        st.text_area(

            "Welcome Email",

            st.session_state["welcome_email"],

            height=350

        )

    st.divider()



    # ==========================================
    # Welcome Status
    # ==========================================

    welcome_status = st.selectbox(

        "Email Status",

        [

            "Draft",

            "Sent"

        ]

    )

    hr_notes = st.text_area(
        "HR Notes"
    )

    if st.button(

        "💾 Save Welcome Email",

        use_container_width=True

    ):

        from utils.database import save_welcome_status

        save_welcome_status(

            candidate["id"],

            employee_id,

            str(joining_date),

            reporting_manager,

            work_location,

            welcome_status,

            hr_notes

        )

        st.success(
            "Welcome Email Saved Successfully!"
        )

        st.balloons()

        st.subheader("📊 Welcome Dashboard")

        c1, c2 = st.columns(2)

        with c1:

            st.metric("Employee", candidate["name"])
            st.metric("Employee ID", employee_id)
            st.metric("Status", welcome_status)

        with c2:

            st.metric("Joining Date", str(joining_date))
            st.metric("Manager", reporting_manager)
            st.metric("Location", work_location)

        st.divider()

        st.success("🎉 Welcome Email Module Completed Successfully!")
