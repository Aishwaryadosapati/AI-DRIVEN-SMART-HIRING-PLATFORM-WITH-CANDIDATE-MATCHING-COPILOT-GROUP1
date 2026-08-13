import re
import streamlit as st
from models.llama import ask_llama
from utils.database import get_all_candidates


# =====================================================
# APP CONFIGURATION
# =====================================================

PAGE_TITLE = "🤖 AI Recruitment Assistant"

WELCOME_MESSAGE = """
👋 **Welcome!**

I'm your **AI Recruitment Assistant**.

I can help you with:

- 📄 Resume Analysis
- 👤 Candidate Evaluation
- 🏆 Candidate Comparison
- 🎯 Hiring Recommendations
- 📈 Recruitment Analytics
- 💼 Job Descriptions
- 🎤 Interview Questions
- 🔍 Skill Gap Analysis

Ask me any recruitment-related question.
"""


# =====================================================
# BLOCKED QUESTIONS
# =====================================================

BLOCKED_WORDS = [

    "weather",
    "temperature",
    "movie",
    "movies",
    "actor",
    "actress",
    "football",
    "cricket",
    "ipl",
    "virat",
    "kohli",
    "politics",
    "election",
    "history",
    "science",
    "math",
    "capital",
    "country",
    "algorithm",
    "html",
    "css",
    "javascript",
    "python code",
    "java code",
    "chatgpt",
    "bitcoin",
    "stock market"

]


# =====================================================
# ALLOWED TOPICS
# =====================================================



# =====================================================
# HELPER FUNCTION
# Build Candidate Context for Llama
# =====================================================

def build_candidate_context(candidates):

    candidate_text = ""

    for candidate in candidates:

        candidate_text += f"""

Candidate Name : {candidate['name']}

Skills : {candidate['skills']}

Experience : {extract_experience(candidate['experience'])} Years



Resume Score : {candidate['resume_score']}

Recommendation : {candidate['recommendation']}

------------------------------------------------------------

"""

    return candidate_text


# =====================================================
# HELPER FUNCTION
# Count Recommendation Statistics
# =====================================================

def recommendation_summary(candidates):

    total = len(candidates)

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

    return total, hire, hold, reject


# =====================================================
# MAIN PAGE
# =====================================================





def extract_experience(exp):
    if not exp:
        return 0

    exp = str(exp).lower()

    if "entry-level" in exp or "fresher" in exp:
        return 0

    match = re.search(r"(\d+)", exp)
    if match:
        return int(match.group(1))

    return 0

STOP_WORDS = {
    "who", "is", "the", "a", "an", "for", "with",
    "show", "find", "recommend", "compare",
    "candidate", "candidates", "best", "me"
}

def get_relevant_candidates(question, candidates):
    words = [
        w for w in question.lower().split()
        if w not in STOP_WORDS
    ]

    matched = []

    for c in candidates:
        text = f"{c['name']} {c['skills']}".lower()

        if any(word in text for word in words):
            matched.append(c)

    return matched if matched else candidates
    
@st.cache_data
def load_candidates():
    return get_all_candidates()


def show():

    # -------------------------------
    # Session State
    # -------------------------------

    if "chat_history" not in st.session_state:

        st.session_state.chat_history = [

            {

                "role": "assistant",

                "content": WELCOME_MESSAGE

            }

        ]


    if "typing" not in st.session_state:

        st.session_state.typing = False

    # Candidate Database

    

    candidates = load_candidates()

    total, hire, hold, reject = recommendation_summary(candidates)

    # Remaining UI starts in Part 2

        # =====================================================
    # CUSTOM CSS
    # =====================================================

    st.markdown("""
    <style>

    .block-container{
        max-width:1150px;
        padding-top:1.5rem;
        padding-bottom:2rem;
    }

    /* Hide Streamlit Menu */

    #MainMenu{
        visibility:hidden;
    }

    footer{
        visibility:hidden;
    }

    header{
        visibility:hidden;
    }

    /* Header */

    .hero{

        background:linear-gradient(135deg,#4F46E5,#7C3AED);

        padding:28px;

        border-radius:18px;

        color:white;

        margin-bottom:20px;

    }

    .hero h1{

        margin-bottom:8px;

        font-size:36px;

    }

    .hero p{

        font-size:16px;

        opacity:.92;

    }

    /* Cards */

    .info-card{

        background:white;

        border-radius:16px;

        padding:18px;

        border:1px solid #ECECEC;

        box-shadow:0 4px 15px rgba(0,0,0,.05);

    }

    .section-title{

        font-size:22px;

        font-weight:700;

        margin-top:25px;

        margin-bottom:15px;

    }

    </style>
    """, unsafe_allow_html=True)


    # =====================================================
    # SIDEBAR
    # =====================================================

    with st.sidebar:

        st.title("🤖 AI Assistant")

        st.caption("Recruitment & Talent Management")

        st.divider()

        if st.button(
            "🆕 New Conversation",
            use_container_width=True
        ):

            st.session_state.chat_history = [
                {
                    "role":"assistant",
                    "content":WELCOME_MESSAGE
                }
            ]

            st.rerun()

        

        


    # =====================================================
    # HEADER
    # =====================================================

    st.markdown(f"""
    <div class="hero">

    <h1>{PAGE_TITLE}</h1>

    <p>

    Your intelligent hiring companion.

    Analyse resumes, compare candidates,
    generate hiring recommendations,
    interview questions and recruitment insights.

    </p>

    </div>

    """, unsafe_allow_html=True)


    # =====================================================
    # DASHBOARD METRICS
    # =====================================================

    m1,m2,m3,m4 = st.columns(4)

    with m1:

        st.metric(

            "👥 Candidates",

            total

        )

    with m2:

        st.metric(

            "✅ Hire",

            hire

        )

    with m3:

        st.metric(

            "⏳ Hold",

            hold

        )

    with m4:

        st.metric(

            "❌ Reject",

            reject

        )


    st.divider()


    # =====================================================
    # AI INSIGHTS
    # =====================================================

    st.markdown(
        '<div class="section-title">📈 AI Recruitment Insights</div>',
        unsafe_allow_html=True
    )

    left,right = st.columns([2,1])

    with left:

        st.markdown("""

<div class="info-card">

### 💡 Today's Insights

- Highest resume scores are recommended first.
- Candidates with multiple technical skills receive better rankings.
- Resume score combines skills, education, projects and experience.
- Use AI chat below for deeper candidate analysis.

</div>

""", unsafe_allow_html=True)

    with right:

        st.markdown("""

<div class="info-card">

### 🚀 Suggested Questions

### 💬 Try These Questions

• Compare Python developers

• Who has the highest resume score?

• Recommend the best backend developer

• Generate interview questions for Java

• Create a Data Analyst job description

• Find candidates with Machine Learning skills

• Show hiring recommendations

• Explain candidate rankings

</div>

""", unsafe_allow_html=True)


    st.divider()

    # =====================================================
    # CHAT UI STARTS IN PART 3
    # =====================================================


        # =====================================================
    # CHAT HEADER
    # =====================================================

    st.markdown(
        '<div class="section-title">💬 AI Conversation</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "Ask questions about resumes, candidates, hiring, interviews and recruitment."
    )

    st.divider()


    # =====================================================
    # DISPLAY CHAT HISTORY
    # =====================================================

    for message in st.session_state.chat_history:

        avatar = "🤖" if message["role"] == "assistant" else "👤"

        with st.chat_message(
            message["role"],
            avatar=avatar
        ):

            st.markdown(message["content"])


    # =====================================================
    # QUICK QUESTION HANDLER
    # =====================================================

    user_question = st.chat_input(
        "Ask about candidates, resumes, hiring, interviews..."
    )


    # =====================================================
    # STOP IF NO QUESTION
    # =====================================================

    if not user_question:

        st.divider()

        st.caption(
            "🤖 AI Recruitment Assistant • Powered by Llama"
        )

        return


    # =====================================================
    # SHOW USER MESSAGE
    # =====================================================

    st.session_state.chat_history.append(
        {
            "role": "user",
            "content": user_question
        }
    )

    with st.chat_message(
        "user",
        avatar="👤"
    ):

        st.markdown(user_question)


    # =====================================================
    # AI THINKING ANIMATION
    # =====================================================

    

    # =====================================================
    # AI PROCESSING STARTS IN PART 4
    # =====================================================


        # =====================================================
    # RECRUITMENT VALIDATION
    # =====================================================

    question_lower = user_question.lower().strip()

    # Block unrelated questions
    if any(word in question_lower for word in BLOCKED_WORDS):

        answer = """
I'm your **AI Recruitment Assistant**.

I can only answer questions related to recruitment and talent management.

You can ask about:

- Candidate Profiles
- Resume Analysis
- Resume Matching
- Hiring Recommendations
- Interview Questions
- Job Descriptions
- Recruitment Analytics
"""

        st.session_state.chat_history.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        st.rerun()

    


    # Check whether the question is recruitment related
    
    


    # =====================================================
    # FILTER CANDIDATES
    # =====================================================

    



    # If no candidates match
    filtered_candidates = get_relevant_candidates(
    user_question,
    candidates
)

    if not filtered_candidates:
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": "No matching candidates found."
        })
        st.rerun()


    # =====================================================
    # BUILD AI CONTEXT
    # =====================================================

    candidate_context = build_candidate_context(
        filtered_candidates
    )


    # =====================================================
    # AI PROMPT
    # =====================================================

    prompt = f"""
You are an AI Recruitment Assistant.

You answer ONLY recruitment and talent management questions.

Candidate Database:

{candidate_context}

Use ONLY the above candidate information.

When recommending candidates:
- Match the requested role with candidate skills.
Consider only the candidate information provided below.
Do not assume or invent any missing information.
- If the role is AI, Artificial Intelligence, Machine Learning, Data Science,
Computer Vision, NLP, or Generative AI, prefer candidates with those skills.
- If multiple candidates qualify, rank them from best to least suitable and explain why.
- If no candidate matches, clearly say so.
Rules:

- Never assume skills, education, projects, or experience that are not explicitly provided.
- If information is missing, state "Not available".
- Do not invent candidate details.

Recruiter Question:
{user_question}
"""


    # =====================================================
    # GENERATE RESPONSE
    # =====================================================

    import time

    with st.spinner("Generating AI response..."):
        try:
            answer = ask_llama(prompt)
        except Exception as e:
            answer = f"Error: {e}"

    with st.chat_message(
        "assistant",
        avatar="🤖"
    ):
        st.markdown(answer)


    # =====================================================
    # SAVE RESPONSE
    # =====================================================

    st.session_state.chat_history.append(

        {

            "role":"assistant",

            "content":answer

        }

    )



    # =====================================================
    # PART 5 STARTS BELOW
    # =====================================================


        # =====================================================
    # AI RECRUITMENT REPORT
    # =====================================================

    st.divider()

    st.markdown(
        '<div class="section-title">📊 Recruitment Summary</div>',
        unsafe_allow_html=True
    )

    report_col1, report_col2 = st.columns(2)

    with report_col1:

        st.success(f"👥 Total Candidates : {total}")

        st.success(f"✅ Hire Recommendations : {hire}")

    with report_col2:

        st.warning(f"⏳ Hold Recommendations : {hold}")

        st.error(f"❌ Reject Recommendations : {reject}")


    # =====================================================
    # AI INSIGHTS
    # =====================================================

    st.divider()

    st.markdown(
        '<div class="section-title">💡 AI Insights</div>',
        unsafe_allow_html=True
    )

    if candidates:

        best_candidate = max(
            candidates,
            key=lambda x: int(x["resume_score"])
        )

        st.info(
            f"""
🏆 **Top Candidate:** {best_candidate['name']}

⭐ Resume Score: {best_candidate['resume_score']}

💻 Skills: {best_candidate['skills']}

🎯 Recommendation: {best_candidate['recommendation']}
"""
        )


    # =====================================================
    # EXPORT CHAT
    # =====================================================

    st.divider()

    chat_text = ""

    for message in st.session_state.chat_history:

        role = "AI" if message["role"] == "assistant" else "Recruiter"

        chat_text += f"{role}\n"

        chat_text += f"{message['content']}\n"

        chat_text += "\n--------------------------\n\n"

    st.download_button(
        label="📥 Download Chat History",
        data=chat_text,
        file_name="Recruitment_AI_Chat.txt",
        mime="text/plain",
        use_container_width=True
    )


    # =====================================================
    # SAMPLE QUESTIONS
    # =====================================================

    with st.expander("💬 Sample Questions"):

        st.markdown("""
- Compare Python Developers

- Recommend the best candidate

- Explain Resume Score

- Show candidates with Java skills

- Generate Interview Questions

- Generate Job Description

- Show Hiring Recommendation

- Analyse Candidate Skills

- Compare candidates with more than 3 years of experience
""")


    # =====================================================
    # AI TIPS
    # =====================================================

    st.divider()

    st.markdown(
        '<div class="section-title">🚀 Tips</div>',
        unsafe_allow_html=True
    )

    st.info("""
✔ Ask specific recruitment questions.

✔ Use the filters in the sidebar before asking.

✔ Compare candidates to understand their strengths.

✔ Generate interview questions for any role.

✔ Create professional job descriptions instantly.

✔ Download the conversation for future reference.
""")


    # =====================================================
    # FOOTER
    # =====================================================

    st.divider()

    st.caption(
        "🤖 AI Recruitment Assistant | Powered by Llama | Built with Streamlit"
    )