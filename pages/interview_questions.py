import streamlit as st

from utils.database import (
    get_all_candidates,
    get_job
)


def show():

    st.title("🤖 AI Interview Questions")

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
        st.write("**Status:**", candidate["candidate_status"])

    st.progress(candidate["resume_score"] / 100)

    st.divider()

    # ==========================================
    # Job Details
    # ==========================================

    job = get_job(candidate["job_id"])

    if job is None:

        st.error("Job details not found.")

        return

    st.subheader("💼 Job Information")

    col1, col2 = st.columns(2)

    with col1:

        st.write("**Job Title:**", job["job_title"])
        st.write("**Department:**", job["department"])
        st.write("**Experience:**", job["experience"])

    with col2:

        st.write("**Location:**", job["location"])
        st.write("**Employment Type:**", job["employment_type"])

    st.write("### 🛠 Required Skills")

    st.info(job["skills"])

    st.divider()

    # ==========================================
    # Interview Settings
    # ==========================================

    st.subheader("⚙ Interview Question Settings")

    col1, col2, col3 = st.columns(3)

    with col1:

        interview_type = st.selectbox(

            "Interview Type",

            [

                "🤖 AI Interview",

                "💻 Technical Interview",

                "👨‍💼 HR Interview",

                "🎯 Final Manager Interview"

            ]

        )

    with col2:

        difficulty = st.selectbox(

            "Difficulty",

            [

                "Easy",

                "Medium",

                "Hard"

            ]

        )

    with col3:

        question_count = st.selectbox(

            "Questions",

            [

                5,

                10,

                15,

                20

            ],

            index=1

        )

    st.divider()


    # ==========================================
    # Generate Interview Questions
    # ==========================================

    st.subheader("🤖 AI Question Generator")

    if st.button(

        "Generate Questions",

        use_container_width=True

    ):

        from models.interview_questions_ai import generate_questions
        from utils.interview_parser import parse_questions

        with st.spinner(

            "Generating AI Interview Questions..."

        ):

            response = generate_questions(

                interview_type,

                difficulty,

                question_count,

                job["skills"],

                candidate["resume_text"]

            )

        questions = parse_questions(response)

        st.session_state["questions"] = questions

        st.success(

            "✅ Interview Questions Generated Successfully!"

        )

    st.divider()

    # ==========================================
    # Display Questions
    # ==========================================

    if "questions" in st.session_state:

        st.subheader("📋 Interview Questions")

        questions = st.session_state["questions"]

        if len(questions) == 0:

            st.warning("No questions generated.")

        else:

            for i, question in enumerate(questions):

                st.markdown(f"### Q{i+1}")

                st.write(question)

                st.divider()




    # ==========================================
    # Question Actions
    # ==========================================

    if "questions" in st.session_state:

        questions = st.session_state["questions"]

        st.subheader("📨 Question Actions")

        col1, col2 = st.columns(2)

        # -------------------------------
        # Copy Questions
        # -------------------------------

        with col1:

            if st.button(

                "📋 Copy Questions",

                use_container_width=True

            ):

                question_text = "\n\n".join(

                    [f"{i+1}. {q}" for i, q in enumerate(questions)]

                )

                st.code(

                    question_text,

                    language="text"

                )

                st.success(

                    "Questions are ready to copy."

                )

        # -------------------------------
        # Save Questions
        # -------------------------------

        with col2:

            if st.button(

                "💾 Save Questions",

                use_container_width=True

            ):

                from utils.database import save_interview_questions

                save_interview_questions(

                    candidate["id"],

                    job["id"],

                    interview_type,

                    "\n".join(questions)

                )

                st.success(

                    "✅ Interview Questions Saved Successfully!"

                )

        st.divider()

        # ==========================================
        # Question Summary
        # ==========================================

        st.subheader("📊 Question Summary")

        c1, c2, c3 = st.columns(3)

        with c1:

            st.metric(

                "Interview Type",

                interview_type

            )

        with c2:

            st.metric(

                "Difficulty",

                difficulty

            )

        with c3:

            st.metric(

                "Questions",

                len(questions)

            )

        st.divider()




    # ==========================================
    # View Saved Questions
    # ==========================================

    st.divider()

    st.subheader("📚 Saved Interview Questions")

    from utils.database import get_saved_interview_questions

    saved_questions = get_saved_interview_questions()

    if len(saved_questions) == 0:

        st.info("No interview questions available.")

    else:

        for item in saved_questions:

            with st.expander(

                f"{item['interview_type']} | Candidate ID : {item['candidate_id']}"

            ):

                st.write("### Interview Type")

                st.write(item["interview_type"])

                st.write("### Questions")

                st.text(item["questions"])

                st.write("### Created On")

                st.write(item["created_at"])

    st.divider()

    # ==========================================
    # Question Analytics
    # ==========================================

    st.subheader("📊 Question Analytics")

    total = len(saved_questions)

    ai = len(

        [

            q for q in saved_questions

            if "AI" in q["interview_type"]

        ]

    )

    technical = len(

        [

            q for q in saved_questions

            if "Technical" in q["interview_type"]

        ]

    )

    hr = len(

        [

            q for q in saved_questions

            if "HR" in q["interview_type"]

        ]

    )

    manager = len(

        [

            q for q in saved_questions

            if "Manager" in q["interview_type"]

        ]

    )

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric(

        "Total",

        total

    )

    c2.metric(

        "AI",

        ai

    )

    c3.metric(

        "Technical",

        technical

    )

    c4.metric(

        "HR",

        hr

    )

    c5.metric(

        "Manager",

        manager

    )

    st.divider()

    st.success(

        "🎉 Interview Questions Module Completed Successfully!"

    )