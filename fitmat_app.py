import streamlit as st
from datetime import datetime
import pandas as pd
import plotly.express as px
import hashlib
import random

# ── CONFIG ─────────────────────────────────────────
st.set_page_config(page_title="Fitmat Coaching", layout="wide")

# ── PASSWORD HASHING ───────────────────────────────
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ── USERS ──────────────────────────────────────────
USERS = {
    "admin": {"password": hash_password("admin123"), "role": "Admin", "name": "Admin"},
    "rahul": {"password": hash_password("1234"), "role": "Student", "name": "Rahul"},
}

# ── SESSION STATE ──────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ── LOGIN ──────────────────────────────────────────
def login():
    st.title("🔐 Fitmat Login")

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        if user in USERS and USERS[user]["password"] == hash_password(pwd):
            st.session_state.logged_in = True
            st.session_state.user = USERS[user]
            st.rerun()
        else:
            st.error("Invalid credentials")

# ── DATA ───────────────────────────────────────────
def get_performance():
    return {
        "tests": [60, 70, 75, 80, 85],
        "subjects": {"Math": 85, "Science": 78, "English": 82}
    }

def get_notes():
    return [
        ("Algebra", "Math"),
        ("Trigonometry", "Math"),
        ("Physics Basics", "Science"),
    ]

def get_attendance():
    dates = pd.date_range(end=datetime.today(), periods=7)
    return pd.DataFrame({
        "Date": dates,
        "Status": [random.choice(["Present", "Absent"]) for _ in dates]
    })

# ── DASHBOARD ──────────────────────────────────────
def dashboard():
    st.sidebar.title("📚 Fitmat Panel")

    menu = st.sidebar.radio("Menu", [
        "Dashboard",
        "Timetable",
        "Study Material",
        "Performance"
    ])

    st.title(f"Welcome {st.session_state.user['name']} 👋")

    # 🔔 Notifications
    st.toast("Welcome back!")

    # ── DASHBOARD ──
    if menu == "Dashboard":
        st.metric("Attendance", "92%")
        st.metric("Avg Score", "82")

    # ── TIMETABLE ──
    elif menu == "Timetable":
        df = pd.DataFrame({
            "Day": ["Mon", "Tue"],
            "Subject": ["Math", "Science"]
        })
        st.dataframe(df)

    # ── STUDY MATERIAL ──
    elif menu == "Study Material":
        st.subheader("📄 Notes")

        search = st.text_input("Search")

        notes = get_notes()
        notes = [n for n in notes if search.lower() in n[0].lower()]

        for title, subject in notes:
            st.write(f"📘 {title} ({subject})")

            st.download_button(
                "Download",
                data="Sample content",
                file_name=f"{title}.txt"
            )

    # ── PERFORMANCE ──
    elif menu == "Performance":
        data = get_performance()

        # 📊 Chart
        fig = px.line(y=data["tests"], markers=True, title="Performance")
        st.plotly_chart(fig, use_container_width=True)

        # 📊 Subject
        fig2 = px.bar(x=list(data["subjects"].keys()),
                      y=list(data["subjects"].values()),
                      title="Subjects")
        st.plotly_chart(fig2, use_container_width=True)

        # 📅 Attendance
        st.subheader("Attendance")
        st.dataframe(get_attendance())

# ── ROUTER ─────────────────────────────────────────
if st.session_state.logged_in:
    dashboard()
else:
    login()
