import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import matplotlib.pyplot as plt

# --- Page Config ---
st.set_page_config(page_title="📊 Student Marks Dashboard", layout="wide")
st.title("📊 Cloud-Based Student Marks Dashboard")

# --- Load Firebase config from secrets ---
firebase_config = st.secrets["firebase"]

# Fix private key newlines
firebase_config["private_key"] = firebase_config["private_key"].replace('\\n', '\n')

# --- Initialize Firebase ---
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate(firebase_config)
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://student-dashboard-default-rtdb.firebaseio.com/'
        })
        st.success("✅ Firebase connection established successfully!")
    except Exception as e:
        st.error(f"🔥 Error initializing Firebase: {e}")
        st.stop()

# --- Reference to 'students' node ---
ref = db.reference("students")

# --- Sidebar: Add or Update Student Marks ---
st.sidebar.header("Add / Update Student Marks")
student_name = st.sidebar.text_input("Student Name")
subject = st.sidebar.text_input("Subject")
marks = st.sidebar.number_input("Marks", min_value=0, max_value=100, step=1)
add_button = st.sidebar.button("Add / Update Marks")

if add_button:
    if student_name.strip() and subject.strip():
        try:
            student_ref = ref.child(student_name.strip())
            student_ref.update({subject.strip(): marks})
            st.sidebar.success(f"✅ {subject} marks for {student_name} updated successfully!")
        except Exception as e:
            st.sidebar.error(f"🔥 Error updating data: {e}")
    else:
        st.sidebar.warning("⚠️ Please enter both student name and subject.")

# --- Fetch and display student data ---
st.subheader("📊 Student Marks Data")
try:
    data = ref.get()

    if not data:
        st.info("⚠️ No student data found.")
    else:
        for student, subjects in data.items():
            st.markdown(f"### {student}'s Marks")
            fig, ax = plt.subplots(figsize=(6,4))
            ax.bar(subjects.keys(), subjects.values(), color="skyblue")
            ax.set_xlabel("Subjects")
            ax.set_ylabel("Marks")
            ax.set_ylim(0, 100)
            ax.set_title(f"{student}'s Performance")
            st.pyplot(fig)

except Exception as e:
    st.error(f"🔥 Error fetching data from Firebase: {e}")

