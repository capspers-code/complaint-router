import json, re
import joblib
import numpy as np
import streamlit as st

st.set_page_config(page_title='Complaint Router', page_icon='📮', layout='centered')

@st.cache_resource
def load():
    m = joblib.load('model.joblib')
    with open('model_meta.json', encoding='utf-8') as f:
        meta = json.load(f)
    return m, meta

model, meta = load()
TH = meta.get('confidence_threshold', 0.6)

RE_MASK  = re.compile(r'\bX{2,}\b|X{4,}')
RE_URL   = re.compile(r'http\S+|www\.\S+')
RE_NUM   = re.compile(r'\d+')
RE_PUNCT = re.compile(r'[^a-z\s]')
RE_SPACE = re.compile(r'\s+')

def clean_text(s):
    s = RE_MASK.sub(' ', str(s)).lower()
    s = RE_URL.sub(' ', s)
    s = RE_NUM.sub(' ', s)
    s = RE_PUNCT.sub(' ', s)
    return RE_SPACE.sub(' ', s).strip()

st.title('📮 Automated Complaint Routing')
st.caption('QE830 Project #1 — จำแนกหมวดข้อร้องเรียนทางการเงินจากข้อความ')

c1, c2, c3 = st.columns(3)
c1.metric('Macro F1', round(meta['macro_f1'], 3))
c2.metric('Accuracy', round(meta['accuracy'], 3))
c3.metric('จำนวนหมวด', len(meta['classes']))

EXAMPLES = {
    '— เลือกตัวอย่าง —': '',
    'เครดิตบูโร': 'I checked my credit report and found an account I never opened. I disputed it three times and they keep saying it is verified.',
    'ทวงหนี้': 'A debt collector calls me at 2 in the morning every day and threatened to tell my employer about the debt.',
    'สินเชื่อบ้าน': 'My mortgage servicer applied my payment to the wrong month and is now reporting me as delinquent with late fees on escrow.',
    'บัญชีเงินฝาก': 'The bank charged me six overdraft fees in one day even though I had enough money in my savings account.',
}
pick = st.selectbox('ตัวอย่างข้อความ', list(EXAMPLES.keys()))
txt = st.text_area('ข้อความร้องเรียน (ภาษาอังกฤษ)',
                   value=EXAMPLES[pick], height=190,
                   placeholder='พิมพ์หรือวางข้อความร้องเรียนที่นี่ ...')

if st.button('จำแนกหมวด', type='primary', use_container_width=True):
    if len(txt.strip()) < 30:
        st.warning('กรุณาใส่ข้อความอย่างน้อย 30 ตัวอักษร')
    else:
        p = model.predict_proba([clean_text(txt)])[0]
        order = np.argsort(p)[::-1]
        top, conf = model.classes_[order[0]], float(p[order[0]])
        st.divider()
        if conf >= TH:
            st.success('ส่งเข้าทีมอัตโนมัติได้')
        else:
            st.warning('ความมั่นใจต่ำกว่าเกณฑ์ — ควรให้เจ้าหน้าที่ตรวจก่อน')
        st.subheader(top)
        st.progress(conf, text='ความมั่นใจ ' + format(conf, '.1%')
                    + '  (เกณฑ์ ' + format(TH, '.2f') + ')')
        st.markdown('**อันดับรองลงมา**')
        for i in order[1:4]:
            st.write('- ' + str(model.classes_[i]) + '  —  ' + format(float(p[i]), '.1%'))

with st.expander('รายละเอียดโมเดล'):
    st.json(meta)