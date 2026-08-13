import streamlit as st

from utils.database import (
    get_all_candidates,
    get_job
)


def show():

    st.title("❌ Rejection Email")

    candidates = get_all_candidates()

    if len(candidates) == 0:

        st.warning("No candidates available.")

        return

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

    st.subheader("Candidate Details")

    c1, c2 = st.columns(2)

    with c1:

        st.write("Name:", candidate["name"])
        st.write("Email:", candidate["email"])

    with c2:

        st.write("ATS Score:", candidate["resume_score"])
        st.write("Status:", candidate["candidate_status"])

    job = get_job(candidate["job_id"])

    st.divider()

    st.subheader("Job Details")

    st.write("Job Title:", job["job_title"])
    st.write("Department:", job["department"])

    st.divider()



    st.subheader("Rejection Details")

    rejection_reason = st.selectbox(

        "Reason",

        [

            "Technical Skills",

            "Communication Skills",

            "Experience",

            "Culture Fit",

            "Position Filled",

            "Other"

        ]

    )

    feedback = st.text_area(

        "Feedback"

    )

    future_opportunity = st.checkbox(

        "Consider for Future Opportunities"

    )

    hr_notes = st.text_area(

        "HR Notes"

    )

    st.divider()



    st.subheader("🤖 AI Rejection Email")

    if st.button(

        "Generate Rejection Email",

        use_container_width=True

    ):

        from models.rejection_email_ai import generate_rejection_email

        with st.spinner("Generating..."):

            email = generate_rejection_email(

                candidate["name"],

                job["job_title"],

                rejection_reason,

                feedback,

                future_opportunity

            )

        st.session_state["rejection_email"] = email

        st.success("Email Generated Successfully!")

    if "rejection_email" in st.session_state:

        st.text_area(

            "Email Preview",

            st.session_state["rejection_email"],

            height=350

        )



    st.divider()

    rejection_status = st.selectbox(

        "Email Status",

        [

            "Draft",

            "Sent"

        ]

    )

    if st.button(

        "💾 Save Rejection",

        use_container_width=True

    ):

        from utils.database import save_rejection_status

        save_rejection_status(

            candidate["id"],

            rejection_status,

            rejection_reason,

            feedback,

            future_opportunity,

            hr_notes

        )

        st.success(

            "Rejection Email Saved Successfully!"

        )

        st.balloons()

        st.subheader("Summary")

        c1, c2 = st.columns(2)

        with c1:

            st.metric("Candidate", candidate["name"])
            st.metric("Status", rejection_status)

        with c2:

            st.metric("Reason", rejection_reason)
            st.metric("Job", job["job_title"])

        st.success("🎉 Rejection Email Completed!")