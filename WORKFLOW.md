# End-to-End Research-to-Production Workflow Prompt

> **Role mapping in this repo:** the `mit-ai-professor` role named below is played by [`.agents/research-principal-investigator.md`](.agents/research-principal-investigator.md) (the PI). Every other role name matches a file in [`.agents/`](.agents/). The PI brief's note still applies: the role is an expected expertise profile, not a claim of any real title or affiliation.

## เป้าหมายและบทบาทหลัก (Objective & Division of Labor)
- **เป้าหมายสูงสุด:** สร้างงานวิจัยระดับ Top-Tier Conference/Journal (NeurIPS, ICML, IEEE — ห้ามทำงานระดับทั่วไปหรือแค่ต่อท่อปกติ) ที่สามารถนำไปใช้งานจริงได้ (Research-to-Production)
- **บทบาทของ User:** เป็นผู้กำหนดโจทย์วิจัย (Research Question), บริบทแวดล้อม (Context), ข้อมูล (Dataset) และรูปแบบการนำไปใช้งานจริง (Target Practical Usage)
- **บทบาทของ Agent Team:** ทำงานร่วมกันตามลำดับ 5 ขั้นตอน (`01-brainstorm` → `02-literature-review` → `03-solution-design` → `04-implementation` → `05-report`) โดยทุกไฟล์เป็น **Living Document** ที่ต้องย้อนกลับมาอัปเดตทันทีเมื่อมีการเปลี่ยนแปลงในขั้นตอนถัดไป

---

## ขั้นตอนที่ 1: `01-brainstorm` (การระดมสมองและสังเคราะห์ปัญหา)
- **ผู้รับผิดชอบ:** **Agent ทุก Role** (`mit-ai-professor`, `researcher`, `product-manager`, `domain-expert`, `data-scientist`, `data-engineer`, `data-analyst`, `ai-engineer`, `ux-ui-designer`, `full-stack-developer`)
- **กระบวนการ:**
  1. แต่ละ Role วิเคราะห์โจทย์ บริบท และรูปแบบการนำไปใช้จริง จากมุมมองและหน้าที่รับผิดชอบของตนเอง
  2. `mit-ai-professor` และ `researcher` ตรวจสอบความแปลกใหม่ (Novelty), กลุ่มเป้าหมายของงานวิจัย, ความถูกต้องของระเบียบวิธีวิจัย (Methodology) และวิธีวัดผล (Evaluation)
  3. สังเคราะห์มุมมองทั้งหมดออกมาเป็นประเด็นปัญหาที่ต้องแก้ไข (Core Problems) และสมมติฐานที่ตรวจสอบได้
- **Output:** บันทึกรวมเป็นไฟล์เดียวที่ `./01-brainstorm/brainstorm.md`
- **Update Rule:** หากพบปัญหาใหม่ ข้อจำกัดใหม่ หรือสมมติฐานที่เปลี่ยนไปใน Downstream Tasks (`02`–`05`) **ต้องย้อนกลับมาอัปเดต `./01-brainstorm/brainstorm.md` เสมอ**

---

## ขั้นตอนที่ 2: `02-literature-review` (การทบทวนวรรณกรรมแบบ LLMwiki)
- **ผู้รับผิดชอบหลัก:** Lead โดย `researcher` (ภายใต้การตรวจสอบความเข้มข้นทางวิชาการโดย `mit-ai-professor`)
- **กระบวนการสืบค้นและสกัดข้อมูล:**
  1. ค้นหาบทความวิจัยระดับแนวหน้า (NeurIPS, ICML, ICLR, KDD, WWW, IEEE ฯลฯ) ที่เกี่ยวข้องกับทุกประเด็นปัญหาใน `./01-brainstorm/brainstorm.md`
  2. สกัดสาระสำคัญจากแต่ละบทความให้ครบ **9 หัวข้อบังคับ**:
     - `Research question` (คำถามวิจัย)
     - `Limitation of existing methods` (ข้อจำกัดของวิธีเดิมก่อนหน้า)
     - `Contributions` (คุณูปการหลักของงาน)
     - `Proposed methods` (วิธีการที่นำเสนอ)
     - `Key findings` (ผลลัพธ์และข้อค้นพบสำคัญ)
     - `Limitations` (ข้อจำกัดของงานชิ้นนี้)
     - `Author names` (รายชื่อผู้แต่ง)
     - `Publish year` (ปีที่ตีพิมพ์)
     - `Proceedings or journal name` (ชื่อการประชุมวิชาการหรือวารสาร)
- **การจัดเก็บไฟล์ตามโครงสร้าง LLMwiki:**
  - **ไฟล์ต้นฉบับ (Original Paper):** บันทึกไว้ที่ `./02-literature-review/raw/`
  - **ไฟล์ข้อมูลที่สกัดแล้ว (Extracted Wiki):** บันทึกไว้ที่ `./02-literature-review/wiki/`
  - **กฎการตั้งชื่อไฟล์ใน `wiki/`:** ใช้รูปแบบ `first_author-publish_year-keywords.md` (หากมี keyword มากกว่า 1 คำ ให้ใส่ทุกคำเชื่อมด้วย `-` เช่น `angelopoulos-2024-conformal-risk-control.md`)
- **การจัดทำ Index และบทสรุปวรรณกรรม (Auto-Sync Rules):**
  - **Search Index (`./02-literature-review/index.md`):** สร้างสารบัญดัชนีของทุกไฟล์ใน `./02-literature-review/wiki/` เพื่อรองรับการสืบค้น และ **ต้องอัปเดต `index.md` ทุกครั้งที่มีไฟล์ใหม่เพิ่มเข้ามาใน `wiki/`**
  - **Narrative Summary (`./02-literature-review/summary/review.md`):** ให้ `researcher` เขียนสรุปทบทวนวรรณกรรมแบบ **Narrative Style** พร้อมอ้างอิง Citation แบบ **APA Style** ให้ครบทุกไฟล์ที่อยู่ใน `./02-literature-review/wiki/` และ **ต้องกลับมาอัปเดต `review.md` ทุกครั้งที่มีการเพิ่มบทความใหม่ใน `raw/` หรือ `wiki/`**

---

## ขั้นตอนที่ 3: `03-solution-design` (การออกแบบโซลูชันและสถาปัตยกรรมระบบ)
- **ผู้รับผิดชอบหลัก:** Lead โดย `product-manager` ทำงานร่วมกับ `ux-ui-designer` (และสอบทานความถูกต้องเชิงอัลกอริทึมกับ `mit-ai-professor`, `researcher`, `ai-engineer`, `data-scientist`)
- **กระบวนการและ Output บังคับ (2 เอกสาร):**
  1. **Project Specification (`./03-solution-design/project-spec.md`):**
     - ออกแบบและระบุ Features ทั้งหมดของโซลูชัน ขอบเขตการใช้งาน และเกณฑ์ประเมินผลสำหรับโจทย์ที่ได้รับ
     - **Update Rule:** หากมีการเพิ่ม ลด หรือแก้ไข Feature ใน Downstream Tasks **ต้องย้อนกลับมาอัปเดต `./03-solution-design/project-spec.md` เสมอ**
  2. **Implementation Specification (`./03-solution-design/implement-spec.md`):**
     - แสดงรายการ Modules ทั้งหมดที่ต้องสร้าง
     - เขียน **System Diagram** และ **System Architecture** เพื่ออธิบายภาพรวมของระบบ
     - อธิบายการทำงานของแต่ละ Module ในรูปแบบ **`Input → Process → Output`** อย่างชัดเจน
     - อธิบายความเชื่อมโยงและการส่งต่อข้อมูลว่าแต่ละ Module ทำงานร่วมกันอย่างไร
     - **Update Rule:** หากมีการปรับเปลี่ยนการออกแบบในภายหลัง **ต้องย้อนกลับมาอัปเดต `./03-solution-design/implement-spec.md` เสมอ**

---

## ขั้นตอนที่ 4: `04-implementation` (การพัฒนาระบบและการทดสอบคุณภาพ)
- **การเลือก Tech Stack (`./04-implementation/tech-stack.md`):**
  - `full-stack-developer` เป็นผู้เลือก Tech Stack ที่เหมาะสมสำหรับแต่ละ Module และบันทึกเหตุผลประกอบไว้ที่ `./04-implementation/tech-stack.md`
- **การพัฒนาแต่ละ Module:**
  - `data-scientist`, `data-engineer`, `ai-engineer`, และ `full-stack-developer` ทำงานร่วมกันเพื่อพัฒนาทุก Module ตามที่ระบุไว้ใน `./03-solution-design/implement-spec.md`
- **การทดสอบบังคับ (`./04-implementation/qa.md`):**
  - **กฎเหล็ก:** ทุก Module ที่สร้างขึ้น **ต้องถูกทดสอบ (Test) เสมอ**
  - บันทึกวิธีการทดสอบและผลการทดสอบของแต่ละ Module ไว้ที่ `./04-implementation/qa.md`

---

## ขั้นตอนที่ 5: `05-report` (การรายงานผลการทดสอบระบบและงานวิจัย)
- **ผู้รับผิดชอบ:** `researcher`, `mit-ai-professor`, `data-scientist`, `data-analyst`, และ `ai-engineer` ทำงานร่วมกัน
- **กระบวนการและ Output:**
  - สรุปรายงานผลการทดสอบระบบและผลการทดลองทางวิทยาศาสตร์ทั้งหมด บันทึกไว้ที่ `./05-report/report.md`
  - **ต้องระบุวันที่ทำการทดสอบ (`YYYY-MM-DD`) ไว้อย่างชัดเจนทุกครั้ง**
  - **Update Rule:** หากมีการรันการทดสอบใหม่หรือการทดลองเพิ่มเติม **ต้องกลับมาอัปเดตไฟล์ `./05-report/report.md` เสมอ**

---

## งานเดิมใน `is-topic/` เทียบกับขั้นตอน (Existing work mapped to stages)

| ไฟล์เดิม | ขั้นตอนที่ใช้เป็นข้อมูลตั้งต้น |
|---|---|
| `is-topic/research_proposal.md`, `is-topic/topic-comparison.md`, `is-topic/refined-thesis-plan.md`, `is-topic/neurips-mock-review.md` | `01-brainstorm` (โจทย์, สมมติฐาน, ข้อวิจารณ์ด้าน novelty และ methodology) |
| `is-topic/literature-review.md` | `02-literature-review` (ต้องแตกแต่ละบทความเป็นไฟล์ใน `wiki/` ตาม 9 หัวข้อ แล้วเขียน `summary/review.md`) |
| `is-topic/project-plan.md`, `is-topic/refined-thesis-plan.md` | `03-solution-design` (ขอบเขต, เกณฑ์ประเมินผล) |
