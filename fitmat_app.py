import streamlit as st
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random

# ── CONFIG ─────────────────────────────────────────
st.set_page_config(
    page_title="Fitmat Coaching Classes",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CUSTOM CSS ─────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── ROOT PALETTE ── */
:root {
    --bg:        #0f1117;
    --surface:   #181c27;
    --card:      #1e2336;
    --border:    #2a2f45;
    --accent:    #f5a623;
    --accent2:   #e86c3a;
    --text:      #e8eaf2;
    --muted:     #7a7f9a;
    --green:     #3ecf8e;
    --red:       #e85d75;
    --blue:      #4f8ef7;
}

/* ── GLOBAL ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

/* ── HIDE STREAMLIT CHROME ── */
#MainMenu, footer, header {visibility: hidden;}
.block-container { padding: 2rem 2.5rem !important; }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--text) !important; }

/* ── SIDEBAR RADIO ── */
[data-testid="stSidebar"] .stRadio label {
    padding: 10px 14px !important;
    border-radius: 10px !important;
    margin-bottom: 4px !important;
    display: block !important;
    transition: background 0.2s !important;
    font-size: 0.9rem !important;
    cursor: pointer !important;
}
[data-testid="stSidebar"] .stRadio label:hover {
    background: var(--card) !important;
}

/* ── METRIC CARDS ── */
[data-testid="metric-container"] {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 16px !important;
    padding: 1.25rem !important;
}
[data-testid="metric-container"] label { color: var(--muted) !important; font-size: 0.8rem !important; }
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-family: 'Playfair Display', serif !important;
    font-size: 2rem !important;
    color: var(--accent) !important;
}

/* ── BUTTONS ── */
.stButton > button {
    background: linear-gradient(135deg, var(--accent), var(--accent2)) !important;
    color: #0f1117 !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.5rem 1.4rem !important;
    transition: transform 0.15s, box-shadow 0.15s !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(245,166,35,0.35) !important;
}

/* ── INPUTS ── */
.stTextInput > div > div > input,
.stSelectbox > div > div,
.stTextArea > div > div > textarea {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(245,166,35,0.2) !important;
}

/* ── DATAFRAME ── */
[data-testid="stDataFrame"] { border-radius: 12px !important; overflow: hidden !important; }

/* ── EXPANDER ── */
.streamlit-expanderHeader {
    background: var(--card) !important;
    border-radius: 10px !important;
    border: 1px solid var(--border) !important;
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--card) !important;
    border-radius: 12px !important;
    padding: 4px !important;
    gap: 4px !important;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px !important;
    color: var(--muted) !important;
    font-weight: 500 !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, var(--accent), var(--accent2)) !important;
    color: #0f1117 !important;
}

/* ── DOWNLOAD BUTTON ── */
.stDownloadButton > button {
    background: var(--card) !important;
    color: var(--accent) !important;
    border: 1px solid var(--accent) !important;
    border-radius: 8px !important;
    font-size: 0.8rem !important;
}

/* ── HERO CARD ── */
.hero-card {
    background: linear-gradient(135deg, #1a2340 0%, #252d4a 60%, #1e2a50 100%);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 1.5rem;
}
.hero-avatar {
    width: 64px; height: 64px;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    display: flex; align-items: center; justify-content: center;
    font-size: 1.8rem; font-weight: 700;
    color: #0f1117; flex-shrink: 0;
}
.hero-text h1 {
    font-family: 'Playfair Display', serif;
    font-size: 1.8rem;
    margin: 0 0 4px 0;
    color: var(--text);
}
.hero-text p { margin: 0; color: var(--muted); font-size: 0.9rem; }
.role-badge {
    display: inline-block;
    padding: 3px 12px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    margin-top: 6px;
    letter-spacing: 0.5px;
}
.badge-admin   { background: rgba(245,166,35,0.15); color: var(--accent); border: 1px solid rgba(245,166,35,0.3); }
.badge-teacher { background: rgba(79,142,247,0.15); color: var(--blue);   border: 1px solid rgba(79,142,247,0.3); }
.badge-student { background: rgba(62,207,142,0.15); color: var(--green);  border: 1px solid rgba(62,207,142,0.3); }

/* ── INFO CARD ── */
.info-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1rem;
}
.info-card h4 { margin: 0 0 0.5rem 0; font-size: 0.85rem; color: var(--muted); text-transform: uppercase; letter-spacing: 0.8px; }

/* ── NOTICE BANNER ── */
.notice {
    background: rgba(245,166,35,0.08);
    border-left: 4px solid var(--accent);
    border-radius: 0 10px 10px 0;
    padding: 0.75rem 1rem;
    margin-bottom: 1rem;
    font-size: 0.9rem;
}

/* ── SECTION TITLE ── */
.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.4rem;
    margin-bottom: 1rem;
    color: var(--text);
}

/* ── LOGIN PAGE ── */
.login-wrap {
    max-width: 420px;
    margin: 4rem auto;
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 24px;
    padding: 3rem 2.5rem;
    box-shadow: 0 24px 80px rgba(0,0,0,0.5);
}
.login-logo {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    font-weight: 700;
    text-align: center;
    margin-bottom: 0.25rem;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.login-sub { text-align: center; color: var(--muted); font-size: 0.9rem; margin-bottom: 2rem; }
</style>
""", unsafe_allow_html=True)

# ── USERS ──────────────────────────────────────────
USERS = {
    "admin": {
        "password": "admin123",
        "role": "Admin",
        "name": "Admin",
        "subjects": [],
        "email": "admin@fitmat.edu"
    },
    "teacher1": {
        "password": "teach123",
        "role": "Teacher",
        "name": "Mrs. Priya Sharma",
        "subjects": ["Math", "Science"],
        "email": "priya@fitmat.edu"
    },
    "teacher2": {
        "password": "teach456",
        "role": "Teacher",
        "name": "Mr. Arjun Mehta",
        "subjects": ["English", "History"],
        "email": "arjun@fitmat.edu"
    },
    "student1": {
        "password": "1234",
        "role": "Student",
        "name": "Rahul Patil",
        "class": "10-A",
        "email": "rahul@student.fitmat.edu"
    },
    "student2": {
        "password": "5678",
        "role": "Student",
        "name": "Sneha Kulkarni",
        "class": "10-A",
        "email": "sneha@student.fitmat.edu"
    },
}

# ── SESSION STATE ──────────────────────────────────
for k, v in {"logged_in": False, "user": None}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── SAMPLE DATA ───────────────────────────────────
NOTES = [
    ("Algebra Basics",     "Math",    "Chapter 1–3: Linear equations and polynomials"),
    ("Trigonometry",       "Math",    "Chapter 4–5: Sine, cosine, and unit circle"),
    ("Newton's Laws",      "Science", "Chapter 2: Force, mass, acceleration"),
    ("Cell Biology",       "Science", "Chapter 7: Cell structure and function"),
    ("Grammar Essentials", "English", "Parts of speech and sentence formation"),
]

STUDENTS_DATA = [
    {"Name": "Rahul Patil",     "Class": "10-A", "Attendance": "92%", "Avg Score": 82},
    {"Name": "Sneha Kulkarni",  "Class": "10-A", "Attendance": "88%", "Avg Score": 79},
    {"Name": "Aditya Joshi",    "Class": "10-B", "Attendance": "95%", "Avg Score": 91},
    {"Name": "Meera Nair",      "Class": "10-B", "Attendance": "70%", "Avg Score": 65},
    {"Name": "Ravi Deshmukh",   "Class": "10-A", "Attendance": "85%", "Avg Score": 74},
]

TIMETABLE = {
    "Monday":    [("8:00",  "Math",    "Mrs. Priya Sharma"),  ("10:00", "Science",  "Mrs. Priya Sharma"),  ("12:00", "English", "Mr. Arjun Mehta")],
    "Tuesday":   [("8:00",  "History", "Mr. Arjun Mehta"),    ("10:00", "Math",     "Mrs. Priya Sharma"),  ("12:00", "Science", "Mrs. Priya Sharma")],
    "Wednesday": [("8:00",  "English", "Mr. Arjun Mehta"),    ("10:00", "History",  "Mr. Arjun Mehta"),    ("12:00", "Math",    "Mrs. Priya Sharma")],
    "Thursday":  [("8:00",  "Science", "Mrs. Priya Sharma"),  ("10:00", "English",  "Mr. Arjun Mehta"),    ("12:00", "History", "Mr. Arjun Mehta")],
    "Friday":    [("8:00",  "Math",    "Mrs. Priya Sharma"),  ("10:00", "English",  "Mr. Arjun Mehta"),    ("12:00", "Science", "Mrs. Priya Sharma")],
}

def get_attendance():
    dates = pd.date_range(end=datetime.today(), periods=14)
    random.seed(42)
    return pd.DataFrame({
        "Date":   [d.strftime("%d %b %Y") for d in dates],
        "Status": [random.choice(["✅ Present", "✅ Present", "✅ Present", "❌ Absent"]) for _ in dates]
    })

def get_performance():
    return {
        "tests":    [60, 68, 74, 78, 82, 85, 88],
        "labels":   ["Test 1","Test 2","Test 3","Test 4","Test 5","Test 6","Test 7"],
        "subjects": {"Math": 85, "Science": 78, "English": 82, "History": 74},
    }

def role_badge(role):
    cls = {"Admin": "badge-admin", "Teacher": "badge-teacher", "Student": "badge-student"}.get(role, "badge-student")
    return f'<span class="role-badge {cls}">{role.upper()}</span>'

# ── PLOTLY THEME ──────────────────────────────────
PLOT_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#e8eaf2", family="DM Sans"),
    margin=dict(l=20, r=20, t=40, b=20),
    xaxis=dict(gridcolor="#2a2f45", linecolor="#2a2f45"),
    yaxis=dict(gridcolor="#2a2f45", linecolor="#2a2f45"),
)

# ══════════════════════════════════════════════════
# LOGIN
# ══════════════════════════════════════════════════
def login():
    st.markdown('<div class="login-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="login-logo">🎓 Fitmat</div>', unsafe_allow_html=True)
    st.markdown('<div class="login-sub">Coaching Classes Portal</div>', unsafe_allow_html=True)

    username = st.text_input("Username", placeholder="Enter your username")
    password = st.text_input("Password", type="password", placeholder="Enter your password")

    if st.button("Sign In →", use_container_width=True):
        if username in USERS and USERS[username]["password"] == password:
            st.session_state.logged_in = True
            st.session_state.user = {**USERS[username], "username": username}
            st.rerun()
        else:
            st.error("Invalid username or password. Please try again.")

    st.markdown("---")
    with st.expander("ℹ️ Demo Credentials"):
        st.markdown("""
| Role | Username | Password |
|---|---|---|
| Admin | `admin` | `admin123` |
| Teacher | `teacher1` | `teach123` |
| Teacher | `teacher2` | `teach456` |
| Student | `student1` | `1234` |
""")
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════
# SHARED HERO
# ══════════════════════════════════════════════════
def hero():
    u = st.session_state.user
    initial = u["name"][0].upper()
    badge = role_badge(u["role"])
    now = datetime.now().strftime("%A, %d %B %Y")
    st.markdown(f"""
    <div class="hero-card">
        <div class="hero-avatar">{initial}</div>
        <div class="hero-text">
            <h1>Welcome back, {u['name'].split()[0]}!</h1>
            <p>{now}</p>
            {badge}
        </div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════
# STUDENT DASHBOARD
# ══════════════════════════════════════════════════
def student_dashboard():
    u = st.session_state.user
    menu_items = ["🏠 Dashboard", "📅 Timetable", "📄 Study Material", "📈 Performance"]
    menu = st.sidebar.radio("Navigation", menu_items, label_visibility="collapsed")

    hero()

    if "Dashboard" in menu:
        st.markdown('<div class="section-title">📊 Your Overview</div>', unsafe_allow_html=True)
        st.markdown('<div class="notice">📢 <b>Notice:</b> Unit Test 3 scheduled for next Monday. Check study material for revision notes.</div>', unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Attendance",    "92%",   "↑ 2% this month")
        c2.metric("Average Score", "82",    "↑ 4 pts")
        c3.metric("Tests Taken",   "7",     "1 upcoming")
        c4.metric("Rank in Class", "#3",    "↑ 2 places")

        st.markdown("---")
        col1, col2 = st.columns([3, 2])

        with col1:
            st.markdown('<div class="section-title">📈 Recent Performance</div>', unsafe_allow_html=True)
            data = get_performance()
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=data["labels"], y=data["tests"],
                mode="lines+markers",
                line=dict(color="#f5a623", width=3),
                marker=dict(size=8, color="#e86c3a"),
                fill="tozeroy",
                fillcolor="rgba(245,166,35,0.08)"
            ))
            fig.update_layout(title="Score Trend", **PLOT_LAYOUT)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown('<div class="section-title">📚 Subject Scores</div>', unsafe_allow_html=True)
            data = get_performance()
            fig2 = go.Figure(go.Bar(
                x=list(data["subjects"].values()),
                y=list(data["subjects"].keys()),
                orientation="h",
                marker=dict(
                    color=list(data["subjects"].values()),
                    colorscale=[[0, "#e86c3a"], [1, "#f5a623"]],
                    showscale=False
                )
            ))
            fig2.update_layout(title="By Subject", **PLOT_LAYOUT)
            st.plotly_chart(fig2, use_container_width=True)

    elif "Timetable" in menu:
        st.markdown('<div class="section-title">📅 Weekly Timetable</div>', unsafe_allow_html=True)
        day_cols = st.columns(len(TIMETABLE))
        for i, (day, slots) in enumerate(TIMETABLE.items()):
            with day_cols[i]:
                st.markdown(f'<div class="info-card"><h4>{day}</h4>', unsafe_allow_html=True)
                for time, subj, teacher in slots:
                    colors = {"Math": "#f5a623", "Science": "#3ecf8e", "English": "#4f8ef7", "History": "#e85d75"}
                    c = colors.get(subj, "#7a7f9a")
                    st.markdown(f"""
                    <div style="border-left:3px solid {c}; padding:6px 10px; margin:6px 0; border-radius:0 8px 8px 0; background:rgba(255,255,255,0.03);">
                        <div style="font-size:0.7rem;color:#7a7f9a;">{time}</div>
                        <div style="font-weight:600;color:{c};">{subj}</div>
                        <div style="font-size:0.75rem;color:#7a7f9a;">{teacher}</div>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

    elif "Study Material" in menu:
        st.markdown('<div class="section-title">📄 Study Material</div>', unsafe_allow_html=True)
        search = st.text_input("🔍 Search notes...", placeholder="e.g. Algebra, Newton...")
        subj_filter = st.selectbox("Filter by subject", ["All", "Math", "Science", "English"])

        notes = NOTES
        if search:
            notes = [n for n in notes if search.lower() in n[0].lower() or search.lower() in n[1].lower()]
        if subj_filter != "All":
            notes = [n for n in notes if n[1] == subj_filter]

        if not notes:
            st.info("No notes found matching your search.")
        else:
            cols = st.columns(3)
            colors = {"Math": "#f5a623", "Science": "#3ecf8e", "English": "#4f8ef7", "History": "#e85d75"}
            for i, (title, subject, desc) in enumerate(notes):
                c = colors.get(subject, "#7a7f9a")
                with cols[i % 3]:
                    st.markdown(f"""
                    <div class="info-card" style="border-top: 3px solid {c};">
                        <div style="font-size:0.75rem;font-weight:600;color:{c};text-transform:uppercase;letter-spacing:0.5px;margin-bottom:6px;">{subject}</div>
                        <div style="font-size:1rem;font-weight:600;margin-bottom:4px;">{title}</div>
                        <div style="font-size:0.8rem;color:#7a7f9a;margin-bottom:10px;">{desc}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.download_button(
                        f"⬇ Download",
                        data=f"# {title}\nSubject: {subject}\n\n{desc}\n\n[Full content would appear here]",
                        file_name=f"{title.replace(' ', '_')}.txt",
                        key=f"dl_{i}"
                    )

    elif "Performance" in menu:
        st.markdown('<div class="section-title">📈 Performance Analysis</div>', unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["📊 Charts", "📅 Attendance"])

        with tab1:
            data = get_performance()
            c1, c2 = st.columns(2)
            with c1:
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=data["labels"], y=data["tests"],
                    mode="lines+markers",
                    line=dict(color="#f5a623", width=3),
                    marker=dict(size=9, color="#e86c3a"),
                    fill="tozeroy", fillcolor="rgba(245,166,35,0.07)"
                ))
                fig.update_layout(title="Score Progression", **PLOT_LAYOUT)
                st.plotly_chart(fig, use_container_width=True)
            with c2:
                fig2 = go.Figure(go.Bar(
                    x=list(data["subjects"].keys()),
                    y=list(data["subjects"].values()),
                    marker=dict(color=["#f5a623","#3ecf8e","#4f8ef7","#e85d75"])
                ))
                fig2.update_layout(title="Subject-wise Scores", **PLOT_LAYOUT)
                st.plotly_chart(fig2, use_container_width=True)

        with tab2:
            att = get_attendance()
            present = sum(1 for s in att["Status"] if "Present" in s)
            total   = len(att)
            pct     = int(present / total * 100)

            fig3 = go.Figure(go.Pie(
                values=[present, total - present],
                labels=["Present", "Absent"],
                hole=0.65,
                marker=dict(colors=["#3ecf8e", "#e85d75"])
            ))
            fig3.update_traces(textinfo="none")
            fig3.update_layout(
                title=f"Attendance: {pct}%",
                annotations=[dict(text=f"<b>{pct}%</b>", x=0.5, y=0.5, font_size=20, showarrow=False, font_color="#f5a623")],
                **PLOT_LAYOUT
            )
            c1, c2 = st.columns([1, 2])
            with c1:
                st.plotly_chart(fig3, use_container_width=True)
            with c2:
                st.dataframe(att, use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════
# TEACHER DASHBOARD
# ══════════════════════════════════════════════════
def teacher_dashboard():
    u = st.session_state.user
    menu_items = ["🏠 Dashboard", "👥 Students", "📅 My Schedule", "📤 Upload Material", "📝 Mark Attendance"]
    menu = st.sidebar.radio("Navigation", menu_items, label_visibility="collapsed")

    # Teacher info in sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**Subjects:** {', '.join(u.get('subjects', []))}")
    st.sidebar.markdown(f"**Email:** {u.get('email','')}")

    hero()

    if "Dashboard" in menu:
        st.markdown('<div class="section-title">📊 Class Overview</div>', unsafe_allow_html=True)
        st.markdown('<div class="notice">📢 <b>Reminder:</b> Submit Unit Test 3 marks by Friday.</div>', unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Students", "38")
        c2.metric("Avg Attendance", "87%")
        c3.metric("Avg Class Score", "79")
        c4.metric("Tests Graded",   "6 / 7")

        st.markdown("---")
        col1, col2 = st.columns([3, 2])
        with col1:
            st.markdown('<div class="section-title">📈 Class Score Trend</div>', unsafe_allow_html=True)
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=["Test 1","Test 2","Test 3","Test 4","Test 5","Test 6"],
                y=[72, 74, 76, 77, 80, 79],
                mode="lines+markers",
                line=dict(color="#4f8ef7", width=3),
                fill="tozeroy", fillcolor="rgba(79,142,247,0.07)"
            ))
            fig.update_layout(title="Class Average per Test", **PLOT_LAYOUT)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown('<div class="section-title">🏆 Top Performers</div>', unsafe_allow_html=True)
            top = sorted(STUDENTS_DATA, key=lambda x: x["Avg Score"], reverse=True)[:3]
            for rank, s in enumerate(top, 1):
                medal = ["🥇", "🥈", "🥉"][rank - 1]
                st.markdown(f"""
                <div class="info-card" style="padding:0.9rem 1.2rem;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <div>{medal} <b>{s['Name']}</b> <span style="color:#7a7f9a;font-size:0.8rem;">{s['Class']}</span></div>
                        <div style="color:#f5a623;font-weight:600;">{s['Avg Score']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    elif "Students" in menu:
        st.markdown('<div class="section-title">👥 Student Management</div>', unsafe_allow_html=True)

        search = st.text_input("🔍 Search student...", placeholder="Name or class")
        df = pd.DataFrame(STUDENTS_DATA)
        if search:
            df = df[df["Name"].str.contains(search, case=False) | df["Class"].str.contains(search, case=False)]

        st.dataframe(df, use_container_width=True, hide_index=True)

        st.markdown("---")
        st.markdown('<div class="section-title">📊 Score Distribution</div>', unsafe_allow_html=True)
        fig = go.Figure(go.Bar(
            x=[s["Name"].split()[0] for s in STUDENTS_DATA],
            y=[s["Avg Score"] for s in STUDENTS_DATA],
            marker=dict(color=[s["Avg Score"] for s in STUDENTS_DATA],
                        colorscale=[[0,"#e85d75"],[0.5,"#f5a623"],[1,"#3ecf8e"]],
                        showscale=False)
        ))
        fig.update_layout(title="Student Average Scores", **PLOT_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)

    elif "Schedule" in menu:
        st.markdown('<div class="section-title">📅 My Weekly Schedule</div>', unsafe_allow_html=True)
        my_subjects = u.get("subjects", [])
        day_cols = st.columns(len(TIMETABLE))
        colors = {"Math": "#f5a623", "Science": "#3ecf8e", "English": "#4f8ef7", "History": "#e85d75"}

        for i, (day, slots) in enumerate(TIMETABLE.items()):
            with day_cols[i]:
                st.markdown(f'<div class="info-card"><h4>{day}</h4>', unsafe_allow_html=True)
                for time, subj, teacher in slots:
                    if subj in my_subjects:
                        c = colors.get(subj, "#7a7f9a")
                        st.markdown(f"""
                        <div style="border-left:3px solid {c}; padding:6px 10px; margin:6px 0; border-radius:0 8px 8px 0; background:rgba(255,255,255,0.04);">
                            <div style="font-size:0.7rem;color:#7a7f9a;">{time}</div>
                            <div style="font-weight:600;color:{c};">{subj}</div>
                            <div style="font-size:0.75rem;color:#3ecf8e;">✓ Your class</div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        c = colors.get(subj, "#7a7f9a")
                        st.markdown(f"""
                        <div style="border-left:3px solid #2a2f45; padding:6px 10px; margin:6px 0; border-radius:0 8px 8px 0; opacity:0.45;">
                            <div style="font-size:0.7rem;color:#7a7f9a;">{time}</div>
                            <div style="font-weight:500;color:#7a7f9a;">{subj}</div>
                        </div>
                        """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

    elif "Upload" in menu:
        st.markdown('<div class="section-title">📤 Upload Study Material</div>', unsafe_allow_html=True)
        with st.form("upload_form"):
            title   = st.text_input("Note Title",   placeholder="e.g. Chapter 5: Quadratic Equations")
            subject = st.selectbox("Subject", u.get("subjects", ["General"]))
            desc    = st.text_area("Description / Summary", placeholder="Brief summary of the content...")
            file    = st.file_uploader("Attach File (PDF / DOCX / Image)", type=["pdf","docx","png","jpg"])
            submitted = st.form_submit_button("Upload Material")
            if submitted:
                if title and subject:
                    st.success(f"✅ '{title}' uploaded successfully for {subject}!")
                else:
                    st.error("Please fill in all required fields.")

    elif "Attendance" in menu:
        st.markdown('<div class="section-title">📝 Mark Attendance</div>', unsafe_allow_html=True)
        date_sel = st.date_input("Select Date", value=datetime.today())
        subject  = st.selectbox("Subject", u.get("subjects", []))
        st.markdown("---")

        if "attendance_state" not in st.session_state:
            st.session_state.attendance_state = {s["Name"]: True for s in STUDENTS_DATA}

        for s in STUDENTS_DATA:
            name = s["Name"]
            cols = st.columns([4, 1])
            with cols[0]:
                st.markdown(f"**{name}** — {s['Class']}")
            with cols[1]:
                st.session_state.attendance_state[name] = st.checkbox(
                    "Present", value=st.session_state.attendance_state[name], key=f"att_{name}"
                )

        st.markdown("---")
        if st.button("Save Attendance", use_container_width=True):
            present_count = sum(1 for v in st.session_state.attendance_state.values() if v)
            st.success(f"✅ Attendance saved for {date_sel.strftime('%d %b %Y')} — {present_count}/{len(STUDENTS_DATA)} present.")

# ══════════════════════════════════════════════════
# ADMIN DASHBOARD
# ══════════════════════════════════════════════════
def admin_dashboard():
    menu_items = ["🏠 Dashboard", "👥 All Students", "👩‍🏫 Teachers", "📅 Timetable"]
    menu = st.sidebar.radio("Navigation", menu_items, label_visibility="collapsed")

    hero()

    if "Dashboard" in menu:
        st.markdown('<div class="section-title">📊 Institute Overview</div>', unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Students", "156")
        c2.metric("Teachers",       "8")
        c3.metric("Classes",        "6")
        c4.metric("Avg Attendance", "89%")

        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="section-title">📈 Monthly Attendance</div>', unsafe_allow_html=True)
            fig = go.Figure(go.Bar(
                x=["Jan","Feb","Mar","Apr","May"],
                y=[88, 85, 90, 87, 89],
                marker=dict(color=["#f5a623","#e86c3a","#3ecf8e","#4f8ef7","#f5a623"])
            ))
            fig.update_layout(title="Avg Monthly Attendance %", **PLOT_LAYOUT)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown('<div class="section-title">📊 Subject Performance</div>', unsafe_allow_html=True)
            fig2 = go.Figure(go.Bar(
                x=["Math","Science","English","History"],
                y=[79, 82, 85, 71],
                marker=dict(color=["#f5a623","#3ecf8e","#4f8ef7","#e85d75"])
            ))
            fig2.update_layout(title="Avg Score by Subject", **PLOT_LAYOUT)
            st.plotly_chart(fig2, use_container_width=True)

    elif "Students" in menu:
        st.markdown('<div class="section-title">👥 All Students</div>', unsafe_allow_html=True)
        df = pd.DataFrame(STUDENTS_DATA)
        st.dataframe(df, use_container_width=True, hide_index=True)

    elif "Teachers" in menu:
        st.markdown('<div class="section-title">👩‍🏫 Teacher Directory</div>', unsafe_allow_html=True)
        teachers = [(k, v) for k, v in USERS.items() if v["role"] == "Teacher"]
        for uname, t in teachers:
            st.markdown(f"""
            <div class="info-card" style="display:flex;justify-content:space-between;align-items:center;">
                <div>
                    <div style="font-weight:600;font-size:1rem;">{t['name']}</div>
                    <div style="color:#7a7f9a;font-size:0.85rem;">{t['email']}</div>
                    <div style="margin-top:6px;">
                        {''.join(f'<span style="background:#4f8ef720;color:#4f8ef7;border:1px solid #4f8ef730;border-radius:20px;padding:2px 10px;font-size:0.75rem;margin-right:6px;">{s}</span>' for s in t['subjects'])}
                    </div>
                </div>
                <div style="color:#3ecf8e;font-size:0.85rem;">● Active</div>
            </div>
            """, unsafe_allow_html=True)

    elif "Timetable" in menu:
        st.markdown('<div class="section-title">📅 Full Timetable</div>', unsafe_allow_html=True)
        colors = {"Math": "#f5a623", "Science": "#3ecf8e", "English": "#4f8ef7", "History": "#e85d75"}
        day_cols = st.columns(len(TIMETABLE))
        for i, (day, slots) in enumerate(TIMETABLE.items()):
            with day_cols[i]:
                st.markdown(f'<div class="info-card"><h4>{day}</h4>', unsafe_allow_html=True)
                for time, subj, teacher in slots:
                    c = colors.get(subj, "#7a7f9a")
                    st.markdown(f"""
                    <div style="border-left:3px solid {c}; padding:6px 10px; margin:6px 0; border-radius:0 8px 8px 0; background:rgba(255,255,255,0.03);">
                        <div style="font-size:0.7rem;color:#7a7f9a;">{time}</div>
                        <div style="font-weight:600;color:{c};">{subj}</div>
                        <div style="font-size:0.75rem;color:#7a7f9a;">{teacher}</div>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════
# SIDEBAR BRAND
# ══════════════════════════════════════════════════
def sidebar_brand():
    u = st.session_state.user
    st.sidebar.markdown("""
    <div style="text-align:center;padding:1.5rem 0 1rem;">
        <div style="font-family:'Playfair Display',serif;font-size:1.6rem;font-weight:700;
                    background:linear-gradient(135deg,#f5a623,#e86c3a);
                    -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
            🎓 Fitmat
        </div>
        <div style="font-size:0.75rem;color:#7a7f9a;margin-top:2px;">Coaching Classes</div>
    </div>
    """, unsafe_allow_html=True)
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**{u['name']}**")
    st.sidebar.markdown(role_badge(u["role"]), unsafe_allow_html=True)
    st.sidebar.markdown("---")

# ══════════════════════════════════════════════════
# ROUTER
# ══════════════════════════════════════════════════
if st.session_state.logged_in:
    sidebar_brand()
    if st.sidebar.button("⏻  Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.rerun()

    role = st.session_state.user["role"]
    if role == "Admin":
        admin_dashboard()
    elif role == "Teacher":
        teacher_dashboard()
    else:
        student_dashboard()
else:
    login()
