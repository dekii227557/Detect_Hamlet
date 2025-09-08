🛣️ Sprint-01 (1 Tuần) — MVP “No-Helmet + ALPR”

Mục tiêu tuần: Phát hiện người đi xe máy không đội mũ bảo hiểm và đọc biển số từ video/RTSP; xuất video overlay + gói bằng chứng (ảnh + JSON).
Teamsize: 5 người (A, B, C, D, E).
Timezone: Asia/Bangkok (UTC+07:00).
Kết thúc sprint: Demo chạy end-to-end trên 1–2 video mẫu + báo cáo KPI.

0) Chuẩn KPI & Tiêu chí hoàn thành (DoD)

Helmet (no-helmet): Precision ≥ 0.85, Recall ≥ 0.75 (tập test nội bộ).

ALPR: Exact-match ≥ 70% trên khung ảnh đủ rõ (≥100×30 px).

Hiệu năng: ≥ 15 FPS (GPU phổ thông) / ≥ 5 FPS (CPU) ở 720p–1080p.

Output:

video_overlay.mp4 (bbox/label/plate).

evidence/ chứa frame.jpg, rider_crop.jpg, plate_crop.jpg, meta.json.

1) Vai trò & phạm vi công việc
Người	Vai trò	Phạm vi chính
A	Leader/PM	Charter, KPI, phân việc, review PR, quyết định kỹ thuật, tích hợp cuối
B	Data Lead	Trích khung, gán nhãn (CVAT/Label Studio), guideline, QA, chia train/val/test
C	CV Eng – Helmet	Detector person/motorcycle/helmet, pairing rider-xe, logic head-region
D	CV Eng – ALPR	Detector license_plate, tiền xử lý, OCR (PaddleOCR/EasyOCR), hậu xử lý
E	MLOps/Backend	Repo, Docker/venv, scripts train/infer, overlay, evidence, demo UI (Streamlit/FastAPI)
2) Lịch họp & nhịp điều phối

Daily Standup 10:00 (15’) — Hôm qua/Hôm nay/Blockers.

Checkpoint 14:30 (5–10’/người) — Ra quyết định nhanh.

Sync 17:30 (5’) — Chốt commit/PR trọng yếu.

Ngày 3 — Error Clinic 15:00 (30’).

Ngày 4 — KPI Review 16:00.

Ngày 6 — Dry-run Demo 15:00.

3) Kế hoạch theo NGÀY & theo NGƯỜI
📆 Ngày 1 — Nền tảng & Khởi tạo

A (Leader)

 Soạn Project Charter (1 trang): mục tiêu, KPI, phạm vi, rủi ro chính.

 Tạo Decision Log & thông báo nhịp họp.

 Chốt lớp nhãn: person, motorcycle, helmet, license_plate.

 Chốt I/O contracts (detector output, evidence JSON).

B (Data)

 Chuẩn bị 1–2h video đa bối cảnh (ngày/đêm/mưa/ngược sáng).

 Viết Guideline gán nhãn (1–2 trang) (mũ thật vs nón thời trang, hoodie…).

 Setup dự án trong CVAT/Label Studio, định danh class.

C (Helmet)

 Lấy YOLO (n/s) pretrained; cấu hình dataset.yaml.

 Chuẩn bị augment (mosaic, brightness/contrast, motion blur).

D (ALPR)

 Chọn OCR baseline (PaddleOCR khuyến nghị).

 Tạo pipeline: plate-detector → crop → preproc (gray/CLAHE) → OCR.

E (MLOps)

 Dựng repo & Docker/venv; requirements.txt.

 Khởi tạo cấu trúc thư mục (xem §6).

 Script frame-extractor & infer stub (ghi JSON kết quả).

📆 Ngày 2 — Dữ liệu & Baseline

A

 Kiểm guideline, chốt Eval Protocol (cách đo Precision/Recall/Exact-match).

 Lấy eval set tạm: ~150 khung chưa dùng để train.

B

 Trích & gán nhãn 1,000 khung (ưu tiên cận cảnh rider/plate).

 QA 5% mẫu (double annotate) → sửa lệch guideline.

C

 Fine-tune detector (person/motorcycle/helmet) trên ~800 khung đầu.

 Báo cáo mAP50/95; lưu weights-v0.

D

 Fine-tune detector license_plate trên ~600 khung đã nhãn.

 Tích hợp OCR → in ra 10 mẫu kết quả minh họa.

E

 Hoàn thiện batch infer cho 2 model; log JSON: cls, conf, bbox.

📆 Ngày 3 — Logic vi phạm & Gom pipeline

A

 Chốt helmet logic: head-region = top-40% bbox person.

 Tổ chức Error Clinic: xem 100 khung lỗi → tạo action items.

B

 Gán thêm 600 khung khó (đêm/mưa/che khuất/ngược sáng).

 Cập nhật train/val/test split minh bạch.

C

 Pairing rider–motorcycle (IoU + gần tâm).

 Kiểm tra “no-helmet” dựa head-region; thống kê lỗi (mũ nửa đầu, kính…).

D

 Tiền xử lý biển số: binarize, sharpen, rotate (0/±5°).

 Hậu xử lý regex format VN (lọc ký tự lạ, chuẩn hóa).

E

 Ghép pipeline end-to-end: no-helmet → plate-detector → OCR.

 Lưu evidence pack (frame/crops/meta.json).

📆 Ngày 4 — Đánh giá giữa kỳ & Tracking nhẹ

A

 Chạy Eval set: báo Precision/Recall (vi phạm) & ALPR exact-match.

 Chốt ngưỡng conf/NMS cho 2 ca (ngày/đêm).

B

 Bổ sung nhãn theo lỗi điển hình vừa phát hiện (hard negatives).

C

 Tuning ngưỡng; thử head-classifier (nếu kịp) trên crop đầu.

D

 Đo accuracy OCR theo per-char + per-plate; log case mờ/nhỏ.

E

 Tích hợp tracking nhẹ (ByteTrack/StrongSORT optional)
→ chọn khung “đẹp nhất” để OCR; xuất video overlay.

📆 Ngày 5 — Vòng cải tiến cuối & Code Freeze

A

 Code freeze 18:00; kiểm repro từ README trên máy sạch.

B

 Label bổ sung chỉ nhắm mẫu lỗi quan trọng (focus labeling).

C/D

 Retrain nhanh (5–8 epoch) trên tập bổ sung → weights-v1.

 Cập nhật metric & so sánh v0 vs v1.

E

 Thêm rate limiter & dedupe (không spam 1 rider).

 Chuẩn hóa outputs/ theo date-time.

📆 Ngày 6 — Đóng gói & Demo

A

 Viết báo cáo 1 trang KPI + known issues + khuyến nghị.

B

 Thống kê dữ liệu: tổng khung, phân bổ ngày/đêm, tỉ lệ khó.

C/D

 Model Cards (dữ liệu, huấn luyện, metric, caveats).

E

 App demo (Streamlit/FastAPI): upload video/RTSP → hiển thị overlay + export evidence.zip.

 Soạn script demo kịch bản (đường đi nước bước).

📆 Ngày 7 — Tổng duyệt & Bàn giao

A

 Tổng duyệt & ghi hình demo (nếu cần); lập plan tuần 2 (đèn đỏ).

 Checklist bàn giao.

All

 Test chéo; đóng các issue còn mở/hạ rủi ro.

4) Backlog chính theo người (có thể tạo thành GitHub Issues)
A — Leader/PM

 charter: Project Charter + KPI (1 trang).

 eval-protocol: định nghĩa cách đo & tập test.

 decision-log: file log quyết định kỹ thuật.

 Lịch họp & nhịp review; SLA review PR ≤ 6h.

B — Data

 data-guideline: file hướng dẫn gán nhãn có hình minh họa.

 extract-frames: script trích khung theo fps động (tránh trùng).

 labeling-run-1: 1,000 khung ngày 1–2; QA-5%.

 hard-negatives: gán nhãn khung đêm/mưa/che khuất.

 split-dataset: train/val/test minh bạch + stats.

C — Helmet

 helmet-baseline: train YOLO (n/s) + mAP report.

 pairing-logic: IoU + proximity; unit test tối thiểu.

 head-region-check: top-40% bbox person; kiểm no-helmet; tham số hóa.

D — ALPR

 plate-detector-baseline: train model + mAP report.

 plate-preproc: gray/CLAHE/rotate; so sánh OCR.

 vn-regex-postproc: regex + mapping O/0, I/1; per-char stats.

E — MLOps/Backend

 repo-setup: Docker/venv, requirements.txt, Makefile (nếu có).

 infer-pipeline: chạy video → JSON → overlay → evidence pack.

 ui-demo: trang upload + hiển thị + export zip.

 logging/metrics: chuẩn log; seed reproducible.

5) Định nghĩa Evidence JSON (schema mẫu)
{
  "video_id": "cam01_2025-09-08_1100",
  "frame": 1250,
  "timestamp": "2025-09-08T11:05:23+07:00",
  "rider_id": "trk_17",
  "violation": "no_helmet",
  "plate_text": "29A-12345",
  "plate_conf": 0.86,
  "bboxes": {
    "person": [x1, y1, x2, y2],
    "motorcycle": [x1, y1, x2, y2],
    "helmet": null,
    "plate": [x1, y1, x2, y2]
  },
  "assets": {
    "frame_path": "outputs/20250908_110523/frames/frame_1250.jpg",
    "rider_crop": "outputs/20250908_110523/crops/rider_trk_17.jpg",
    "plate_crop": "outputs/20250908_110523/crops/plate_trk_17.jpg"
  }
}

6) Cấu trúc thư mục khởi tạo
project/
├─ configs/
├─ data/
│  ├─ raw/              # video/rtsp dump
│  ├─ frames/           # trích khung
│  └─ labels/           # YOLO txt/json (CVAT export)
├─ models/              # weights, checkpoints
├─ notebooks/
├─ scripts/
│  ├─ extract_frames.py
│  ├─ train_helmet.py
│  ├─ train_plate.py
│  └─ infer_video.py
├─ src/
│  ├─ detectors/
│  ├─ tracking/
│  ├─ helmet_logic/
│  ├─ alpr/
│  └─ utils/
├─ ui/                  # streamlit/fastapi
├─ outputs/
│  └─ YYYYMMDD_HHMMSS/  # frames, crops, results.json, video_overlay.mp4
├─ docs/
│  ├─ charter.md
│  ├─ eval_protocol.md
│  └─ data_labeling_guideline.md
└─ README.md

7) Tiêu chuẩn DoR/DoD & Nhãn GitHub

Definition of Ready (DoR)

 Mô tả rõ mục tiêu & đầu vào/đầu ra

 Accept/Reject criteria & cách test

 Assignee + due date

Definition of Done (DoD)

 Chạy được trên máy sạch theo README

 Log/metrics kèm theo

 Không hard-code đường dẫn

 Ảnh/GIF minh họa ở PR

Labels: data, helmet, alpr, infra, bug, hotfix, eval, demo, docs.

8) Templates hữu ích cho GitHub
.github/PULL_REQUEST_TEMPLATE.md
## Mục tiêu
- (Tóm tắt thay đổi, liên quan issue #ID)

## Cách test
1. Lệnh chạy:


python scripts/infer_video.py --video data/raw/sample.mp4 --out outputs/test_run

2. Kỳ vọng: sinh `results.json`, `video_overlay.mp4`, crops.

## Ảnh/GIF minh họa
- (đính kèm)

## Checklist
- [ ] Không hard-code đường dẫn
- [ ] Có log/metrics cơ bản
- [ ] Cập nhật README/docs nếu cần

.github/ISSUE_TEMPLATE/task.md
---
name: "Task"
about: "Công việc nhỏ trong sprint"
labels: ["task"]
---

## Mô tả
(ngắn gọn)

## Đầu vào / Đầu ra
- Input:
- Output:

## Acceptance Criteria
- [ ]

## Cách test
- Lệnh:
- Kỳ vọng:

.github/ISSUE_TEMPLATE/bug_report.md
---
name: "Bug report"
about: "Báo lỗi"
labels: ["bug"]
---

## Mô tả lỗi
(điều gì sai)

## Cách tái hiện
1. Lệnh/Thao tác:
2. Kết quả thực tế:
3. Kỳ vọng:

## Log / Ảnh màn hình
(đính kèm)

9) Lệnh nhanh (gợi ý cho E đưa vào README)
# Tạo venv
python -m venv .venv && source .venv/bin/activate  # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt

# Train Helmet
python scripts/train_helmet.py --data configs/helmet.yaml --epochs 30 --img 1280 --batch 8

# Train Plate
python scripts/train_plate.py --data configs/plate.yaml --epochs 30 --img 1280 --batch 8

# Inference Video (end-to-end)
python scripts/infer_video.py --video data/raw/sample.mp4 --out outputs/$(date +%Y%m%d_%H%M%S)

10) Rủi ro chính & phương án trong tuần

Plate nhỏ/mờ → tracking chọn khung đẹp nhất, upscale crop, CLAHE.

Mũ nửa đầu/hoodie → tăng mẫu khó + thử head-classifier nhẹ.

Đêm/ngược sáng → augment brightness/contrast; ngưỡng riêng ca đêm.

Hiệu năng yếu → dùng YOLO n/s, FP16, giảm kích thước input, tắt tracking.

✅ Checklist bàn giao cuối sprint
 Weights (helmet/plate) + configs + seed
 Script infer + demo UI + README
 Tập test + báo cáo KPI
 Evidence mẫu (ảnh + JSON + overlay)
 Kế hoạch tuần 2 (đèn đỏ, đa camera, dashboard)