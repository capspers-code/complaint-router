# -*- coding: utf-8 -*-
"""เนื้อหาอินโฟกราฟิก CFPB สำหรับฝังในแอป Streamlit

สร้างอัตโนมัติจาก CFPB_Complaint_Journey.html
CSS ถูกจำกัดขอบเขตด้วย .cfpb-doc เพื่อไม่ให้ไปกวน UI ของ Streamlit
"""

FONT_LINK = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;600;800&family=Libre+Franklin:wght@500;700&family=IBM+Plex+Mono:wght@400;600&display=swap">'

CSS = '''<style>
.cfpb-doc{background:var(--paper);color:var(--ink);font-family:var(--sans);font-size:16px;line-height:1.72;-webkit-font-smoothing:antialiased;padding:8px 0 40px}
.cfpb-doc .wrap{padding:0}
.cfpb-doc section:first-child{margin-top:8px}

:root{
  --paper:#EFF2F6;
  --card:#FFFFFF;
  --sunk:#E4E9F0;
  --ink:#151E2B;
  --ink-2:#4A5769;
  --ink-3:#7B8798;
  --rule:#C9D2DE;
  --rule-soft:#DDE4EC;
  --navy:#1B3A6B;
  --navy-soft:#DCE5F3;
  --stamp:#B03626;
  --stamp-soft:#F6E2DE;
  --amber:#96650A;
  --amber-soft:#F7ECD6;
  --green:#1C6349;
  --green-soft:#DDEDE5;
  --sans:"Sarabun",-apple-system,"Segoe UI",sans-serif;
  --disp:"Libre Franklin","Sarabun",sans-serif;
  --mono:"IBM Plex Mono",ui-monospace,monospace;
  --shadow:0 1px 2px rgba(21,30,43,.07),0 8px 24px -14px rgba(21,30,43,.28);
}
@media (prefers-color-scheme:dark){
:root:not([data-theme="light"]){
    --paper:#0E141C; --card:#161E28; --sunk:#1D2833;
    --ink:#E6EBF2; --ink-2:#AAB6C6; --ink-3:#78859A;
    --rule:#2C3947; --rule-soft:#232F3C;
    --navy:#8FB0E0; --navy-soft:#1B2A40;
    --stamp:#E37E6C; --stamp-soft:#38211C;
    --amber:#D6A54C; --amber-soft:#33280F;
    --green:#68C69C; --green-soft:#152B22;
    --shadow:0 1px 2px rgba(0,0,0,.4),0 10px 28px -16px rgba(0,0,0,.8);
  }
}
:root[data-theme="dark"]{
  --paper:#0E141C; --card:#161E28; --sunk:#1D2833;
  --ink:#E6EBF2; --ink-2:#AAB6C6; --ink-3:#78859A;
  --rule:#2C3947; --rule-soft:#232F3C;
  --navy:#8FB0E0; --navy-soft:#1B2A40;
  --stamp:#E37E6C; --stamp-soft:#38211C;
  --amber:#D6A54C; --amber-soft:#33280F;
  --green:#68C69C; --green-soft:#152B22;
  --shadow:0 1px 2px rgba(0,0,0,.4),0 10px 28px -16px rgba(0,0,0,.8);
}
.cfpb-doc *{box-sizing:border-box}
.cfpb-doc body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--sans);font-weight:400;font-size:16px;line-height:1.72;-webkit-font-smoothing:antialiased}
.cfpb-doc .wrap{max-width:1040px;margin:0 auto;padding:0 24px 96px}
.cfpb-doc h1, .cfpb-doc h2, .cfpb-doc h3{text-wrap:balance;margin:0}
.cfpb-doc p{margin:0}
.cfpb-doc /* ---------- masthead ---------- */
.mast{padding:56px 0 32px;border-bottom:2px solid var(--ink)}
.cfpb-doc .eyebrow{font-family:var(--disp);font-weight:700;font-size:11.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--stamp)}
.cfpb-doc h1{font-size:clamp(34px,5.4vw,54px);line-height:1.14;font-weight:800;letter-spacing:-.015em;margin:14px 0 0}
.cfpb-doc .sub-th{margin-top:10px;font-size:22px;font-weight:600;color:var(--navy);max-width:44ch;line-height:1.45}
.cfpb-doc .dek{margin-top:14px;max-width:60ch;color:var(--ink-2);font-size:16.5px;font-weight:300}
.cfpb-doc .filing{display:flex;flex-wrap:wrap;gap:0;margin-top:30px;border:1px solid var(--rule);border-radius:3px;background:var(--card);overflow:hidden}
.cfpb-doc .filing div{flex:1 1 160px;padding:12px 16px;border-right:1px solid var(--rule-soft)}
.cfpb-doc .filing div:last-child{border-right:0}
.cfpb-doc .filing dt{font-family:var(--disp);font-size:10px;font-weight:700;letter-spacing:.13em;text-transform:uppercase;color:var(--ink-3);margin:0}
.cfpb-doc .filing dd{margin:3px 0 0;font-family:var(--mono);font-size:13.5px;font-weight:600;color:var(--navy)}
.cfpb-doc /* ---------- sections ---------- */
section{margin-top:64px}
.cfpb-doc .shead{display:flex;align-items:baseline;gap:14px;border-bottom:1px solid var(--rule);padding-bottom:10px;margin-bottom:28px}
.cfpb-doc .snum{font-family:var(--mono);font-size:12px;font-weight:600;color:var(--stamp);letter-spacing:.05em}
.cfpb-doc h2{font-size:24px;font-weight:800;letter-spacing:-.01em}
.cfpb-doc .shead{flex-wrap:wrap}
.cfpb-doc .h2en{font-family:var(--disp);font-size:11px;font-weight:700;letter-spacing:.13em;text-transform:uppercase;color:var(--ink-3);margin-left:auto;white-space:nowrap}
.cfpb-doc .lede{max-width:66ch;color:var(--ink-2);margin-bottom:26px;font-weight:300;font-size:16.5px}
.cfpb-doc /* ---------- actors ---------- */
.cast{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px}
.cfpb-doc .actor{background:var(--card);border:1px solid var(--rule);border-radius:3px;padding:15px 16px;box-shadow:var(--shadow)}
.cfpb-doc .actor .tag{font-family:var(--disp);font-size:10px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--ink-3)}
.cfpb-doc .actor b{display:block;font-size:16.5px;font-weight:800;margin:5px 0 5px}
.cfpb-doc .actor span{font-size:14px;color:var(--ink-2);font-weight:300;line-height:1.55;display:block}
.cfpb-doc .actor.a1{border-top:3px solid var(--stamp)}
.cfpb-doc .actor.a2{border-top:3px solid var(--navy)}
.cfpb-doc .actor.a3{border-top:3px solid var(--amber)}
.cfpb-doc .actor.a4{border-top:3px solid var(--green)}
.cfpb-doc /* ---------- figure ---------- */
figure{margin:0;background:var(--card);border:1px solid var(--rule);border-radius:3px;padding:22px 20px 16px;box-shadow:var(--shadow)}
.cfpb-doc .scroll{overflow-x:auto}
.cfpb-doc figure svg{display:block;width:100%;min-width:820px;height:auto;color:var(--ink-2);font-family:var(--sans)}
.cfpb-doc figcaption{margin-top:16px;padding-top:12px;border-top:1px solid var(--rule-soft);font-size:13.5px;color:var(--ink-3);font-weight:300;line-height:1.6}
.cfpb-doc .svg-t{font-size:13px;font-weight:600;fill:var(--ink)}
.cfpb-doc .svg-s{font-size:11px;font-weight:400;fill:var(--ink-2)}
.cfpb-doc .svg-lane{font-family:var(--disp);font-size:10.5px;font-weight:700;letter-spacing:.09em;fill:var(--ink-3)}
.cfpb-doc .svg-edge{font-family:var(--mono);font-size:10.5px;fill:var(--ink-2)}
.cfpb-doc .svg-n{font-family:var(--mono);font-size:11px;font-weight:600;fill:var(--stamp)}
.cfpb-doc /* ---------- stages ---------- */
.stages{display:flex;flex-direction:column;gap:0;border-top:1px solid var(--rule)}
.cfpb-doc .stage{display:grid;grid-template-columns:52px 1fr 250px;gap:22px;padding:22px 0;border-bottom:1px solid var(--rule-soft);align-items:start}
.cfpb-doc .stage .idx{font-family:var(--mono);font-size:22px;font-weight:600;color:var(--rule);line-height:1.1;padding-top:2px}
.cfpb-doc .stage h3{font-size:17.5px;font-weight:800;margin-bottom:4px}
.cfpb-doc .who{display:inline-block;font-family:var(--disp);font-size:10px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;padding:2px 8px;border-radius:2px;margin-bottom:8px}
.cfpb-doc .w-con{background:var(--stamp-soft);color:var(--stamp)}
.cfpb-doc .w-cfpb{background:var(--navy-soft);color:var(--navy)}
.cfpb-doc .w-co{background:var(--amber-soft);color:var(--amber)}
.cfpb-doc .w-pub{background:var(--green-soft);color:var(--green)}
.cfpb-doc .stage p{font-size:15px;color:var(--ink-2);font-weight:300;max-width:56ch}
.cfpb-doc .out{background:var(--sunk);border-radius:3px;padding:12px 14px}
.cfpb-doc .out .lbl{font-family:var(--disp);font-size:9.5px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--ink-3);display:block;margin-bottom:7px}
.cfpb-doc .col{display:inline-block;font-family:var(--mono);font-size:11.5px;background:var(--card);border:1px solid var(--rule);border-radius:2px;padding:2px 6px;margin:0 4px 4px 0;color:var(--ink)}
.cfpb-doc .col.key{border-color:var(--stamp);color:var(--stamp);font-weight:600}
.cfpb-doc .none{font-size:12.5px;color:var(--ink-3);font-weight:300;font-style:italic}
.cfpb-doc /* ---------- primer blocks ---------- */
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:1px;background:var(--rule);border:1px solid var(--rule);border-radius:3px;overflow:hidden;margin-top:4px}
.cfpb-doc .stats div{background:var(--card);padding:18px 20px}
.cfpb-doc .stats .n{font-family:var(--mono);font-size:28px;font-weight:600;color:var(--navy);line-height:1.15;font-variant-numeric:tabular-nums;display:block}
.cfpb-doc .stats .k{font-size:13.5px;color:var(--ink-2);font-weight:300;display:block;margin-top:6px;line-height:1.5}
.cfpb-doc .origin{display:grid;grid-template-columns:repeat(auto-fit,minmax(215px,1fr));gap:0;margin:4px 0 6px}
.cfpb-doc .origin div{padding:2px 22px 14px;border-left:1px solid var(--rule)}
.cfpb-doc .origin div:first-child{border-left:2px solid var(--stamp)}
.cfpb-doc .origin .yr{font-family:var(--mono);font-size:12px;font-weight:600;color:var(--stamp);letter-spacing:.06em;display:block}
.cfpb-doc .origin b{display:block;font-size:16px;font-weight:800;margin:5px 0 5px}
.cfpb-doc .origin p{font-size:14.5px;color:var(--ink-2);font-weight:300;line-height:1.6}
.cfpb-doc .powers{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px;margin-top:4px}
.cfpb-doc .power{background:var(--card);border:1px solid var(--rule);border-radius:3px;padding:16px 18px;box-shadow:var(--shadow);display:flex;gap:14px;align-items:flex-start}
.cfpb-doc .power .no{font-family:var(--mono);font-size:13px;font-weight:600;color:var(--stamp);padding-top:3px;flex:none}
.cfpb-doc .power b{display:block;font-size:16px;font-weight:800;margin-bottom:4px}
.cfpb-doc .power span{font-size:14.5px;color:var(--ink-2);font-weight:300;line-height:1.6;display:block}
.cfpb-doc .chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:4px}
.cfpb-doc .chip{font-size:14px;background:var(--card);border:1px solid var(--rule);border-radius:999px;padding:5px 14px;color:var(--ink-2);font-weight:300}
.cfpb-doc .chip b{font-weight:700;color:var(--ink)}
.cfpb-doc .compare{width:100%;border-collapse:collapse;margin-top:4px;font-size:14.5px;background:var(--card);border:1px solid var(--rule);border-radius:3px;overflow:hidden}
.cfpb-doc .compare th{text-align:left;font-family:var(--disp);font-size:10px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--ink-3);padding:11px 16px;border-bottom:1px solid var(--rule);background:var(--sunk)}
.cfpb-doc .compare td{padding:12px 16px;border-bottom:1px solid var(--rule-soft);color:var(--ink-2);font-weight:300;vertical-align:top}
.cfpb-doc .compare tr:last-child td{border-bottom:0}
.cfpb-doc .compare td:first-child{font-weight:600;color:var(--ink);white-space:nowrap}
.cfpb-doc .sub{font-family:var(--disp);font-size:10px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--ink-3);margin:34px 0 12px}
.cfpb-doc /* ---------- callout ---------- */
.note{border-left:3px solid var(--amber);background:var(--amber-soft);border-radius:0 3px 3px 0;padding:18px 22px;margin-top:28px}
.cfpb-doc .note.alert{border-left-color:var(--stamp);background:var(--stamp-soft)}
.cfpb-doc .note b{display:block;font-size:15.5px;font-weight:800;margin-bottom:6px;color:var(--ink)}
.cfpb-doc .note p{font-size:15px;color:var(--ink-2);font-weight:300;max-width:70ch}
.cfpb-doc .note p + p{margin-top:10px}
.cfpb-doc /* ---------- deliverable box ---------- */
.pitch{background:var(--card);border:1px solid var(--rule);border-radius:3px;box-shadow:var(--shadow);overflow:hidden;margin-top:26px}
.cfpb-doc .pitch-h{padding:18px 24px;border-bottom:1px solid var(--rule);background:var(--sunk)}
.cfpb-doc .pitch-h .tag{font-family:var(--disp);font-size:10px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--stamp)}
.cfpb-doc .pitch-h b{display:block;font-size:19px;font-weight:800;margin-top:5px}
.cfpb-doc .pitch-g{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr))}
.cfpb-doc .pitch-g div{padding:18px 24px;border-right:1px solid var(--rule-soft);border-bottom:1px solid var(--rule-soft)}
.cfpb-doc .pitch-g div:last-child{border-right:0}
.cfpb-doc .pitch-g dt{font-family:var(--disp);font-size:10px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--ink-3);margin:0}
.cfpb-doc .pitch-g dd{margin:6px 0 0;font-size:15px;font-weight:300;color:var(--ink-2)}
.cfpb-doc .pitch-g dd strong{font-weight:800;color:var(--ink);font-size:16px}
.cfpb-doc .metric{font-family:var(--mono);font-size:26px;font-weight:600;color:var(--green);line-height:1.2;display:block;font-variant-numeric:tabular-nums}
.cfpb-doc .metric small{font-family:var(--sans);font-size:13px;color:var(--ink-3);font-weight:300;display:block;margin-top:2px}
.cfpb-doc footer{margin-top:64px;padding-top:20px;border-top:1px solid var(--rule);font-size:13px;color:var(--ink-3);font-weight:300}
.cfpb-doc footer a{color:var(--navy);text-decoration:none;border-bottom:1px solid var(--rule)}
.cfpb-doc footer a:hover{border-bottom-color:var(--navy)}
.cfpb-doc footer a:focus-visible{outline:2px solid var(--navy);outline-offset:3px}

@media(max-width:760px){
.cfpb-doc .stage{grid-template-columns:36px 1fr;gap:14px}
.cfpb-doc .stage .out{grid-column:2}
.cfpb-doc .stage .idx{font-size:17px}
}

</style>'''

CFPB = '''<div class="cfpb-doc">
<!-- ============ 0 PRIMER ============ -->
<section>
  <div class="shead"><span class="snum">01</span><h2>CFPB คืออะไร</h2><span class="h2en">What is the CFPB</span></div>
  <p class="lede"><b>Consumer Financial Protection Bureau</b> — สำนักงานคุ้มครองผู้บริโภคทางการเงิน เป็นหน่วยงานอิสระของรัฐบาลกลางสหรัฐฯ ตั้งขึ้นเพื่อทำหน้าที่เดียว คือคุ้มครองประชาชนจากการถูกเอาเปรียบโดยสถาบันการเงิน</p>

  <div class="origin">
    <div>
      <span class="yr">2008</span>
      <b>วิกฤตแฮมเบอร์เกอร์</b>
      <p>ธนาคารขายสินเชื่อบ้านให้คนที่ผ่อนไม่ไหว โดยซ่อนเงื่อนไขดอกเบี้ยลอยตัวไว้ในสัญญา เมื่อดอกเบี้ยขึ้น คนอเมริกันหลายล้านครัวเรือนถูกยึดบ้าน</p>
    </div>
    <div>
      <span class="yr">2010</span>
      <b>กฎหมาย Dodd-Frank</b>
      <p>สภาคองเกรสออกกฎหมายปฏิรูปการเงินครั้งใหญ่ ระบุให้ตั้งหน่วยงานใหม่ขึ้นมาเฉพาะเพื่อดูแลฝั่งผู้บริโภค แยกออกจากหน่วยงานที่ดูแลความมั่นคงของธนาคาร</p>
    </div>
    <div>
      <span class="yr">2011</span>
      <b>CFPB เปิดทำการ</b>
      <p>เริ่มรับเรื่องร้องเรียนจากประชาชนโดยตรง และเปิดเผยข้อมูลสู่สาธารณะตั้งแต่ปี 2013 เป็นต้นมา</p>
    </div>
  </div>

  <div class="sub">ผลงานสะสมตั้งแต่ก่อตั้ง</div>
  <div class="stats">
    <div><span class="n">$21B+</span><span class="k">เงินที่บังคับให้บริษัทคืนหรือชดเชยให้ผู้บริโภค</span></div>
    <div><span class="n">205M+</span><span class="k">จำนวนคน/บัญชี ที่ได้รับการเยียวยา</span></div>
    <div><span class="n">6.8M+</span><span class="k">เรื่องร้องเรียนที่รับมาทั้งหมด</span></div>
    <div><span class="n">$6.1B</span><span class="k">ค่าธรรมเนียมเบิกเกินบัญชีที่ประหยัดได้ต่อปี</span></div>
  </div>

  <div class="sub">CFPB มีอำนาจทำอะไรได้บ้าง</div>
  <div class="powers">
    <div class="power"><span class="no">01</span><div><b>ออกกฎ</b><span>เขียนระเบียบบังคับใช้กฎหมายการเงินระดับรัฐบาลกลาง เช่น บังคับให้เปิดเผยดอกเบี้ยจริงก่อนเซ็นสัญญา</span></div></div>
    <div class="power"><span class="no">02</span><div><b>เข้าตรวจ</b><span>ส่งเจ้าหน้าที่เข้าไปตรวจสอบธนาคารและบริษัทการเงินขนาดใหญ่ถึงที่ทำการ</span></div></div>
    <div class="power"><span class="no">03</span><div><b>ปรับและฟ้อง</b><span>สั่งปรับได้จริง เช่น Wells Fargo เคยถูกสั่งจ่าย 3.7 พันล้านดอลลาร์จากการเปิดบัญชีปลอมในชื่อลูกค้า</span></div></div>
    <div class="power"><span class="no">04</span><div><b>รับเรื่องร้องเรียน</b><span>เป็นคนกลางบังคับให้บริษัทต้องตอบประชาชนภายในกำหนด แล้วเปิดเผยผลสู่สาธารณะ ← ส่วนนี้คือที่มาของข้อมูลเรา</span></div></div>
  </div>

  <div class="sub">ดูแลสินค้าการเงินอะไรบ้าง</div>
  <div class="chips">
    <span class="chip"><b>เครดิตบูโร</b> รายงานเครดิต</span>
    <span class="chip"><b>ทวงหนี้</b> บริษัทตามหนี้</span>
    <span class="chip"><b>บัตรเครดิต</b></span>
    <span class="chip"><b>สินเชื่อบ้าน</b></span>
    <span class="chip"><b>บัญชีเงินฝาก</b></span>
    <span class="chip"><b>สินเชื่อรถ</b></span>
    <span class="chip"><b>กู้ยืมเรียน</b></span>
    <span class="chip"><b>เงินกู้นอกระบบ</b> payday loan</span>
    <span class="chip"><b>โอนเงิน</b> รวมคริปโต</span>
    <span class="chip"><b>บัตรเติมเงิน</b></span>
  </div>

  <div class="sub">เทียบกับหน่วยงานไทย</div>
  <div style="overflow-x:auto">
  <table class="compare">
    <thead><tr><th>หน้าที่</th><th>CFPB (สหรัฐฯ)</th><th>เทียบไทยประมาณ</th></tr></thead>
    <tbody>
      <tr><td>กำกับธนาคาร</td><td>ออกกฎฝั่งผู้บริโภคโดยเฉพาะ</td><td>ธนาคารแห่งประเทศไทย (ฝ่ายคุ้มครองผู้ใช้บริการ)</td></tr>
      <tr><td>รับเรื่องร้องเรียน</td><td>ศูนย์กลางเดียว บังคับบริษัทตอบใน 15 วัน</td><td>สคบ. + ศูนย์คุ้มครองผู้ใช้บริการทางการเงิน (ศคง. 1213)</td></tr>
      <tr><td>คุมบริษัททวงหนี้</td><td>อยู่ในอำนาจโดยตรง</td><td>กรมการปกครอง (พ.ร.บ.ทวงถามหนี้)</td></tr>
      <tr><td>เปิดข้อมูลสาธารณะ</td><td>เปิดทุกเรื่อง ดาวน์โหลดฟรี ไม่ต้องสมัคร</td><td>ไม่มีหน่วยงานไทยเปิดข้อมูลระดับนี้</td></tr>
    </tbody>
  </table>
  </div>

  <div class="note alert">
    <b>ข้อมูลชุดนี้กำลังจะหาไม่ได้อีกแล้ว</b>
    <p>วันที่ <b>14 สิงหาคม 2026</b> CFPB ประกาศ <b>หยุดเผยแพร่ข้อความร้องเรียนของผู้บริโภค</b> (narratives) ในฐานข้อมูลสาธารณะ กลับคำตัดสินใจเดิมที่ทำมาตั้งแต่ปี 2013 — จากนี้จะเหลือเปิดเผยแค่ข้อมูลเชิงหมวดหมู่และจำนวน ไม่มีข้อความดิบให้อ่านอีก</p>
    <p>ไฟล์ที่เราโหลดมามีข้อความครบถึงกลางปี 2026 จึงกลายเป็น <b>snapshot ที่ทำซ้ำไม่ได้</b> — ข้อดีคือทำให้งานนี้มีคุณค่าเชิงวิชาการ ข้อเสียคือต้องเขียนใน CRISP-DM ขั้น Deployment ว่าโมเดลนี้ retrain ด้วยข้อมูลสาธารณะใหม่ไม่ได้แล้ว ต้องพึ่งข้อมูลภายในองค์กรแทน</p>
  </div>
</section>
</div>'''

PROCESS = '''<div class="cfpb-doc">
<!-- ============ 1 CAST ============ -->
<section>
  <div class="shead"><span class="snum">02</span><h2>ผู้เกี่ยวข้อง 4 ฝ่าย</h2><span class="h2en">Who is involved</span></div>
  <p class="lede">มีผู้เล่นแค่ 4 ฝ่าย และแต่ละฝ่ายมีอำนาจไม่เท่ากัน จุดสำคัญคือ CFPB ไม่ได้ตัดสินคดี แต่เป็น “คนกลางที่มีอำนาจบังคับให้บริษัทต้องตอบ”</p>
  <div class="cast">
    <div class="actor a1">
      <span class="tag">Consumer</span>
      <b>ผู้ร้องเรียน</b>
      <span>ประชาชนที่เดือดร้อน เขียนเล่าปัญหาด้วยภาษาตัวเอง เป็นคนสร้างข้อความที่เราจะเอาไปเทรน</span>
    </div>
    <div class="actor a2">
      <span class="tag">Regulator</span>
      <b>CFPB</b>
      <span>รับเรื่อง คัดกรองว่าอยู่ในอำนาจไหม แล้วส่งต่อ บังคับเส้นตาย และเปิดเผยข้อมูลสู่สาธารณะ</span>
    </div>
    <div class="actor a3">
      <span class="tag">Respondent</span>
      <b>บริษัทการเงิน</b>
      <span>ธนาคาร บัตรเครดิต เครดิตบูโร บริษัททวงหนี้ — ถูกบังคับให้ตอบและเลือกประเภทคำตอบ</span>
    </div>
    <div class="actor a4">
      <span class="tag">Public</span>
      <b>ฐานข้อมูลสาธารณะ</b>
      <span>ทุกเรื่องถูกเปิดเผยหลังลบข้อมูลส่วนบุคคล ใครก็โหลดได้ฟรี — รวมถึงเรา</span>
    </div>
  </div>
</section>

<!-- ============ 2 FLOW ============ -->
<section>
  <div class="shead"><span class="snum">03</span><h2>ภาพรวมกระบวนการ</h2><span class="h2en">Process overview</span></div>
  <p class="lede">แถวนอนแต่ละแถวคือหนึ่งฝ่าย ลูกศรคือการส่งต่อ ตัวเลขบนเส้นคือเส้นตายตามกฎหมาย เส้นประคือทางแยกที่ไม่ได้เกิดทุกครั้ง</p>

  <figure>
    <div class="scroll">
    <svg viewBox="0 0 960 452" role="img" aria-label="แผนภาพ swimlane แสดงเส้นทางเรื่องร้องเรียน CFPB จากผู้ร้องเรียน ไปยัง CFPB ไปยังบริษัทการเงิน กลับมาที่ CFPB แล้วเผยแพร่สู่ฐานข้อมูลสาธารณะ พร้อมเส้นตาย 15 และ 60 วัน">
      <defs>
        <marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse">
          <path d="M0 0 L10 5 L0 10 z" fill="var(--navy)"/>
        </marker>
        <marker id="ard" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse">
          <path d="M0 0 L10 5 L0 10 z" fill="var(--ink-3)"/>
        </marker>
        <marker id="ars" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse">
          <path d="M0 0 L10 5 L0 10 z" fill="var(--stamp)"/>
        </marker>
      </defs>

      <!-- lane bands -->
      <g>
        <rect x="112" y="26"  width="836" height="86" fill="var(--stamp-soft)" opacity=".45"/>
        <rect x="112" y="128" width="836" height="86" fill="var(--navy-soft)" opacity=".55"/>
        <rect x="112" y="230" width="836" height="86" fill="var(--amber-soft)" opacity=".45"/>
        <rect x="112" y="332" width="836" height="86" fill="var(--green-soft)" opacity=".5"/>
      </g>
      <g class="svg-lane" text-anchor="end">
        <text x="100" y="64">ผู้ร้องเรียน</text>
        <text x="100" y="82" fill="var(--ink-3)" font-size="9">CONSUMER</text>
        <text x="100" y="166">CFPB</text>
        <text x="100" y="184" fill="var(--ink-3)" font-size="9">REGULATOR</text>
        <text x="100" y="268">บริษัท</text>
        <text x="100" y="286" fill="var(--ink-3)" font-size="9">COMPANY</text>
        <text x="100" y="370">สาธารณะ</text>
        <text x="100" y="388" fill="var(--ink-3)" font-size="9">PUBLIC DB</text>
      </g>
      <line x1="112" y1="20" x2="112" y2="424" stroke="var(--rule)" stroke-width="1"/>

      <!-- A: submit -->
      <g>
        <rect x="132" y="42" width="164" height="54" rx="2" fill="var(--card)" stroke="var(--stamp)" stroke-width="1.5"/>
        <text class="svg-n" x="142" y="60">1</text>
        <text class="svg-t" x="158" y="61">ยื่นเรื่องร้องเรียน</text>
        <text class="svg-s" x="142" y="80">เว็บ · โทร · ไปรษณีย์ · ส่งต่อ</text>
      </g>

      <!-- B: intake -->
      <g>
        <rect x="336" y="144" width="164" height="54" rx="2" fill="var(--card)" stroke="var(--navy)" stroke-width="1.5"/>
        <text class="svg-n" x="346" y="162">2</text>
        <text class="svg-t" x="362" y="163">คัดกรอง + จัดหมวด</text>
        <text class="svg-s" x="346" y="182">อยู่ในอำนาจไหม / ใครรับผิดชอบ</text>
      </g>

      <!-- branch: other agency -->
      <g>
        <rect x="352" y="46" width="140" height="34" rx="2" fill="none" stroke="var(--ink-3)" stroke-width="1" stroke-dasharray="4 3"/>
        <text class="svg-s" x="422" y="60" text-anchor="middle">ส่งต่อหน่วยงานอื่น</text>
        <text class="svg-s" x="422" y="73" text-anchor="middle" font-size="10">FTC · ธนาคารกลาง · มลรัฐ</text>
      </g>
      <line x1="418" y1="144" x2="418" y2="86" stroke="var(--ink-3)" stroke-width="1.2" stroke-dasharray="4 3" marker-end="url(#ard)"/>
      <text class="svg-edge" x="426" y="118" fill="var(--ink-3)">ไม่อยู่ในอำนาจ</text>

      <!-- C: company -->
      <g>
        <rect x="540" y="246" width="176" height="54" rx="2" fill="var(--card)" stroke="var(--amber)" stroke-width="1.5"/>
        <text class="svg-n" x="550" y="264" fill="var(--amber)">3</text>
        <text class="svg-t" x="566" y="265">ตรวจสอบ + ตอบกลับ</text>
        <text class="svg-s" x="550" y="284">ผ่าน Company Portal (ระบบปิด)</text>
      </g>

      <!-- D: publish -->
      <g>
        <rect x="756" y="144" width="176" height="54" rx="2" fill="var(--card)" stroke="var(--navy)" stroke-width="1.5"/>
        <text class="svg-n" x="766" y="162">4</text>
        <text class="svg-t" x="782" y="163">ลบข้อมูลส่วนบุคคล</text>
        <text class="svg-s" x="766" y="182">แล้วบันทึกผลลงฐานข้อมูล</text>
      </g>

      <!-- E: public db -->
      <g>
        <rect x="756" y="348" width="176" height="54" rx="2" fill="var(--card)" stroke="var(--green)" stroke-width="1.5"/>
        <text class="svg-n" x="766" y="366" fill="var(--green)">5</text>
        <text class="svg-t" x="782" y="367">Complaint Database</text>
        <text class="svg-s" x="766" y="386">เปิดให้ดาวน์โหลดฟรี ← ข้อมูลเรา</text>
      </g>

      <!-- F: consumer feedback -->
      <g>
        <rect x="756" y="42" width="176" height="54" rx="2" fill="var(--card)" stroke="var(--stamp)" stroke-width="1.5"/>
        <text class="svg-n" x="766" y="60">6</text>
        <text class="svg-t" x="782" y="61">อ่านคำตอบ + ให้คะแนน</text>
        <text class="svg-s" x="766" y="80">พอใจหรือไม่พอใจ</text>
      </g>

      <!-- arrows -->
      <path d="M296 69 L316 69 L316 171 L332 171" fill="none" stroke="var(--navy)" stroke-width="1.6" marker-end="url(#ar)"/>
      <text class="svg-edge" x="322" y="120">ส่งเรื่อง</text>

      <path d="M500 171 L520 171 L520 273 L536 273" fill="none" stroke="var(--navy)" stroke-width="1.6" marker-end="url(#ar)"/>
      <text class="svg-edge" x="527" y="256">ส่งเข้า Portal</text>

      <path d="M716 273 L736 273 L736 171 L752 171" fill="none" stroke="var(--stamp)" stroke-width="2" marker-end="url(#ars)"/>
      <text class="svg-edge" x="628" y="324" text-anchor="middle" fill="var(--stamp)" font-weight="600">ต้องตอบใน 15 วัน (สูงสุด 60 วัน)</text>

      <line x1="866" y1="204" x2="866" y2="342" stroke="var(--navy)" stroke-width="1.6" marker-end="url(#ar)"/>
      <text class="svg-edge" x="874" y="278">เผยแพร่</text>

      <line x1="800" y1="140" x2="800" y2="102" stroke="var(--navy)" stroke-width="1.6" marker-end="url(#ar)"/>
      <text class="svg-edge" x="810" y="124">แจ้งผลกลับ</text>

      <path d="M756 88 L608 88 L608 222 L344 222 L344 202" fill="none" stroke="var(--ink-3)" stroke-width="1.2" stroke-dasharray="4 3" marker-end="url(#ard)"/>
      <text class="svg-s" x="352" y="216" fill="var(--ink-3)">feedback ภายใน 60 วัน</text>
    </svg>
    </div>
    <figcaption>เส้นทึบคือเส้นทางหลักที่ทุกเรื่องต้องผ่าน เส้นประคือทางแยกที่เกิดเฉพาะบางกรณี เส้นสีแดงคือขาที่มีบทลงโทษตามกฎหมายกำกับอยู่</figcaption>
  </figure>
</section>

<!-- ============ 4 CLOCK ============ -->
<section>
  <div class="shead"><span class="snum">05</span><h2>เส้นตาย 15 วัน กับ 60 วัน</h2><span class="h2en">The legal deadlines</span></div>
  <p class="lede">เส้นตายคือหัวใจของ business case ทั้งหมด ถ้าเรื่องถูกส่งผิดทีม เวลาที่เสียไปกินเข้าไปในโควตา 15 วันทันที และ “ตอบไม่ทัน” จะถูกบันทึกลงฐานข้อมูลสาธารณะให้ทุกคนเห็น</p>

  <figure>
    <div class="scroll">
    <svg viewBox="0 0 960 176" role="img" aria-label="เส้นเวลาแสดงเส้นตายของกระบวนการ วันที่ 0 ยื่นเรื่อง วันที่ 1 ส่งถึงบริษัท วันที่ 15 ต้องตอบเบื้องต้น วันที่ 60 ตอบสุดท้ายและปิดรับ feedback">
      <line x1="60" y1="86" x2="900" y2="86" stroke="var(--rule)" stroke-width="2"/>
      <rect x="60" y="80" width="270" height="12" fill="var(--stamp)" opacity=".22"/>
      <rect x="330" y="80" width="570" height="12" fill="var(--amber)" opacity=".18"/>

      <g text-anchor="middle">
        <circle cx="60" cy="86" r="6" fill="var(--stamp)"/>
        <text class="svg-t" x="60" y="60">ยื่นเรื่อง</text>
        <text class="svg-edge" x="60" y="118" fill="var(--stamp)">DAY 0</text>

        <circle cx="118" cy="86" r="5" fill="var(--navy)"/>
        <text class="svg-s" x="118" y="140">ส่งถึงบริษัท</text>
        <text class="svg-edge" x="118" y="156" fill="var(--ink-3)">DAY 1</text>

        <circle cx="330" cy="86" r="7" fill="var(--stamp)"/>
        <text class="svg-t" x="330" y="60">ต้องตอบเบื้องต้น</text>
        <text class="svg-edge" x="330" y="118" fill="var(--stamp)">DAY 15</text>

        <circle cx="900" cy="86" r="7" fill="var(--amber)"/>
        <text class="svg-t" x="912" y="60" text-anchor="end">ตอบสุดท้าย + ปิดรับ feedback</text>
        <text class="svg-edge" x="900" y="118" fill="var(--amber)">DAY 60</text>
      </g>

      <rect x="60" y="26" width="118" height="3" fill="var(--navy)"/>
      <text class="svg-edge" x="66" y="20" fill="var(--navy)">ช่วงที่การส่งผิดทีมกินเวลา</text>
    </svg>
    </div>
    <figcaption>ในข้อมูลจริง 150,000 แถวของเรา มี 2,452 เรื่อง (1.6%) ที่ถูกบันทึกว่า “ตอบไม่ทัน” — ตัวเลขนี้คือขนาดของปัญหาที่โมเดลเราตั้งใจจะลด</figcaption>
  </figure>
</section>
</div>'''

DATA = '''<div class="cfpb-doc">
<!-- ============ 3 STAGES ============ -->
<section>
  <div class="shead"><span class="snum">04</span><h2>แต่ละขั้นตอนสร้างคอลัมน์อะไร</h2><span class="h2en">Where the data comes from</span></div>
  <p class="lede">คอลัมน์ในไฟล์ CSV ของเราไม่ได้โผล่มาพร้อมกัน แต่ละคอลัมน์เกิดคนละขั้นตอนกัน — เรื่องนี้สำคัญมาก เพราะคอลัมน์ที่เกิดหลังเราทำนาย จะใช้เป็น feature ไม่ได้ (data leakage)</p>

  <div class="stages">

    <div class="stage">
      <div class="idx">01</div>
      <div>
        <span class="who w-con">ผู้ร้องเรียน</span>
        <h3>กรอกแบบฟอร์มเล่าปัญหา</h3>
        <p>เข้าเว็บ consumerfinance.gov ใช้เวลาราว 10 นาที หรือโทร 1-855-411-2372 ใช้เวลา 25–30 นาที ในฟอร์มต้อง <b>เลือกหมวดสินค้าและประเภทปัญหาจาก dropdown เอง</b> แล้วพิมพ์เล่าเรื่องด้วยภาษาตัวเอง พร้อมระบุว่าจะยอมให้เปิดเผยข้อความหรือไม่</p>
      </div>
      <div class="out">
        <span class="lbl">คอลัมน์ที่เกิดขึ้น</span>
        <span class="col key">Consumer complaint narrative</span>
        <span class="col key">Product</span>
        <span class="col">Sub-product</span>
        <span class="col">Issue</span>
        <span class="col">Sub-issue</span>
        <span class="col">Company</span>
        <span class="col">State</span>
        <span class="col">Submitted via</span>
      </div>
    </div>

    <div class="stage">
      <div class="idx">02</div>
      <div>
        <span class="who w-cfpb">CFPB</span>
        <h3>รับเรื่อง ออกเลข แล้วคัดกรอง</h3>
        <p>ระบบออกเลขคดีให้ทันที ผู้ร้องได้อีเมลและติดตามสถานะได้ตลอด จากนั้น CFPB ดูว่าเรื่องนี้อยู่ในอำนาจตัวเองไหม ถ้าเป็นเรื่องนอกขอบเขต (เช่น โฆษณาหลอกลวงทั่วไป) จะส่งต่อให้ FTC หรือหน่วยงานอื่น ถ้าอยู่ในขอบเขตก็ส่งเข้า Company Portal ของบริษัทนั้น</p>
      </div>
      <div class="out">
        <span class="lbl">คอลัมน์ที่เกิดขึ้น</span>
        <span class="col">Complaint ID</span>
        <span class="col">Date received</span>
        <span class="col">Date sent to company</span>
      </div>
    </div>

    <div class="stage">
      <div class="idx">03</div>
      <div>
        <span class="who w-co">บริษัทการเงิน</span>
        <h3>ทีมภายในตรวจสอบ แล้วเลือกประเภทคำตอบ</h3>
        <p>บริษัทล็อกอินเข้า Company Portal ทีม compliance ตรวจบัญชีลูกค้า ติดต่อกลับ แล้วต้องส่งคำตอบพร้อม <b>เลือกหมวดคำตอบ</b> ว่าปิดเรื่องแบบไหน กฎบังคับว่าต้องตอบเบื้องต้นภายใน 15 วัน ถ้ายังไม่จบให้ตอบสุดท้ายภายใน 60 วัน</p>
      </div>
      <div class="out">
        <span class="lbl">คอลัมน์ที่เกิดขึ้น <span style="color:var(--stamp)">⚠ หลังการทำนาย</span></span>
        <span class="col">Company response to consumer</span>
        <span class="col">Timely response?</span>
        <span class="col">Company public response</span>
      </div>
    </div>

    <div class="stage">
      <div class="idx">04</div>
      <div>
        <span class="who w-cfpb">CFPB</span>
        <h3>ลบข้อมูลส่วนบุคคล แล้วเปิดเผย</h3>
        <p>ก่อนเผยแพร่ ระบบจะลบชื่อ เลขบัญชี ที่อยู่ ออกจากข้อความ แทนที่ด้วย <span class="col">XXXX</span> — นี่คือเหตุผลที่ในข้อมูลของเราจะเจอ XXXX เต็มไปหมด ถือเป็น noise ที่ต้องจัดการตอน text cleaning</p>
      </div>
      <div class="out">
        <span class="lbl">ผลลัพธ์</span>
        <p class="none">ข้อความถูกปิดบัง (redacted) แต่โครงสร้างประโยคยังอยู่ครบ</p>
      </div>
    </div>

    <div class="stage">
      <div class="idx">05</div>
      <div>
        <span class="who w-pub">สาธารณะ</span>
        <h3>เข้าฐานข้อมูลเปิด</h3>
        <p>ทุกเรื่องถูกบันทึกลง Consumer Complaint Database เปิดให้ค้นหาและดาวน์โหลดเป็น CSV ได้ฟรีโดยไม่ต้องสมัครสมาชิก นักวิจัย นักข่าว และคู่แข่งในตลาดใช้ข้อมูลนี้ตรวจสอบพฤติกรรมบริษัท</p>
      </div>
      <div class="out">
        <span class="lbl">ผลลัพธ์</span>
        <p class="none">complaints.csv ขนาด 8.7 GB — ไฟล์ที่เราโหลดมาใช้</p>
      </div>
    </div>

    <div class="stage">
      <div class="idx">06</div>
      <div>
        <span class="who w-con">ผู้ร้องเรียน</span>
        <h3>อ่านคำตอบ แล้วให้คะแนน</h3>
        <p>ผู้ร้องได้รับแจ้งคำตอบและมีเวลา 60 วันในการบอกว่าพอใจหรือไม่ ความเห็นนี้ถูกส่งกลับให้บริษัทดู และ CFPB เก็บเป็นสถิติใช้ตัดสินใจว่าจะเข้าไปตรวจสอบบริษัทไหนเป็นพิเศษ</p>
      </div>
      <div class="out">
        <span class="lbl">ผลลัพธ์</span>
        <p class="none">ไม่ปรากฏเป็นคอลัมน์ในไฟล์สาธารณะ</p>
      </div>
    </div>

  </div>

  <div class="note">
    <b>จุดที่อาจารย์น่าจะถาม — ตอบให้ตรง</b>
    <p><b>“ถ้า Product เป็นสิ่งที่ผู้ร้องเลือกเองอยู่แล้ว จะให้ AI ทายไปทำไม?”</b> เพราะสามเหตุผล หนึ่ง — ฟอร์มมี dropdown ซ้อนหลายชั้น คนทั่วไปแยกไม่ออกว่า “Credit reporting” กับ “Credit repair services” ต่างกันตรงไหน จึงติดหมวดผิดบ่อย สอง — เรื่องที่มาทางโทรศัพท์และทางไปรษณีย์ ต้องมีเจ้าหน้าที่นั่งฟังแล้วติดหมวดให้เอง สาม — บริษัทที่รับเรื่องเข้ามาวันละหลายพันต้องกระจายเข้าทีมย่อยอีกที ซึ่งไม่มีระบบอัตโนมัติรองรับ</p>
    <p>โมเดลของเราจึงทำหน้าที่เป็น <b>ตัวช่วยติดหมวดและตรวจสอบซ้ำ</b> ไม่ใช่มาแทนที่ dropdown — ทายจากข้อความล้วน ๆ ได้ถูก 70% จาก 14 หมวด ทั้งที่ไม่เห็นตัวเลือกที่ผู้ร้องกดเลย</p>
  </div>
</section>
</div>'''

MODEL = '''<div class="cfpb-doc">
<!-- ============ 5 WHERE THE MODEL GOES ============ -->
<section>
  <div class="shead"><span class="snum">06</span><h2>โมเดลเข้าไปแทนที่ขั้นตอนไหน</h2><span class="h2en">Where the model fits</span></div>
  <p class="lede">เราไม่ได้เปลี่ยนทั้งระบบ เราเปลี่ยนแค่เส้นเดียว — เส้นที่แปลง “ข้อความที่คนเขียน” ให้กลายเป็น “หมวดที่ใช้ route ต่อ”</p>

  <figure>
    <div class="scroll">
    <svg viewBox="0 0 960 260" role="img" aria-label="เปรียบเทียบก่อนและหลัง แบบเดิมข้อความไปที่คนติดหมวดด้วยมือแล้วส่งเข้าทีม แบบใหม่ข้อความผ่านโมเดล TF-IDF และ Logistic Regression แล้วส่งเข้าทีม โดยเปลี่ยนเฉพาะกล่องตรงกลาง">
      <defs>
        <marker id="ar2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse">
          <path d="M0 0 L10 5 L0 10 z" fill="var(--ink-3)"/>
        </marker>
        <marker id="ar3" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse">
          <path d="M0 0 L10 5 L0 10 z" fill="var(--green)"/>
        </marker>
      </defs>

      <text class="svg-lane" x="16" y="62">แบบเดิม</text>
      <text class="svg-lane" x="16" y="186" fill="var(--green)">แบบใหม่</text>

      <!-- shared input -->
      <rect x="112" y="30" width="176" height="52" rx="2" fill="var(--sunk)" stroke="var(--rule)"/>
      <text class="svg-t" x="200" y="52" text-anchor="middle">ข้อความร้องเรียน</text>
      <text class="svg-s" x="200" y="70" text-anchor="middle">เฉลี่ย 1,047 ตัวอักษร</text>

      <rect x="112" y="154" width="176" height="52" rx="2" fill="var(--sunk)" stroke="var(--rule)"/>
      <text class="svg-t" x="200" y="176" text-anchor="middle">ข้อความร้องเรียน</text>
      <text class="svg-s" x="200" y="194" text-anchor="middle">ข้อความเดียวกัน</text>

      <!-- the box that differs : OLD -->
      <rect x="368" y="24" width="216" height="64" rx="2" fill="none" stroke="var(--ink-3)" stroke-width="1.4" stroke-dasharray="5 4"/>
      <text class="svg-t" x="476" y="48" text-anchor="middle" fill="var(--ink-2)">คนติดหมวดเอง</text>
      <text class="svg-s" x="476" y="66" text-anchor="middle">dropdown 14 หมวด · ผิดบ่อย · ช้า</text>

      <!-- the box that differs : NEW -->
      <rect x="368" y="148" width="216" height="64" rx="2" fill="var(--green-soft)" stroke="var(--green)" stroke-width="2"/>
      <text class="svg-t" x="476" y="172" text-anchor="middle" fill="var(--green)">TF-IDF + Logistic Regression</text>
      <text class="svg-s" x="476" y="190" text-anchor="middle">ทายหมวดจากข้อความล้วน · &lt;1 วินาที</text>

      <!-- shared output -->
      <rect x="664" y="30" width="200" height="52" rx="2" fill="var(--sunk)" stroke="var(--rule)"/>
      <text class="svg-t" x="764" y="52" text-anchor="middle">ส่งเข้าทีมที่รับผิดชอบ</text>
      <text class="svg-s" x="764" y="70" text-anchor="middle">นาฬิกา 15 วันเริ่มเดิน</text>

      <rect x="664" y="154" width="200" height="52" rx="2" fill="var(--sunk)" stroke="var(--rule)"/>
      <text class="svg-t" x="764" y="176" text-anchor="middle">ส่งเข้าทีมที่รับผิดชอบ</text>
      <text class="svg-s" x="764" y="194" text-anchor="middle">ปลายทางเดิม ไม่ต้องแก้ระบบ</text>

      <line x1="288" y1="56" x2="364" y2="56" stroke="var(--ink-3)" stroke-width="1.5" marker-end="url(#ar2)"/>
      <line x1="584" y1="56" x2="660" y2="56" stroke="var(--ink-3)" stroke-width="1.5" marker-end="url(#ar2)"/>
      <line x1="288" y1="180" x2="364" y2="180" stroke="var(--green)" stroke-width="1.8" marker-end="url(#ar3)"/>
      <line x1="584" y1="180" x2="660" y2="180" stroke="var(--green)" stroke-width="1.8" marker-end="url(#ar3)"/>

      <text class="svg-edge" x="476" y="122" text-anchor="middle" fill="var(--stamp)">↕ เปลี่ยนแค่กล่องนี้กล่องเดียว — ต้นทางและปลายทางเหมือนเดิมทุกอย่าง</text>
    </svg>
    </div>
    <figcaption>การวางขอบเขตแบบนี้ทำให้ Deployment ใน CRISP-DM เป็นไปได้จริง — โมเดลเป็นบริการเสริมที่แทรกเข้าไประหว่างฟอร์มกับระบบ routing โดยไม่ต้องรื้อระบบเดิม</figcaption>
  </figure>

  <div class="pitch">
    <div class="pitch-h">
      <span class="tag">Project #1 · Problem Statement</span>
      <b>จำแนกหมวดข้อร้องเรียนการเงินอัตโนมัติจากข้อความที่ผู้บริโภคเขียนเอง</b>
    </div>
    <div class="pitch-g">
      <div><dt>Input</dt><dd><strong>ข้อความล้วน</strong><br>Consumer complaint narrative</dd></div>
      <div><dt>Output</dt><dd><strong>Product</strong><br>14 หมวด</dd></div>
      <div><dt>Baseline</dt><dd><span class="metric" style="color:var(--ink-3)">0.050<small>macro F1 · เดาหมวดที่เจอบ่อยสุด</small></span></dd></div>
      <div><dt>ผลที่ได้</dt><dd><span class="metric">0.561<small>macro F1 · ดีขึ้น 11 เท่า</small></span></dd></div>
    </div>
  </div>
</section>
</div>'''

FOOTER = '''<div class="cfpb-doc">
<footer>
  ข้อมูลกระบวนการอ้างอิงจากเอกสารทางการของ CFPB · ตัวเลขสถิติคำนวณจากไฟล์ <span class="col">complaints_clean_150k.csv</span> (150,000 แถว ปี 2023–2026)<br>
  แหล่งอ้างอิง: <a href="https://www.consumerfinance.gov/complaint/process/">Learn how the complaint process works</a> · <a href="https://www.consumerfinance.gov/compliance/consumer-complaint-program/company-process/">Your company's role in the complaint process</a> · <a href="https://www.consumerfinance.gov/data-research/consumer-complaints/">Consumer Complaint Database</a>
</footer>
</div>'''
