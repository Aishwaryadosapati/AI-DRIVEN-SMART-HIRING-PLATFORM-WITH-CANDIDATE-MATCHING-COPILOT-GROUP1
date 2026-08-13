import streamlit as st

from utils.database import (
    get_all_candidates,
    get_job,
    get_interview
)


def show():

    st.title("🎯 Round 4 - Final Manager Interview")

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

    col1, col2 = st.columns(2)

    with col1:

        st.write("**Name:**", candidate["name"])
        st.write("**Email:**", candidate["email"])
        st.write("**Phone:**", candidate["phone"])

    with col2:

        st.write("**ATS Score:**", candidate["resume_score"])
        st.write("**Candidate Status:**", candidate["candidate_status"])

    st.progress(candidate["resume_score"] / 100)

    st.divider()

    # ==========================================
    # Interview Summary
    # ==========================================

    interview = get_interview(candidate["id"])

    if interview is None:

        st.error("Candidate has not completed previous interview rounds.")

        return

    st.subheader("📊 Previous Interview Scores")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "MCQ Score",
        interview["mcq_score"]
    )

    c2.metric(
        "Technical Score",
        interview["technical_score"]
    )

    c3.metric(
        "HR Score",
        interview["hr_score"]
    )

    st.divider()

    # ==========================================
    # Applied Job
    # ==========================================

    job = get_job(candidate["job_id"])

    if job:

        st.subheader("💼 Applied Job")

        col1, col2 = st.columns(2)

        with col1:

            st.write("**Job Title:**", job["job_title"])
            st.write("**Department:**", job["department"])
            st.write("**Experience:**", job["experience"])

        with col2:

            st.write("**Employment Type:**", job["employment_type"])
            st.write("**Minimum ATS:**", job["minimum_ats_score"])
            st.write("**Openings:**", job["openings"])

        st.write("### 🛠 Required Skills")

        st.info(job["skills"])

    else:

        st.warning("Job details not available.")

        return

    st.divider()

    # ==========================================
    # AI Hiring Summary
    # ==========================================

    st.subheader("🤖 AI Hiring Summary")

    mcq_score = interview["mcq_score"] or 0
    technical_score = interview["technical_score"] or 0
    hr_score = interview["hr_score"] or 0

    overall_score = round(
        (
            mcq_score +
            technical_score +
            hr_score
        ) / 3
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "MCQ",
        f"{mcq_score}%"
    )

    c2.metric(
        "Technical",
        f"{technical_score}%"
    )

    c3.metric(
        "HR",
        f"{hr_score}%"
    )

    c4.metric(
        "Overall",
        f"{overall_score}%"
    )

    st.progress(overall_score / 100)

    if overall_score >= 85:

        st.success(
            "🌟 Excellent Candidate"
        )

    elif overall_score >= 70:

        st.success(
            "✅ Good Candidate"
        )

    elif overall_score >= 50:

        st.warning(
            "⚠ Average Candidate"
        )

    else:

        st.error(
            "❌ Poor Candidate"
        )

    st.divider()

    # ==========================================
    # Manager Evaluation
    # ==========================================

    st.subheader("👨‍💼 Manager Evaluation")

    manager_name = st.text_input(
        "Manager Name"
    )

    col1, col2 = st.columns(2)

    with col1:

        technical_confidence = st.slider(
            "Technical Confidence",
            0,
            10,
            7
        )

        leadership = st.slider(
            "Leadership Potential",
            0,
            10,
            7
        )

    with col2:

        culture_fit = st.slider(
            "Culture Fit",
            0,
            10,
            7
        )

        overall_impression = st.slider(
            "Overall Impression",
            0,
            10,
            7
        )

    manager_remarks = st.text_area(
        "Manager Remarks"
    )

    st.divider()

    # ==========================================
    # Manager Score
    # ==========================================

    manager_score = round(

        (
            technical_confidence +
            leadership +
            culture_fit +
            overall_impression
        ) / 40 * 100

    )

    st.subheader("📊 Manager Evaluation Score")

    m1, m2, m3, m4 = st.columns(4)

    m1.metric(
        "Technical",
        technical_confidence
    )

    m2.metric(
        "Leadership",
        leadership
    )

    m3.metric(
        "Culture Fit",
        culture_fit
    )

    m4.metric(
        "Overall",
        overall_impression
    )

    st.progress(manager_score / 100)

    st.metric(
        "Manager Score",
        f"{manager_score}%"
    )

    st.divider()

    # ==========================================
    # Final Hiring Score
    # ==========================================

    st.subheader("🎯 Final Hiring Score")

    final_score = round(

        (

            mcq_score * 0.20 +

            technical_score * 0.40 +

            hr_score * 0.20 +

            manager_score * 0.20

        )

    )

    c1, c2 = st.columns(2)

    with c1:

        st.metric(
            "Final Score",
            f"{final_score}%"
        )

    with c2:

        st.metric(
            "Overall Candidate Score",
            f"{overall_score}%"
        )

    st.progress(final_score / 100)

    st.divider()

    # ==========================================
    # Final Decision
    # ==========================================

    st.subheader("✅ Final Hiring Decision")

    decision = st.radio(

        "Manager Decision",

        [

            "Selected",

            "Hold",

            "Rejected"

        ],

        horizontal=True

    )

    st.divider()

    # ==========================================
    # AI Recommendation
    # ==========================================

    st.subheader("🤖 AI Recommendation")

    if final_score >= 85:

        st.success("🌟 Excellent Candidate")

        ai_recommendation = "Strongly Hire"

    elif final_score >= 70:

        st.success("✅ Good Candidate")

        ai_recommendation = "Hire"

    elif final_score >= 50:

        st.warning("⚠ Average Candidate")

        ai_recommendation = "Hold"

    else:

        st.error("❌ Poor Candidate")

        ai_recommendation = "Reject"

    st.info(
        f"AI Recommendation : {ai_recommendation}"
    )

    st.divider()


    # ==========================================
    # Save Final Selection
    # ==========================================

    if st.button(
        "💾 Save Final Decision",
        use_container_width=True
    ):

        if manager_name == "":

            st.warning("Please enter Manager Name.")

        else:

            from utils.database import update_manager_interview

            update_manager_interview(

                candidate["id"],

                manager_score,

                decision,

                manager_remarks

            )

            st.success("✅ Final Selection Saved Successfully!")

            st.balloons()

            st.divider()

            # ==========================================
            # Final Hiring Summary
            # ==========================================

            st.subheader("🎉 Final Hiring Summary")

            c1, c2, c3, c4 = st.columns(4)

            c1.metric(
                "MCQ",
                f"{mcq_score}%"
            )

            c2.metric(
                "Technical",
                f"{technical_score}%"
            )

            c3.metric(
                "HR",
                f"{hr_score}%"
            )

            c4.metric(
                "Manager",
                f"{manager_score}%"
            )

            st.divider()

            st.metric(
                "Final Hiring Score",
                f"{final_score}%"
            )

            st.progress(final_score / 100)

            st.write("### Manager Decision")

            if decision == "Selected":

                st.success("🎉 Candidate Selected")

            elif decision == "Hold":

                st.warning("⏳ Candidate Put on Hold")

            else:

                st.error("❌ Candidate Rejected")

            st.write("### AI Recommendation")

            st.info(ai_recommendation)

            st.write("### Manager Remarks")

            st.info(manager_remarks)

            st.divider()

            st.success(
                "🏆 Interview Process Completed Successfully!"
            )

            st.info(
                "➡️ Next Module: AI Communication"
            )