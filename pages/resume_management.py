import streamlit as st

import pages.resume_upload as resume_upload
import pages.resume_analysis as resume_analysis
import pages.resume_matching as resume_matching
import pages.candidate_ranking as candidate_ranking
import pages.skill_gap as skill_gap
import pages.hiring_recommendation as hiring_recommendation
import pages.resume_repository as resume_repository


def show():

    st.title("📄 Resume Management")

    option = st.radio(
        "Select Option",
        [
            "📤 Resume Upload",
            "🤖 Resume Analysis",
            "🎯 Resume Matching",
            "🏆 Candidate Ranking",
            "📉 Skill Gap Analysis",
            "✅ Hiring Recommendation",
            "🗂 Resume Repository"
        ],
        horizontal=True
    )

    st.divider()

    if option == "📤 Resume Upload":
        resume_upload.show()

    elif option == "🤖 Resume Analysis":
        resume_analysis.show()

    elif option == "🎯 Resume Matching":
        resume_matching.show()

    elif option == "🏆 Candidate Ranking":
        candidate_ranking.show()

    elif option == "📉 Skill Gap Analysis":
        skill_gap.show()

    elif option == "✅ Hiring Recommendation":
        hiring_recommendation.show()

    elif option == "🗂 Resume Repository":
        resume_repository.show()