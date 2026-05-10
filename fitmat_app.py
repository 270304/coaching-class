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

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"],
[data-testid="stMain"],
[data-testid="stVerticalBlock"],
section.main,
.main, .block-container {
    background-color: #0d0d0d !important;
}
.block-container { padding: 0 !important; max-width: 100% !important; }

html, body, p, div, span, label, li, a, h1, h2, h3,
[data-testid="stMarkdown"],
[data-testid="stText"],
[data-testid="stVerticalBlock"] * {
    color: #e8e8e8 !important;
    font-family: 'DM Sans', sans-serif !important;
}

#MainMenu, footer, header { visibility: hidden; }

[data-testid="stSidebar"],
[data-testid="stSidebar"] > div,
[data-testid="stSidebar"] section {
    background-color: #141414 !important;
    border-right: 1px solid #222 !important;
    min-width: 210px !important;
    max-width: 210px !important;
}
[data-testid="stSidebar"] * { color: #e8e8e8 !important; }
[data-testid="stSidebar"] .stRadio > div { gap: 0 !important; }
[data-testid="stSidebar"] .stRadio label {
    display: block !important;
    padding: 13px 20px !important;
    margin: 0 !important;
    border-radius: 0 !important;
    font-size: 0.88rem !important;
    cursor: pointer !important;
    border-left: 3px solid transparent !important;
    color: #777 !important;
    background: transparent !important;
}
[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(34,197,94,0.08) !important;
    color: #22c55e !important;
    border-left-color: #22c55e !important;
}
[data-testid="stSidebar"] .stRadio [data-baseweb="radio"] > div:first-child { display: none !important; }

input, textarea, select,
.stTextInput input,
.stTextArea textarea,
[data-baseweb="input"] input,
[data-baseweb="textarea"] textarea {
    background-color: #1e1e1e !important;
    color: #e8e8e8 !important;
    border: 1px solid #333 !important;
    border-radius: 8px !important;
}
input::placeholder, textarea::placeholder { color: #555 !important; }
input:focus, textarea:focus { border-color: #22c55e !important; outline: none !important; }

[data-baseweb="select"] > div {
    background-color: #1e1e1e !important;
    border: 1px solid #333 !important;
    color: #e8e8e8 !important;
}
[data-baseweb="popover"] > div, [role="listbox"] { background-color: #1e1e1e !important; }
[role="option"] { color: #e8e8e8 !important; background-color: #1e1e1e !important; }
[role="option"]:hover { background-color: #252525 !important; }

.stButton > button {
    background: #22c55e !important;
    color: #000 !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    padding: 0.55rem 1.5rem !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stButton > button:hover { background: #16a34a !important; }
.stDownloadButton > button {
    background: transparent !important;
    color: #22c55e !important;
    border: 1px solid #22c55e !important;
    border-radius: 8px !important;
}

[data-testid="metric-container"] {
    background: #1a1a1a !important;
    border: 1px solid #22c55e !important;
    border-radius: 12px !important;
    padding: 1.1rem !important;
}
[data-testid="metric-container"] label { color: #888 !important; font-size: 0.72rem !important; text-transform: uppercase !important; letter-spacing: 1px !important; }
[data-testid="stMetricValue"] { font-family: 'Bebas Neue', sans-serif !important; font-size: 2.2rem !important; color: #22c55e !important; line-height: 1 !important; }

[data-testid="stForm"] {
    background: #1a1a1a !important;
    border: 1px solid #2a2a2a !important;
    border-radius: 12px !important;
    padding: 1.2rem !important;
}

.streamlit-expanderHeader {
    background: #1a1a1a !important;
    border: 1px solid #2a2a2a !important;
    border-radius: 8px !important;
    color: #e8e8e8 !important;
}
.streamlit-expanderContent { background: #1a1a1a !important; }

[data-baseweb="checkbox"] span { border-color: #22c55e !important; }

[data-testid="stFileUploader"] { background: #1a1a1a !important; border-radius: 8px !important; }
[data-testid="stFileUploaderDropzone"] {
    background: #1a1a1a !important;
    border: 1px dashed #333 !important;
    border-radius: 8px !important;
}
[data-testid="stAlert"] { border-radius: 8px !important; }
[data-testid="stDataFrame"] { border: 1px solid #2a2a2a !important; border-radius: 10px !important; }
</style>
""", unsafe_allow_html=True)

# ── DATA ──────────────────────────────────────────────────────────────────────
TEACHERS = {
    "teacher1": {
        "password": "teach123",
        "name": "Mrs. Priya Sharma",
        "subjects": ["Math", "Science"],
        "img": "https://images.unsplash.com/photo-1607990281513-2c110a25bd8c?w=200&q=80"
    },
    "teacher2": {
        "password": "teach456",
        "name": "Mr. Arjun Mehta",
        "subjects": ["English", "History"],
        "img": "https://images.unsplash.com/photo-1531746020798-e6953c6e8e04?w=200&q=80"
    },
}

DEFAULT_STUDENTS = [
    {"Name": "Rahul Patil",    "Class": "10-A", "Roll": "01", "Attendance": "92%", "Score": 82,
     "Contact": "98201 11111", "Joined": "Jun 2024",
     "img": "https://images.unsplash.com/photo-1570295999919-56ceb5ecca61?w=100&q=80"},
    {"Name": "Sneha Kulkarni", "Class": "10-A", "Roll": "02", "Attendance": "88%", "Score": 79,
     "Contact": "98201 22222", "Joined": "Jun 2024",
     "img": "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=100&q=80"},
    {"Name": "Aditya Joshi",   "Class": "10-B", "Roll": "03", "Attendance": "95%", "Score": 91,
     "Contact": "98201 33333", "Joined": "Jun 2024",
     "img": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=100&q=80"},
    {"Name": "Meera Nair",     "Class": "10-B", "Roll": "04", "Attendance": "70%", "Score": 65,
     "Contact": "98201 44444", "Joined": "Jun 2024",
     "img": "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=100&q=80"},
    {"Name": "Ravi Deshmukh",  "Class": "10-A", "Roll": "05", "Attendance": "85%", "Score": 74,
     "Contact": "98201 55555", "Joined": "Jun 2024",
     "img": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=100&q=80"},
]

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

SUBJ_COLOR = {"Math": "#22c55e", "Science": "#3b82f6", "English": "#f59e0b", "History": "#ef4444"}
PLOT = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#888", family="DM Sans"),
    margin=dict(l=10, r=10, t=36, b=10),
    xaxis=dict(gridcolor="#222", linecolor="#333", tickfont=dict(size=11, color="#666")),
    yaxis=dict(gridcolor="#222", linecolor="#333", tickfont=dict(size=11, color="#666")),
)

# ── SESSION STATE INIT ────────────────────────────────────────────────────────
if "teacher" not in st.session_state:
    st.session_state.teacher = None
# Single source of truth for students — shared by Students + Attendance pages
if "students" not in st.session_state:
    st.session_state.students = [s.copy() for s in DEFAULT_STUDENTS]
# Attendance records  { "YYYY-MM-DD": { "StudentName": True/False, ... } }
if "att_records" not in st.session_state:
    st.session_state.att_records = {}
if "uploaded_notes" not in st.session_state:
    st.session_state.uploaded_notes = []

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
t = st.session_state.teacher

st.sidebar.markdown(f"""
<div style="padding:1.8rem 1.2rem 1rem;">
    <div style="font-family:'Bebas Neue',sans-serif;font-size:2rem;color:#22c55e;letter-spacing:2px;line-height:1;">FITMAT</div>
    <div style="font-size:0.65rem;color:#555;letter-spacing:2px;text-transform:uppercase;margin-top:2px;">Class Portal</div>
</div>
<hr style="border:none;border-top:1px solid #222;margin:0 0 0.5rem 0;">
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
    <hr style="border:none;border-top:1px solid #222;margin:0 0 0.3rem 0;">
    """, unsafe_allow_html=True)

pages = ["About Us", "Teacher Login", "Attendance", "Notes", "Students"]
icons = ["🏫", "👩‍🏫", "📋", "📝", "🎒"]
menu = st.sidebar.radio(
    "",
    [f"{icons[i]}  {p}" for i, p in enumerate(pages)],
    label_visibility="collapsed"
)
selected = menu.split("  ", 1)[1]

if t:
    st.sidebar.markdown("<hr style='border:none;border-top:1px solid #222;margin:0.5rem 0;'>", unsafe_allow_html=True)
    if st.sidebar.button("Sign out", use_container_width=True):
        st.session_state.teacher = None
        st.rerun()

# ── HELPERS ───────────────────────────────────────────────────────────────────
def G(html):
    st.markdown(
        f'<div style="color:#e8e8e8;font-family:DM Sans,sans-serif;">{html}</div>',
        unsafe_allow_html=True
    )

def header(title, subtitle="", badge=None):
    badge_html = f'<span style="background:rgba(34,197,94,0.12);border:1px solid #22c55e;border-radius:20px;padding:5px 14px;font-size:0.78rem;font-weight:500;color:#22c55e;">● {badge}</span>' if badge else ""
    G(f"""
    <div style="display:flex;justify-content:space-between;align-items:flex-start;
                padding-bottom:1.2rem;margin-bottom:1.5rem;border-bottom:1px solid #222;">
        <div>
            <div style="font-family:'Bebas Neue',sans-serif;font-size:2.4rem;
                        color:#e8e8e8;letter-spacing:1px;line-height:1;">{title}</div>
            <div style="font-size:0.82rem;color:#555;margin-top:4px;">{subtitle}</div>
        </div>
        {badge_html}
    </div>
    """)

def lock_gate(section):
    G(f"""
    <div style="background:#1a1a1a;border:1px solid #2a2a2a;border-radius:14px;
                padding:3rem 2rem;text-align:center;max-width:400px;">
        <div style="font-size:2.5rem;margin-bottom:1rem;">🔒</div>
        <div style="font-family:'Bebas Neue',sans-serif;font-size:1.6rem;color:#e8e8e8;
                    letter-spacing:1px;margin-bottom:0.5rem;">Teacher Login Required</div>
        <div style="font-size:0.85rem;color:#666;line-height:1.6;">
            Sign in via <b style="color:#22c55e;">Teacher Login</b> to access {section}.
        </div>
    </div>
    """)

def sec(text):
    G(f'<div style="font-size:0.72rem;font-weight:600;letter-spacing:1px;text-transform:uppercase;color:#444;margin:1rem 0 0.5rem;">{text}</div>')

def pad(px=12):
    st.markdown(f"<div style='height:{px}px'></div>", unsafe_allow_html=True)

def att_badge(status):
    if status == "Present":
        return '<span style="background:rgba(34,197,94,0.12);color:#22c55e;border:1px solid rgba(34,197,94,0.3);border-radius:20px;padding:2px 10px;font-size:0.72rem;font-weight:600;">P</span>'
    elif status == "Absent":
        return '<span style="background:rgba(239,68,68,0.12);color:#ef4444;border:1px solid rgba(239,68,68,0.3);border-radius:20px;padding:2px 10px;font-size:0.72rem;font-weight:600;">A</span>'
    else:
        return '<span style="background:rgba(245,158,11,0.12);color:#f59e0b;border:1px solid rgba(245,158,11,0.3);border-radius:20px;padding:2px 10px;font-size:0.72rem;font-weight:600;">L</span>'

# ── MAIN ──────────────────────────────────────────────────────────────────────
pad(32)
left, content, right = st.columns([0.05, 11, 0.05])
with content:

    # ══════════════════════════════════════════════════════════════
    # ABOUT US
    # ══════════════════════════════════════════════════════════════
    if selected == "About Us":
        header("ABOUT US", "Welcome to Fitmat Coaching Classes", "ACTIVE")
        G("""
        <div style="position:relative;border-radius:12px;overflow:hidden;margin-bottom:1.2rem;">
            <img src="https://images.unsplash.com/photo-1524178232363-1fb2b075b655?w=1200&q=80"
                 style="width:100%;height:190px;object-fit:cover;display:block;filter:brightness(0.35);">
            <div style="position:absolute;inset:0;display:flex;flex-direction:column;
                        justify-content:center;padding:0 2rem;">
                <div style="font-family:'Bebas Neue',sans-serif;font-size:2.4rem;
                            color:#22c55e;letter-spacing:2px;line-height:1;">SHAPING BRIGHT FUTURES</div>
                <div style="font-size:0.9rem;color:#ccc;margin-top:6px;">
                    Academic excellence meets physical discipline — since 2010.
                </div>
            </div>
        </div>
        """)

        c1, c2 = st.columns(2)
        with c1:
            G("""
            <div style="background:#1a1a1a;border:1px solid #2a2a2a;border-top:2px solid #22c55e;border-radius:12px;overflow:hidden;margin-bottom:1rem;">
                <img src="https://images.unsplash.com/photo-1509062522246-3755977927d7?w=600&q=80"
                     style="width:100%;height:120px;object-fit:cover;display:block;filter:brightness(0.45);">
                <div style="padding:1.1rem 1.3rem;">
                    <div style="font-family:'Bebas Neue',sans-serif;font-size:1.2rem;color:#22c55e;letter-spacing:1px;margin-bottom:0.5rem;">OUR MISSION</div>
                    <div style="font-size:0.85rem;color:#999;line-height:1.8;">
                        Fitmat is dedicated to building a thriving, energetic learning environment where every
                        student is empowered to grow physically and mentally through structured fitness and education.
                    </div>
                </div>
            </div>
            """)
        with c2:
            G("""
            <div style="background:#1a1a1a;border:1px solid #2a2a2a;border-top:2px solid #22c55e;border-radius:12px;overflow:hidden;margin-bottom:1rem;">
                <img src="https://images.unsplash.com/photo-1488190211105-8b0e65b80b4e?w=600&q=80"
                     style="width:100%;height:120px;object-fit:cover;display:block;filter:brightness(0.45);">
                <div style="padding:1.1rem 1.3rem;">
                    <div style="font-family:'Bebas Neue',sans-serif;font-size:1.2rem;color:#22c55e;letter-spacing:1px;margin-bottom:0.5rem;">OUR VISION</div>
                    <div style="font-size:0.85rem;color:#999;line-height:1.8;">
                        To cultivate disciplined, healthy, and well-rounded individuals ready to contribute positively
                        to society through the power of consistent learning and physical activity.
                    </div>
                </div>
            </div>
            """)

        total_s = len(st.session_state.students)
        G(f"""
        <div style="background:#1a1a1a;border:1px solid #2a2a2a;border-radius:12px;overflow:hidden;margin-bottom:1rem;">
            <img src="https://images.unsplash.com/photo-1580582932707-520aed937b7b?w=1200&q=80"
                 style="width:100%;height:150px;object-fit:cover;display:block;filter:brightness(0.35);">
            <div style="padding:1.5rem 1.8rem;">
                <div style="font-family:'Bebas Neue',sans-serif;font-size:1.4rem;color:#e8e8e8;letter-spacing:1px;margin-bottom:0.8rem;">WHO WE ARE</div>
                <div style="font-size:0.87rem;color:#999;line-height:1.9;margin-bottom:0.7rem;">
                    Fitmat is a specialized class designed around holistic student development. We combine academic rigor
                    with physical fitness programs, creating a unique environment where students excel both in the classroom and on the field.
                </div>
                <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:0.8rem;">
                    <div style="background:#111;border:1px solid #22c55e;border-radius:10px;padding:1rem;text-align:center;">
                        <div style="font-family:'Bebas Neue',sans-serif;font-size:2rem;color:#22c55e;">{total_s}</div>
                        <div style="font-size:0.65rem;color:#555;letter-spacing:1.5px;text-transform:uppercase;margin-top:3px;">Students</div>
                    </div>
                    <div style="background:#111;border:1px solid #22c55e;border-radius:10px;padding:1rem;text-align:center;">
                        <div style="font-family:'Bebas Neue',sans-serif;font-size:2rem;color:#22c55e;">12</div>
                        <div style="font-size:0.65rem;color:#555;letter-spacing:1.5px;text-transform:uppercase;margin-top:3px;">Teachers</div>
                    </div>
                    <div style="background:#111;border:1px solid #22c55e;border-radius:10px;padding:1rem;text-align:center;">
                        <div style="font-family:'Bebas Neue',sans-serif;font-size:2rem;color:#22c55e;">95%</div>
                        <div style="font-size:0.65rem;color:#555;letter-spacing:1.5px;text-transform:uppercase;margin-top:3px;">Attendance Rate</div>
                    </div>
                </div>
            </div>
        </div>
        """)

        sec("Meet Our Teachers")
        tc1, tc2 = st.columns(2)
        for col, td in zip([tc1, tc2], TEACHERS.values()):
            tags = " ".join(f'<span style="background:rgba(34,197,94,0.1);color:#22c55e;border:1px solid rgba(34,197,94,0.3);border-radius:20px;padding:2px 8px;font-size:0.68rem;">{s}</span>' for s in td["subjects"])
            with col:
                G(f"""
                <div style="background:#1a1a1a;border:1px solid #2a2a2a;border-radius:12px;
                            padding:1rem 1.2rem;display:flex;align-items:center;gap:12px;margin-bottom:0.5rem;">
                    <img src="{td['img']}" style="width:50px;height:50px;border-radius:50%;object-fit:cover;border:2px solid #22c55e;flex-shrink:0;">
                    <div>
                        <div style="font-weight:600;font-size:0.9rem;color:#e8e8e8;margin-bottom:4px;">{td['name']}</div>
                        <div>{tags}</div>
                    </div>
                </div>
                """)

    # ══════════════════════════════════════════════════════════════
    # TEACHER LOGIN
    # ══════════════════════════════════════════════════════════════
    elif selected == "Teacher Login":
        t = st.session_state.teacher
        if t:
            header("TEACHER PANEL", f"Logged in as {t['name']}", "ACTIVE")
            tags = " ".join(f'<span style="background:rgba(34,197,94,0.1);color:#22c55e;border:1px solid rgba(34,197,94,0.3);border-radius:20px;padding:2px 10px;font-size:0.72rem;">{s}</span>' for s in t.get("subjects", []))
            G(f"""
            <div style="background:#1a1a1a;border:1px solid #2a2a2a;border-top:2px solid #22c55e;
                        border-radius:12px;overflow:hidden;max-width:500px;margin-bottom:1.5rem;">
                <img src="https://images.unsplash.com/photo-1580582932707-520aed937b7b?w=800&q=80"
                     style="width:100%;height:80px;object-fit:cover;display:block;filter:brightness(0.3);">
                <div style="padding:1rem 1.2rem;display:flex;align-items:center;gap:12px;">
                    <img src="{t['img']}" style="width:50px;height:50px;border-radius:50%;object-fit:cover;border:2px solid #22c55e;flex-shrink:0;margin-top:-24px;">
                    <div>
                        <div style="font-weight:600;font-size:0.95rem;color:#e8e8e8;">{t['name']}</div>
                        <div style="font-size:0.76rem;color:#555;margin-bottom:5px;">Teacher · Fitmat Class Portal</div>
                        <div>{tags}</div>
                    </div>
                </div>
            </div>
            """)
            sec("Upload Study Material")
            with st.form("upload"):
                note_title   = st.text_input("Note Title", placeholder="e.g. Chapter 5: Quadratic Equations")
                note_subject = st.selectbox("Subject", t.get("subjects", ["General"]))
                note_desc    = st.text_area("Description", placeholder="Brief summary…")
                note_file    = st.file_uploader("Attach file (PDF/DOCX/Image)", type=["pdf","docx","png","jpg","jpeg"])
                submitted    = st.form_submit_button("Upload Material")

            if submitted:
                if not note_title:
                    st.error("Please enter a note title.")
                elif not note_file:
                    st.error("Please attach a file.")
                else:
                    import os
                    save_dir = "uploaded_notes"
                    os.makedirs(save_dir, exist_ok=True)
                    file_path = os.path.join(save_dir, note_file.name)
                    with open(file_path, "wb") as fh:
                        fh.write(note_file.getbuffer())
                    st.session_state.uploaded_notes.append({
                        "title": note_title, "subject": note_subject,
                        "desc": note_desc or "No description.",
                        "filename": note_file.name, "path": file_path,
                        "uploader": t["name"],
                        "date": datetime.now().strftime("%d %b %Y"),
                    })
                    st.success(f"✅ '{note_title}' uploaded! It now appears in the Notes section.")

            if st.session_state.uploaded_notes:
                my_uploads = [n for n in st.session_state.uploaded_notes if n["uploader"] == t["name"]]
                if my_uploads:
                    sec("Your Uploaded Notes")
                    for n in my_uploads:
                        ext = n["filename"].rsplit(".", 1)[-1].upper()
                        ext_color = {"PDF":"#ef4444","DOCX":"#3b82f6","PNG":"#22c55e","JPG":"#f59e0b","JPEG":"#f59e0b"}.get(ext,"#888")
                        G(f"""
                        <div style="background:#1a1a1a;border:1px solid #2a2a2a;border-left:3px solid #22c55e;
                                    border-radius:10px;padding:0.9rem 1.1rem;margin-bottom:0.6rem;
                                    display:flex;align-items:center;gap:14px;">
                            <div style="width:42px;height:42px;border-radius:8px;background:{ext_color}20;
                                        border:1px solid {ext_color}40;display:flex;align-items:center;
                                        justify-content:center;font-size:0.65rem;font-weight:700;
                                        color:{ext_color};flex-shrink:0;">{ext}</div>
                            <div style="flex:1;">
                                <div style="font-weight:600;font-size:0.9rem;color:#e8e8e8;">{n['title']}</div>
                                <div style="font-size:0.76rem;color:#555;margin-top:2px;">{n['subject']} · {n['date']} · {n['filename']}</div>
                                <div style="font-size:0.78rem;color:#777;margin-top:2px;">{n['desc']}</div>
                            </div>
                        </div>
                        """)
                        with open(n["path"], "rb") as fh:
                            st.download_button(
                                f"⬇ Download {n['filename']}",
                                data=fh.read(), file_name=n["filename"],
                                key=f"up_dl_{n['filename']}_{n['date']}"
                            )
        else:
            header("TEACHER LOGIN", "Sign in to access your panel")
            G("""
            <div style="border-radius:12px;overflow:hidden;margin-bottom:1.2rem;">
                <img src="https://images.unsplash.com/photo-1524178232363-1fb2b075b655?w=1200&q=80"
                     style="width:100%;height:130px;object-fit:cover;display:block;filter:brightness(0.28);">
            </div>
            """)
            _, col, _ = st.columns([1, 1.1, 1])
            with col:
                sec("Teacher Credentials")
                username = st.text_input("Username", placeholder="teacher1 or teacher2")
                password = st.text_input("Password", type="password", placeholder="Enter password")
                pad(4)
                if st.button("Sign In →", use_container_width=True):
                    u, p = username.strip(), password.strip()
                    if u in TEACHERS and TEACHERS[u]["password"] == p:
                        st.session_state.teacher = TEACHERS[u]
                        st.rerun()
                    else:
                        st.error("❌ Invalid credentials. Try: teacher1 / teach123  or  teacher2 / teach456")
                with st.expander("Demo credentials"):
                    st.markdown("| Username | Password |\n|---|---|\n| `teacher1` | `teach123` |\n| `teacher2` | `teach456` |")

    # ══════════════════════════════════════════════════════════════
    # ATTENDANCE  ← now fully driven by st.session_state.students
    # ══════════════════════════════════════════════════════════════
    elif selected == "Attendance":
        t = st.session_state.teacher
        header("ATTENDANCE", "Mark daily attendance")
        if not t:
            lock_gate("Attendance")
        else:
            students = st.session_state.students

            G("""<div style="border-radius:12px;overflow:hidden;margin-bottom:1rem;">
                <img src="https://images.unsplash.com/photo-1588072432836-e10032774350?w=1200&q=80"
                     style="width:100%;height:110px;object-fit:cover;display:block;filter:brightness(0.28);">
            </div>""")

            c1, c2 = st.columns([1, 2])
            with c1:
                date_sel = st.date_input("Date", value=datetime.today())
            with c2:
                subject_sel = st.selectbox("Subject", t.get("subjects", []))

            date_key = str(date_sel)

            # Initialise attendance state for this date if missing
            if date_key not in st.session_state.att_records:
                st.session_state.att_records[date_key] = {
                    s["Name"]: "Present" for s in students
                }
            # Add any newly added students to existing date records
            for s in students:
                if s["Name"] not in st.session_state.att_records[date_key]:
                    st.session_state.att_records[date_key][s["Name"]] = "Present"

            sec(f"Student List — {date_sel.strftime('%d %b %Y')} · {subject_sel}")

            STATUS_OPTIONS = ["Present", "Absent", "Late"]
            for s in students:
                name = s["Name"]
                c1, c2 = st.columns([5, 2])
                with c1:
                    G(f"""
                    <div style="display:flex;align-items:center;gap:10px;padding:8px 0;border-bottom:1px solid #1a1a1a;">
                        <img src="{s.get('img','https://images.unsplash.com/photo-1570295999919-56ceb5ecca61?w=100&q=80')}"
                             style="width:34px;height:34px;border-radius:50%;object-fit:cover;border:1px solid #333;flex-shrink:0;">
                        <span style="font-weight:500;color:#ddd;font-size:0.88rem;">{name}</span>
                        <span style="font-size:0.74rem;color:#444;">{s.get('Class','—')} · Roll {s.get('Roll','—')}</span>
                    </div>""")
                with c2:
                    current = st.session_state.att_records[date_key].get(name, "Present")
                    choice  = st.selectbox(
                        "Status", STATUS_OPTIONS,
                        index=STATUS_OPTIONS.index(current),
                        key=f"att_{date_key}_{name}",
                        label_visibility="collapsed"
                    )
                    st.session_state.att_records[date_key][name] = choice

            pad(10)
            if st.button("Save Attendance"):
                rec    = st.session_state.att_records[date_key]
                p_cnt  = sum(1 for v in rec.values() if v == "Present")
                a_cnt  = sum(1 for v in rec.values() if v == "Absent")
                l_cnt  = sum(1 for v in rec.values() if v == "Late")
                st.success(f"✅ Saved for {date_sel.strftime('%d %b %Y')} — {p_cnt} Present · {a_cnt} Absent · {l_cnt} Late")

            # ── Summary metrics ──
            pad(8)
            rec = st.session_state.att_records[date_key]
            p_cnt = sum(1 for v in rec.values() if v == "Present")
            a_cnt = sum(1 for v in rec.values() if v == "Absent")
            l_cnt = sum(1 for v in rec.values() if v == "Late")
            m1, m2, m3 = st.columns(3)
            m1.metric("Present", p_cnt)
            m2.metric("Absent",  a_cnt)
            m3.metric("Late",    l_cnt)

            # ── Donut chart ──
            total = len(students)
            if total > 0:
                fig = go.Figure(go.Pie(
                    values=[p_cnt, a_cnt, l_cnt],
                    labels=["Present", "Absent", "Late"],
                    hole=0.65,
                    marker_colors=["#22c55e", "#ef4444", "#f59e0b"]
                ))
                fig.update_traces(textinfo="none")
                fig.update_layout(
                    height=220,
                    annotations=[dict(
                        text=f"<b>{int(p_cnt/total*100)}%</b>",
                        x=0.5, y=0.5, font_size=18, showarrow=False, font_color="#22c55e"
                    )],
                    **PLOT
                )
                st.plotly_chart(fig, use_container_width=True)

            # ── Weekly summary table if multiple dates saved ──
            if len(st.session_state.att_records) > 1:
                sec("Weekly Attendance Overview")
                dates_sorted = sorted(st.session_state.att_records.keys())[-7:]
                rows = []
                for s in students:
                    row = {"Student": s["Name"], "Roll": s.get("Roll", "—"), "Class": s.get("Class", "—")}
                    for d in dates_sorted:
                        short = datetime.strptime(d, "%Y-%m-%d").strftime("%d %b")
                        row[short] = st.session_state.att_records.get(d, {}).get(s["Name"], "—")
                    rows.append(row)
                df = pd.DataFrame(rows)
                st.dataframe(df, use_container_width=True, hide_index=True)

    # ══════════════════════════════════════════════════════════════
    # NOTES
    # ══════════════════════════════════════════════════════════════
    elif selected == "Notes":
        t = st.session_state.teacher
        header("NOTES", "Study material library")
        if not t:
            lock_gate("Notes")
        else:
            G("""<div style="border-radius:12px;overflow:hidden;margin-bottom:1rem;">
                <img src="https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=1200&q=80"
                     style="width:100%;height:100px;object-fit:cover;display:block;filter:brightness(0.28);">
            </div>""")
            search = st.text_input("Search…", placeholder="Algebra, Newton…")
            subj_f = st.selectbox("Filter", ["My Subjects"] + t.get("subjects", []) + ["All"])
            notes  = list(NOTES)
            if search: notes = [n for n in notes if search.lower() in n[0].lower()]
            if subj_f == "My Subjects": notes = [n for n in notes if n[1] in t.get("subjects", [])]
            elif subj_f != "All":       notes = [n for n in notes if n[1] == subj_f]

            for un in st.session_state.uploaded_notes:
                if subj_f == "All" or (subj_f == "My Subjects" and un["subject"] in t.get("subjects",[])) or subj_f == un["subject"]:
                    if not search or search.lower() in un["title"].lower():
                        notes = notes + [(un["title"], un["subject"], un["desc"],
                                          "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=400&q=80", un)]

            if not notes:
                st.info("No notes found.")
            else:
                cols = st.columns(3)
                for i, entry in enumerate(notes):
                    title, subj, desc, img = entry[0], entry[1], entry[2], entry[3]
                    uploaded_meta = entry[4] if len(entry) > 4 else None
                    c     = SUBJ_COLOR.get(subj, "#22c55e")
                    mine  = subj in t.get("subjects", [])
                    with cols[i % 3]:
                        badge = ('<span style="font-size:0.68rem;color:#f59e0b;font-weight:600;">⬆ Uploaded</span>'
                                 if uploaded_meta else
                                 ('<span style="font-size:0.68rem;color:#22c55e;font-weight:600;">✓ Yours</span>' if mine else ''))
                        G(f"""
                        <div style="background:#1a1a1a;border:1px solid #2a2a2a;
                                    border-top:2px solid {c if mine else '#2a2a2a'};
                                    border-radius:12px;overflow:hidden;margin-bottom:0.8rem;
                                    opacity:{'1' if (mine or uploaded_meta) else '0.4'};">
                            <img src="{img}" style="width:100%;height:100px;object-fit:cover;display:block;filter:brightness(0.5);">
                            <div style="padding:0.9rem 1rem;">
                                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:5px;">
                                    <span style="background:{c}20;color:{c};font-size:0.68rem;font-weight:600;
                                                 padding:2px 8px;border-radius:20px;border:1px solid {c}40;">{subj}</span>
                                    {badge}
                                </div>
                                <div style="font-size:0.92rem;font-weight:600;color:#e8e8e8;margin-bottom:3px;">{title}</div>
                                <div style="font-size:0.78rem;color:#666;margin-bottom:6px;">{desc}</div>
                            </div>
                        </div>""")
                        if uploaded_meta:
                            with open(uploaded_meta["path"], "rb") as fh:
                                st.download_button("⬇ Download", data=fh.read(),
                                    file_name=uploaded_meta["filename"], key=f"ndl_{i}")
                        elif mine:
                            st.download_button("⬇ Download", data=f"# {title}\n{desc}",
                                file_name=f"{title.replace(' ','_')}.txt", key=f"dl_{i}")

    # ══════════════════════════════════════════════════════════════
    # STUDENTS  ← add students here; attendance auto-syncs
    # ══════════════════════════════════════════════════════════════
    elif selected == "Students":
        t = st.session_state.teacher
        header("STUDENTS", "Enrolled students overview")
        if not t:
            lock_gate("Students")
        else:
            students = st.session_state.students

            G("""<div style="border-radius:12px;overflow:hidden;margin-bottom:1rem;">
                <img src="https://images.unsplash.com/photo-1427504494785-3a9ca7044f45?w=1200&q=80"
                     style="width:100%;height:110px;object-fit:cover;display:block;filter:brightness(0.28);">
            </div>""")

            avg_att   = round(sum(int(s["Attendance"].replace("%","")) for s in students) / len(students)) if students else 0
            avg_score = round(sum(s["Score"] for s in students) / len(students)) if students else 0
            c1, c2, c3 = st.columns(3)
            c1.metric("Total Students", len(students))
            c2.metric("Avg Attendance", f"{avg_att}%")
            c3.metric("Avg Score",      avg_score)
            pad(12)

            # ── ADD STUDENT FORM ──────────────────────────────────
            with st.expander("➕  Add New Student", expanded=False):
                with st.form("add_student_form", clear_on_submit=True):
                    sec("Student Details")
                    fa, fb = st.columns(2)
                    with fa:
                        new_name    = st.text_input("Full Name *", placeholder="e.g. Riya Mehta")
                        new_roll    = st.text_input("Roll No. *",  placeholder="e.g. 06")
                        new_cls     = st.text_input("Class",       placeholder="e.g. 10-A")
                        new_contact = st.text_input("Parent Contact", placeholder="e.g. 98200 12345")
                    with fb:
                        new_score   = st.number_input("Score (0–100)", min_value=0, max_value=100, value=75)
                        new_att     = st.number_input("Attendance %",  min_value=0, max_value=100, value=90)
                        new_img     = st.text_input("Photo URL (optional)",
                                                    placeholder="https://…",
                                                    value="https://images.unsplash.com/photo-1570295999919-56ceb5ecca61?w=100&q=80")
                    add_btn = st.form_submit_button("Add Student")

                if add_btn:
                    if not new_name.strip() or not new_roll.strip():
                        st.error("Name and Roll No. are required.")
                    else:
                        now = datetime.now()
                        new_student = {
                            "Name":       new_name.strip(),
                            "Roll":       new_roll.strip(),
                            "Class":      new_cls.strip() or "—",
                            "Score":      int(new_score),
                            "Attendance": f"{int(new_att)}%",
                            "Contact":    new_contact.strip() or "—",
                            "Joined":     now.strftime("%b %Y"),
                            "img":        new_img.strip() or "https://images.unsplash.com/photo-1570295999919-56ceb5ecca61?w=100&q=80",
                        }
                        st.session_state.students.append(new_student)
                        # Auto-add this student to ALL existing attendance records as "Present"
                        for date_key in st.session_state.att_records:
                            if new_student["Name"] not in st.session_state.att_records[date_key]:
                                st.session_state.att_records[date_key][new_student["Name"]] = "Present"
                        st.success(f"✅ {new_name} added! They will appear in the Attendance list automatically.")
                        st.rerun()

            # ── SEARCH & FILTER ───────────────────────────────────
            search_s = st.text_input("🔍  Search students", placeholder="Name or Roll No…")
            filter_s = st.selectbox("Filter by Class", ["All"] + sorted({s.get("Class","—") for s in students}))

            filtered = students
            if search_s:
                filtered = [s for s in filtered if search_s.lower() in s["Name"].lower() or search_s in s.get("Roll","")]
            if filter_s != "All":
                filtered = [s for s in filtered if s.get("Class","—") == filter_s]

            sec(f"Student Roster ({len(filtered)} shown)")

            for s in filtered:
                score      = s["Score"]
                bar_color  = "#22c55e" if score >= 80 else "#f59e0b" if score >= 70 else "#ef4444"
                perf_label = "Top" if score >= 80 else "Average" if score >= 70 else "Needs Attention"
                label_color = bar_color

                # Latest attendance status for this student
                latest_status = "—"
                if st.session_state.att_records:
                    latest_date = sorted(st.session_state.att_records.keys())[-1]
                    latest_status = st.session_state.att_records[latest_date].get(s["Name"], "—")

                G(f"""
                <div style="background:#1a1a1a;border:1px solid #2a2a2a;border-radius:12px;
                            padding:0.9rem 1.2rem;margin-bottom:0.6rem;
                            display:flex;align-items:center;gap:14px;">
                    <img src="{s.get('img','')}" style="width:44px;height:44px;border-radius:50%;object-fit:cover;border:2px solid #2a2a2a;flex-shrink:0;">
                    <div style="flex:1;">
                        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;">
                            <span style="font-weight:600;font-size:0.9rem;color:#e8e8e8;">{s['Name']}</span>
                            <span style="font-size:0.72rem;color:#444;">Roll {s.get('Roll','—')} · {s.get('Class','—')}</span>
                        </div>
                        <div style="display:flex;align-items:center;gap:10px;margin-bottom:4px;">
                            <div style="flex:1;background:#222;border-radius:4px;height:4px;">
                                <div style="width:{score}%;background:{bar_color};height:4px;border-radius:4px;"></div>
                            </div>
                            <span style="font-size:0.75rem;font-weight:600;color:{bar_color};flex-shrink:0;">{score}/100</span>
                        </div>
                        <div style="display:flex;gap:14px;flex-wrap:wrap;">
                            <span style="font-size:0.72rem;color:#444;">Attendance: <b style="color:#aaa;">{s['Attendance']}</b></span>
                            <span style="font-size:0.72rem;color:#444;">Today: {att_badge(latest_status) if latest_status != '—' else '<span style="color:#444;font-size:0.72rem;">not marked</span>'}</span>
                            <span style="font-size:0.72rem;color:{label_color};font-weight:600;">{perf_label}</span>
                        </div>
                    </div>
                </div>
                """)

            # ── DELETE STUDENT ────────────────────────────────────
            if students:
                pad(8)
                sec("Remove a Student")
                del_name = st.selectbox("Select student to remove", ["— select —"] + [s["Name"] for s in students])
                if del_name != "— select —":
                    if st.button(f"🗑  Remove {del_name}", type="primary"):
                        st.session_state.students = [s for s in st.session_state.students if s["Name"] != del_name]
                        for dk in st.session_state.att_records:
                            st.session_state.att_records[dk].pop(del_name, None)
                        st.success(f"Removed {del_name} from students and attendance.")
                        st.rerun()

            # ── SCORE CHART ───────────────────────────────────────
            if filtered:
                sec("Score Chart")
                fig = go.Figure(go.Bar(
                    x=[s["Name"].split()[0] for s in filtered],
                    y=[s["Score"] for s in filtered],
                    marker=dict(
                        color=[s["Score"] for s in filtered],
                        colorscale=[[0,"#ef4444"],[0.5,"#f59e0b"],[1,"#22c55e"]],
                        showscale=False
                    )
                ))
                fig.update_layout(height=260, **PLOT)
                st.plotly_chart(fig, use_container_width=True)
