import json, re
import joblib
import numpy as np
import streamlit as st

st.set_page_config(page_title="Complaint Router", page_icon="📮", layout="centered")


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
st.title("📮 Automated Complaint Routing")
st.caption("QE830 Project #1 — จำแนกหมวดข้อร้องเรียนทางการเงินจากข้อความ")

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
