import streamlit as st
from datetime import datetime
import pandas as pd
import plotly.graph_objects as go
import random

st.set_page_config(
    page_title="Fitmat Class Portal",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --bg:      #0d0d0d;
    --surface: #141414;
    --card:    #1a1a1a;
    --border:  #2a2a2a;
    --green:   #22c55e;
    --green2:  #16a34a;
    --green3:  rgba(34,197,94,0.12);
    --text:    #e8e8e8;
    --muted:   #666;
    --muted2:  #888;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
    background: var(--bg) !important;
    color: var(--text) !important;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }

[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
    min-width: 210px !important; max-width: 210px !important;
}
[data-testid="stSidebar"] > div { padding: 0 !important; }
[data-testid="stSidebar"] * { color: var(--text) !important; }
[data-testid="stSidebar"] .stRadio > div { gap: 0 !important; }
[data-testid="stSidebar"] .stRadio label {
    display: block !important; padding: 13px 20px !important;
    margin: 0 !important; border-radius: 0 !important;
    font-size: 0.88rem !important; cursor: pointer !important;
    border-left: 3px solid transparent !important; color: #888 !important;
    transition: all 0.15s !important;
}
[data-testid="stSidebar"] .stRadio label:hover {
    background: var(--green3) !important; color: var(--green) !important;
    border-left-color: var(--green) !important;
}
[data-testid="stSidebar"] .stRadio [data-baseweb="radio"] > div:first-child { display: none !important; }

.stButton > button {
    background: var(--green) !important; color: #000 !important;
    border: none !important; border-radius: 8px !important;
    font-weight: 600 !important; font-size: 0.88rem !important;
    padding: 0.55rem 1.5rem !important; transition: all 0.15s !important;
}
.stButton > button:hover { background: var(--green2) !important; }

.stTextInput > div > div > input,
.stSelectbox > div > div,
.stTextArea textarea,
.stDateInput input {
    background: var(--card) !important; border: 1px solid var(--border) !important;
    border-radius: 8px !important; color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--green) !important;
    box-shadow: 0 0 0 2px rgba(34,197,94,0.2) !important;
}

[data-testid="stDataFrame"] {
    border-radius: 12px !important; border: 1px solid var(--border) !important;
}

[data-testid="metric-container"] {
    background: var(--card) !important; border: 1px solid var(--green) !important;
    border-radius: 12px !important; padding: 1.2rem !important;
}
[data-testid="metric-container"] label {
    font-size: 0.72rem !important; color: var(--muted2) !important;
    text-transform: uppercase !important; letter-spacing: 1px !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 2.4rem !important; color: var(--green) !important; line-height: 1 !important;
}

.stDownloadButton > button {
    background: transparent !important; color: var(--green) !important;
    border: 1px solid var(--green) !important; border-radius: 8px !important;
    font-size: 0.82rem !important;
}

/* image styles */
.hero-img {
    width: 100%; height: 200px; object-fit: cover;
    border-radius: 12px; border: 1px solid #2a2a2a;
    display: block;
}
.card-img {
    width: 100%; height: 140px; object-fit: cover;
    border-radius: 10px 10px 0 0; display: block;
}
.teacher-img {
    width: 56px; height: 56px; border-radius: 50%;
    object-fit: cover; border: 2px solid #22c55e; flex-shrink: 0;
}
.note-img {
    width: 100%; height: 110px; object-fit: cover;
    border-radius: 8px; margin-bottom: 10px; display: block;
}
</style>
""", unsafe_allow_html=True)

# ── DATA ──────────────────────────────────────────
TEACHERS = {
    "teacher1": {
        "password": "teach123",
        "name": "Mrs. Priya Sharma",
        "subjects": ["Math","Science"],
        "img": "https://images.unsplash.com/photo-1607990281513-2c110a25bd8c?w=200&q=80"
    },
    "teacher2": {
        "password": "teach456",
        "name": "Mr. Arjun Mehta",
        "subjects": ["English","History"],
        "img": "https://images.unsplash.com/photo-1531746020798-e6953c6e8e04?w=200&q=80"
    },
}

NOTES = [
    ("Algebra Basics",     "Math",    "Chapter 1–3: Linear equations",
     "https://images.unsplash.com/photo-1509228468518-180dd4864904?w=400&q=80"),
    ("Trigonometry",       "Math",    "Chapter 4–5: Sine, cosine, unit circle",
     "https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=400&q=80"),
    ("Newton's Laws",      "Science", "Chapter 2: Force, mass, acceleration",
     "https://images.unsplash.com/photo-1636466497217-26a8cbeaf0aa?w=400&q=80"),
    ("Cell Biology",       "Science", "Chapter 7: Cell structure and function",
     "https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=400&q=80"),
    ("Grammar Essentials", "English", "Parts of speech and sentence formation",
     "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=400&q=80"),
    ("Modern History",     "History", "Chapter 3: World War II overview",
     "https://images.unsplash.com/photo-1461360228754-6e81c478b882?w=400&q=80"),
]

STUDENTS = [
    {"Name":"Rahul Patil",    "Class":"10-A","Attendance":"92%","Score":82,
     "img":"https://images.unsplash.com/photo-1570295999919-56ceb5ecca61?w=100&q=80"},
    {"Name":"Sneha Kulkarni", "Class":"10-A","Attendance":"88%","Score":79,
     "img":"https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=100&q=80"},
    {"Name":"Aditya Joshi",   "Class":"10-B","Attendance":"95%","Score":91,
     "img":"https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=100&q=80"},
    {"Name":"Meera Nair",     "Class":"10-B","Attendance":"70%","Score":65,
     "img":"https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=100&q=80"},
    {"Name":"Ravi Deshmukh",  "Class":"10-A","Attendance":"85%","Score":74,
     "img":"https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=100&q=80"},
]

SUBJ_COLOR = {"Math":"#22c55e","Science":"#3b82f6","English":"#f59e0b","History":"#ef4444"}

PLOT = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#888", family="DM Sans"), margin=dict(l=10,r=10,t=36,b=10),
    xaxis=dict(gridcolor="#222", linecolor="#333", tickfont=dict(size=11,color="#666")),
    yaxis=dict(gridcolor="#222", linecolor="#333", tickfont=dict(size=11,color="#666")),
)

def att_data():
    random.seed(7)
    dates = pd.date_range(end=datetime.today(), periods=14)
    return pd.DataFrame({
        "Date":   [d.strftime("%d %b %Y") for d in dates],
        "Status": [random.choice(["Present","Present","Present","Absent"]) for _ in dates]
    })

# ── SESSION ───────────────────────────────────────
if "teacher" not in st.session_state: st.session_state.teacher = None

# ── SIDEBAR ───────────────────────────────────────
t = st.session_state.teacher
st.sidebar.markdown("""
<div style="padding:1.8rem 1.2rem 1rem;">
    <div style="font-family:'Bebas Neue',sans-serif;font-size:2rem;color:#22c55e;letter-spacing:2px;line-height:1;">FITMAT</div>
    <div style="font-size:0.65rem;color:#555;letter-spacing:2px;text-transform:uppercase;margin-top:2px;">Class Portal</div>
</div>
<div style="border-top:1px solid #222;margin-bottom:0.5rem;"></div>
""", unsafe_allow_html=True)

if t:
    st.sidebar.markdown(f"""
    <div style="display:flex;align-items:center;gap:10px;padding:0.6rem 1.2rem 0.8rem;">
        <img src="{t['img']}" style="width:34px;height:34px;border-radius:50%;object-fit:cover;border:2px solid #22c55e;flex-shrink:0;">
        <div>
            <div style="font-size:0.78rem;font-weight:500;color:#ddd;">{t['name'].split()[-1]}</div>
            <div style="font-size:0.65rem;color:#22c55e;">● Active</div>
        </div>
    </div>
    <div style="border-top:1px solid #222;margin-bottom:0.3rem;"></div>
    """, unsafe_allow_html=True)

pages = ["About Us","Teacher Login","Attendance","Notes","Students"]
icons = ["🏫","👩‍🏫","📋","📝","🎒"]
menu  = st.sidebar.radio("", [f"{icons[i]}  {p}" for i,p in enumerate(pages)], label_visibility="collapsed")
selected = menu.split("  ",1)[1]

if t:
    st.sidebar.markdown("<div style='border-top:1px solid #222;margin:0.5rem 0;'></div>", unsafe_allow_html=True)
    if st.sidebar.button("Sign out", use_container_width=True):
        st.session_state.teacher = None
        st.rerun()

# ── HELPERS ───────────────────────────────────────
def header(title, subtitle="", badge=None):
    badge_html = f'<div style="background:rgba(34,197,94,0.12);border:1px solid #22c55e;border-radius:20px;padding:5px 14px;font-size:0.78rem;font-weight:500;color:#22c55e;white-space:nowrap;">● {badge}</div>' if badge else ""
    st.markdown(f"""
    <div style="display:flex;justify-content:space-between;align-items:flex-start;
                padding-bottom:1.2rem;margin-bottom:1.5rem;border-bottom:1px solid #222;">
        <div>
            <div style="font-family:'Bebas Neue',sans-serif;font-size:2.4rem;
                        color:#e8e8e8;letter-spacing:1px;line-height:1;">{title}</div>
            <div style="font-size:0.82rem;color:#666;margin-top:4px;">{subtitle}</div>
        </div>
        {badge_html}
    </div>
    """, unsafe_allow_html=True)

def lock_gate(section):
    st.markdown(f"""
    <div style="background:#1a1a1a;border:1px solid #2a2a2a;border-radius:14px;
                padding:3rem 2rem;text-align:center;max-width:400px;">
        <div style="font-size:2.5rem;margin-bottom:1rem;">🔒</div>
        <div style="font-family:'Bebas Neue',sans-serif;font-size:1.6rem;color:#e8e8e8;
                    letter-spacing:1px;margin-bottom:0.5rem;">Teacher Login Required</div>
        <div style="font-size:0.85rem;color:#666;line-height:1.6;">
            Sign in via <b style="color:#22c55e;">Teacher Login</b> to access {section}.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════
st.markdown('<div style="padding:2rem 2.5rem;min-height:100vh;">', unsafe_allow_html=True)

# ── ABOUT US ──────────────────────────────────────
if selected == "About Us":
    header("ABOUT US", "Welcome to Fitmat Coaching Classes", "ACTIVE")

    # Hero banner image
    st.markdown("""
    <div style="position:relative;margin-bottom:1.5rem;border-radius:14px;overflow:hidden;">
        <img src="https://images.unsplash.com/photo-1524178232363-1fb2b075b655?w=1200&q=80"
             style="width:100%;height:220px;object-fit:cover;display:block;filter:brightness(0.45);">
        <div style="position:absolute;inset:0;display:flex;flex-direction:column;
                    justify-content:center;padding:0 2.5rem;">
            <div style="font-family:'Bebas Neue',sans-serif;font-size:2.6rem;
                        color:#22c55e;letter-spacing:2px;line-height:1;">SHAPING BRIGHT FUTURES</div>
            <div style="font-size:0.95rem;color:#ccc;margin-top:6px;max-width:500px;">
                Academic excellence meets physical discipline — since 2010.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Mission + Vision
    c1,c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div style="background:#1a1a1a;border:1px solid #2a2a2a;border-top:2px solid #22c55e;border-radius:12px;overflow:hidden;">
            <img src="https://images.unsplash.com/photo-1509062522246-3755977927d7?w=600&q=80"
                 style="width:100%;height:130px;object-fit:cover;display:block;filter:brightness(0.5);">
            <div style="padding:1.2rem 1.4rem;">
                <div style="font-family:'Bebas Neue',sans-serif;font-size:1.3rem;color:#22c55e;letter-spacing:1px;margin-bottom:0.6rem;">OUR MISSION</div>
                <div style="font-size:0.88rem;color:#aaa;line-height:1.8;">
                    Fitmat is dedicated to building a thriving, energetic learning environment where every student is
                    empowered to grow physically and mentally through structured fitness and education.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div style="background:#1a1a1a;border:1px solid #2a2a2a;border-top:2px solid #22c55e;border-radius:12px;overflow:hidden;">
            <img src="https://images.unsplash.com/photo-1488190211105-8b0e65b80b4e?w=600&q=80"
                 style="width:100%;height:130px;object-fit:cover;display:block;filter:brightness(0.5);">
            <div style="padding:1.2rem 1.4rem;">
                <div style="font-family:'Bebas Neue',sans-serif;font-size:1.3rem;color:#22c55e;letter-spacing:1px;margin-bottom:0.6rem;">OUR VISION</div>
                <div style="font-size:0.88rem;color:#aaa;line-height:1.8;">
                    To cultivate disciplined, healthy, and well-rounded individuals ready to contribute positively
                    to society through the power of consistent learning and physical activity.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    # Who We Are
    st.markdown("""
    <div style="background:#1a1a1a;border:1px solid #2a2a2a;border-radius:12px;overflow:hidden;margin-bottom:1rem;">
        <img src="https://images.unsplash.com/photo-1580582932707-520aed937b7b?w=1200&q=80"
             style="width:100%;height:180px;object-fit:cover;display:block;filter:brightness(0.4);">
        <div style="padding:1.8rem 2rem;">
            <div style="font-family:'Bebas Neue',sans-serif;font-size:1.4rem;color:#e8e8e8;letter-spacing:1px;margin-bottom:0.9rem;">WHO WE ARE</div>
            <div style="font-size:0.9rem;color:#aaa;line-height:1.9;margin-bottom:0.8rem;">
                Fitmat is a specialized class designed around holistic student development. We combine academic rigor
                with physical fitness programs, creating a unique environment where students excel both in the classroom and on the field.
            </div>
            <div style="font-size:0.9rem;color:#aaa;line-height:1.9;margin-bottom:1.5rem;">
                Our approach is student-first. With a team of dedicated educators and coaches, we ensure every learner
                receives personalized attention, structured routines, and the tools they need to succeed.
            </div>
            <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;">
                <div style="background:#111;border:1px solid #22c55e;border-radius:12px;padding:1.2rem;text-align:center;">
                    <div style="font-family:'Bebas Neue',sans-serif;font-size:2.2rem;color:#22c55e;line-height:1;">120+</div>
                    <div style="font-size:0.7rem;color:#666;letter-spacing:1.5px;text-transform:uppercase;margin-top:4px;">Students</div>
                </div>
                <div style="background:#111;border:1px solid #22c55e;border-radius:12px;padding:1.2rem;text-align:center;">
                    <div style="font-family:'Bebas Neue',sans-serif;font-size:2.2rem;color:#22c55e;line-height:1;">12</div>
                    <div style="font-size:0.7rem;color:#666;letter-spacing:1.5px;text-transform:uppercase;margin-top:4px;">Teachers</div>
                </div>
                <div style="background:#111;border:1px solid #22c55e;border-radius:12px;padding:1.2rem;text-align:center;">
                    <div style="font-family:'Bebas Neue',sans-serif;font-size:2.2rem;color:#22c55e;line-height:1;">95%</div>
                    <div style="font-size:0.7rem;color:#666;letter-spacing:1.5px;text-transform:uppercase;margin-top:4px;">Attendance Rate</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Meet the teachers
    st.markdown('<div style="font-size:0.72rem;font-weight:600;letter-spacing:1px;text-transform:uppercase;color:#555;margin-bottom:0.8rem;">Meet Our Teachers</div>', unsafe_allow_html=True)
    tc1,tc2 = st.columns(2)
    for i,(col,(_,td)) in enumerate(zip([tc1,tc2], TEACHERS.items())):
        tags = " ".join(f'<span style="background:rgba(34,197,94,0.1);color:#22c55e;border:1px solid rgba(34,197,94,0.3);border-radius:20px;padding:2px 8px;font-size:0.68rem;">{s}</span>' for s in td["subjects"])
        with col:
            st.markdown(f"""
            <div style="background:#1a1a1a;border:1px solid #2a2a2a;border-radius:12px;padding:1.1rem 1.3rem;
                        display:flex;align-items:center;gap:14px;">
                <img src="{td['img']}" style="width:52px;height:52px;border-radius:50%;object-fit:cover;border:2px solid #22c55e;flex-shrink:0;">
                <div>
                    <div style="font-weight:600;font-size:0.92rem;color:#e8e8e8;margin-bottom:3px;">{td['name']}</div>
                    <div>{tags}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ── TEACHER LOGIN ─────────────────────────────────
elif selected == "Teacher Login":
    t = st.session_state.teacher
    if t:
        header("TEACHER PANEL", f"Logged in as {t['name']}", "ACTIVE")
        tags = " ".join(f'<span style="background:rgba(34,197,94,0.1);color:#22c55e;border:1px solid rgba(34,197,94,0.3);border-radius:20px;padding:2px 10px;font-size:0.72rem;">{s}</span>' for s in t.get("subjects",[]))
        st.markdown(f"""
        <div style="background:#1a1a1a;border:1px solid #2a2a2a;border-top:2px solid #22c55e;
                    border-radius:12px;overflow:hidden;max-width:520px;margin-bottom:1.5rem;">
            <img src="https://images.unsplash.com/photo-1580582932707-520aed937b7b?w=800&q=80"
                 style="width:100%;height:100px;object-fit:cover;display:block;filter:brightness(0.35);">
            <div style="padding:1.2rem 1.4rem;display:flex;align-items:center;gap:14px;">
                <img src="{t['img']}" style="width:54px;height:54px;border-radius:50%;object-fit:cover;border:2px solid #22c55e;flex-shrink:0;margin-top:-28px;">
                <div>
                    <div style="font-weight:600;font-size:1rem;color:#e8e8e8;">{t['name']}</div>
                    <div style="font-size:0.78rem;color:#666;margin-bottom:5px;">Teacher · Fitmat Class Portal</div>
                    <div>{tags}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div style="font-size:0.72rem;font-weight:600;letter-spacing:1px;text-transform:uppercase;color:#555;margin-bottom:0.8rem;">Upload Study Material</div>', unsafe_allow_html=True)
        with st.form("upload"):
            title   = st.text_input("Note Title", placeholder="e.g. Chapter 5: Quadratic Equations")
            subject = st.selectbox("Subject", t.get("subjects",["General"]))
            desc    = st.text_area("Description", placeholder="Brief summary…")
            _f      = st.file_uploader("Attach file", type=["pdf","docx","png","jpg"])
            if st.form_submit_button("Upload Material"):
                if title: st.success(f"✅ '{title}' uploaded for {subject}!")
                else:     st.error("Please enter a title.")
    else:
        header("TEACHER LOGIN", "Sign in to access your panel")
        # login hero
        st.markdown("""
        <div style="border-radius:14px;overflow:hidden;margin-bottom:1.5rem;">
            <img src="https://images.unsplash.com/photo-1524178232363-1fb2b075b655?w=1200&q=80"
                 style="width:100%;height:160px;object-fit:cover;display:block;filter:brightness(0.35);">
        </div>
        """, unsafe_allow_html=True)
        _, col, _ = st.columns([1,1.2,1])
        with col:
            st.markdown('<div style="background:#1a1a1a;border:1px solid #2a2a2a;border-radius:14px;padding:2rem;">', unsafe_allow_html=True)
            st.markdown('<div style="font-size:0.72rem;font-weight:600;letter-spacing:1px;text-transform:uppercase;color:#555;margin-bottom:1rem;">Teacher Credentials</div>', unsafe_allow_html=True)
            username = st.text_input("Username", placeholder="teacher1 or teacher2")
            password = st.text_input("Password", type="password", placeholder="Enter password")
            st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
            if st.button("Sign In →", use_container_width=True):
                if username in TEACHERS and TEACHERS[username]["password"] == password:
                    st.session_state.teacher = TEACHERS[username]
                    st.rerun()
                else:
                    st.error("Invalid credentials.")
            st.markdown("</div>", unsafe_allow_html=True)
            with st.expander("Demo credentials"):
                st.markdown("| Username | Password |\n|---|---|\n| `teacher1` | `teach123` |\n| `teacher2` | `teach456` |")

# ── ATTENDANCE ────────────────────────────────────
elif selected == "Attendance":
    t = st.session_state.teacher
    header("ATTENDANCE", "Mark daily attendance")
    if not t:
        lock_gate("Attendance")
    else:
        st.markdown("""
        <div style="border-radius:12px;overflow:hidden;margin-bottom:1.2rem;">
            <img src="https://images.unsplash.com/photo-1588072432836-e10032774350?w=1200&q=80"
                 style="width:100%;height:130px;object-fit:cover;display:block;filter:brightness(0.35);">
        </div>
        """, unsafe_allow_html=True)

        c1,c2 = st.columns([1,2])
        with c1: date_sel = st.date_input("Date", value=datetime.today())
        with c2: subject  = st.selectbox("Subject", t.get("subjects",[]))

        st.markdown('<div style="font-size:0.72rem;font-weight:600;letter-spacing:1px;text-transform:uppercase;color:#555;margin:1rem 0 0.6rem;">Student List</div>', unsafe_allow_html=True)
        if "att_state" not in st.session_state:
            st.session_state.att_state = {s["Name"]: True for s in STUDENTS}

        for s in STUDENTS:
            name = s["Name"]
            c1,_,c3 = st.columns([4,1,1])
            with c1:
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;padding:8px 0;border-bottom:1px solid #1f1f1f;">
                    <img src="{s['img']}" style="width:34px;height:34px;border-radius:50%;object-fit:cover;border:1px solid #333;flex-shrink:0;">
                    <div>
                        <span style="font-weight:500;color:#ddd;font-size:0.9rem;">{name}</span>
                        <span style="font-size:0.74rem;color:#555;margin-left:8px;">{s['Class']}</span>
                    </div>
                </div>""", unsafe_allow_html=True)
            with c3:
                st.session_state.att_state[name] = st.checkbox(
                    "Present", value=st.session_state.att_state.get(name,True), key=f"att_{name}")

        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
        if st.button("Save Attendance"):
            p = sum(1 for v in st.session_state.att_state.values() if v)
            st.success(f"✅ Saved for {date_sel.strftime('%d %b %Y')} — {p}/{len(STUDENTS)} present.")

        att = att_data()
        present = sum(1 for s in att["Status"] if s=="Present")
        total   = len(att)
        fig = go.Figure(go.Pie(
            values=[present,total-present], labels=["Present","Absent"],
            hole=0.65, marker_colors=["#22c55e","#ef4444"]
        ))
        fig.update_traces(textinfo="none")
        fig.update_layout(height=220,
            annotations=[dict(text=f"<b>{int(present/total*100)}%</b>",x=0.5,y=0.5,font_size=18,showarrow=False,font_color="#22c55e")],
            **PLOT)
        st.plotly_chart(fig, use_container_width=True)

# ── NOTES ─────────────────────────────────────────
elif selected == "Notes":
    t = st.session_state.teacher
    header("NOTES", "Study material library")
    if not t:
        lock_gate("Notes")
    else:
        st.markdown("""
        <div style="border-radius:12px;overflow:hidden;margin-bottom:1.2rem;">
            <img src="https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=1200&q=80"
                 style="width:100%;height:120px;object-fit:cover;display:block;filter:brightness(0.35);">
        </div>
        """, unsafe_allow_html=True)

        search = st.text_input("Search…", placeholder="Algebra, Newton…")
        subj_f = st.selectbox("Filter", ["My Subjects"] + t.get("subjects",[]) + ["All"])
        notes  = NOTES
        if search: notes = [n for n in notes if search.lower() in n[0].lower()]
        if subj_f == "My Subjects": notes = [n for n in notes if n[1] in t.get("subjects",[])]
        elif subj_f != "All":       notes = [n for n in notes if n[1]==subj_f]

        if not notes:
            st.info("No notes found.")
        else:
            cols = st.columns(3)
            for i,(title,subj,desc,img) in enumerate(notes):
                c    = SUBJ_COLOR.get(subj,"#22c55e")
                mine = subj in t.get("subjects",[])
                with cols[i%3]:
                    st.markdown(f"""
                    <div style="background:#1a1a1a;border:1px solid #2a2a2a;border-top:2px solid {c if mine else '#2a2a2a'};
                                border-radius:12px;overflow:hidden;margin-bottom:0.8rem;opacity:{'1' if mine else '0.4'};">
                        <img src="{img}" style="width:100%;height:110px;object-fit:cover;display:block;filter:brightness(0.55);">
                        <div style="padding:1rem 1.1rem;">
                            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
                                <span style="background:rgba(34,197,94,0.1);color:{c};font-size:0.7rem;font-weight:600;
                                             padding:2px 8px;border-radius:20px;border:1px solid {c}30;">{subj}</span>
                                {'<span style="font-size:0.7rem;color:#22c55e;font-weight:600;">✓ Yours</span>' if mine else ''}
                            </div>
                            <div style="font-size:0.95rem;font-weight:600;color:#e8e8e8;margin-bottom:4px;">{title}</div>
                            <div style="font-size:0.8rem;color:#666;margin-bottom:10px;">{desc}</div>
                        </div>
                    </div>""", unsafe_allow_html=True)
                    if mine:
                        st.download_button("⬇ Download", data=f"# {title}\n{desc}",
                            file_name=f"{title.replace(' ','_')}.txt", key=f"dl_{i}")

# ── STUDENTS ──────────────────────────────────────
elif selected == "Students":
    t = st.session_state.teacher
    header("STUDENTS", "Enrolled students overview")
    if not t:
        lock_gate("Students")
    else:
        st.markdown("""
        <div style="border-radius:12px;overflow:hidden;margin-bottom:1.2rem;">
            <img src="https://images.unsplash.com/photo-1427504494785-3a9ca7044f45?w=1200&q=80"
                 style="width:100%;height:130px;object-fit:cover;display:block;filter:brightness(0.35);">
        </div>
        """, unsafe_allow_html=True)

        c1,c2,c3 = st.columns(3)
        c1.metric("Total Students","38")
        c2.metric("Avg Attendance","87%")
        c3.metric("Avg Score","79")

        st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)
        st.markdown('<div style="font-size:0.72rem;font-weight:600;letter-spacing:1px;text-transform:uppercase;color:#555;margin-bottom:0.8rem;">Student Roster</div>', unsafe_allow_html=True)

        for s in STUDENTS:
            score = s["Score"]
            bar_color = "#22c55e" if score>=80 else "#f59e0b" if score>=70 else "#ef4444"
            bar_w = int(score)
            st.markdown(f"""
            <div style="background:#1a1a1a;border:1px solid #2a2a2a;border-radius:12px;
                        padding:1rem 1.3rem;margin-bottom:0.65rem;
                        display:flex;align-items:center;gap:14px;">
                <img src="{s['img']}" style="width:44px;height:44px;border-radius:50%;object-fit:cover;
                           border:2px solid #2a2a2a;flex-shrink:0;">
                <div style="flex:1;min-width:0;">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;">
                        <span style="font-weight:600;font-size:0.92rem;color:#e8e8e8;">{s['Name']}</span>
                        <span style="font-size:0.78rem;color:#555;">{s['Class']}</span>
                    </div>
                    <div style="display:flex;align-items:center;gap:10px;">
                        <div style="flex:1;background:#222;border-radius:4px;height:5px;">
                            <div style="width:{bar_w}%;background:{bar_color};height:5px;border-radius:4px;"></div>
                        </div>
                        <span style="font-size:0.78rem;color:{bar_color};font-weight:600;flex-shrink:0;">
                            {score}/100
                        </span>
                    </div>
                    <div style="font-size:0.74rem;color:#555;margin-top:3px;">Attendance: {s['Attendance']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
        st.markdown('<div style="font-size:0.72rem;font-weight:600;letter-spacing:1px;text-transform:uppercase;color:#555;margin-bottom:0.6rem;">Score Chart</div>', unsafe_allow_html=True)
        fig = go.Figure(go.Bar(
            x=[s["Name"].split()[0] for s in STUDENTS],
            y=[s["Score"] for s in STUDENTS],
            marker=dict(
                color=[s["Score"] for s in STUDENTS],
                colorscale=[[0,"#ef4444"],[0.5,"#f59e0b"],[1,"#22c55e"]],
                showscale=False
            )
        ))
        fig.update_layout(height=240, **PLOT)
        st.plotly_chart(fig, use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)
