import streamlit as st
import pandas as pd
import database as db
from datetime import date, time

# Page configuration
st.set_page_config(
    page_title="Smarti Business Manager",
    page_icon="🌿",
    layout="wide"
)

# Initialise database
db.initialise_database()

# Sidebar navigation
st.sidebar.title("SMARTI")
st.sidebar.caption("Business Management System")

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Customers", "Staff", "Jobs & Appointments"]
)

st.sidebar.divider()
st.sidebar.caption("Smarti Environmental Limited")


# DASHBOARD
if page == "Dashboard":

    st.title("Business Dashboard")
    st.caption("Overview of your business operations")

    customers, active, pending, completed = db.get_dashboard_counts()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Customers", customers)
    col2.metric("Active Customers", active)
    col3.metric("Pending Jobs", pending)
    col4.metric("Completed Jobs", completed)

    st.divider()
    st.subheader("Upcoming Appointments")

    jobs = db.get_jobs()
    today = date.today().isoformat()

    upcoming = [job for job in jobs if job[3] >= today]

    if upcoming:
        st.dataframe(
            pd.DataFrame(
                upcoming,
                columns=[
                    "Job ID", "Customer", "Description",
                    "Date", "Time", "Assigned Staff", "Status"
                ]
            ),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No upcoming appointments.")


# CUSTOMER MANAGEMENT
elif page == "Customers":

    st.title("Customer Management")

    tab1, tab2, tab3 = st.tabs(
        ["Add Customer", "View Customers", "Edit Customer"]
    )

    with tab1:
        st.subheader("Register New Customer")

        with st.form("add_customer_form"):
            name = st.text_input("Customer Name")
            email = st.text_input("Email Address")
            phone = st.text_input("Phone Number")
            address = st.text_area("Customer Address")

            submitted = st.form_submit_button("Add Customer")

            if submitted:
                if not name.strip() or not email.strip() or not address.strip():
                    st.error("Name, email and address are required.")
                elif "@" not in email or "." not in email:
                    st.error("Please enter a valid email address.")
                else:
                    db.add_customer(name.strip(), email.strip(), phone.strip(), address.strip())
                    st.success("Customer successfully registered!")
                    st.rerun()

    with tab2:
        st.subheader("Customer Records")

        customers = db.get_customers()

        if customers:
            st.dataframe(
                pd.DataFrame(
                    customers,
                    columns=[
                        "ID", "Name", "Email", "Phone",
                        "Address", "Onboarding Status"
                    ]
                ),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No customers registered yet.")

    with tab3:
        st.subheader("Edit Customer Record")

        customers = db.get_customers()

        if customers:
            customer_options = {
                f"{c[1]} (ID: {c[0]})": c for c in customers
            }

            selected = st.selectbox(
                "Select Customer",
                list(customer_options.keys())
            )

            customer = customer_options[selected]

            with st.form("edit_customer_form"):
                name = st.text_input("Name", value=customer[1])
                email = st.text_input("Email", value=customer[2])
                phone = st.text_input("Phone", value=customer[3] or "")
                address = st.text_area("Address", value=customer[4])

                statuses = ["New Enquiry", "In Progress", "Active"]

                status = st.selectbox(
                    "Onboarding Status",
                    statuses,
                    index=statuses.index(customer[5])
                )

                submitted = st.form_submit_button("Save Changes")

                if submitted:
                    if not name.strip() or not email.strip() or not address.strip():
                        st.error("Name, email and address are required.")
                    elif "@" not in email or "." not in email:
                        st.error("Please enter a valid email address.")
                    else:
                        db.update_customer(
                            customer[0], name.strip(), email.strip(),
                            phone.strip(), address.strip(), status
                        )
                        st.success("Customer record updated!")
                        st.rerun()

        else:
            st.info("Add a customer before editing records.")


# STAFF MANAGEMENT
elif page == "Staff":

    st.title("Staff Management")
    st.caption("Manage fitters and maintenance engineers")

    tab1, tab2 = st.tabs(["Add Staff", "View Staff"])

    with tab1:
        with st.form("add_staff_form"):

            name = st.text_input("Staff Member Name")

            role = st.selectbox(
                "Staff Role",
                ["Fitter", "Maintenance Engineer"]
            )

            submitted = st.form_submit_button("Add Staff Member")

            if submitted:
                if not name.strip():
                    st.error("Please enter a staff member's name.")
                else:
                    db.add_staff(name.strip(), role)
                    st.success("Staff member added!")
                    st.rerun()

        with tab2:
            staff = db.get_staff()

        if staff:
            st.dataframe(
                pd.DataFrame(
                    staff,
                    columns=["Staff ID", "Name", "Role"]
                ),
                use_container_width=True,
                hide_index=True
            )

            selected_staff = st.selectbox(
                "Select staff member to delete",
                staff,
                format_func=lambda s: f"{s[1]} - {s[2]} (ID: {s[0]})"
            )

            if st.button("Delete Staff Member"):
                try:
                    db.delete_staff(selected_staff[0])
                    st.success("Staff member deleted.")
                    st.rerun()
                except ValueError as e:
                    st.error(str(e))

        else:
            st.info("No staff members registered yet.")


# JOBS AND APPOINTMENTS
elif page == "Jobs & Appointments":

    st.title("Jobs & Appointments")

    tab1, tab2 = st.tabs(
        ["Create Appointment", "Manage Jobs"]
    )

    with tab1:
        customers = db.get_customers()
        staff = db.get_staff()

        if not customers:
            st.warning("Register a customer before creating an appointment.")

        else:
            customer_options = {
                f"{c[1]} (ID: {c[0]})": c[0] for c in customers
            }

            staff_options = {"Unassigned": None}
            staff_options.update({
                f"{s[1]} - {s[2]}": s[0] for s in staff
            })

            with st.form("create_job_form"):

                customer = st.selectbox(
                    "Select Customer",
                    list(customer_options.keys())
                )

                assigned_staff = st.selectbox(
                    "Assign Staff Member",
                    list(staff_options.keys())
                )

                description = st.text_area("Job Description")

                appointment_date = st.date_input(
                    "Appointment Date",
                    min_value=date.today()
                )

                appointment_time = st.time_input(
                    "Appointment Time",
                    value=time(9, 0)
                )

                submitted = st.form_submit_button("Book Appointment")

                if submitted:
                    if not description.strip():
                        st.error("Please enter a job description.")
                    else:
                        db.add_job(
                            customer_options[customer],
                            staff_options[assigned_staff],
                            description.strip(),
                            appointment_date.isoformat(),
                            appointment_time.strftime("%H:%M")
                        )

                        st.success("Appointment successfully booked!")
                        st.rerun()

    with tab2:
        jobs = db.get_jobs()

        if jobs:
            st.subheader("Job Records")

            st.dataframe(
                pd.DataFrame(
                    jobs,
                    columns=[
                        "Job ID", "Customer", "Description",
                        "Date", "Time", "Assigned Staff", "Status"
                    ]
                ),
                use_container_width=True,
                hide_index=True
            )

            job_options = {
                f"Job {j[0]} - {j[1]} ({j[2]})": j[0]
                for j in jobs
            }

            selected_job = st.selectbox(
                "Select Job to Update",
                list(job_options.keys())
            )

            new_status = st.selectbox(
                "Update Job Status",
                ["Pending", "In Progress", "Completed"]
            )

            if st.button("Update Job Status"):
                db.update_job_status(
                    job_options[selected_job],
                    new_status
                )

                st.success("Job status updated!")
                st.rerun()

        else:
            st.info("No jobs or appointments have been created yet.")