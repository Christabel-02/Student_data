import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import matplotlib.pyplot as plt

st.set_page_config(page_title="📊 Student Marks Dashboard", layout="wide")
st.title("📊 Cloud-Based Student Marks Dashboard")

# --- Load Firebase config from Streamlit Secrets ---
firebase_config = st.secrets["firebase"]

# Replace escaped newlines with actual newlines
firebase_config["private_key"] = firebase_config["private_key"].replace("\\n", "\n")

try:
    # Initialize Firebase app if not already initialized
    if not firebase_admin._apps:
        cred = credentials.Certificate(firebase_config)
        firebase_admin.initialize_app(cred, {
            "databaseURL": "https://student-dashboard-default-rtdb.firebaseio.com/"
        })
    st.success("✅ Firebase connection established successfully!")
except Exception as e:
    st.error(f"🔥 Error connecting to Firebase: {e}")

# --- Fetch student data ---
try:
    ref = db.reference("students")
    data = ref.get()
    
    if data:
        st.write("### Student Marks Data", data)
        for student, subjects in data.items():
            st.subheader(f"{student}'s Marks")
            fig, ax = plt.subplots()
            ax.bar(subjects.keys(), subjects.values(), color="skyblue")
            ax.set_xlabel("Subjects")
            ax.set_ylabel("Marks")
            ax.set_title(f"{student}'s Performance")
            st.pyplot(fig)
    else:
        st.info("No student data found in Firebase.")
except Exception as e:
    st.error(f"🔥 Error fetching data from Firebase: {e}")
