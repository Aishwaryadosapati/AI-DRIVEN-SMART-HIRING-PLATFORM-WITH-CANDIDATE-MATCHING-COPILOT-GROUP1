import streamlit as st

from utils.database import (
    get_all_employees,
    save_performance
)


def show():

    st.title("🌟 Talent Management")

    employees = get_all_employees()

    if len(employees) == 0:

        st.warning("No employees available.")

        return

    employee_options = {

        f"{e['employee_name']} ({e['employee_id']})": e

        for e in employees

    }

    selected = st.selectbox(

        "👤 Select Employee",

        list(employee_options.keys())

    )

    employee = employee_options[selected]

    st.divider()

    st.subheader("👤 Employee Information")

    col1, col2 = st.columns(2)

    with col1:

        st.write("**Employee ID:**", employee["employee_id"])
        st.write("**Employee Name:**", employee["employee_name"])
        st.write("**Email:**", employee["email"])
        st.write("**Phone:**", employee["phone"])

    with col2:

        st.write("**Department:**", employee["department"])
        st.write("**Designation:**", employee["designation"])
        st.write("**Manager:**", employee["manager"])
        st.write("**Status:**", employee["status"])

    st.divider()

    st.subheader("📈 Employee Performance")


    col1, col2 = st.columns(2)

    with col1:

        performance_rating = st.slider(

            "Performance Rating",

            1,

            5,

            3

        )

        kpi_score = st.slider(

            "KPI Score",

            0,

            100,

            80

        )

        attendance = st.slider(

            "Attendance (%)",

            0,

            100,

            95

        )

    with col2:

        goal_completion = st.slider(

            "Goal Completion (%)",

            0,

            100,

            85

        )

        manager_feedback = st.text_area(

            "Manager Feedback"

        )

    st.divider()


    # ==========================================
# AI Performance Review
# ==========================================

    st.subheader("🤖 AI Performance Review")

    if st.button(

        "Generate Performance Review",

        use_container_width=True

    ):

        from models.performance_ai import generate_performance_review

        with st.spinner("Generating AI Review..."):

            review = generate_performance_review(

                employee["employee_name"],

            employee["designation"],

            performance_rating,

            kpi_score,

            attendance,

            goal_completion,

            manager_feedback

            )

        st.session_state["performance_review"] = review

        st.success(
        "AI Performance Review Generated!"
        )

    st.divider()


    if "performance_review" in st.session_state:

        st.subheader("📄 AI Review")

        st.text_area(

        "Performance Review",

        st.session_state["performance_review"],

        height=350

        )  

    st.divider()

    st.subheader("🚀 Promotion Recommendation")

    promotion = st.selectbox(

        "Recommendation",

        [

        "Promotion Ready",

        "Needs Improvement",

        "Training Required"

        ]

    )

    hr_notes = st.text_area(

        "HR Notes"

    )

    st.divider()

    if st.button(

    "💾 Save Performance",

    use_container_width=True

    ):

        

        save_performance(

        employee["employee_id"],

        employee["employee_name"],

        performance_rating,

        kpi_score,

        attendance,

        goal_completion,

        manager_feedback,

        st.session_state.get("performance_review", ""),

        promotion,

        hr_notes

        )

        st.success(
        "Performance Saved Successfully!"
        )

        st.balloons()



    st.divider()

    st.subheader("📊 Performance Dashboard")

    c1, c2, c3,c4 = st.columns(4)

    with c1:

        st.metric(

                "Performance",

                f"{performance_rating}/5"

        )

    with c2:

        st.metric(

                "KPI",

                f"{kpi_score}%"

        )

    with c3:

        st.metric(

                "Attendance",

                f"{attendance}%"

        )


    with c4:
        st.metric(
        "🎯 Goals",
        f"{goal_completion}%"
        )

    st.success(
        f" 🚀 Promotion Recommendation: {promotion}"
    )

    st.divider()

    st.success(
                "🎉 Employee Performance has been saved successfully!"
    )

