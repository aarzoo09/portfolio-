import streamlit as st
from io import BytesIO
import base64
import textwrap
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import os
import json

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

creds_dict = json.loads(st.secrets["GOOGLE_SHEETS_KEY"])
creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
client = gspread.authorize(creds)


import json
creds_dict = json.loads(st.secrets["GOOGLE_SHEETS_KEY"])
print(creds_dict["project_id"])


SHEET_ID = "1eE0xqfRk1KWnI5PbMyBQNWVjkgYq11mKuxsyX6nv3tI"  
sheet = client.open_by_key(SHEET_ID).sheet1

# ---------- GOOGLE SHEETS SETUP ----------
SERVICE_ACCOUNT_FILE = "portfolio-messages.json"  

# ---------------- Page config ----------------
st.set_page_config(page_title="Aarzoo's Portfolio", layout="wide", page_icon="✨")

# ---------------- Styling (CSS) ----------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }
    .hero {
        background: linear-gradient(135deg, #0f172a 0%, #0ea5a4 100%);
        color: white;
        padding: 48px;
        border-radius: 16px;
        box-shadow: 0 10px 30px rgba(2,6,23,0.6);
    }
    .glass-card {
        background: rgba(255,255,255,0.03);
        border-radius: 12px;
        padding: 18px;
        box-shadow: 0 6px 20px rgba(2,6,23,0.35);
        backdrop-filter: blur(6px);
    }
    .project-card { border-radius:12px; padding:14px; margin-bottom:12px; }
    .skill-pill { display:inline-block; padding:6px 10px; margin:4px; border-radius:999px; font-weight:600; }
    .download-btn { margin-top:10px }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------- Helper utilities ----------------

def avatar_url(seed: str, style: str = "pixel-art", size: int = 280) -> str:
    """Return a DiceBear avatar URL (SVG). You can change style (e.g. 'avataaars', 'pixel-art')."""
    seed_safe = seed.replace(" ", "_")
    return f"https://api.dicebear.com/6.x/{style}/svg?seed={seed_safe}&scale=120&size={size}"


def download_bytes_button(data: bytes, filename: str, label: str):
    """Create a download button for raw bytes using st.download_button with proper MIME type guesses."""
    return st.download_button(label=label, data=data, file_name=filename)


# ---------------- Header / Hero ----------------
name = "Aarzoo Maurya"
role = "Python Developer | Data Visualisation | Full-Stack Enthusiast"
short_bio = (
    "I build clean, data-driven web apps and visualizations. Currently exploring Streamlit, Plotly, FastAPI, "
    "and modern cloud workflows. I love turning messy data into beautiful, actionable interfaces."
)

col1, col2 = st.columns([1, 3])

with col1:
    st.image("avatar.png", width=180, caption=name, use_container_width='auto', output_format="")

with col2:
    st.markdown(
        f"""
        <div class="hero">
            <h1 style="font-size:2.1rem; margin-bottom:0.2rem;">Hey, I'm {name} ✨</h1>
            <p style="font-size:1.05rem; opacity:0.95; margin-bottom:0.6rem;">{short_bio}</p>
            <div style="display:flex; gap:8px; align-items:center;">
                <a href="#projects" style="padding:10px 16px; background:#06202b; color:white;
                   border-radius:10px; text-decoration:none; font-weight:700;">See projects</a>
                <a href="#contact" style="padding:10px 16px; background:transparent; color:white;
                   border-radius:10px; text-decoration:underline; margin-left:8px;">Contact me</a>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

skills1, skills2, skills3 = st.columns([1,5,1])
with skills2:
    st.subheader("About Me")
    st.markdown(
        "I’m a Python Developer and Data Analyst skilled in Pandas, NumPy, Matplotlib, Power BI, Excel, and MySQL. "
        "I enjoy coding, analyzing data, and creating solutions that make work smarter. Open to opportunities that let me grow in both development and analytics."
    )
    st.markdown("### Skills & tools")
    skills = ["Python", "Streamlit", "Pandas", "Plotly", "MySQL", "HTML/CSS", "Django", "API", "Numpy", "Matplotlib", "Seaborn", "C/C++", "Power BI",]
    skill_html = " ".join(
        [
            f"<span class='skill-pill' style='display:inline-block; margin:4px; padding:8px 15px; "
            f"border-radius:20px; background:linear-gradient(90deg,#eef2ff,#e0f2fe); "
            f"color:#06202b; font-weight:500; font-size:14px;'>{s}</span>"
            for s in skills
        ]
    )
    
    st.markdown(skill_html, unsafe_allow_html=True)

st.write("---")

# ---------------- Projects Section ----------------
st.markdown("<a name=\"projects\"></a>", unsafe_allow_html=True)
st.header("Projects")

projects = [
    {
        "title": "Online Quiz App",
        "desc": "This project is a web-based quiz platform where users can create, manage, and attempt quizzes in real-time. It is designed to be simple, scalable, and easy to deploy, making it perfect for educational institutions, small organizations, or individual learning purposes.",
        "tags": ["Streamlit", "Python", "API", "SQLite"],
        "link": "https://github.com/aarzoo09/Online_Quiz_App"
    },
    {
        "title": "SuperStoreData Dashboard",
        "desc": "A professional interactive dashboard built using Power BI to analyze sales, profit, regional distribution, and time-based performance metrics of Superstore data.",
        "tags": ["Power BI", "Data Visualization", "DAX Measures"],
        "link": "https://github.com/aarzoo09/SuperStoreData_Dashboard"
    },
    {
        "title": "Terminal Visualization",
        "desc": "It is an interactive Streamlit web app designed to visualize terminal data, including monthly trends, yearly performance, commodity analysis, and geospatial mapping of terminals.",
        "tags": ["Python", "Streamlit", "Plotly", "Folium", "Pandas"],
        "link": "https://github.com/aarzoo09/terminal_visualization"
    },
]

cols = st.columns([1,1,1])
for i, p in enumerate(projects):
    with cols[i % 3]:
        st.markdown(f"<div class=\"project-card glass-card\">\n"
                    f"<h4 style=\"margin-bottom:6px\">{p['title']}</h4>\n"
                    f"<p style=\"margin-top:0.2rem; opacity:0.9\">{p['desc']}</p>\n"
                    f"<p style=\"margin-top:8px; margin-bottom:6px\">"
                    + " ".join([f"<span class=\"skill-pill\" style=\"background:#f1f5f9; color:#0f172a\">{t}</span>" for t in p['tags']])
                    + "</p>\n"
                    f"<a href=\"{p['link']}\" target=\"_blank\" style=\"text-decoration:none; font-weight:700\">View on GitHub →</a>\n"
                    f"</div>", unsafe_allow_html=True)

st.write("---")

contact_col1, contact_col2, contact_col3 = st.columns([1,6, 1])
with contact_col2:
    st.markdown("<a name=\"contact\"></a>", unsafe_allow_html=True)
    st.header("Contact Me")
    with st.form("contact_form"):
        name_in = st.text_input("Your name")
        email_in = st.text_input("Your email")
        message_in = st.text_area("Message", value="Hi Aarzoo — I'd like to talk about...")
        submitted = st.form_submit_button("Send message")

        if submitted:
            if not name_in or not email_in or not message_in:
                st.warning("⚠️ Please fill all fields before submitting.")
            else:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                sheet.append_row([timestamp, name_in, email_in, message_in])
                st.success("✅ Message sent! She 'll get back to you at " + email_in)


st.write("---")

# ---------------- Footer / Socials ----------------
st.markdown(
    "<div style='text-align:center; opacity:0.8; padding:18px;'>"
    "Let's Connect: "
    "<a href='https://github.com/aarzoo09' target='_blank'>GitHub</a> · "
    "<a href='www.linkedin.com/in/aarz00' target='_blank'>LinkedIn</a>"
    "</div>", unsafe_allow_html=True
)

