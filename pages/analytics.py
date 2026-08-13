import streamlit as st
import pandas as pd
import plotly.express as px

from utils.database import *

def show():

    st.title("📊 Recruitment Analytics Dashboard")

    candidates = get_candidate_count()

    jobs = get_job_count()

    col1,col2 = st.columns(2)

    with col1:

        st.metric(

            "👥 Candidates",

            candidates

        )

    with col2:

        st.metric(

            "💼 Jobs",

            jobs

        )

    st.divider()

    # ---------------- Resume Score ---------------- #

    scores = get_resume_scores()

    score_list = []

    for row in scores:

        if row["resume_score"] is not None:

            score_list.append(row["resume_score"])

    if len(score_list)>0:

        df = pd.DataFrame({

            "Resume Score":score_list

        })

        fig = px.histogram(

            df,

            x="Resume Score",

            nbins=10,

            title="Resume Score Distribution"

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    # ---------------- Recommendation ---------------- #

    recommendations = get_recommendations()

    rec = []

    for row in recommendations:

        if row["recommendation"]:

            rec.append(row["recommendation"])

    if len(rec)>0:

        df = pd.DataFrame({

            "Recommendation":rec

        })

        fig = px.pie(

            df,

            names="Recommendation",

            title="Hiring Recommendation"

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    st.divider()

    st.subheader("📋 Recent Candidates")

    all_candidates = get_all_candidates()

    if len(all_candidates)>0:

        table=[]

        for c in all_candidates:

            table.append({

                "Name":c["name"],

                "Email":c["email"],

                "Score":c["resume_score"],

                "Recommendation":c["recommendation"]

            })

        st.dataframe(

            pd.DataFrame(table),

            use_container_width=True

        )