import streamlit as st
import pandas as pd
import plotly.express as px
import io
from collections import Counter


from utils.database import (
    get_all_candidates,
    get_all_jobs,
    get_all_interviews
)


from utils.database import (
    get_candidate_count,
    get_job_count,
    get_interview_count,
    get_joined_count
)

from utils.database import (
    get_all_candidates,
    get_all_jobs,
    get_all_interviews,
    get_candidate_count,
    get_job_count,
    get_interview_count,
    get_joined_count,
    get_candidate_status_counts
)




def show():

    # -----------------------------
    # Load Data
    # -----------------------------

    candidates = get_all_candidates()
    jobs = get_all_jobs()
    interviews = get_all_interviews()

    from datetime import datetime

    today = datetime.today().strftime("%Y-%m-%d")

    today_interviews = [
        interview
        for interview in interviews
        if interview["interview_date"] == today
    ]


    # ==========================
# Search Candidate
# ==========================

    search = st.text_input(
        "🔍 Search Candidate",
        placeholder="Enter candidate name..."
    )

    if search:

        candidates = [
            c for c in candidates
            if search.lower() in c["name"].lower()
        ]

    # ==========================
# Filter by Status
# ==========================

    status_filter = st.selectbox(
        "📂 Filter by Status",
            [
                "All",
                "Applied",
                "Resume Analysed",
                "Shortlisted",
                "Interview Scheduled",
                "Offer Sent",
                "Joined"
            ]
        )

    if status_filter != "All":

        candidates = [
            c for c in candidates
            if c["candidate_status"] == status_filter
        ]

    # -----------------------------
    # Basic Statistics
    # -----------------------------

    total_candidates = len(candidates)
    total_jobs = len(jobs)
    total_interviews = len(interviews)


    joined_count = get_joined_count()


    applied_count = sum(
        1 for c in candidates
        if c["candidate_status"] == "Applied"
    )

    analysed_count = sum(
        1 for c in candidates
        if c["candidate_status"] == "Resume Analysed"
    )

    shortlisted_count = sum(
        1 for c in candidates
        if c["candidate_status"] == "Shortlisted"
    )


    interview_scheduled_count = sum(
        1 for c in candidates
        if c["candidate_status"] == "Interview Scheduled"
    )


    offer_sent_count = sum(
        1 for c in candidates
        if c["candidate_status"] == "Offer Sent"
    )





    hire = sum(
        1
        for c in candidates
        if str(c["recommendation"]).lower() == "hire"
    )

    hold = sum(
        1
        for c in candidates
        if str(c["recommendation"]).lower() == "hold"
    )

    reject = sum(
        1
        for c in candidates
        if str(c["recommendation"]).lower() == "reject"
    )

    if total_candidates > 0:

        avg_score = round(
            sum(
                int(c["resume_score"] or 0)
                for c in candidates
            ) / total_candidates
        )

    else:

        avg_score = 0


        # =====================================
    # CUSTOM CSS
    # =====================================

    st.markdown("""
    <style>

    .block-container{
        padding-top:1.5rem;
        padding-bottom:2rem;
        max-width:1300px;
    }

    #MainMenu{
        visibility:hidden;
    }

    footer{
        visibility:hidden;
    }

    header{
        visibility:hidden;
    }

    .hero{

        background:linear-gradient(135deg,#4F46E5,#2563EB);

        padding:30px;

        border-radius:20px;

        color:white;

        margin-bottom:25px;

        box-shadow:0px 6px 18px rgba(0,0,0,0.15);

    }

    .hero h1{

        font-size:38px;

        margin-bottom:8px;

    }

    .hero p{

        font-size:18px;

        opacity:0.95;

    }

    </style>
    """, unsafe_allow_html=True)


    # =====================================
    # HEADER
    # =====================================

    st.title("📊 Dashboard")
    st.write("Welcome to your AI-powered Recruitment Dashboard.")


    # =====================================
    # KPI CARDS
    # =====================================

    

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        with st.container(border=True):
            st.markdown("#### 👥 Candidates")
            st.markdown(
                f"<h2 style='margin:0;color:#2563EB'>{total_candidates}</h2>",
                unsafe_allow_html=True
            )

    with c2:
        with st.container(border=True):
            st.markdown("#### 💼 Jobs")
            st.markdown(
                f"<h2 style='margin:0;color:#2563EB'>{total_jobs}</h2>",
                unsafe_allow_html=True
            )

    with c3:
        with st.container(border=True):
            st.markdown("#### 📅 Interviews")
            st.markdown(
                f"<h2 style='margin:0;color:#2563EB'>{total_interviews}</h2>",
                unsafe_allow_html=True
            )

    with c4:
        with st.container(border=True):
            st.markdown("#### 🎉 Joined")
            st.markdown(
            f"<h2 style='margin:0;color:#2563EB'>{joined_count}</h2>",
            unsafe_allow_html=True
        )

    c5, c6, c7, c8, c9 = st.columns(5)

    with c5:
        with st.container(border=True):
            st.markdown("#### 📄 Applied")
            st.markdown(
            f"<h2 style='margin:0;color:#2563EB'>{applied_count}</h2>",
            unsafe_allow_html=True
        )

    with c6:
        with st.container(border=True):
            st.markdown("#### 🧠 Analysed")
            st.markdown(
            f"<h2 style='margin:0;color:#2563EB'>{analysed_count}</h2>",
            unsafe_allow_html=True
        )

    with c7:
        with st.container(border=True):
            st.markdown("#### ⭐ Shortlisted")
            st.markdown(
            f"<h2 style='margin:0;color:#2563EB'>{shortlisted_count}</h2>",
            unsafe_allow_html=True
        )


    with c8:
        with st.container(border=True):
            st.markdown("#### 📅 Scheduled")
            st.markdown(
            f"<h2 style='margin:0;color:#2563EB'>{interview_scheduled_count}</h2>",
            unsafe_allow_html=True
        )
            
    with c9:
        with st.container(border=True):
            st.markdown("#### 🎁 Offer Sent")
            st.markdown(
            f"<h2 style='margin:0;color:#2563EB'>{offer_sent_count}</h2>",
            unsafe_allow_html=True
        )
            
    st.divider()

    st.subheader("🔔 Recruitment Alerts")

    col1, col2 = st.columns(2)

    with col1:
        st.warning(f"📄 {applied_count} Candidates waiting for resume analysis")
        st.info(f"📅 {interview_scheduled_count} Interviews Scheduled")

    with col2:
        st.success(f"🎁 {offer_sent_count} Offer Letters Sent")
        st.success(f"🎉 {joined_count} Employees Joined")

    st.subheader("📌 Recruitment Pipeline")

    status_data = get_candidate_status_counts()

    if status_data:

        pipeline_df = pd.DataFrame(status_data)

        fig = px.bar(
            pipeline_df,
            x="candidate_status",
            y="total",
            color="candidate_status",
            text="total",
            title="Candidate Recruitment Pipeline"
        )

        fig.update_layout(
            showlegend=False,
            xaxis_title="Candidate Status",
            yaxis_title="Number of Candidates",
            height=450
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:
        st.info("No pipeline data available.")
    # RECRUITMENT ANALYTICS
    # =====================================

    st.divider()

    st.subheader("🥧 Candidate Status Distribution")

    status_data = get_candidate_status_counts()

    if status_data:

        status_df = pd.DataFrame(status_data)

        fig = px.pie(
            status_df,
            names="candidate_status",
            values="total",
            hole=0.45,
            title="Candidate Status Distribution"
        )

        fig.update_layout(height=450)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:
        st.info("No status data available.")

    st.subheader("📊 Recruitment Analytics")

    left, right = st.columns(2)

    # =====================================
    # Resume Score Chart
    # =====================================

    with left:

        st.markdown("#### ⭐ Resume Scores")

        if candidates:

            score_df = pd.DataFrame(candidates)

            fig = px.bar(
                score_df,
                x="name",
                y="resume_score",
                color="resume_score",
                text="resume_score",
                title="Candidate Resume Scores"
            )

            fig.update_layout(
                xaxis_title="Candidate",
                yaxis_title="Resume Score",
                height=400
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.info("No candidate data available.")

    # =====================================
    # Recommendation Chart
    # =====================================

    with right:

        st.markdown("#### 🎯 Hiring Recommendations")

        recommendation_df = pd.DataFrame({

            "Recommendation":[
                "Hire",
                "Hold",
                "Reject"
            ],

            "Count":[
                hire,
                hold,
                reject
            ]

        })

        fig = px.pie(

            recommendation_df,

            values="Count",

            names="Recommendation",

            hole=0.5

        )

        fig.update_layout(height=400)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.divider()

    # =====================================
    # SKILLS ANALYTICS
    # =====================================

    st.subheader("💻 Skills Analytics")

    skill_list = []

    for candidate in candidates:

        if candidate["skills"]:

            skills = candidate["skills"].split(",")

            for skill in skills:

                skill_list.append(skill.strip())

    if skill_list:

        skill_counter = Counter(skill_list)

        skill_df = pd.DataFrame(

            skill_counter.items(),

            columns=[
                "Skill",
                "Count"
            ]

        )

        skill_df = skill_df.sort_values(
            by="Count",
            ascending=False
        )

        fig = px.bar(

            skill_df,

            x="Skill",

            y="Count",

            color="Count",

            text="Count"

        )

        fig.update_layout(height=450)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.info("No skills available.")

    st.divider()


        # =====================================
    # TOP CANDIDATES
    # =====================================

    st.subheader("🏆 Top Candidates")

    if candidates:

        top_candidates = sorted(
            candidates,
            key=lambda x: int(x["resume_score"] or 0),
            reverse=True
        )

        top_df = pd.DataFrame(top_candidates)[[
            "name",
            "skills",
            "experience",
            "resume_score",
            "recommendation"
        ]]

        top_df.columns = [
            "Candidate",
            "Skills",
            "Experience",
            "Resume Score",
            "Recommendation"
        ]

        st.dataframe(
            top_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No candidates available.")

    st.divider()


    # =====================================
    # RECENT CANDIDATES & RECENT JOBS
    # =====================================

    left, right = st.columns(2)

    # -----------------------------
    # Recent Candidates
    # -----------------------------

    with left:

        st.subheader("📄 Recent Candidates")

        if candidates:

            recent_candidates = pd.DataFrame(candidates)[[
                "name",
                "email",
                "resume_score",
                "recommendation"
            ]]

            recent_candidates.columns = [
                "Candidate",
                "Email",
                "Score",
                "Recommendation"
            ]

            st.dataframe(
                recent_candidates.head(5),
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info("No candidates found.")


    # -----------------------------
    # Recent Jobs
    # -----------------------------

    with right:

        st.subheader("💼 Recent Jobs")

        if jobs:

            job_df = pd.DataFrame(jobs)[[
                "job_title",
                "department",
                "location",
                "status"
            ]]

            job_df.columns = [
                "Job Title",
                "Department",
                "Location",
                "Status"
            ]

            st.dataframe(
                job_df.head(5),
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info("No jobs available.")

    st.divider()


    # =====================================
    # UPCOMING INTERVIEWS
    # =====================================

    st.subheader("📅 Upcoming Interviews")

    if interviews:

        interview_df = pd.DataFrame(interviews)[[
            "candidate_name",
            "interviewer",
            "interview_date",
            "interview_time",
            "interview_mode",
            "status"
        ]]

        interview_df.columns = [
            "Candidate",
            "Interviewer",
            "Date",
            "Time",
            "Mode",
            "Status"
        ]

        st.dataframe(
            interview_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No interviews scheduled.")

    st.divider()


    st.subheader("📅 Today's Interviews")

    if today_interviews:

        df = pd.DataFrame(today_interviews)

        st.dataframe(
            df[[
            "candidate_name",
            "interviewer",
            "interview_date",
            "interview_time",
            "status"
            ]],
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("No interviews scheduled for today.")


        # =====================================
    # AI RECRUITMENT INSIGHTS
    # =====================================

    st.subheader("🧠 AI Recruitment Insights")

    if candidates:

        best_candidate = max(
            candidates,
            key=lambda x: int(x["resume_score"] or 0)
        )

        # Most Common Skill
        all_skills = []

        for c in candidates:

            if c["skills"]:

                all_skills.extend(
                    [s.strip() for s in c["skills"].split(",")]
                )

        if all_skills:

            most_common_skill = Counter(all_skills).most_common(1)[0][0]

        else:

            most_common_skill = "Not Available"

        hire_rate = 0

        if total_candidates > 0:

            hire_rate = round(
                (hire / total_candidates) * 100
            )

        insight1, insight2 = st.columns(2)

        with insight1:

            st.success(f"""
🏆 **Best Candidate**

**{best_candidate['name']}**

⭐ Resume Score: **{best_candidate['resume_score']}**

💻 Skills: **{best_candidate['skills']}**
""")

        with insight2:

            st.info(f"""
📊 **Recruitment Summary**

👥 Candidates : **{total_candidates}**

💼 Jobs : **{total_jobs}**

📅 Interviews : **{total_interviews}**

📈 Hire Rate : **{hire_rate}%**

🔥 Top Skill : **{most_common_skill}**
""")

    st.divider()

    # =====================================
    # QUICK ACTIONS
    # =====================================

    st.subheader("⚡ Quick Actions")

    qa1, qa2, qa3, qa4 = st.columns(4)

    with qa1:

        if st.button(
            "📄 Upload Resume",
            use_container_width=True
        ):
            st.info("Go to Resume Upload module.")

    with qa2:

        if st.button(
            "💼 Create Job",
            use_container_width=True
        ):
            st.info("Go to Job Description module.")

    with qa3:

        if st.button(
            "📅 Schedule Interview",
            use_container_width=True
        ):
            st.info("Go to Interview Scheduler module.")

    with qa4:

        if st.button(
            "🤖 Open AI Copilot",
            use_container_width=True
        ):
            st.info("Go to AI Copilot module.")

    st.divider()

    # =====================================
    # DASHBOARD SUMMARY
    # =====================================

    st.subheader("📈 Dashboard Summary")

    summary = pd.DataFrame({

        "Metric":[

            "Total Candidates",

            "Active Jobs",

            "Scheduled Interviews",

            "Hire",

            "Hold",

            "Reject",

            "Average Resume Score"

        ],

        "Value":[

            total_candidates,

            total_jobs,

            total_interviews,

            hire,

            hold,

            reject,

            avg_score

        ]

    })

    st.dataframe(
        summary,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # =====================================
    # FOOTER
    # =====================================

    # =====================================
# EXPORT REPORTS
# =====================================

    st.divider()

    st.subheader("📥 Export Reports")

    if candidates:

        export_df = pd.DataFrame(candidates)[[
        "name",
        "email",
        "phone",
        "location",
        "resume_score",
        "recommendation",
        "candidate_status"
        ]]

        export_df.columns = [
        "Name",
        "Email",
        "Phone",
        "Location",
        "Resume Score",
        "Recommendation",
        "Status"
        ]

        csv = export_df.to_csv(index=False).encode("utf-8")

        st.download_button(
        label="📄 Download Candidates CSV",
        data=csv,
        file_name="candidates_report.csv",
        mime="text/csv"
        )

    else:
        st.info("No candidate data available to export.")

    st.markdown(
        """
        <center>

        <h4>🤖 AI Recruitment & Talent Management Copilot</h4>

        Built with ❤️ using Streamlit, SQLite and AI

        </center>
        """,
        unsafe_allow_html=True
    )


# =====================================
# FOOTER
# =====================================

st.divider()

st.markdown(
    """
    <div style="
        background:#f8f9fa;
        padding:20px;
        border-radius:12px;
        text-align:center;
        color:#555;
        margin-top:30px;
    ">

    <h3>🤖 AI Recruitment & Talent Management Copilot</h3>

    <p><b>Version:</b> 1.0</p>

    <p>
    Built with ❤️ using
    <b>Python</b> |
    <b>Streamlit</b> |
    <b>SQLite</b> |
    <b>Ollama (Llama)</b>
    </p>

    <hr>

    <p>© 2026 AI Recruitment & Talent Management Copilot</p>

    </div>
    """,
    unsafe_allow_html=True
)


