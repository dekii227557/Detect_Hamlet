from ultralytics import YOLO
import cv2
import easyocr
import os

# Load model đã train
model = YOLO("runs/detect/train5/weights/best.pt")

# Load OCR
reader = easyocr.Reader(['en'])

# Ảnh test
img_path = "archive/test/images/Clip31_new_0.jpg"
results = model.predict(img_path, conf=0.25, save=True)

# Đọc ảnh gốc
img = cv2.imread(img_path)

# Duyệt qua bbox của YOLO
for r in results:
    for box in r.boxes:
        # Lấy tọa độ bounding box
        x1, y1, x2, y2 = map(int, box.xyxy[0])

        # Crop vùng biển số
        plate_crop = img[y1:y2, x1:x2]

        # ===== Tiền xử lý ảnh =====
        gray = cv2.cvtColor(plate_crop, cv2.COLOR_BGR2GRAY)
        # phóng to ảnh cho dễ đọc
        gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        # làm nét và nhị phân ảnh
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # OCR trên vùng crop sau tiền xử lý
        ocr_result = reader.readtext(thresh)

        if ocr_result:
            text = " ".join([res[1] for res in ocr_result])
            print("Biển số nhận được:", text)

            # Vẽ lên ảnh
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(img, text, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

# Lưu ảnh kết quả
os.makedirs("runs/final_output", exist_ok=True)
cv2.imwrite("runs/final_output/result.jpg", img)
print("Ảnh kết quả lưu ở: runs/final_output/result.jpg")