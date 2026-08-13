import streamlit as st
from utils.database import (
    get_all_candidates,
    update_candidate_status,
    save_employee
)

def show():

    st.title("🎉 Employee Onboarding")

    candidates = get_all_candidates()

    if len(candidates) == 0:
        st.info("No candidates available.")
        return

    selected = st.selectbox(
        "Select Candidate",
        [c["name"] for c in candidates]
    )

    candidate = next(
        c for c in candidates
        if c["name"] == selected
    )

    st.divider()

    st.subheader("Employee Details")

    st.write("**Name:**", candidate["name"])
    st.write("**Email:**", candidate["email"])
    st.write("**Phone:**", candidate["phone"])
    st.write("**Location:**", candidate["location"])


# ==========================================
# Employee Information
# ==========================================

    st.divider()

    st.subheader("👨‍💼 Employee Information")

    col1, col2 = st.columns(2)

    with col1:

        employee_id = st.text_input(
            "Employee ID",
            value=f"EMP{candidate['id']:04d}"
        )

        designation = st.text_input(
            "Designation"
        )

        department = st.text_input(
            "Department"
        )

    with col2:

        manager = st.text_input(
            "Reporting Manager"
        )

        joining_date = st.date_input(
            "Joining Date"
        )

        emergency_contact = st.text_input(
            "Emergency Contact"
        )

    st.divider()

    st.subheader("📋 Onboarding Status")

    status = st.selectbox(
        "Status",
        [
            "Offer Accepted",
            "Documents Pending",
            "Documents Verified",
            "Joining Scheduled",
            "Joined"
        ]
    )

    st.success(f"Current Status: {status}")

    st.subheader("📂 Document Verification")

    pan = st.checkbox("PAN Card")
    aadhaar = st.checkbox("Aadhaar Card")
    degree = st.checkbox("Degree Certificate")
    photo = st.checkbox("Passport Photo")

    notes = st.text_area(
        "HR Notes"
    )  

    if st.button(
        "✅ Complete Onboarding",
        use_container_width=True
    ):

    # Save Employee Details
        save_employee(

        candidate["id"],

        employee_id,

        candidate["name"],

        candidate["email"],

        candidate["phone"],

        designation,

        department,

        manager,

        str(joining_date),

        candidate["location"],

        emergency_contact,

        "Active"

        )

    # Update Candidate Status
        update_candidate_status(

            candidate["id"],

            "Joined"

        )

        st.success("🎉 Employee Onboarding Completed Successfully!")

        st.balloons()


        st.divider()

        st.subheader("📊 Employee Summary")

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Employee ID",
                employee_id
            )

            st.metric(
                "Employee",
                candidate["name"]
            )

            st.metric(
                "Department",
                department
            )

        with col2:

            st.metric(
                "Designation",
                designation
            )

            st.metric(
                "Manager",
                manager
            )

            st.metric(
                "Status",
                "Active"
            )

        st.divider()

        st.subheader("📄 HR Notes")

        if notes.strip():

            st.info(notes)

        else:

            st.info("No HR notes added.")

        st.success(
            "Recruitment process completed successfully."
        )          
