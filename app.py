import json, re
import joblib
import numpy as np
import streamlit as st
import content
import streamlit.components.v1 as components

st.set_page_config(page_title="Complaint Router", page_icon="📮", layout="wide")


@st.cache_resource
def load():
    m = joblib.load("model.joblib")
    with open("model_meta.json", encoding="utf-8") as f:
        meta = json.load(f)
    return m, meta


model, meta = load()
TH = meta.get("confidence_threshold", 0.6)

# ── ทำความสะอาดข้อความ (ต้องตรงกับตอนเทรนใน notebook) ──────────────
RE_MASK  = re.compile(r"\bX{2,}\b|X{4,}")
RE_URL   = re.compile(r"http\S+|www\.\S+")
RE_NUM   = re.compile(r"\d+")
RE_PUNCT = re.compile(r"[^a-z\s]")
RE_SPACE = re.compile(r"\s+")
RE_THAI  = re.compile(r"[฀-๿]")


def clean_text(s):
    s = RE_MASK.sub(" ", str(s)).lower()
    s = RE_URL.sub(" ", s)
    s = RE_NUM.sub(" ", s)
    s = RE_PUNCT.sub(" ", s)
    return RE_SPACE.sub(" ", s).strip()


def is_thai(s):
    '''ถือว่าเป็นภาษาไทยเมื่อมีอักษรไทยเกิน 15% ของตัวอักษรทั้งหมด'''
    s = str(s)
    if not s.strip():
        return False
    return len(RE_THAI.findall(s)) / max(len(s), 1) > 0.15


def _chunks(text, size=460):
    '''ตัดข้อความเป็นท่อนตามช่องว่าง (MyMemory จำกัดความยาวต่อครั้ง)'''
    words, cur, out = text.split(), "", []
    for w in words:
        if len(cur) + len(w) + 1 > size:
            out.append(cur.strip())
            cur = w
        else:
            cur += " " + w
    if cur.strip():
        out.append(cur.strip())
    return out or [text[:size]]


def to_english(text):
    '''แปลไทย -> อังกฤษ ลองหลายตัวแปลตามลำดับ คืนค่า (ข้อความ, error, ชื่อตัวแปล)'''
    import time
    errs = []
    text = text.strip()

    # ── ตัวที่ 1: Google (ลอง 2 ครั้ง) ─────────────────────────────
    try:
        from deep_translator import GoogleTranslator
        for attempt in range(2):
            try:
                out = GoogleTranslator(source="auto", target="en").translate(text[:4500])
                if out and out.strip():
                    return out, None, "Google"
                errs.append("Google: คืนค่าว่าง")
            except Exception as e:
                errs.append(f"Google: {type(e).__name__}")
            time.sleep(1.2)
    except Exception as e:
        errs.append(f"Google import: {type(e).__name__}")

    # ── ตัวที่ 2: MyMemory (ฟรี ไม่ต้องใช้คีย์ ต้องตัดเป็นท่อน) ──────
    try:
        from deep_translator import MyMemoryTranslator
        tr = MyMemoryTranslator(source="th-TH", target="en-US")
        parts = []
        for ch in _chunks(text):
            r = tr.translate(ch)
            if r and r.strip():
                parts.append(r.strip())
        if parts:
            return " ".join(parts), None, "MyMemory"
        errs.append("MyMemory: คืนค่าว่าง")
    except Exception as e:
        errs.append(f"MyMemory: {type(e).__name__}")

    return None, " | ".join(errs), None




# ══════════════════════════════════════════════════════════════════
#  CFPB Application — mockup หน้าจอระบบจริง (เปิดผ่าน ?app=1)
#  หน้านี้ใช้ "โมเดลจริง" จาก model.joblib ไม่ใช่ตัวจำลองใน JS
# ══════════════════════════════════════════════════════════════════
APP_HTML_FILE = "static/cfpb_app.html"

URGENT_PATTERNS = {
    "legal threat":  re.compile(r"threat|lawsuit|legal action|\bsue\b|\bsued\b|attorney|lawyer", re.I),
    "police report": re.compile(r"police|law enforcement|criminal complaint", re.I),
    "repossession":  re.compile(r"repossess|garnish|foreclos|\blien\b|seiz(e|ed|ure)", re.I),
    "eviction":      re.compile(r"evict", re.I),
    "harassment":    re.compile(r"harass|every day|constantly|repeatedly|multiple times a day", re.I),
}


def urgency_flags(text):
    return [k for k, rx in URGENT_PATTERNS.items() if rx.search(text or "")]


DEFAULT_APP_TEXT = (
    "I am writing about inaccurate information on my credit report. A tradeline appears on "
    "my credit file that does not belong to me. It was opened fraudulently after my identity "
    "was stolen, and I filed a police report about the identity theft. I have disputed this "
    "item with the credit bureau three separate times since XX/XX/2026 and sent them my FTC "
    "identity theft affidavit and the police report number XXXXXXXX. Each time the credit "
    "bureau completes its reinvestigation it reports back that the item was verified as "
    "accurate, but it never explains what method of verification was used or which records "
    "were reviewed, which I believe violates the Fair Credit Reporting Act. This inaccurate "
    "credit reporting has lowered my credit score and I was denied a mortgage because of it. "
    "The company has also threatened to take legal action against me. I am asking that this "
    "fraudulent account be deleted from my consumer report and that the credit bureau send "
    "me a corrected credit report in writing."
)


FULLSCREEN_CSS = """
<style>
  header[data-testid="stHeader"], [data-testid="stToolbar"],
  [data-testid="stDecoration"], [data-testid="stStatusWidget"], footer {display:none !important;}
  [data-testid="stAppViewContainer"] {padding:0 !important;}
  [data-testid="stAppViewContainer"] > .main {padding:0 !important;}
  .block-container, [data-testid="stMainBlockContainer"],
  [data-testid="block-container"] {padding:0 !important; max-width:100% !important;}
  [data-testid="stVerticalBlock"], [data-testid="stVerticalBlockBorderWrapper"] {gap:0 !important;}
  [data-testid="stIFrame"] {height:100vh !important;}
  [data-testid="stIFrame"] iframe, iframe[title="st.iframe"],
  .stIFrame iframe {height:100vh !important; width:100% !important; border:0 !important;}
  /* ปุ่มออกจากเต็มจอ — ใช้ widget ของ Streamlit เพราะ HTML ดิบถูก sanitize ทิ้ง */
  [data-testid="stLinkButton"] {position:fixed !important; left:12px; bottom:12px;
    z-index:99999; width:auto !important;}
  [data-testid="stLinkButton"] a {background:rgba(16,24,32,.86) !important;
    color:#fff !important; border:0 !important; font-size:12.5px !important;
    padding:6px 13px !important; box-shadow:0 4px 16px rgba(0,0,0,.3) !important;
    min-height:0 !important;}
  [data-testid="stLinkButton"] a:hover {background:#101820 !important;}
</style>
"""


def render_cfpb_app():
    """หน้า CFPB Application — mockup + โมเดลจริง (full=1 = ซ่อน chrome ของ Streamlit)"""
    fullscreen = bool(st.query_params.get("full"))
    try:
        with open(APP_HTML_FILE, encoding="utf-8") as f:
            html = f.read()
    except FileNotFoundError:
        st.error("ไม่พบไฟล์ " + APP_HTML_FILE)
        st.stop()

    if fullscreen:
        st.markdown(FULLSCREEN_CSS, unsafe_allow_html=True)
        st.link_button("← ออกจากโหมดเต็มจอ", "?app=1")
        _txt = st.session_state.get("app_text", DEFAULT_APP_TEXT)
        _en = _txt
        if is_thai(_txt):
            _out, _err, _eng = to_english(_txt)
            if _out:
                _en = _out
        _cl = clean_text(_en)
        _pay = {"text": _txt, "ranked": [], "urgency": urgency_flags(_en), "threshold": TH}
        if len(_cl.split()) >= 5:
            _p = model.predict_proba([_cl])[0]
            _o = np.argsort(_p)[::-1]
            _pay["ranked"] = [{"c": str(model.classes_[i]), "p": float(_p[i])} for i in _o]
        _inj = ("<script>window.__MODEL=" + json.dumps(_pay, ensure_ascii=False) + ";"
                "window.__TEXT=" + json.dumps(_txt, ensure_ascii=False) + ";</script>")
        components.html(html.replace("</head>", _inj + "</head>", 1), height=1500, scrolling=True)
        st.stop()

    st.markdown(
        "### 📮 CFPB Application — mockup ระบบจริง\n"
        "แบบจำลองหน้าจอ **ผู้ร้องเรียน → CFPB → ธนาคาร → ผู้ร้องเรียน → หน้าผู้บริหาร** "
        "โดยขั้นจำแนกหมวดเรียก **โมเดลจริง** (`model.joblib`) ไม่ใช่ตัวจำลอง"
    )
    st.caption(
        "หน้าจอทั้งหมดเป็นแบบจำลองเพื่อการนำเสนอ ไม่ใช่ระบบจริงของ CFPB · "
        "ไม่มีการเก็บหรือส่งข้อมูลจริง · ชื่อบริษัทและเลขเคสสมมติขึ้น"
    )
    st.markdown(
        '<a href="?app=1&full=1" target="_self" '
        'style="display:inline-block;background:#254b87;color:#fff;font-weight:700;'
        'padding:9px 20px;border-radius:6px;text-decoration:none;font-size:15px;'
        'margin:2px 0 10px">⛶ โหมดเต็มจอ — แสดงเฉพาะ CFPB Application</a>',
        unsafe_allow_html=True,
    )

    with st.expander("✍️ แก้ข้อความร้องเรียนที่จะส่งเข้าระบบ (พิมพ์ไทยได้ ระบบแปลให้)", expanded=False):
        txt = st.text_area("ข้อความร้องเรียน", DEFAULT_APP_TEXT, height=190,
                           label_visibility="collapsed", key="app_text")
        run = st.button("▶ ส่งเข้าโมเดลจริง แล้วโหลดหน้าจอใหม่", type="primary")
    txt = st.session_state.get("app_text", DEFAULT_APP_TEXT)

    text_en, engine = txt, None
    if is_thai(txt):
        with st.spinner("แปลไทย → อังกฤษ ..."):
            out, err, engine = to_english(txt)
        if out:
            text_en = out
            st.caption("แปลด้วย " + str(engine) + " แล้วส่งเข้าโมเดล")
        else:
            st.warning("แปลไม่สำเร็จ ใช้ข้อความเดิมส่งเข้าโมเดลแทน")

    cleaned = clean_text(text_en)
    payload = {"text": txt, "ranked": [], "urgency": urgency_flags(text_en), "threshold": TH}
    if len(cleaned.split()) >= 5:
        p = model.predict_proba([cleaned])[0]
        order = np.argsort(p)[::-1]
        payload["ranked"] = [
            {"c": str(model.classes_[i]), "p": float(p[i])} for i in order
        ]
        top, conf = str(model.classes_[order[0]]), float(p[order[0]])
        c1, c2, c3 = st.columns(3)
        c1.metric("โมเดลทำนาย", top)
        c2.metric("ความมั่นใจ", format(conf, ".3f"))
        c3.metric("ผลการตัดสิน", "ส่งอัตโนมัติ" if conf >= TH else "ให้เจ้าหน้าที่ตรวจ")
    else:
        st.warning("ข้อความสั้นเกินไป — หน้าจอด้านล่างจะใช้ตัวจำลองในเบราว์เซอร์แทน")

    inject = (
        "<script>window.__MODEL=" + json.dumps(payload, ensure_ascii=False) + ";"
        "window.__TEXT=" + json.dumps(txt, ensure_ascii=False) + ";</script>"
    )
    html = html.replace("</head>", inject + "</head>", 1)
    components.html(html, height=1500, scrolling=True)
    st.stop()


if st.query_params.get("app"):
    render_cfpb_app()

# ── สไตล์แท็บให้ดูเป็นแท็บแฟ้มจริง มีมิติ ──────────────────────────
st.html("""
<style>
/* รองรับทั้ง DOM เก่า (baseweb) และใหม่ (react-aria) ของ Streamlit */
.stTabs [data-baseweb="tab-list"],
.stTabs [role="tablist"]{
  gap:5px !important;
  align-items:flex-end !important;
  padding:0 2px !important;
  border-bottom:2px solid #33465C !important;
  margin-bottom:6px !important;
  /* ห่อบรรทัดแทนการตัดขอบ — แท็บที่ 7 จะไม่หลุดขอบขวาอีก */
  flex-wrap:wrap !important;
  overflow-x:visible !important;
  overflow-y:visible !important;
  row-gap:6px !important;
}
/* ซ่อนปุ่มลูกศรเลื่อนแท็บของ Streamlit เพราะไม่ต้องเลื่อนแล้ว */
.stTabs [data-testid="stTabsScrollButton"],
.stTabs [data-baseweb="tab-list"] > button[aria-label*="scroll" i]{ display:none !important; }
.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"]{ display:none !important; }

.stTabs button[data-baseweb="tab"],
.stTabs [data-testid="stTab"]{
  position:relative !important;
  top:4px;
  margin-bottom:-2px !important;
  padding:9px 20px 10px !important;
  border:1px solid #33465C !important;
  border-bottom:none !important;
  border-radius:11px 11px 0 0 !important;
  background:linear-gradient(180deg,#1E2836 0%,#141B24 100%) !important;
  box-shadow:inset 0 1px 0 rgba(255,255,255,.07), 0 -2px 6px rgba(0,0,0,.45) !important;
  transition:top .13s ease, background .13s ease, box-shadow .13s ease;
  white-space:nowrap;
}
.stTabs button[data-baseweb="tab"]::after,
.stTabs [data-testid="stTab"]::after{ display:none !important; }

.stTabs button[data-baseweb="tab"] p,
.stTabs [data-testid="stTab"] p{
  font-size:15px !important; font-weight:600 !important;
  color:#9AA8BA !important; margin:0 !important;
  text-shadow:0 1px 0 rgba(0,0,0,.55);
}

.stTabs button[data-baseweb="tab"]:hover,
.stTabs [data-testid="stTab"]:hover{
  top:1px;
  background:linear-gradient(180deg,#273547 0%,#18212C 100%) !important;
}
.stTabs button[data-baseweb="tab"]:hover p,
.stTabs [data-testid="stTab"]:hover p{ color:#D6E0EC !important; }

.stTabs button[data-baseweb="tab"][aria-selected="true"],
.stTabs [data-testid="stTab"][aria-selected="true"]{
  top:0;
  border-color:#6EA8FF !important;
  background:linear-gradient(180deg,#2B3D55 0%,#0E1117 92%) !important;
  box-shadow:inset 0 2px 0 #6EA8FF,
             inset 0 1px 0 rgba(255,255,255,.10),
             0 -4px 12px rgba(110,168,255,.22) !important;
}
.stTabs button[data-baseweb="tab"][aria-selected="true"] p,
.stTabs [data-testid="stTab"][aria-selected="true"] p{
  color:#FFFFFF !important; font-weight:700 !important;
}

/* ═══════════ มือถือ / จอแคบ ═══════════ */
@media (max-width: 900px){
  .stTabs button[data-baseweb="tab"],
  .stTabs [data-testid="stTab"]{ padding:7px 13px 8px !important; border-radius:9px 9px 0 0 !important; }
  .stTabs button[data-baseweb="tab"] p,
  .stTabs [data-testid="stTab"] p{ font-size:13.5px !important; }
  h1{ font-size:30px !important; line-height:1.18 !important; }
  h2{ font-size:22px !important; }
  h3{ font-size:19px !important; }
  .block-container, [data-testid="stMainBlockContainer"]{
    padding-left:12px !important; padding-right:12px !important; padding-top:12px !important; }
  [data-testid="stMetricValue"]{ font-size:22px !important; }
  [data-testid="stMetricLabel"]{ font-size:12.5px !important; }
}
@media (max-width: 640px){
  .stTabs button[data-baseweb="tab"],
  .stTabs [data-testid="stTab"]{ padding:6px 10px 7px !important; }
  .stTabs button[data-baseweb="tab"] p,
  .stTabs [data-testid="stTab"] p{ font-size:12.5px !important; }
  h1{ font-size:24px !important; }
  /* หัวกระดาษ: โลโก้ + ชื่อ ให้เล็กลงและชิดซ้ายเมื่อคอลัมน์ถูกวางซ้อน */
  [data-testid="stImage"] img{ max-width:100% !important; }
  .qe-head{ text-align:left !important; }
  .qe-head img{ height:40px !important; }
  .qe-head span{ font-size:13.5px !important; }
  [data-testid="stLinkButton"] a, .stButton button{ width:100% !important; }
}
</style>
""")

# ══════════════════════════════════════════════════════════════════
# ── แถบบนสุด: โลโก้ + ชื่อผู้จัดทำ + สังกัด ──────────────────────────
DPU_LOGO = "https://www.dpu.ac.th/frontend-images/logo/dpu-logo-color.svg"
NEON = "#3A8763"

_top_l, _top_r = st.columns([3, 2])
_top_r.markdown(
    "<div class='qe-head' style='text-align:right;line-height:1.7'>"
    "<img src='" + DPU_LOGO + "' alt='DPU' "
    "style='height:56px;margin-bottom:10px;display:inline-block'><br>"
    "<span style='font-size:16px;font-weight:700;color:" + NEON + "'>"
    "วงศ์วริศ ศิรหิรัญชานนท์ &nbsp;69140005</span><br>"
    "<span style='font-size:16px;font-weight:700;color:" + NEON + "'>"
    "ศุภิสรา ชีวนันทพร &nbsp;69140001</span><br>"
    "<span style='font-size:12.5px;font-weight:700;letter-spacing:.22em;"
    "color:rgba(250,250,250,.55);display:inline-block;margin-top:6px'>"
    "CITE</span></div>",
    unsafe_allow_html=True,
)

st.markdown(
    "<div style='font-size:22px;font-weight:800;letter-spacing:.10em;"
    "text-transform:uppercase;color:#6EA8FF;margin-bottom:-2px'>"
    "Consumer Financial Protection Bureau</div>",
    unsafe_allow_html=True,
)
st.title("📮 Automated Complaint Routing")
st.caption("QE830 Project #1 — จำแนกหมวดข้อร้องเรียนทางการเงินจากข้อความ")

TAB_CFPB, TAB_PROC, TAB_DATA, TAB_MODEL, TAB_NB, TAB_DEMO, TAB_APP = st.tabs([
    "CFPB คืออะไร",
    "กระบวนการ",
    "ที่มาของข้อมูล",
    "โมเดลของเรา",
    "Colab Notebook",
    "ลองใช้โมเดล",
    "CFPB Application",
])


# ── แถบปุ่มข้ามแท็บ (ปุ่ม 3D กดแล้วสลับแท็บจริง) ────────────────────
_NAV = """
<style>
 *{box-sizing:border-box}
 body{margin:0;background:transparent;
      font-family:"Sarabun",-apple-system,"Segoe UI",sans-serif}
 .bar{display:flex;justify-content:space-between;align-items:center;
      gap:12px;padding:6px 2px 0}
 .btn{
   position:relative; top:0;
   display:inline-flex; align-items:center; gap:10px;
   padding:12px 24px 13px;
   font-family:inherit; font-size:15.5px; font-weight:700; color:#EAF1FA;
   border-radius:11px; cursor:pointer;
   text-shadow:0 1px 0 rgba(0,0,0,.55);
   transition:top .08s ease, box-shadow .08s ease, background .12s ease;
 }
 .next{
   background:linear-gradient(180deg,#33506F 0%,#1D2A3A 100%);
   border:1px solid #6EA8FF;
   box-shadow:inset 0 1px 0 rgba(255,255,255,.22),
              inset 0 -2px 0 rgba(0,0,0,.35),
              0 5px 0 -1px #16202C,
              0 8px 16px rgba(0,0,0,.55),
              0 0 18px rgba(110,168,255,.16);
 }
 .next:hover{
   background:linear-gradient(180deg,#3D5F84 0%,#22303F 100%);
   box-shadow:inset 0 1px 0 rgba(255,255,255,.28),
              inset 0 -2px 0 rgba(0,0,0,.35),
              0 5px 0 -1px #16202C,
              0 10px 20px rgba(0,0,0,.6),
              0 0 24px rgba(110,168,255,.28);
 }
 .prev{
   color:#C6D2E0;
   background:linear-gradient(180deg,#2A3646 0%,#171F29 100%);
   border:1px solid #46596F;
   box-shadow:inset 0 1px 0 rgba(255,255,255,.15),
              inset 0 -2px 0 rgba(0,0,0,.35),
              0 5px 0 -1px #12181F,
              0 8px 16px rgba(0,0,0,.5);
 }
 .prev:hover{
   color:#EAF1FA;
   background:linear-gradient(180deg,#35455A 0%,#1C2531 100%);
   box-shadow:inset 0 1px 0 rgba(255,255,255,.2),
              inset 0 -2px 0 rgba(0,0,0,.35),
              0 5px 0 -1px #12181F,
              0 10px 20px rgba(0,0,0,.55);
 }
 .btn:active{
   top:4px;
   box-shadow:inset 0 2px 5px rgba(0,0,0,.55),
              0 1px 0 -1px #16202C,
              0 2px 6px rgba(0,0,0,.5) !important;
 }
 .arw{font-size:18px;line-height:1;transform:translateY(-1px)}
 .sp{flex:1}
</style>
<div class="bar">__LEFT____RIGHT__</div>
<script>
function jump(i){
  try{
    var t = window.parent.document.querySelectorAll('[role="tab"]');
    if(t[i]){ t[i].click(); window.parent.scrollTo({top:0, behavior:'smooth'}); }
  }catch(e){}
}
</script>
"""

_PREV_HTML = ('<button class="btn prev" onclick="jump({i})">'
              '<span class="arw">&#10229;</span>{label}</button>')
_NEXT_HTML = ('<button class="btn next" onclick="jump({i})">'
              '{label}<span class="arw">&#10142;</span></button>')


def tab_nav(prev=None, next=None):
    """prev / next = (index, label) หรือ None"""
    left = _PREV_HTML.format(i=prev[0], label=prev[1]) if prev else '<span class="sp"></span>'
    right = _NEXT_HTML.format(i=next[0], label=next[1]) if next else '<span></span>'
    components.html(_NAV.replace("__LEFT__", left).replace("__RIGHT__", right), height=78)



# ── ปรับความสูง iframe ให้เท่าเนื้อหาจริง (สำคัญมากบนมือถือ ที่เนื้อหายืดยาวกว่าเดิม) ──
st.html("""
<style>
/* Streamlit ตั้ง iframe เป็น display:inline ทำให้กล่องแม่ไม่สูงตาม iframe จริง
   พอเนื้อหายืดยาวบนมือถือ ปุ่ม "ถัดไป" เลยไปทับเนื้อหา — บังคับเป็น block แล้วให้กล่องสูงอัตโนมัติ */
[data-testid="stElementContainer"] > iframe{ display:block !important; }
/* กล่องเป็น flex item ที่ถูกตรึงด้วย flex-basis เป็น px ตายตัว (เช่น 0 0 1830px)
   ต้องปลดตรงนี้ก่อน ความสูงถึงจะยืดตามเนื้อหาจริงได้ */
[data-testid="stElementContainer"]:has(> iframe){
  flex:0 0 auto !important; height:auto !important; min-height:0 !important;
}
</style>
""")

components.html("""
<script>
(function(){
  var doc = window.parent && window.parent.document;
  if (!doc || doc.__qe830Resizer) return;
  doc.__qe830Resizer = true;

  var wanted = [];               // [{win, h}] ความสูงที่ประกาศไว้ของแต่ละ iframe

  function apply(){
    var frames = doc.querySelectorAll("iframe");
    for (var i = 0; i < frames.length; i++) {
      for (var j = 0; j < wanted.length; j++) {
        if (frames[i].contentWindow === wanted[j].win) {
          var h = wanted[j].h;
          if (parseInt(frames[i].style.height, 10) !== h) {
            frames[i].style.height = h + "px";
            frames[i].setAttribute("height", h);
          }
          // React ล้าง inline style ทิ้งเป็นระยะ จึงต้องยัดกลับทุกครั้ง
          var box = frames[i].parentElement;
          for (var k = 0; k < 2 && box; k++) {
            if (box.getAttribute && box.getAttribute("data-testid") === "stElementContainer") {
              box.style.setProperty("flex", "0 0 auto", "important");
              box.style.setProperty("height", "auto", "important");
              break;
            }
            box = box.parentElement;
          }
          break;
        }
      }
    }
  }

  window.parent.addEventListener("message", function(e){
    var h = e.data && e.data.qe830Height;
    if (!h || !e.source) return;
    var found = false;
    for (var j = 0; j < wanted.length; j++) {
      if (wanted[j].win === e.source) { wanted[j].h = h; found = true; break; }
    }
    if (!found) wanted.push({win: e.source, h: h});
    apply();
  });

  setInterval(apply, 400);
})();
</script>
""", height=0)

with TAB_CFPB:
    components.html(content.doc(content.CFPB), height=content.HEIGHT['CFPB'], scrolling=True)
    tab_nav(next=(1, "กระบวนการ"))

with TAB_PROC:
    components.html(content.doc(content.PROCESS), height=content.HEIGHT['PROCESS'], scrolling=True)
    tab_nav(prev=(0, "CFPB คืออะไร"), next=(2, "ที่มาของข้อมูล"))

with TAB_DATA:
    components.html(content.doc(content.DATA), height=content.HEIGHT['DATA'], scrolling=True)
    tab_nav(prev=(1, "กระบวนการ"), next=(3, "โมเดลของเรา"))

with TAB_MODEL:
    components.html(content.doc(content.MODEL), height=content.HEIGHT['MODEL'], scrolling=True)
    tab_nav(prev=(2, "ที่มาของข้อมูล"), next=(4, "Colab Notebook"))

def load_notebook_html(fname):
    """อ่านสดทุกครั้ง — ห้าม cache ไม่งั้นได้ไฟล์เก่าหลัง deploy ใหม่"""
    with open("static/" + fname, encoding="utf-8") as f:
        return f.read()


NOTEBOOKS = [
    {
        "key": "screening",
        "file": "screening.html",
        "name": "QE830_Dataset_Screening_Tool.ipynb",
        "desc": ("**Dataset Screening Tool** ตรวจก่อนลงมือว่าชุดข้อมูลมีสัญญาณจริงไหม — "
                 "lookup-table · leakage · chi-square · baseline vs model · "
                 "single-feature dominance → GO/NO-GO"),
    },
    {
        "key": "main",
        "file": "notebook.html",
        "name": "QE830_Project1_CFPB_Complaint_Routing.ipynb",
        "desc": ("**CRISP-DM ฉบับเต็ม** งานหลัก §0–§10 กรอง 17.5 ล้าน → 150,000 · "
                 "EDA 13 กราฟ · เทรน 5 โมเดล · เลือกโมเดล · สร้างไฟล์ deploy · "
                 "**+ §9.3 งานต่อยอด 5 ข้อ ลงมือทำจริงแล้ว** (Issue-model · GridSearchCV · "
                 "fairness audit · urgency flag · โค้ด BERT พร้อมรัน)"),
    },
]


with TAB_NB:
    st.markdown(
        "โน้ตบุ๊กที่รันจริงบน Google Colab — โค้ด ผลลัพธ์ ตาราง และกราฟทุกภาพ "
        "ตามที่รันออกมาจริง ไม่ได้พิมพ์ผลลัพธ์ใส่เอง "
        "(ไฟล์ค่อนข้างใหญ่ จึงต้องกดเปิดเอง เพื่อไม่ให้แท็บอื่นโหลดช้า)"
    )

    for _nb in NOTEBOOKS:
        st.divider()
        _c_sw, _c_txt = st.columns([1, 6])
        with _c_sw:
            _show = st.toggle("แสดง", key="sw_" + _nb["key"], value=False)
        with _c_txt:
            st.markdown("**`" + _nb["name"] + "`**")
            st.caption(_nb["desc"])
        if _show:
            with st.spinner("กำลังโหลดโน้ตบุ๊ก ..."):
                components.html(load_notebook_html(_nb["file"]),
                                height=1500, scrolling=True)

    st.divider()
    tab_nav(prev=(3, "โมเดลของเรา"), next=(5, "ลองใช้โมเดล"))

with TAB_DEMO:
    _pad_l, _mid, _pad_r = st.columns([1, 3, 1])
    with _mid:
        c1, c2, c3 = st.columns(3)
        c1.metric("Macro F1", round(meta["macro_f1"], 3))
        c2.metric("Accuracy", round(meta["accuracy"], 3))
        c3.metric("จำนวนหมวด", len(meta["classes"]))

        st.info(
            "โมเดลเทรนด้วยข้อความภาษาอังกฤษ — ถ้าพิมพ์ภาษาไทย "
            "ระบบจะแปลเป็นอังกฤษให้อัตโนมัติก่อนส่งเข้าโมเดล",
            icon="🌐",
        )

        EXAMPLES = {
            "— เลือกตัวอย่าง —": "",
            "TH · ทวงหนี้ข่มขู่":
                "บริษัททวงหนี้โทรมาหาผมตอนตีสองทุกวันติดต่อกันสามสัปดาห์ "
                "เขาขู่ว่าจะโทรไปบอกที่ทำงานและบอกเพื่อนร่วมงานว่าผมเป็นหนี้ "
                "ผมส่งหนังสือขอให้หยุดติดต่อไปแล้วแต่ก็ยังโทรมาอยู่",
            "TH · ค่าธรรมเนียมเบิกเกินบัญชี":
                "ธนาคารเก็บค่าธรรมเนียมเบิกเกินบัญชีจากผมหกครั้งในวันเดียว ครั้งละสามสิบห้าดอลลาร์ "
                "ทั้งที่ผมมีเงินในบัญชีออมทรัพย์ที่ผูกกันอยู่มากพอ "
                "ธนาคารไม่ได้โอนเงินมาให้และไม่ได้แจ้งเตือนผมก่อนหักค่าธรรมเนียม",
            "TH · สินเชื่อบ้าน":
                "บริษัทที่ดูแลสินเชื่อบ้านลงบัญชีค่างวดของผมผิดเดือน "
                "แล้วรายงานไปยังเครดิตบูโรว่าผมค้างชำระสามสิบวัน "
                "นอกจากนี้ยังขึ้นค่า escrow โดยไม่ส่งเอกสารสรุปประจำปีตามที่กฎหมายกำหนด",
            "TH · กำกวม (ควรให้คนตรวจ)":
                "ผมพยายามให้ใครสักคนช่วยแก้ปัญหาบัญชีนี้มาหลายเดือนแล้ว "
                "ไม่มีใครในบริษัทตอบผมตรงๆ เลย โทรไปทีไรก็โดนโอนสายไปแผนกอื่นทุกครั้ง "
                "เรื่องแบบนี้รับไม่ได้จริงๆ",
            "EN · Credit reporting":
                "I pulled my credit report and there is a collection account listed that does not "
                "belong to me. I have disputed it with the bureau three separate times and each time "
                "they respond that the information was verified as accurate.",
            "EN · Student loan":
                "My student loan servicer placed my account into forbearance without my consent while "
                "I was enrolled in an income driven repayment plan. The unpaid interest capitalized "
                "onto my principal balance.",
        }

        pick = st.selectbox("ตัวอย่างข้อความ", list(EXAMPLES.keys()))
        txt = st.text_area(
            "ข้อความร้องเรียน (พิมพ์ไทยหรืออังกฤษก็ได้)",
            value=EXAMPLES[pick],
            height=190,
            placeholder="พิมพ์หรือวางข้อความร้องเรียนที่นี่ ...",
        )

        if st.button("จำแนกหมวด", type="primary", use_container_width=True):
            if len(txt.strip()) < 30:
                st.warning("กรุณาใส่ข้อความอย่างน้อย 30 ตัวอักษร")
                st.stop()

            text_en, engine = txt, None
            if is_thai(txt):
                with st.spinner("กำลังแปลภาษาไทยเป็นอังกฤษ ..."):
                    text_en, err, engine = to_english(txt)
                if err:
                    st.error(
                        "แปลภาษาไม่สำเร็จจากทุกตัวแปล — กดปุ่มอีกครั้ง หรือวางข้อความภาษาอังกฤษแทน"
                        "\n\nรายละเอียด: " + err
                    )
                    st.stop()
                with st.expander("ข้อความหลังแปลเป็นอังกฤษ (สิ่งที่โมเดลเห็นจริง) · ตัวแปล: " + str(engine)):
                    st.write(text_en)

            cleaned = clean_text(text_en)
            if len(cleaned.split()) < 5:
                st.warning("หลังทำความสะอาดแล้วเหลือคำน้อยเกินไป — ลองใส่ข้อความที่ยาวขึ้น")
                st.stop()

            p = model.predict_proba([cleaned])[0]
            order = np.argsort(p)[::-1]
            top, conf = model.classes_[order[0]], float(p[order[0]])

            st.divider()
            if conf >= TH:
                st.success("ส่งเข้าทีมอัตโนมัติได้", icon="✅")
            else:
                st.warning("ความมั่นใจต่ำกว่าเกณฑ์ — ควรให้เจ้าหน้าที่ตรวจก่อน", icon="👤")

            st.subheader(top)
            st.progress(conf, text="ความมั่นใจ " + format(conf, ".1%")
                        + "  (เกณฑ์ " + format(TH, ".2f") + ")")

            st.markdown("**อันดับรองลงมา**")
            for i in order[1:4]:
                st.write("- " + str(model.classes_[i]) + "  —  " + format(float(p[i]), ".1%"))

        with st.expander("รายละเอียดโมเดล"):
            st.json(meta)

        tab_nav(prev=(4, "Colab Notebook"))


# ══════════════════════════════════════════════════════════════════
with TAB_APP:
    _l, _m, _r = st.columns([1, 3, 1])
    with _m:
        st.subheader("CFPB Application — ระบบจริงจะหน้าตาแบบไหน")
        st.write(
            "แบบจำลองหน้าจอทั้งเส้นทาง ตั้งแต่ผู้บริโภคกรอกเรื่อง จนธนาคารตอบกลับ "
            "และหน้าผู้บริหารที่เฝ้าดูโมเดล — ขั้นจำแนกหมวดเรียก **โมเดลจริง** ตัวเดียวกับแท็บ *ลองใช้โมเดล*"
        )
        st.markdown(
            '<a href="?app=1" target="_blank" rel="noopener" '
            'style="display:inline-block;background:#20aa3f;color:#fff;font-weight:700;'
            'padding:13px 30px;border-radius:6px;text-decoration:none;font-size:17px;'
            'margin:10px 8px 6px 0">🚀 เปิด CFPB Application (แท็บใหม่)</a>'
            '<a href="?app=1&full=1" target="_blank" rel="noopener" '
            'style="display:inline-block;background:#254b87;color:#fff;font-weight:700;'
            'padding:13px 26px;border-radius:6px;text-decoration:none;font-size:17px;'
            'margin:10px 0 6px">⛶ เปิดแบบเต็มจอ</a>',
            unsafe_allow_html=True,
        )
        st.caption(
            "**เต็มจอ** = ซ่อนทุกอย่างของ Streamlit เหลือแต่หน้าจอ CFPB Application อย่างเดียว "
            "เหมาะกับตอนนำเสนอ · ในหน้าจอยังมีปุ่ม ⛶ Full screen ให้ขยายเต็มหน้าจอเครื่องอีกชั้น (หรือกด F11)"
        )

        st.divider()
        st.markdown("**5 หน้าจอในเดโม**")
        _c = st.columns(5)
        for _col, _t, _d in zip(
            _c,
            ["1 · ผู้ร้องเรียน", "2 · เจ้าหน้าที่ CFPB", "3 · ธนาคาร", "4 · สถานะเรื่อง", "5 · ผู้บริหาร"],
            ["กรอกเรื่องเป็นข้อความอิสระ ไม่ต้องเลือกหมวด",
             "โมเดลเสนอหมวด + ความมั่นใจ + ธงเร่งด่วน เจ้าหน้าที่กดยืนยัน",
             "รับเรื่องเข้าคิวที่ถูกต้อง พร้อมนาฬิกา 15 วัน",
             "ผู้ร้องเรียนเห็นคำตอบและเส้นทางเดินเรื่อง",
             "ปริมาณงาน · การกระจายความมั่นใจ · SLA · ธงเร่งด่วน"],
        ):
            _col.markdown("**" + _t + "**")
            _col.caption(_d)

        st.divider()
        st.info(
            "หน้าจอทั้งหมดเป็นแบบจำลองเพื่อการนำเสนอ **ไม่ใช่ระบบจริงของ CFPB** — "
            "ไม่มีการเก็บหรือส่งข้อมูลจริง ชื่อบริษัทและเลขเคสสมมติขึ้น "
            "ส่วนตัวเลขความแม่นยำและการกระจายข้อมูลเป็นค่าจริงจากโครงงาน",
            icon="ℹ️",
        )
        tab_nav(prev=(5, "ลองใช้โมเดล"), next=None)
