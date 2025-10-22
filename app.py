import streamlit as st
import pandas as pd
import firebase_admin
from firebase_admin import credentials, db
from datetime import date
import plotly.express as px

# ----------------------------
# Firebase Initialization
# ----------------------------
if not firebase_admin._apps:
    firebase_config = st.secrets["firebase"]
    cred = credentials.Certificate(firebase_config)
    firebase_admin.initialize_app(cred, {
        "databaseURL": firebase_config["databaseURL"]
    })

# ----------------------------
# Streamlit Page Setup
# ----------------------------
st.set_page_config(page_title="Cloud-Based Student Marks Dashboard", layout="wide")

st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            background-color: #1E1E1E;
            color: white;
        }
        h1, h2, h3, h4 {
            color: #f1f1f1 !important;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# ----------------------------
# Sidebar: Add / Manage Marks
# ----------------------------
st.sidebar.header("Add / Manage Marks")

name = st.sidebar.text_input("Student Name")
student_id = st.sidebar.text_input("Student ID (optional)")
subject = st.sidebar.text_input("Subject")
marks = st.sidebar.number_input("Marks (0-100)", min_value=0, max_value=100, step=1)
today = st.sidebar.date_input("Date", value=date.today())

if st.sidebar.button("Add Record"):
    if name and subject:
        ref = db.reference("/marks")
        ref.push({
            "name": name,
            "student_id": student_id if student_id else "-",
            "subject": subject,
            "marks": marks,
            "date": str(today)
        })
        st.sidebar.success("Record added successfully!")
    else:
        st.sidebar.error("Please enter student name and subject")

# ----------------------------
# Fetch Data from Firebase
# ----------------------------
st.title("🎓 Cloud-Based Student Marks Dashboard")

try:
    ref = db.reference("/marks")
    data = ref.get()

    if data:
        df = pd.DataFrame(data.values())
        st.subheader("📊 Dashboard - All Records")
        st.dataframe(df)

        # Filters
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            selected_subject = st.selectbox("Filter by Subject", ["All"] + sorted(df["subject"].unique().tolist()))
        with col2:
            selected_student = st.selectbox("Filter by Student", ["All"] + sorted(df["name"].unique().tolist()))
        with col3:
            show_chart = st.checkbox("Show Charts", value=True)

        filtered_df = df.copy()
        if selected_subject != "All":
            filtered_df = filtered_df[filtered_df["subject"] == selected_subject]
        if selected_student != "All":
            filtered_df = filtered_df[filtered_df["name"] == selected_student]

        # Display Average / Aggregate
        st.subheader("📈 Average Marks by Subject")
        avg_df = filtered_df.groupby("subject")["marks"].mean().reset_index()
        st.dataframe(avg_df)

        if show_chart:
            fig = px.bar(avg_df, x="subject", y="marks", title="Average Marks by Subject", text_auto=True)
            st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning("No records found. Please add some data.")
except Exception as e:
    st.error(f"Error fetching data from Firebase: {e}")
