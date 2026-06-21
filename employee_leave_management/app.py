# Import Libraries

import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Page Config

st.set_page_config(
    page_title="Employee Leave Management",
    page_icon="🏢",
    layout="wide"
)

# Custom CSS

st.markdown("""
<style>

/* Main Background */
.stApp {
    background: linear-gradient(135deg,#0f172a,#020617);
    color: white;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #111827;
}

/* Headers */
.main-title {
    font-size: 42px;
    font-weight: 700;
    color: white;
}

.sub-title {
    color: #94a3b8;
    font-size: 18px;
}

/* Cards */
.metric-card {
    background-color: #1e293b;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    border: 1px solid #334155;
}

/* Status badges */
.approved {
    color: #22c55e;
    font-weight: bold;
}

.rejected {
    color: #ef4444;
    font-weight: bold;
}

.pending {
    color: #f59e0b;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

# FastAPI URL

API = "http://127.0.0.1:8001"

# Header

st.markdown(
    """
    <div class='main-title'>
    🏢 Employee Leave Management System
    </div>
    <div class='sub-title'>
    Manage employee leave requests efficiently
    </div>
    <br>
    """,
    unsafe_allow_html=True
)

# Login Screen

if "user" not in st.session_state:

    col1, col2, col3 = st.columns([1,2,1])

    with col2:

        st.markdown("## 🔐 Login")

        email = st.text_input("Email")

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login", use_container_width=True):

            response = requests.post(
                f"{API}/login",
                json={
                    "email": email,
                    "password": password
                }
            )

            data = response.json()

            if "role" in data:

                st.session_state.user = data
                st.rerun()

            else:

                st.error(data["message"])

        st.markdown("---")

        st.info("""
### Demo Accounts

Employee Login

employee@gmail.com  
1234

Manager Login

manager@gmail.com  
1234
""")

# Dashboard

else:

    user = st.session_state.user

    # Sidebar

    st.sidebar.title("🏢 Leave Portal")

    st.sidebar.success(
        f"Logged in as\n\n**{user['name']}**\n\n({user['role']})"
    )

    if st.sidebar.button("🚪 Logout"):

        del st.session_state["user"]
        st.rerun()

    # Employee Dashboard

    if user["role"] == "employee":

        history = requests.get(
            f"{API}/leave_history/{user['id']}"
        ).json()

        total = len(history)

        approved = len(
            [x for x in history if x["status"] == "Approved"]
        )

        pending = len(
            [x for x in history if x["status"] == "Pending"]
        )

        st.header("👨‍💼 Employee Dashboard")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Leaves", total)

        with col2:
            st.metric("Approved", approved)

        with col3:
            st.metric("Pending", pending)

        st.markdown("---")

        # Apply Leave

        st.subheader("📝 Apply New Leave")

        col1, col2 = st.columns(2)

        with col1:
            start = st.date_input("Start Date")

        with col2:
            end = st.date_input("End Date")

        reason = st.text_area("Reason")

        if st.button("Apply Leave"):

            requests.post(
                f"{API}/apply_leave",
                json={
                    "employee_id": user["id"],
                    "start_date": str(start),
                    "end_date": str(end),
                    "reason": reason
                }
            )

            st.success("Leave Applied Successfully")
            st.rerun()

        st.markdown("---")

        # Leave History

        st.subheader("📜 Leave History")

        if history:

            df = pd.DataFrame(history)

            st.dataframe(
                df,
                use_container_width=True
            )

        else:

            st.info("No leave records found")

    # Manager Dashboard

    elif user["role"] == "manager":

        leaves = requests.get(
            f"{API}/all_leaves"
        ).json()

        approved = len(
            [x for x in leaves if x["status"] == "Approved"]
        )

        rejected = len(
            [x for x in leaves if x["status"] == "Rejected"]
        )

        pending = len(
            [x for x in leaves if x["status"] == "Pending"]
        )

        st.header("📋 Manager Dashboard")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Requests", len(leaves))

        with col2:
            st.metric("Approved", approved)

        with col3:
            st.metric("Pending", pending)

        st.markdown("---")

        # Leave Requests

        st.subheader("📑 All Leave Requests")

        if leaves:

            df = pd.DataFrame(leaves)

            st.dataframe(
                df,
                use_container_width=True
            )

        else:

            st.info("No leave requests found")

        st.markdown("---")

        # Update Leave

        st.subheader("✅ Approve / Reject Leave")

        col1, col2 = st.columns(2)

        with col1:
            leave_id = st.number_input(
                "Leave ID",
                min_value=1,
                step=1
            )

        with col2:
            status = st.selectbox(
                "Status",
                ["Approved", "Rejected"]
            )

        if st.button("Update Status"):

            requests.put(
                f"{API}/update_leave/{leave_id}",
                params={
                    "status": status
                }
            )

            st.success(
                f"Leave #{leave_id} updated to {status}"
            )

            st.rerun()

        st.markdown("---")

        # Statistics

        st.subheader("📊 Leave Statistics")

        stats_df = pd.DataFrame(
            {
                "Status": [
                    "Approved",
                    "Rejected",
                    "Pending"
                ],
                "Count": [
                    approved,
                    rejected,
                    pending
                ]
            }
        )

        col1, col2 = st.columns(2)

        with col1:

            st.dataframe(
                stats_df,
                use_container_width=True
            )

        with col2:

            fig = px.pie(
                stats_df,
                values="Count",
                names="Status",
                hole=0.5,
                title="Leave Distribution"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )
            