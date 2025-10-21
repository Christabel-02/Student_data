import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import matplotlib.pyplot as plt

st.set_page_config(page_title="📊 Student Marks Dashboard", layout="wide")
st.title("📊 Cloud-Based Student Marks Dashboard")

# --- Firebase credentials (directly in code) ---
firebase_config = {
    "type": "service_account",
    "project_id": "studentdashboard-31ab6",
    "private_key_id": "cc39422fc7113b909b524ffa83ac2a983d74fe31",
    "private_key": """-----BEGIN PRIVATE KEY-----
MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDJZYp0Ar1aK+Nw
zlG4AZdfvCTH9+IXJRG6wQyt0762hMcMLpheLi68XKaWaFGOEdDhfxi1LY6+MLIG
o6o+VW/BUfIY+bJHPTKIJcXbTYVD0yqVcMUBQDmyAf8NXEAF9fGJcr978SguW2DT
Gr8SvNyPSCuukmbRwIhV8kAx1skyowxEtl8VlwPiBITt00gx/I9khOcTa78EW2kM
M7FG9I0k+vNQ53wXH4ZDkqK7gIgnRccQxyYAuxzv+VQhLOVIcPaBwGT1MAr7d+Ss
77YI2BUphUUU4/SlP8GhQzlpeTkXker9sjp06mWaGAZQv8J1k/MGD5QG+IamaI11
4kCd8d/vAgMBAAECggEAGrTC09hrKJJqUhKh5n8bhh/qVrQJwJzzSWsBFenev9BC
ntxs6ww/uU2l74r8yZSWONjEO35Dj/fgG55HXIWy0JVfv60Y1XaJhWFQ5+BTPCe7
3V47WYudOvwlyK1DdibjdSEIwFQ9ykvmvoes77yomL1uwXL7fHQGADOkDJfZTUPy
O2Xpyetid5U7oxMtJHzPGwA2m7CYAEAxvTLwKdOvdhZikiWNbLCZ/4ZqlpT5AnK4
Lr8U+ILQNNJbsmYn9sNqDYTy5BifOOpXL1K5WvuOXjP0ky1zdSsA+qgo+tITCWZ1
eyLdH0NKN0oncjeVolEDveZvqYF0N1yg0mvcfnMzdQKBgQD7c9kYJCU49cpA2DqP
D43sFEPq322eb8ptYsnpNLub0DPr7wVbGPAbse9GnAxdKZmVd5aHWC1tneSIuYf9
wGCszfhdOwvGoRpN8CRqtu2Lgih3ra3GvBVrQRGzxM1Rge9xQfOWE4VAKlp2qjw7
HIhsCNj1Z7kAz0PeNUZeWpNb5QKBgQDNCfLZZVM0VlPUG4XkuglQ+IUpRp5a/8Ga
VmWaRZI8BvhZxh+W+kRAfDXZMwMBIlrqsgACMUHTVBFVLzzKhK36o/KsKESaFnqh
g5rreVy/qAfPNfzKz/r672HMfS6kGSXJHlBcS1lKTNZT8aiqCXJVBF3ESP5IYgKk
HbJJ6i5XQwKBgHxMC+iPFYdOmKftOyU0vycP7XLQ91L2V84yozSQSJ0BEmlyQeeC
ME7AalMxGDuFMNJdxx8oS2yAPFQJwluBGUjSmA8d/Pg28tXL+3R08H+h23ctd1Vh
7ASUqbd/dS7xV/dYbpylEZ1iUk2OYS+nLxiYVwcYOq9XxWi2VQ6XH3ixAoGAZRQm
eC2PWxnDsajv1NYxiY06eCKsJkg29RLqe6cYdCcrf3ZAVHmD9BZHpY+UR5bcIx8l
Ce+md7vV35yt51iJPCpek6g2SZATXFQ4pyTpKEJ5txjySjlFjTc9i0WbHKKZEhCz
pQwwNIS0lCVp9Ik7p9XDM+SYFq7ahnVtUyrzNWkCgYBD8TJsf0Yxmzt1Z4iV37AN
XtI8t4cEwOoSqu2UAJ47Z1Xwt83lqKwcpRlPkX3iY2g8ztzz1DVU/U2xaGwpT3no
BeETyrZTDRoHyqIHnA7jrpSyKp0qsoms+tiR/4QgWdo0u5uCXCvbdrw2ZspSSa5G
PHZK42xOVQofd1yDqOZjww==
-----END PRIVATE KEY-----""",
    "client_email": "firebase-adminsdk-fbsvc@studentdashboard-31ab6.iam.gserviceaccount.com",
    "client_id": "106151739209642121553",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40studentdashboard-31ab6.iam.gserviceaccount.com"
}

# --- Initialize Firebase ---
try:
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

