import streamlit as st
import login
import pages.dashboard as dashboard
import pages.resume_upload as resume_upload
import pages.resume_analysis as resume_analysis
import pages.candidate_profile as candidate_profile
import pages.resume_matching as resume_matching
import pages.ai_communication as ai_communication
import pages.candidate_ranking as candidate_ranking
import pages.skill_gap as skill_gap
import pages.interview_questions as interview_questions
import pages.hiring_recommendation as hiring_recommendation
import pages.email_generator as email_generator
import pages.analytics as analytics
from pages import resume_chat
import pages.onboarding as onboarding
import pages.employee_management as employee_management
import pages.ai_communication as ai_communication
import pages.settings as settings
import pages.talent_management as talent_management
import pages.resume_management as resume_management
import pages.ai_copilot as ai_copilot
import pages.ai_assistant as ai_assistant
import pages.job_management as job_management
import pages.resume_repository as resume_repository
import pages.interview_management as interview_management
import pages.interview_scheduling as interview_scheduling
from utils.database import create_tables




st.set_page_config(
    page_title="AI DRIVEN SMART HIRING PLATFORM WITH CANDIDATE MATCHING COPILOT GROUP1",
    page_icon="🤖",
    layout="wide"
)
create_tables()
# Create database tables


# Load CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Header



if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login.show_login()
    st.stop()

st.markdown("""
<div class="main-title">
<h1>🤖 AI DRIVEN SMART HIRING PLATFORM WITH CANDIDATE MATCHING COPILOT GROUP1</h1>
<h4>Smart AI Hiring Assistant</h4>
</div>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.image("assets/logo.png", width=130)
st.sidebar.title("🤖 AI DRIVEN SMART HIRING PLATFORM")
st.sidebar.success("✅ Logged in as Recruiter")

page = st.sidebar.radio(
    "Navigation",
    [
        "📊 Dashboard",
        "💼 Job Management",
        "📄 Resume Management",
        "👤 Candidate Profile",
        "📅 Interview Management",
        "💬 AI Communication",
        "💬 Resume Chat",
        "🤖 AI Copilot",
        "🚀 Onboarding",
        "👨‍💼 Employee Management",
        "🎯 Talent Management"
    ]
)



if page == "📊 Dashboard":
    dashboard.show()

elif page == "💼 Job Management":
    job_management.show()

elif page == "📄 Resume Management":
    resume_management.show()

elif page == "👤 Candidate Profile":
    candidate_profile.show()

elif page == "📅 Interview Management":
    interview_management.show()

elif page == "💬 AI Communication":
    ai_communication.show()

elif page == "💬 Resume Chat":
    resume_chat.show()

elif page == "🤖 AI Copilot":
    ai_copilot.show()

elif page == "🚀 Onboarding":
    onboarding.show()

elif page == "👨‍💼 Employee Management":
    employee_management.show()

elif page == "🎯 Talent Management":
    talent_management.show()