import streamlit as st

from utils.database import (
    get_all_employees,
    get_employee_count,
    update_employee,
    delete_employee
)

import pandas as pd
import plotly.express as px


def show():

    st.title("👨‍💼 Employee Management")

    employees = get_all_employees()

    # ===============================
    # Dashboard
    # ===============================

    total = get_employee_count()

    active = len(
        [e for e in employees if e["status"] == "Active"]
    )

    inactive = len(
        [e for e in employees if e["status"] != "Active"]
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("👨‍💼 Total Employees", total)

    with c2:
        st.metric("🟢 Active", active)

    with c3:
        st.metric("🔴 Inactive", inactive)

    st.divider()

    # ===============================
    # No Employees
    # ===============================

    if len(employees) == 0:

        st.warning("No employees found.")

        return

    # ===============================
    # Select Employee
    # ===============================

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

    # ===============================
    # Employee Details
    # ===============================

    st.subheader("👤 Employee Details")

    col1, col2 = st.columns(2)

    with col1:

        st.write("**Employee ID:**", employee["employee_id"])
        st.write("**Name:**", employee["employee_name"])
        st.write("**Email:**", employee["email"])
        st.write("**Phone:**", employee["phone"])

    with col2:

        st.write("**Department:**", employee["department"])
        st.write("**Designation:**", employee["designation"])
        st.write("**Manager:**", employee["manager"])
        st.write("**Status:**", employee["status"])

    st.divider()



# ==========================================
# Update Employee
# ==========================================

    st.subheader("✏️ Update Employee")

    col1, col2 = st.columns(2)

    with col1:

        designation = st.text_input(
        "Designation",
        value=employee["designation"]
        )

        department = st.text_input(
        "Department",
        value=employee["department"]
        )

        phone = st.text_input(
        "Phone",
        value=employee["phone"]
        )

    with col2:

        manager = st.text_input(
        "Reporting Manager",
        value=employee["manager"]
        )

        location = st.text_input(
        "Location",
        value=employee["location"]
        )

        status_options = [
        "Active",
        "Inactive",
        "On Leave"
        ]

        current_status = employee["status"]

        if current_status not in status_options:
            current_status = "Active"

        status = st.selectbox(

            "Status",

            status_options,

            index=status_options.index(current_status)

        )

    st.divider()

    # ==========================================
# Employee Actions
# ==========================================

    from utils.database import (
        update_employee,
    delete_employee
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
        "💾 Update Employee",
        use_container_width=True
        ):

            update_employee(

            employee["employee_id"],

            designation,

            department,

            manager,

            phone,

            location,

            status

            )

            st.success(
            "✅ Employee Updated Successfully!"
            )

            st.balloons()

    with col2:

        if st.button(
        "🗑 Delete Employee",
        use_container_width=True
        ):

            delete_employee(
            employee["employee_id"]
            )

            st.success(
            "🗑 Employee Deleted Successfully!"
            )

            st.rerun()

    st.divider()

    # ==========================================
# Search Employee
# ==========================================

    st.subheader("🔍 Search Employee")

    search = st.text_input(
    "Search by Employee Name or ID"
    )

    if search:

        filtered = [

            e for e in employees

            if search.lower() in e["employee_name"].lower()

            or search.lower() in e["employee_id"].lower()

        ]

    else:

        filtered = employees

    st.divider()

    # ==========================================
# Employee Analytics
# ==========================================

    st.subheader("📊 Employee Analytics")

    df = pd.DataFrame(employees)

    col1, col2 = st.columns(2)

    with col1:

        dept = (
        df["department"]
        .value_counts()
        .reset_index()
        )

        dept.columns = [
        "Department",
        "Employees"
        ]

        fig = px.bar(

            dept,

        x="Department",

        y="Employees",

        title="Employees by Department"

        )

        st.plotly_chart(

            fig,

        use_container_width=True

        )

    with col2:

        status = (
        df["status"]
        .value_counts()
        .reset_index()
        )

        status.columns = [
        "Status",
        "Employees"
        ]

        fig2 = px.pie(

        status,

        names="Status",

        values="Employees",

        title="Employee Status"

        )

        st.plotly_chart(

            fig2,

        use_container_width=True

        )

    st.divider()


    # ==========================================
# Employee Directory
# ==========================================

    st.subheader("📋 Employee Directory")

    display = pd.DataFrame(filtered)

    if not display.empty:

        display = display[
            [
            "employee_id",
            "employee_name",
            "designation",
            "department",
            "manager",
            "joining_date",
            "status"
            ]
        ]

        st.dataframe(

            display,

            use_container_width=True,

            hide_index=True

        )

    else:

        st.info("No matching employees found.")



    st.divider()

    st.subheader("📈 Employee Summary")

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
        "Total Employees",
        total
        )

    with c2:

        st.metric(
        "Active Employees",
        active
    )

    with c3:

        st.metric(
        "Inactive Employees",
        inactive
    )

    st.divider()

    st.success(
    "🎉 Employee Management Module Completed Successfully!"
    )