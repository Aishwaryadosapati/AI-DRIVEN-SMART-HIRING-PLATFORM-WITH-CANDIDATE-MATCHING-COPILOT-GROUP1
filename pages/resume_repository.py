import os
import streamlit as st
import pandas as pd

from utils.database import get_all_candidates
from utils.database import (
    get_all_candidates,
    delete_candidate
)

def show():

    st.title("📂 Resume Repository")

    candidates = get_all_candidates()

    if len(candidates) == 0:
        st.info("No resumes found.")
        return

    # ===============================
    # Search
    # ===============================

    search = st.text_input(
        "🔍 Search Candidate"
    ).lower()

    filtered = []

    for candidate in candidates:

        if (
            search in candidate["name"].lower()
            or search in candidate["email"].lower()
            or search in candidate["candidate_status"].lower()
        ):

            filtered.append(candidate)

    # ===============================
    # Summary
    # ===============================

    st.subheader("📊 Repository Summary")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Resumes",
        len(filtered)
    )

    shortlisted = len([
        c for c in filtered
        if c["candidate_status"] == "Shortlisted"
    ])

    rejected = len([
        c for c in filtered
        if c["candidate_status"] == "Rejected"
    ])

    col2.metric(
        "Shortlisted",
        shortlisted
    )

    col3.metric(
        "Rejected",
        rejected
    )

    st.divider()

    # ===============================
    # Candidate Table
    # ===============================

    data = []

    for candidate in filtered:

        data.append({

            "Name": candidate["name"],
            "Email": candidate["email"],
            "Phone": candidate["phone"],
            "Location": candidate["location"],
            "ATS Score": candidate["resume_score"],
            "Status": candidate["candidate_status"]

        })

    df = pd.DataFrame(data)

    st.dataframe(
        df,
        use_container_width=True
    )

    st.divider()

    # ===============================
    # Candidate Details
    # ===============================

    names = [
        candidate["name"]
        for candidate in filtered
    ]

    selected = st.selectbox(
        "👤 Select Candidate",
        names
    )

    if st.button(
        "🗑 Delete Candidate",
        use_container_width=True
    ):

        if st.checkbox("I confirm that I want to delete this candidate."):
            delete_candidate(candidate["id"])

            st.success("Candidate deleted successfully.")

            st.rerun()

    candidate = next(
        c for c in filtered
        if c["name"] == selected
    )

    st.subheader("👤 Candidate Profile")

    col1, col2 = st.columns(2)

    with col1:

        st.write("**Name:**", candidate["name"])
        st.write("**Email:**", candidate["email"])
        st.write("**Phone:**", candidate["phone"])

    with col2:

        st.write("**Location:**", candidate["location"])
        st.write("**ATS Score:**", candidate["resume_score"])
        st.write("**Status:**", candidate["candidate_status"])

    st.divider()

    # ===============================
    # Resume Preview
    # ===============================

    st.subheader("📄 Resume Preview")

    st.text_area(
        "Resume",
        candidate["resume_text"],
        height=300,
        disabled=True
    )

    # ===============================
    # Download Resume
    # ===============================

    if (
        candidate["resume_path"]
        and
        os.path.exists(candidate["resume_path"])
    ):

        with open(
            candidate["resume_path"],
            "rb"
        ) as file:

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

    st.success("✅ Resume Repository Loaded Successfully.")