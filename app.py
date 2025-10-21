import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import matplotlib.pyplot as plt

st.title("📊 Cloud-Based Student Marks Dashboard")

cred = credentials.Certificate("firebase_key.json)
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://student-dashboard-default-rtdb.firebaseio.com/'
    })

ref = db.reference("students")
data = ref.get()

st.write("### Student Marks Data", data)

for student, subjects in data.items():
    st.subheader(f"{student}'s Marks")
    fig, ax = plt.subplots()
    ax.bar(subjects.keys(), subjects.values(), color="skyblue")
    ax.set_xlabel("Subjects")
    ax.set_ylabel("Marks")
    ax.set_title(f"{student}'s Performance")
    st.pyplot(fig)
