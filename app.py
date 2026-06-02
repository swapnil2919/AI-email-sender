import streamlit as st
import requests, smtplib, ssl, os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def _secret(key: str, default: str = "") -> str:
    """Read from st.secrets (Streamlit Cloud) then .env, then default."""
    try:
        return st.secrets.get(key, os.getenv(key, default))
    except Exception:
        return os.getenv(key, default)

st.set_page_config(
    page_title="MailAI — Smart Email Composer",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={},
)

# ══════════════════════════════════════════════════════════════════════════════
#  GLOBAL CSS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@24,500,1,0');

*,body { font-family:'Plus Jakarta Sans',sans-serif !important; }
.material-symbols-rounded { font-family:'Material Symbols Rounded' !important; }

/* ── Keyframes ─────────────────────────────────────────────────────── */
@keyframes bgDrift {
  0%   { background-position:0% 0%; }
  25%  { background-position:100% 0%; }
  50%  { background-position:100% 100%; }
  75%  { background-position:0% 100%; }
  100% { background-position:0% 0%; }
}
@keyframes orb1 {
  0%,100%{ transform:translate(0,0) scale(1); }
  33%    { transform:translate(70px,-55px) scale(1.1); }
  66%    { transform:translate(-40px,45px) scale(.92); }
}
@keyframes orb2 {
  0%,100%{ transform:translate(0,0) scale(1); }
  40%    { transform:translate(-80px,60px) scale(1.08); }
  70%    { transform:translate(55px,-65px) scale(.94); }
}
@keyframes orb3 {
  0%,100%{ transform:translate(0,0) scale(1); }
  50%    { transform:translate(35px,70px) scale(1.14); }
}
@keyframes fadeUp   { from{opacity:0;transform:translateY(30px)} to{opacity:1;transform:translateY(0)} }
@keyframes fadeDown { from{opacity:0;transform:translateY(-20px)} to{opacity:1;transform:translateY(0)} }
@keyframes fadeIn   { from{opacity:0} to{opacity:1} }
@keyframes slideDown{ from{opacity:0;transform:translateY(-10px)} to{opacity:1;transform:translateY(0)} }
@keyframes popIn    { 0%{opacity:0;transform:scale(.88)} 70%{transform:scale(1.03)} 100%{opacity:1;transform:scale(1)} }
@keyframes shimmer  { 0%{background-position:-400% center} 100%{background-position:400% center} }
@keyframes scanLine { from{transform:translateY(-100%)} to{transform:translateY(400%)} }
@keyframes breatheTeal {
  0%,100%{ box-shadow:0 0 0 0 rgba(20,184,166,0), 0 4px 28px rgba(20,184,166,.28); }
  50%    { box-shadow:0 0 0 8px rgba(20,184,166,.07), 0 4px 44px rgba(20,184,166,.5); }
}
@keyframes borderFlow {
  0%  { border-color:rgba(20,184,166,.35); }
  33% { border-color:rgba(59,130,246,.5);  }
  66% { border-color:rgba(168,85,247,.4);  }
  100%{ border-color:rgba(20,184,166,.35); }
}
@keyframes dot {
  0%,100%{ opacity:1; transform:scale(1); }
  50%    { opacity:.3; transform:scale(.6); }
}
@keyframes float {
  0%,100%{ transform:translateY(0); }
  50%    { transform:translateY(-10px); }
}
@keyframes cardIn {
  from{ opacity:0; transform:translateY(24px) scale(.98); }
  to  { opacity:1; transform:translateY(0)    scale(1);   }
}
@keyframes spin { to{ transform:rotate(360deg); } }
@keyframes checkPop {
  0%  { transform:scale(0) rotate(-45deg); opacity:0; }
  60% { transform:scale(1.2) rotate(5deg); }
  100%{ transform:scale(1) rotate(0); opacity:1; }
}

/* ── Base ─────────────────────────────────────────────────────────── */
.stApp {
  background:#04060f;
  min-height:100vh; overflow-x:hidden;
}
.stApp::before {
  content:''; position:fixed; z-index:0; pointer-events:none;
  border-radius:50%; filter:blur(120px);
  width:700px; height:700px;
  background:radial-gradient(circle,rgba(20,184,166,.13) 0%,transparent 70%);
  top:-160px; right:-130px;
  animation:orb1 18s ease-in-out infinite;
}
.stApp::after {
  content:''; position:fixed; z-index:0; pointer-events:none;
  border-radius:50%; filter:blur(130px);
  width:750px; height:750px;
  background:radial-gradient(circle,rgba(99,102,241,.11) 0%,transparent 70%);
  bottom:-190px; left:-150px;
  animation:orb2 22s ease-in-out infinite;
}

/* ── Hide chrome ──────────────────────────────────────────────────── */
#MainMenu,footer,header[data-testid="stHeader"],
section[data-testid="stSidebar"],
[data-testid="collapsedControl"] { display:none !important; visibility:hidden !important; }
.stDeployButton { display:none !important; }

/* ── Inputs (shared) ──────────────────────────────────────────────── */
.stTextInput input,.stTextArea textarea {
  background:rgba(255,255,255,.05) !important;
  border:1.5px solid rgba(255,255,255,.1) !important;
  border-radius:14px !important; color:#f1f5f9 !important;
  padding:13px 18px !important; font-size:15px !important;
  transition:all .3s cubic-bezier(.4,0,.2,1) !important;
}
.stTextInput input:focus,.stTextArea textarea:focus {
  border-color:#14b8a6 !important;
  box-shadow:0 0 0 3px rgba(20,184,166,.15),0 0 24px rgba(20,184,166,.1) !important;
  background:rgba(20,184,166,.07) !important;
  transform:translateY(-1px) !important;
}
.stTextInput input::placeholder,.stTextArea textarea::placeholder { color:rgba(255,255,255,.22) !important; }
.stTextInput label,.stTextArea label,.stSelectbox label,
.stNumberInput label,.stFileUploader label {
  color:#5eead4 !important; font-size:10px !important;
  font-weight:800 !important; text-transform:uppercase !important; letter-spacing:1.1px !important;
}
[data-baseweb="select"] > div {
  background:rgba(255,255,255,.05) !important;
  border:1.5px solid rgba(255,255,255,.1) !important;
  border-radius:14px !important; color:#f1f5f9 !important;
  transition:all .3s !important;
}
[data-baseweb="select"] > div:focus-within {
  border-color:#14b8a6 !important;
  box-shadow:0 0 0 3px rgba(20,184,166,.15) !important;
}
[data-baseweb="popover"] {
  background:#071118 !important;
  border:1px solid rgba(20,184,166,.22) !important; border-radius:14px !important;
}
[role="option"] { color:#e2fff9 !important; border-radius:8px !important; }
[role="option"]:hover { background:rgba(20,184,166,.2) !important; }
.stNumberInput input {
  background:rgba(255,255,255,.05) !important;
  border:1.5px solid rgba(255,255,255,.1) !important;
  border-radius:14px !important; color:#f1f5f9 !important;
}

/* ── Buttons ──────────────────────────────────────────────────────── */
.stButton>button {
  border-radius:14px !important; font-weight:700 !important;
  font-size:14px !important; letter-spacing:.3px !important;
  transition:all .3s cubic-bezier(.4,0,.2,1) !important;
  border:none !important; padding:12px 24px !important;
  position:relative !important; overflow:hidden !important;
}
.stButton>button[kind="primary"] {
  background:linear-gradient(135deg,#14b8a6 0%,#0ea5e9 50%,#6366f1 100%) !important;
  color:#fff !important; font-size:16px !important;
  animation:breatheTeal 3s ease-in-out infinite !important;
}
.stButton>button[kind="primary"]:hover {
  transform:translateY(-3px) scale(1.01) !important;
  box-shadow:0 14px 40px rgba(14,165,233,.5) !important;
}
.stButton>button[kind="primary"]:active { transform:translateY(0) scale(.99) !important; }
.stButton>button[kind="secondary"] {
  background:rgba(20,184,166,.1) !important; color:#5eead4 !important;
  border:1.5px solid rgba(20,184,166,.3) !important;
  animation:borderFlow 4s linear infinite !important;
}
.stButton>button[kind="secondary"]:hover {
  background:rgba(20,184,166,.22) !important; color:#fff !important;
  transform:translateY(-2px) !important;
  box-shadow:0 6px 24px rgba(20,184,166,.3) !important;
}
.stButton>button:disabled {
  opacity:.28 !important; animation:none !important;
  cursor:not-allowed !important; transform:none !important;
}

/* ── File uploader ────────────────────────────────────────────────── */
[data-testid="stFileUploader"] {
  background:rgba(20,184,166,.03) !important;
  border:2px dashed rgba(20,184,166,.22) !important;
  border-radius:16px !important; padding:14px !important;
  transition:all .3s !important; animation:borderFlow 5s linear infinite !important;
}
[data-testid="stFileUploader"]:hover {
  border-color:#14b8a6 !important; background:rgba(20,184,166,.08) !important;
  transform:translateY(-1px) !important;
}
[data-testid="stFileUploader"] span { color:#5eead4 !important; }

/* ── Misc ─────────────────────────────────────────────────────────── */
hr { border-color:rgba(20,184,166,.1) !important; }
.stAlert { border-radius:14px !important; animation:slideDown .4s ease both !important; }
.stCaption,small { color:rgba(255,255,255,.3) !important; }

/* ══════════════════════════════════════════════════════════════════
   REUSABLE COMPONENTS
══════════════════════════════════════════════════════════════════ */

/* Section label */
.slabel {
  font-size:10px !important; font-weight:800 !important; color:#5eead4 !important;
  text-transform:uppercase !important; letter-spacing:1.4px !important;
  margin-bottom:14px; display:flex; align-items:center; gap:8px;
}
.slabel::after { content:''; flex:1; height:1px;
  background:linear-gradient(90deg,rgba(20,184,166,.3),transparent); }

/* Badges */
.badge {
  display:inline-flex; align-items:center; gap:6px;
  padding:5px 13px; border-radius:20px;
  font-size:11px; font-weight:700; margin:3px 0; transition:all .2s;
}
.badge:hover { transform:scale(1.05); }
.bg { background:rgba(16,185,129,.12); color:#6ee7b7; border:1px solid rgba(16,185,129,.25); }
.br { background:rgba(239,68,68,.12);  color:#fca5a5; border:1px solid rgba(239,68,68,.25); }
.bt { background:rgba(20,184,166,.14); color:#99f6e4; border:1px solid rgba(20,184,166,.28); }
.bb { background:rgba(59,130,246,.12); color:#93c5fd; border:1px solid rgba(59,130,246,.25); }
.dot { width:7px; height:7px; border-radius:50%; display:inline-block;
  animation:dot 2s ease-in-out infinite; }
.bg .dot{ background:#6ee7b7; }
.br .dot{ background:#fca5a5; }
.bt .dot{ background:#99f6e4; }
.bb .dot{ background:#93c5fd; }

/* Model chip */
.mchip {
  background:rgba(20,184,166,.1); border:1px solid rgba(20,184,166,.25);
  border-radius:10px; padding:7px 11px; font-size:11px; color:#99f6e4;
  word-break:break-all; line-height:1.5; margin-top:6px;
  animation:borderFlow 4s linear infinite;
}

/* Hint box */
.hint {
  background:linear-gradient(135deg,rgba(20,184,166,.1),rgba(14,165,233,.07));
  border:1px solid rgba(20,184,166,.24); border-radius:14px;
  padding:12px 16px; font-size:13px; color:#99f6e4;
  margin:8px 0 4px; line-height:1.6;
  animation:slideDown .4s ease both; transition:all .3s;
}
.hint-warn { background:rgba(239,68,68,.08); border-color:rgba(239,68,68,.28); color:#fca5a5; }

/* Char bar */
.cbar-wrap { height:3px; background:rgba(255,255,255,.07); border-radius:3px; margin-top:8px; overflow:hidden; }
.cbar-fill {
  height:100%; border-radius:3px;
  background:linear-gradient(90deg,#14b8a6,#38bdf8,#6366f1);
  background-size:200% 100%; animation:shimmer 3s linear infinite;
  transition:width .5s cubic-bezier(.4,0,.2,1);
}

/* Attachment row */
.arow {
  display:flex; align-items:center; gap:10px;
  background:rgba(20,184,166,.07); border:1px solid rgba(20,184,166,.14);
  border-radius:12px; padding:9px 16px; margin:5px 0;
  font-size:13px; color:#e2fff9;
  animation:popIn .3s ease both; transition:all .2s;
}
.arow:hover { background:rgba(20,184,166,.14); border-color:rgba(20,184,166,.3); transform:translateX(5px); }

/* ══════════════════════════════════════════════════════════════════
   CONFIG PAGE
══════════════════════════════════════════════════════════════════ */

/* Config hero */
.cfg-hero {
  text-align:center; padding:60px 20px 40px;
  animation:fadeDown .7s ease both;
}
.cfg-hero .logo-wrap {
  width:80px; height:80px; margin:0 auto 20px;
  background:linear-gradient(135deg,#14b8a6,#0ea5e9);
  border-radius:24px; display:flex; align-items:center; justify-content:center;
  font-size:38px;
  box-shadow:0 8px 40px rgba(20,184,166,.5);
  animation:float 4s ease-in-out infinite;
  position:relative; overflow:hidden;
}
.cfg-hero .logo-wrap::after {
  content:''; position:absolute; top:-50%; left:-60%; width:35%; height:200%;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,.25),transparent);
  animation:scanLine 3s linear infinite;
}
.cfg-hero h1 {
  font-size:42px; font-weight:900; margin:0 0 10px;
  background:linear-gradient(135deg,#99f6e4,#38bdf8,#a78bfa);
  background-size:250% auto;
  -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
  animation:shimmer 5s linear infinite;
}
.cfg-hero p { color:rgba(255,255,255,.45); font-size:16px; margin:0; }

/* Config card */
.cfg-card {
  background:rgba(255,255,255,.04);
  border:1px solid rgba(20,184,166,.15);
  border-radius:24px; padding:32px;
  backdrop-filter:blur(20px);
  position:relative; overflow:hidden;
  animation:cardIn .6s ease both;
  transition:border-color .3s, box-shadow .3s;
}
.cfg-card:hover { border-color:rgba(20,184,166,.3) !important; box-shadow:0 12px 60px rgba(20,184,166,.12) !important; }
.cfg-card::before {
  content:''; position:absolute; top:0; left:0; right:0; height:2px; border-radius:24px 24px 0 0;
}
.cfg-card-ai::before    { background:linear-gradient(90deg,#14b8a6,#38bdf8); }
.cfg-card-smtp::before  { background:linear-gradient(90deg,#8b5cf6,#ec4899); }
/* shimmer sweep */
.cfg-card::after {
  content:''; position:absolute; top:0; left:-80%; width:45%; height:100%;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,.025),transparent);
  animation:shimmer 8s linear infinite; pointer-events:none;
}

/* Step circle */
.step-circle {
  width:36px; height:36px; border-radius:50%;
  background:linear-gradient(135deg,#14b8a6,#0ea5e9);
  display:inline-flex; align-items:center; justify-content:center;
  font-size:16px; font-weight:900; color:#fff;
  box-shadow:0 4px 16px rgba(20,184,166,.4);
  margin-right:12px; flex-shrink:0;
  animation:breatheTeal 3s ease-in-out infinite;
}
.step-header { display:flex; align-items:center; margin-bottom:20px; }
.step-header h3 { margin:0; font-size:18px; font-weight:800; color:#f0fdfa; }
.step-header p  { margin:2px 0 0; font-size:12px; color:rgba(255,255,255,.4); }

/* Status row */
.status-row {
  display:flex; align-items:center; gap:10px;
  background:rgba(255,255,255,.03); border:1px solid rgba(255,255,255,.07);
  border-radius:14px; padding:14px 18px; margin-bottom:10px;
  animation:fadeUp .5s ease both; transition:all .3s;
}
.status-row:hover { border-color:rgba(20,184,166,.2) !important; background:rgba(20,184,166,.04) !important; }
.status-row .s-icon { font-size:22px; flex-shrink:0; }
.status-row .s-text h4 { margin:0; font-size:14px; font-weight:700; color:#e2e8f0; }
.status-row .s-text p  { margin:0; font-size:12px; color:rgba(255,255,255,.35); }
.status-row .s-badge { margin-left:auto; }

/* ══════════════════════════════════════════════════════════════════
   COMPOSE PAGE
══════════════════════════════════════════════════════════════════ */

/* Topbar */
.topbar {
  display:flex; align-items:center; justify-content:space-between;
  padding:16px 0 24px;
  animation:fadeDown .5s ease both;
}
.topbar-logo { display:flex; align-items:center; gap:12px; }
.topbar-logo-icon {
  width:42px; height:42px;
  background:linear-gradient(135deg,#14b8a6,#0ea5e9);
  border-radius:13px; font-size:20px;
  display:flex; align-items:center; justify-content:center;
  box-shadow:0 4px 18px rgba(20,184,166,.4);
  animation:breatheTeal 3s ease-in-out infinite;
}
.topbar-logo h2 { margin:0; font-size:20px; font-weight:900; color:#f0fdfa; }
.topbar-logo p  { margin:0; font-size:11px; color:rgba(94,234,212,.5); font-weight:700; letter-spacing:1px; text-transform:uppercase; }

/* Compose cards */
.card {
  background:rgba(255,255,255,.035);
  border-radius:22px; padding:24px 28px; margin-bottom:16px;
  backdrop-filter:blur(16px); position:relative; overflow:hidden;
  transition:border-color .3s, box-shadow .35s, transform .3s;
  animation:cardIn .55s ease both;
}
.card:hover { box-shadow:0 10px 50px rgba(20,184,166,.1) !important; transform:translateY(-2px) !important; }
.card::before { content:''; position:absolute; top:0; left:0; right:0; height:2px; border-radius:22px 22px 0 0; }
.card-blue   { border:1px solid rgba(59,130,246,.14);  }
.card-blue::before   { background:linear-gradient(90deg,#3b82f6,#6366f1); }
.card-purple { border:1px solid rgba(168,85,247,.14); }
.card-purple::before { background:linear-gradient(90deg,#8b5cf6,#ec4899); }
.card-teal   { border:1px solid rgba(20,184,166,.14);  }
.card-teal::before   { background:linear-gradient(90deg,#14b8a6,#38bdf8); }
.card-orange { border:1px solid rgba(249,115,22,.14);  }
.card-orange::before { background:linear-gradient(90deg,#f97316,#eab308); }
.card::after {
  content:''; position:absolute; top:0; left:-80%; width:45%; height:100%;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,.025),transparent);
  animation:shimmer 8s linear infinite; pointer-events:none;
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════════════════════════════
def fetch_models(key):
    r = requests.get("https://openrouter.ai/api/v1/models",
                     headers={"Authorization": f"Bearer {key}"}, timeout=15)
    r.raise_for_status()
    return sorted(
        [{"id": m["id"], "label": f"{m.get('name',m['id'])}  ·  {m['id']}", "name": m.get("name",m["id"])}
         for m in r.json().get("data",[]) if m.get("id")],
        key=lambda x: x["name"].lower())

def ai_generate(key, model, subject, tone):
    r = OpenAI(api_key=key, base_url="https://openrouter.ai/api/v1").chat.completions.create(
        model=model,
        messages=[{"role":"user","content":
            f'Write a {tone.lower()} email body for: "{subject}". '
            'Rules: body only, no subject line, proper greeting and sign-off, '
            'concise, use [Your Name] placeholder, no meta-commentary.'}],
        max_tokens=600, temperature=0.7)
    content = r.choices[0].message.content
    if not content:
        raise ValueError("Model returned an empty response. Try a different model.")
    return content.strip()

def send_email(cfg, to, cc, subject, body, files):
    msg = MIMEMultipart()
    msg["From"]=cfg["user"]; msg["To"]=to; msg["Subject"]=subject
    if cc: msg["Cc"]=cc
    msg.attach(MIMEText(body,"plain"))
    for f in files:
        p=MIMEBase("application","octet-stream"); p.set_payload(f.read()); encoders.encode_base64(p)
        p.add_header("Content-Disposition",f'attachment; filename="{f.name}"'); msg.attach(p)
    ctx=ssl.create_default_context()
    with smtplib.SMTP(cfg["host"],int(cfg["port"])) as s:
        s.ehlo(); s.starttls(context=ctx); s.login(cfg["user"],cfg["pass"])
        s.sendmail(cfg["user"],[to]+([cc] if cc else []),msg.as_string())

# ══════════════════════════════════════════════════════════════════════════════
#  SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════
if "page" not in st.session_state:
    st.session_state.page = "config"

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE 1 — CONFIGURATION
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.page == "config":

    _, mid, _ = st.columns([1, 3, 1])
    with mid:

        # Hero
        st.markdown("""
        <div class="cfg-hero">
          <div class="logo-wrap">🚀</div>
          <h1>MailAI</h1>
          <p>Set up once — compose smarter emails forever.</p>
        </div>
        """, unsafe_allow_html=True)

        # ── STEP 1: AI ─────────────────────────────────────────────────────────
        st.markdown('<div class="cfg-card cfg-card-ai">', unsafe_allow_html=True)
        st.markdown("""
        <div class="step-header">
          <div class="step-circle">1</div>
          <div>
            <h3>AI Engine</h3>
            <p>Connect OpenRouter to unlock 200+ AI models</p>
          </div>
        </div>
        """, unsafe_allow_html=True)

        api_key = st.text_input("OpenRouter API Key", type="password",
                                value=_secret("OPENROUTER_API_KEY"),
                                placeholder="sk-or-v1-…",
                                help="Get a free key at openrouter.ai/keys",
                                key="cfg_api_key")

        c1, c2 = st.columns([2, 1])
        with c1:
            fetch_btn = st.button("⚡ Load All Models", use_container_width=True,
                                  disabled=not api_key, key="cfg_fetch")
        with c2:
            if "models" in st.session_state:
                st.markdown(f'<div class="badge bt"><span class="dot"></span>&nbsp;{len(st.session_state.models)} models</div>',
                            unsafe_allow_html=True)

        if fetch_btn and api_key:
            with st.spinner("Fetching models from OpenRouter…"):
                try:
                    st.session_state.models = fetch_models(api_key)
                    st.success(f"✅ {len(st.session_state.models)} models loaded!")
                    st.rerun()
                except Exception as e:
                    st.error(str(e))

        model_id = None
        if "models" in st.session_state and st.session_state.models:
            lbls = [m["label"] for m in st.session_state.models]
            ids  = [m["id"]    for m in st.session_state.models]
            di   = 0
            for p in ["meta-llama/llama-3.3-70b-instruct","openai/gpt-4o-mini","openai/gpt-3.5-turbo"]:
                if p in ids: di = ids.index(p); break
            chosen = st.selectbox("Select AI Model", lbls, index=di, key="cfg_model")
            model_id = ids[lbls.index(chosen)]
            st.markdown(f'<div class="mchip">📌 {model_id}</div>', unsafe_allow_html=True)
        elif not api_key:
            st.markdown('<div class="hint">🔑 Paste your OpenRouter API key above, then click <b>Load All Models</b>.</div>',
                        unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        # ── STEP 2: SMTP ───────────────────────────────────────────────────────
        st.markdown('<div class="cfg-card cfg-card-smtp">', unsafe_allow_html=True)
        st.markdown("""
        <div class="step-header">
          <div class="step-circle" style="background:linear-gradient(135deg,#8b5cf6,#ec4899);box-shadow:0 4px 16px rgba(139,92,246,.4)">2</div>
          <div>
            <h3>Email Account</h3>
            <p>SMTP credentials to send emails</p>
          </div>
        </div>
        """, unsafe_allow_html=True)

        sc1, sc2 = st.columns([3, 1])
        with sc1:
            smtp_host = st.text_input("SMTP Host", value=_secret("SMTP_HOST","smtp.gmail.com"), key="cfg_host")
        with sc2:
            smtp_port = st.number_input("Port", value=int(_secret("SMTP_PORT","587")),
                                        min_value=1, max_value=65535, step=1, key="cfg_port")
        su1, su2 = st.columns(2)
        with su1:
            smtp_user = st.text_input("Your Email", value=_secret("SMTP_USER",""),
                                      placeholder="you@gmail.com", key="cfg_user")
        with su2:
            smtp_pass = st.text_input("App Password", type="password",
                                      value=_secret("SMTP_PASS",""),
                                      placeholder="xxxx xxxx xxxx xxxx", key="cfg_pass")

        st.markdown("""
        <div class="hint" style="margin-top:12px">
        💡 &nbsp;For Gmail, generate an <b>App Password</b> at
        <b>myaccount.google.com → Security → App passwords</b>. Never use your main password.
        </div>""", unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        # ── STATUS SUMMARY ─────────────────────────────────────────────────────
        ai_ok   = bool(api_key and model_id)
        smtp_ok = bool(smtp_user and smtp_pass)

        st.markdown(f"""
        <div class="status-row">
          <span class="s-icon">{"✅" if ai_ok else "❌"}</span>
          <div class="s-text">
            <h4>AI Engine</h4>
            <p>{"Model selected: " + (model_id or "") if ai_ok else "Add API key and load models"}</p>
          </div>
          <div class="s-badge">
            <div class="badge {"bg" if ai_ok else "br"}"><span class="dot"></span>&nbsp;{"Ready" if ai_ok else "Missing"}</div>
          </div>
        </div>
        <div class="status-row">
          <span class="s-icon">{"✅" if smtp_ok else "❌"}</span>
          <div class="s-text">
            <h4>Email Account</h4>
            <p>{"Sending from: " + smtp_user if smtp_ok else "Enter your email and app password"}</p>
          </div>
          <div class="s-badge">
            <div class="badge {"bg" if smtp_ok else "br"}"><span class="dot"></span>&nbsp;{"Ready" if smtp_ok else "Missing"}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── CTA BUTTON ─────────────────────────────────────────────────────────
        all_ok = ai_ok and smtp_ok
        if st.button("🚀  Start Composing →", use_container_width=True,
                     type="primary", disabled=not all_ok):
            st.session_state.update({
                "api_key": api_key, "model_id": model_id,
                "smtp_host": smtp_host, "smtp_port": smtp_port,
                "smtp_user": smtp_user, "smtp_pass": smtp_pass,
                "page": "compose",
            })
            st.rerun()

        if not all_ok:
            missing = []
            if not ai_ok:   missing.append("AI setup")
            if not smtp_ok: missing.append("SMTP credentials")
            st.markdown(f'<div class="hint hint-warn" style="text-align:center">⚠️ &nbsp;Complete: <b>{" & ".join(missing)}</b> to continue.</div>',
                        unsafe_allow_html=True)

        st.markdown("<br><br>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE 2 — COMPOSE
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "compose":

    api_key   = st.session_state.get("api_key","")
    model_id  = st.session_state.get("model_id","")
    smtp_cfg  = {k: st.session_state.get(f"smtp_{k}","")
                 for k in ["host","port","user","pass"]}

    # Topbar
    col_logo, col_spacer, col_btn = st.columns([3, 5, 2])
    with col_logo:
        st.markdown("""
        <div class="topbar-logo">
          <div class="topbar-logo-icon">🚀</div>
          <div>
            <h2>MailAI</h2>
            <p>Smart Composer</p>
          </div>
        </div>""", unsafe_allow_html=True)
    with col_btn:
        if st.button("⚙️  Settings", use_container_width=True):
            st.session_state.page = "config"; st.rerun()

    st.markdown(f'<div class="badge bt" style="margin-bottom:20px"><span class="dot"></span>&nbsp;{model_id.split("/")[-1]}</div>',
                unsafe_allow_html=True)

    # ── Recipients ─────────────────────────────────────────────────────────────
    st.markdown('<div class="card card-blue">', unsafe_allow_html=True)
    st.markdown('<div class="slabel">👤 &nbsp;Recipients</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: to_addr = st.text_input("To *", placeholder="recipient@example.com")
    with c2: cc_addr = st.text_input("CC", placeholder="cc@example.com (optional)")
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Subject + Tone ──────────────────────────────────────────────────────────
    st.markdown('<div class="card card-purple">', unsafe_allow_html=True)
    st.markdown('<div class="slabel">📝 &nbsp;Subject & Tone</div>', unsafe_allow_html=True)
    cs, ct = st.columns([3, 1])
    with cs: subject = st.text_input("Subject *", placeholder="What's this email about?")
    with ct: tone = st.selectbox("Tone", ["Formal","Professional","Friendly","Casual","Persuasive"])

    cb, ch = st.columns([1, 3])
    with cb:
        gen_btn = st.button("✨ Generate Body", use_container_width=True,
                            disabled=not subject)
    with ch:
        if not subject:
            st.markdown('<div class="hint">✏️ &nbsp;Enter a <b>subject</b>, then click <b>Generate Body</b>.</div>',
                        unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="hint">✨ &nbsp;Ready — <b>{tone}</b> tone with <b>{model_id.split("/")[-1]}</b>.</div>',
                        unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Body ────────────────────────────────────────────────────────────────────
    st.markdown('<div class="card card-teal">', unsafe_allow_html=True)
    st.markdown('<div class="slabel">📄 &nbsp;Email Body</div>', unsafe_allow_html=True)

    if gen_btn and subject:
        with st.spinner(f"Generating with {model_id.split('/')[-1]}…"):
            try:
                st.session_state.body = ai_generate(api_key, model_id, subject, tone)
                st.success("✅ Generated! Edit freely before sending.")
            except Exception as e:
                st.error(f"Generation failed: {e}")

    body = st.text_area("Body", value=st.session_state.get("body",""),
                        height=260, label_visibility="collapsed",
                        placeholder="Click ✨ Generate Body to auto-fill, or type here…")
    pct = min(int(len(body)/5000*100), 100)
    st.markdown(
        f'<div style="display:flex;justify-content:flex-end;margin-top:4px">'
        f'<span style="font-size:11px;color:rgba(255,255,255,.25)">{len(body)}/5000</span></div>'
        f'<div class="cbar-wrap"><div class="cbar-fill" style="width:{pct}%"></div></div>',
        unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Attachments ─────────────────────────────────────────────────────────────
    st.markdown('<div class="card card-orange">', unsafe_allow_html=True)
    st.markdown('<div class="slabel">📎 &nbsp;Attachments (optional)</div>', unsafe_allow_html=True)
    files = st.file_uploader("Drop files here or click to browse",
                             accept_multiple_files=True, label_visibility="visible")
    if files:
        for f in files:
            st.markdown(f'<div class="arow">📄&nbsp;<b>{f.name}</b><span style="margin-left:auto;opacity:.4">{f.size/1024:.1f} KB</span></div>',
                        unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Send ────────────────────────────────────────────────────────────────────
    ready = bool(to_addr and subject and body)
    send  = st.button("🚀  Send Email", use_container_width=True, type="primary", disabled=not ready)

    if not ready:
        missing = [n for n,v in [("To",to_addr),("Subject",subject),("Body",body)] if not v]
        if missing:
            st.markdown(f'<div class="hint hint-warn">⚠️ &nbsp;Still needed: <b>{", ".join(missing)}</b></div>',
                        unsafe_allow_html=True)

    if send and ready:
        with st.spinner("Sending…"):
            try:
                send_email(smtp_cfg, to_addr, cc_addr, subject, body, files or [])
                st.success(f"🎉 Email sent to **{to_addr}** successfully!")
                st.balloons()
                st.session_state.body = ""
            except smtplib.SMTPAuthenticationError:
                st.error("❌ Auth failed — check credentials in Settings.")
            except smtplib.SMTPException as e:
                st.error(f"❌ SMTP error: {e}")
            except Exception as e:
                st.error(f"❌ {e}")
