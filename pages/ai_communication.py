import streamlit as st

from pages import (
    interview_invitation,
    interview_reminder,
    offer_letter,
    rejection_email,
    welcome_email
)


def show():

    st.title("📧 AI Communication")

    menu = st.sidebar.radio(

        "Communication",

        [

            "📩 Interview Invitation",

            "⏰ Interview Reminder",

            "🎉 Offer Letter",

            "❌ Rejection Email",

            "👋 Welcome Email"

        ]

    )

    if menu == "📩 Interview Invitation":

        interview_invitation.show()

    elif menu == "⏰ Interview Reminder":

        interview_reminder.show()

    elif menu == "🎉 Offer Letter":

        offer_letter.show()

    elif menu == "❌ Rejection Email":

        rejection_email.show()

    else:

        welcome_email.show()