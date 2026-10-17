# NeurIPS 2026 Standard — มาตรฐานกลางของทีม

> ไฟล์อ้างอิงกลางที่ทุก agent ต้องโหลดคู่กับ [README.md](./README.md) เมื่อโครงการตั้งเป้าคุณภาพระดับ NeurIPS main track
> **ตรวจสอบจากแหล่งทางการเมื่อ 2026-10-17:** [Call for Papers 2026](https://nips.cc/Conferences/2026/CallForPapers) · [Main Track Handbook 2026](https://nips.cc/Conferences/2026/MainTrackHandbook) · [Reviewer Guidelines 2026](https://nips.cc/Conferences/2026/ReviewerGuidelines) · [Formatting template 2026](https://media.neurips.cc/Conferences/NeurIPS2026/Formatting_Instructions_For_NeurIPS_2026.zip)

> **ข้อควรทราบ**
> - รอบส่ง NeurIPS 2026 ปิดไปแล้ว (abstract 4 พ.ค. 2026, full paper 6 พ.ค. 2026 AoE, ประกาศผล 24 ก.ย. 2026) ไฟล์นี้จึงใช้ NeurIPS 2026 เป็น **เกณฑ์คุณภาพ** หากจะส่งจริงในรอบถัดไป PM ต้องตรวจ CfP และ Handbook ของปีนั้นใหม่ทั้งหมด เพราะนโยบายเปลี่ยนทุกปี
> - มาตรฐานนี้ยกระดับ *ความเข้มงวดของงาน* ไม่ได้รับประกันการตอบรับ ไม่มี agent ใดสัญญาหรือสื่อเป็นนัยว่าจะได้รับการตอบรับ

---

## 1. เกณฑ์ที่ reviewer ใช้ (ทุกบทบาทต้องทำงานให้ผ่านเกณฑ์เหล่านี้)

จาก Reviewer Guidelines 2026 ใช้ 4 มิติเดียวกันทุกประเภทบทความ:

| มิติ | คำถามของ reviewer | เจ้าของหลักในทีม |
|---|---|---|
| **Quality** | งานถูกต้องทางเทคนิคหรือไม่ และผู้เขียนประเมินทั้งจุดแข็งและจุดอ่อนอย่างระมัดระวังและซื่อตรงหรือไม่ | Data Scientist, Research PI |
| **Clarity** | เขียนชัดหรือไม่ และให้ข้อมูลพอให้ผู้เชี่ยวชาญทำซ้ำผลได้หรือไม่ | Research Paper Writer, Data Scientist |
| **Significance** | ผลมีผลกระทบต่อชุมชนวิจัยหรือไม่ | Research PI, Domain Expert |
| **Originality** | ให้ insight ใหม่ เข้าใจลึกขึ้น หรือชี้คุณสมบัติสำคัญของวิธีเดิมหรือไม่ (การประเมินแบบใหม่ หรือ efficiency/fairness ที่ดีขึ้นก็นับได้) | Research PI, Researcher |

## 2. Contribution Type (ใหม่ในปี 2026: ต้องเลือกตอนส่ง)

PI ต้องเลือกประเภทให้ได้ **ตั้งแต่ G1** เพราะประเภทกำหนดหลักฐานที่ต้องหา และ reviewer ใช้เกณฑ์ต่างกัน

| ประเภท | สิ่งที่ reviewer เน้น | ผลต่อแผนงานของทีม |
|---|---|---|
| **General** | เกณฑ์มาตรฐาน 4 มิติ | Baselines, ablations, สถิติครบตาม Section 4 |
| **Theory** | ความถูกต้องของ claims เป็นหลัก; assumptions เหมาะสมกับความใหม่ของผล; ไม่ต้องมีการทดลอง | ต้องมีผู้ตรวจ proof อิสระ (ดู Section 4.3) |
| **Use-Inspired** | use case จริงหรือไม่ และ design ตรงกับ use case หรือไม่; สนับสนุน real-world dataset ที่ไม่ใช่มาตรฐานถ้ามีเหตุผล; ต้องพิจารณา non-ML baselines | Domain Expert เป็นผู้ยืนยัน use case; Data Scientist ต้องรวม non-ML baseline |
| **Concept & Feasibility** | claims ต้องได้รับการสนับสนุนอย่างแข็งแรง; significance สูงมาก ต้องมีศักยภาพเปลี่ยนแนวทางหรือความเข้าใจ และเป็นไอเดียใหม่มาก | PI ต้องมีเหตุผลชัดว่าทำไมไม่ใช่ General |
| **Negative Results** | วิเคราะห์ไปไกลกว่าแค่ผลที่ไม่คาดคิด (ด้วย conjecture, การทดลอง หรือ proof); ต้องเปลี่ยนความเข้าใจต่อคำถามสำคัญ และน่าแปลกใจเมื่อเทียบกับความเชื่อทั่วไป; ไม่จำเป็นต้องมีทางแก้ | ผลลบจาก G4 อาจกลายเป็น contribution ได้ ห้ามทิ้ง |

**กฎ:** ส่งได้ track เดียวและประเภทเดียว เปลี่ยนภายหลังไม่ได้ (main, Evaluations & Datasets และ Position Paper เป็นคนละ track)

## 3. ข้อกำหนดของการส่งที่ต้องผ่าน (desk-reject risks)

| ข้อกำหนด (Handbook 2026) | ผู้รับผิดชอบ | ตรวจที่ gate |
|---|---|---|
| เนื้อหาหลักไม่เกิน **9 หน้า** รวม figures และ tables (references, appendix, checklist ไม่นับ); camera-ready ได้เพิ่ม 1 หน้า | Paper Writer | G6, G7 |
| ใช้ LaTeX style file ของปีนั้นเท่านั้น (ไม่มี Word template แล้ว); ลำดับ PDF: main → references → appendix → checklist; PDF ≤ 50MB, supplementary ZIP ≤ 100MB | Paper Writer, PM | G7 |
| **Double-blind:** ไม่มีข้อมูลระบุตัวตนทั้งใน paper, supplementary และ **code**; ไม่ใส่ acknowledgments ตอนส่ง; self-citation แบบบุคคลที่สาม | Paper Writer, Data Scientist, AI Engineer (ตรวจ code/repo) | G7 |
| กรอก **Paper Checklist** ใน template ให้ครบ (ดู Section 5) | Paper Writer + เจ้าของแต่ละข้อ | G6 |
| **Dual submission:** ห้ามส่ง venue archival อื่นระหว่างรีวิว ห้าม thin slicing ห้ามส่งหลาย track; workshop แบบ non-archival ได้ | PM, PI | G0, G7 |
| **LLM/agents:** ถ้าใช้ LLM หรือ agents เป็นส่วนสำคัญ ใหม่ หรือไม่ใช่มาตรฐานของ *วิธีการ* ต้องอธิบายใน experimental setup; **agents และ LLMs เป็นผู้แต่งไม่ได้**; ผู้แต่งรับผิดชอบทุกเนื้อหารวมถึง figures และ references (Handbook ระบุเรื่อง hallucinated citations ไว้ชัด); **ห้าม prompt injection** หรือการพยายามบิดเบือนการรีวิว | ทุกบทบาท; Paper Writer ตรวจ | G6, G7 |
| **Preprint:** โพสต์ได้ (ใช้ตัวเลือก "preprint" ของ style file) แต่ห้ามเขียนว่า "Under review at NeurIPS" และห้ามโปรโมตเกินควร | PM | ระหว่างรีวิว |
| **Contemporaneous work:** งานที่ออนไลน์หลัง 1 มี.ค. 2026 ถือเป็นงานร่วมสมัย แต่ยังต้องอ้างอิงและอภิปราย | Researcher | G6 |
| **Reciprocal reviewing:** ผู้แต่งที่เป็น reviewer/AC ต้องรีวิวให้เสร็จ ไม่อย่างนั้นจะไม่เห็นรีวิวของตัวเอง และอาจถูก desk reject | PM (ติดตามผู้แต่งมนุษย์) | ระหว่างรีวิว |
| Camera-ready: funding statement, competing-interests disclosure, **lay summary** ภาษาเข้าใจง่าย; รีวิวของบทความที่ได้รับการตอบรับจะเปิดเป็นสาธารณะ; ต้องมีผู้แต่งอย่างน้อยหนึ่งคนไปร่วมงานด้วยตนเอง | PM, Paper Writer | หลังตอบรับ |

## 4. มาตรฐานหลักฐานเชิงเทคนิคระดับ NeurIPS (เกณฑ์ของทีม)

ส่วนนี้คือ **เกณฑ์ขั้นต่ำที่ทีมกำหนดเอง** เพื่อให้ผ่านมิติ Quality และ Clarity ไม่ใช่ข้อความจาก NeurIPS โดยตรง PI อนุมัติข้อยกเว้นได้เมื่อมีเหตุผลบันทึกใน Decision Log

### 4.1 Baselines & Comparisons
- เทียบกับ **SOTA ที่แข็งแรงที่สุดที่ตีพิมพ์แล้ว** และ **baseline ง่ายแต่แข็ง** (เช่น tuned linear/kNN/heuristic หรือ prompting baseline ที่ดีที่สุด) ไม่ใช่แค่ baseline อ่อน
- Baselines ได้ **hyperparameter tuning budget เท่ากัน** กับวิธีที่เสนอ (จำนวน trials หรือ GPU-hours) และระบุใน appendix
- หากใช้ตัวเลขที่ paper อื่นรายงาน ต้องยืนยันว่าเงื่อนไข (data split, preprocessing, metric implementation) ตรงกัน หรือรันใหม่เอง
- Use-Inspired: รวม non-ML baseline ที่ใช้จริงในสาขา

### 4.2 Statistical Reporting
- ผลหลักรายงาน **mean ± std หรือ 95% CI จากอย่างน้อย 5 seeds** (หรือ bootstrap CI บน test set สำหรับงานที่รันซ้ำไม่ได้เพราะต้นทุน พร้อมเหตุผล)
- ระบุ **แหล่งของ variance** ที่ error bar แทน (seeds, data splits, bootstrap) และวิธีคำนวณ
- ทดสอบความแตกต่างด้วย test ที่เหมาะสม แก้ multiple comparisons เมื่อเทียบหลายคู่ และรายงาน effect size
- ห้ามใช้คำว่า "significantly" โดยไม่มี statistical test รองรับ

### 4.3 Ablations, Analysis & Theory
- Ablation ของ **ทุก component ที่อ้างว่าสำคัญ** ใน contribution
- Sensitivity analysis ต่อ hyperparameters หลัก
- Error analysis เชิงคุณภาพ และ **failure cases** ที่ระบุชัด
- Generalization: ทดสอบมากกว่าหนึ่ง dataset/setting หรืออธิบายว่าทำไมไม่จำเป็น
- Theory: ระบุ assumptions ครบทุกข้อ, proof สมบูรณ์ (ใน appendix ได้) และมี **ผู้ตรวจ proof อิสระในทีม** ที่ไม่ใช่ผู้เขียน proof

### 4.4 Efficiency Claims
- รายงานครบ: คุณภาพ, latency/throughput, peak memory, compute (GPU-hours/FLOPs), ต้นทุน บน **hardware และ config เดียวกัน**
- รายงาน **compute ทั้งหมดของโครงการ** รวม runs ที่ล้มเหลวและการทดลองที่ไม่ได้อยู่ในบทความ (ตรงกับข้อ Compute Resources ใน checklist)

### 4.5 Reproducibility Package
- Code แบบ **self-contained และ executable** (ตามที่ Handbook สนับสนุน) พร้อมคำสั่งเดียวจาก raw data ถึงตัวเลขในตาราง
- Anonymized ก่อนส่ง (ลบชื่อ, path, git history, API keys, URL ส่วนตัว)
- Dataset ใหม่: persistent identifier, ที่เก็บระยะยาว, license ชัดเจน (ตาม Handbook)
- Environment lock, seeds, configs, checkpoints (ถ้าแชร์ได้)
- **Dry-run:** มีบทบาทอื่นในทีมรันซ้ำจาก package บนเครื่องสะอาดได้ผลในช่วงที่คาด

### 4.6 Ethics & Societal Impact
- ทำตาม NeurIPS Code of Ethics (ลิงก์อยู่ใน Main Track Handbook): human subjects, consent และ privacy ของข้อมูล, ผลเสียต่อสังคม (safety, security, discrimination, surveillance, deception, environment, human rights, bias)
- Broader impacts section ไม่บังคับ แต่ต้องสื่อสาร consequences ที่รู้หรือคาดได้อย่างโปร่งใส (ผ่าน checklist หรือ section แยก) และส่วนที่อยู่ในเนื้อหาหลักนับรวมใน 9 หน้า
- Safeguards สำหรับโมเดลหรือข้อมูลที่เสี่ยงต่อการนำไปใช้ในทางที่ผิด

## 5. Paper Checklist → ผู้รับผิดชอบ

> รายการข้อด้านล่างอิงจาก checklist ใน template ของ NeurIPS ปี 2025 (Handbook 2026 ไม่ได้แจกแจงรายข้อ บอกเพียงว่าอยู่ใน template และครอบคลุม reproducibility, transparency, research ethics และ societal impact) **Paper Writer ต้องเปิด template 2026 และปรับตารางนี้ให้ตรงก่อน G6** การตอบ "No" มักไม่ใช่เหตุผลให้ถูกปฏิเสธ แต่ต้องมี justification ที่ซื่อตรง

| # | หัวข้อ | เจ้าของคำตอบ | หลักฐานที่ต้องชี้ |
|---|---|---|---|
| 1 | Claims (abstract/intro ตรงกับ contribution และผล) | Paper Writer + PI | Claim–Evidence Matrix |
| 2 | Limitations | Paper Writer + Data Scientist + Domain Expert | Limitations section |
| 3 | Theory assumptions & proofs | PI + ผู้ตรวจ proof | Appendix proofs |
| 4 | Experimental result reproducibility | Data Scientist | Reproducibility Package |
| 5 | Open access to data & code | Data Engineer + AI Engineer | Anonymized repo, dataset card |
| 6 | Experimental setting/details | Data Scientist | Experiment Design + appendix |
| 7 | Statistical significance | Data Scientist | Section 4.2 |
| 8 | Compute resources | AI Engineer | Compute ledger (Section 4.4) |
| 9 | Code of Ethics | PI + PM | Ethics review record |
| 10 | Broader impacts | PI + Domain Expert + Paper Writer | Impact statement |
| 11 | Safeguards | AI Engineer + PI | System/Model Card |
| 12 | Licenses for existing assets | Data Engineer + Researcher | Data Source Register |
| 13 | New assets (เอกสารประกอบ) | Data Engineer | Dataset Card / code docs |
| 14 | Crowdsourcing & human subjects | UX/UI Designer + Data Engineer | Protocol, ค่าตอบแทน, instructions |
| 15 | IRB / ethics approval | PM + PI | หนังสืออนุมัติหรือเหตุผลที่ไม่ต้องขอ |
| 16 | LLM usage declaration | AI Engineer + Paper Writer | Orchestration log (ส่วนที่เป็นวิธีการ) |

## 6. Internal Mock Review (ก่อน G6 และ G7)

ก่อนปิด G6 ต้องมี **mock review** ตามแบบฟอร์มของ NeurIPS อย่างน้อย 2 ฉบับ จากบทบาทที่ไม่ได้เขียนส่วนนั้น (แนะนำ PI และ Researcher หรือ Domain Expert):
- ให้คะแนนและเหตุผลรายมิติ: Quality, Clarity, Significance, Originality ตามเกณฑ์ของ contribution type ที่เลือก
- ระบุ weaknesses 3 ข้อแรกที่ reviewer น่าจะเขียน และคำถามที่จะถามช่วง rebuttal
- Paper Writer ตอบทุกข้อด้วย (a) หลักฐานที่มีแล้ว (b) Strengthening Proposal หรือ (c) ข้อความใน Limitations
- เตรียม **rebuttal kit** ล่วงหน้า: ผลทดลองเพิ่มที่รันได้เร็ว และตารางที่ reviewer น่าจะขอ

## 7. ข้อห้ามที่เพิ่มขึ้นสำหรับทีม Multi-Agent

- Agents เป็นผู้แต่งไม่ได้ ผู้แต่งมนุษย์ต้องตรวจและรับผิดชอบทุกประโยค ทุก figure และทุก reference
- ทุก citation ต้องผ่าน Citation Check ของ Researcher (Handbook ระบุเรื่อง hallucinated citations ไว้ชัด)
- ห้ามใส่ข้อความซ่อน (hidden text), prompt injection หรือเนื้อหาที่มุ่งเป้า reviewer ที่ใช้ LLM ในไฟล์ใด ๆ ที่ส่ง
- บันทึกว่า agent ใดสร้างส่วนใด เพื่อให้ผู้แต่งตอบข้อ LLM usage ได้อย่างถูกต้อง
