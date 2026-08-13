import streamlit as st
import pandas as pd

from utils.database import get_all_candidates


def show():

    st.title("🏆 Candidate Ranking")

    candidates = get_all_candidates()

    if len(candidates) == 0:
        st.warning("No candidates available.")
        return

    data = []

    for candidate in candidates:

        data.append({

            "Name": candidate["name"],
            "Email": candidate["email"],
            "ATS Score": candidate["resume_score"],
            "Status": candidate["candidate_status"]

        })

    df = pd.DataFrame(data)

    df = df.sort_values(
        by="ATS Score",
        ascending=False
    )

    df.index = df.index + 1

    st.subheader("📊 Candidate Ranking")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=False
    )

    st.divider()

    st.subheader("🥇 Top Candidate")

    top = df.iloc[0]

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Candidate",
            top["Name"]
        )

        st.metric(
            "ATS Score",
            f"{top['ATS Score']}%"
        )

    with col2:

        status = top["Status"]

        if status == "Shortlisted":

            st.success("✅ Shortlisted")

        elif status == "Interview Scheduled":

            st.info("📅 Interview Scheduled")

        elif status == "Rejected":

            st.error("❌ Rejected")

        else:

            st.warning(status)

    st.divider()

    st.subheader("📈 Ranking Summary")

    total = len(df)

    shortlisted = len(
        df[df["Status"] == "Shortlisted"]
    )

    interview = len(
        df[df["Status"] == "Interview Scheduled"]
    )

    rejected = len(
        df[df["Status"] == "Rejected"]
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Candidates", total)

    c2.metric("Shortlisted", shortlisted)

    c3.metric("Interview", interview)

    c4.metric("Rejected", rejected)