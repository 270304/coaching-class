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

# ── LOGIN PAGE ─────────────────────────────────────
def login():
    st.markdown("## 📚 Fitmat Coaching Classes")

    st.image(
        "https://images.unsplash.com/photo-1523240795612-9a054b0db644?w=1000",
        use_column_width=True
    )

    st.subheader("🔐 Login")

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
        ("Algebra", "Math", "https://images.unsplash.com/photo-1633356122544-f134324ef6db?w=300"),
        ("Trigonometry", "Math", "https://images.unsplash.com/photo-1509228468518-180dd4864904?w=300"),
        ("Physics Basics", "Science", "https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=300"),
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

    # 🔔 Notification
    st.toast("Welcome back!")

    # ── DASHBOARD ──
    if menu == "Dashboard":
        col1, col2 = st.columns(2)

        with col1:
            st.metric("Attendance", "92%")
            st.metric("Avg Score", "82")

        with col2:
            st.image(
                "https://images.unsplash.com/photo-1588072432836-e10032774350?w=500",
                use_column_width=True
            )

    # ── TIMETABLE ──
    elif menu == "Timetable":
        st.image(
            "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=1000",
            use_column_width=True
        )

        df = pd.DataFrame({
            "Day": ["Monday", "Tuesday", "Wednesday"],
            "Subject": ["Math", "Science", "English"]
        })
        st.dataframe(df)

    # ── STUDY MATERIAL ──
    elif menu == "Study Material":
        st.subheader("📄 Notes")

        search = st.text_input("🔍 Search notes")

        notes = get_notes()
        notes = [n for n in notes if search.lower() in n[0].lower()]

        cols = st.columns(3)

        for i, (title, subject, img) in enumerate(notes):
            with cols[i % 3]:
                st.image(img, use_column_width=True)
                st.write(f"📘 **{title}**")
                st.caption(subject)

                st.download_button(
                    "⬇ Download",
                    data="Sample content",
                    file_name=f"{title}.txt"
                )

    # ── PERFORMANCE ──
    elif menu == "Performance":
        data = get_performance()

        st.image(
            "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=1000",
            use_column_width=True
        )

        # 📊 Line Chart
        fig = px.line(y=data["tests"], markers=True, title="Performance Trend")
        st.plotly_chart(fig, use_container_width=True)

        # 📊 Bar Chart
        fig2 = px.bar(
            x=list(data["subjects"].keys()),
            y=list(data["subjects"].values()),
            title="Subject Scores"
        )
        st.plotly_chart(fig2, use_container_width=True)

        # 📅 Attendance
        st.subheader("📅 Attendance")
        st.dataframe(get_attendance())

# ── ROUTER ─────────────────────────────────────────
if st.session_state.logged_in:
    dashboard()
else:
    login()
