import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import matplotlib.pyplot as plt
import json

st.set_page_config(page_title="📊 Cloud-Based Student Marks Dashboard", layout="wide")
st.title("📊 Cloud-Based Student Marks Dashboard")

# --- Load Firebase credentials securely ---
# On Streamlit Cloud → set this in "Secrets" as [firebase] section
# Locally → you can place the JSON beside app.py and uncomment local option below.

if "firebase" in st.secrets:
    firebase_config = st.secrets["firebase"]
    cred = credentials.Certificate(json.loads(json.dumps(firebase_config)))
else:
    # 🔹 Uncomment this line only for local testing (if JSON file exists locally)
    # cred = credentials.Certificate("studentdashboard-31ab6-firebase-adminsdk-fbsvc-8c7ed1d9e2.json")
    st.error("⚠️ Firebase credentials not found. Please configure them in Streamlit Secrets.")
    st.stop()

# --- Initialize Firebase ---
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://studentdashboard-31ab6-default-rtdb.firebaseio.com/'
    })

# --- Fetch student data ---
try:
    ref = db.reference("students")
    data = ref.get()
except Exception as e:
    st.error(f"Error fetching data: {e}")
    st.stop()

if not data:
    st.warning("No student data found in Firebase Realtime Database.")
else:
    st.write("### Student Marks Data")
    st.json(data)

    # --- Plot marks for each student ---
    for student, subjects in data.items():
        st.subheader(f"📘 {student}'s Marks")
        fig, ax = plt.subplots()
        ax.bar(subjects.keys(), subjects.values(), color="skyblue")
        ax.set_xlabel("Subjects")
        ax.set_ylabel("Marks")
        ax.set_title(f"{student}'s Performance")
        st.pyplot(fig)
