import streamlit as st

import pages.interview_questions as interview_questions
import pages.interview_scheduling as interview_scheduling


def show():

    st.title("📅 Interview Management")

    option = st.radio(

        "Select Module",

        [

            "Interview Questions",

            "Interview Scheduling"

        ],

        horizontal=True

    )

    st.divider()

    if option == "Interview Questions":

        interview_questions.show()

    else:

        interview_scheduling.show()