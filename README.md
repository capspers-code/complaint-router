# Automated Complaint Routing

QE830 Project #1 — จำแนกหมวดข้อร้องเรียนทางการเงินจากข้อความที่ผู้บริโภคเขียนเอง

- ข้อมูล: CFPB Consumer Complaint Database (2023–2026), 150,000 แถว
- โมเดล: TF-IDF (1–2 gram) + Logistic Regression (class_weight=balanced)
- Accuracy 0.877 | Macro F1 0.730 | Baseline Macro F1 0.078

โมเดลทำหน้าที่ **แนะนำ** หมวด ไม่ใช่ตัดสินใจแทนมนุษย์
ความมั่นใจต่ำกว่าเกณฑ์ ระบบส่งเรื่องเข้าคิวให้เจ้าหน้าที่ตรวจ

## Run locally
```
pip install -r requirements.txt
streamlit run app.py
```
