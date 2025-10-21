import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import matplotlib.pyplot as plt

# ---------------------------
# 🎯 Streamlit App Title
# ---------------------------
st.title("📊 Cloud-Based Student Marks Dashboard")

# ---------------------------
# 🔐 Load Firebase credentials securely
# ---------------------------
try:
    firebase_config = st.secrets["firebase"]  # Reads from Streamlit Secrets
    if not firebase_admin._apps:
        cred = credentials.Certificate(firebase_config)
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://student-dashboard-default-rtdb.firebaseio.com/'
        })
    st.success("✅ Firebase connection established successfully!")

except Exception as e:
    st.error("❌ Firebase credentials not found or invalid. Please check Streamlit Secrets.")
    st.stop()

# ---------------------------
# 📦 Fetch Data from Firebase
# ---------------------------
try:
    ref = db.reference("students")
    data = ref.get()

    if data:
        st.write("### Student Marks Data", data)

        # ---------------------------
        # 📈 Display Charts
        # ---------------------------
        for student, subjects in data.items():
            st.subheader(f"{student}'s Marks")

            fig, ax = plt.subplots()
            ax.bar(subjects.keys(), subjects.values(), color="skyblue")
            ax.set_xlabel("Subjects")
            ax.set_ylabel("Marks")
            ax.set_title(f"{student}'s Performance")
            st.pyplot(fig)
    else:
        st.warning("⚠️ No student data found in Firebase Database.")

except Exception as e:
    st.error(f"🔥 Error fetching data from Firebase: {e}")



