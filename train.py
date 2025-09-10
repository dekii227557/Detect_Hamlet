from ultralytics import YOLO

model = YOLO("yolov8n.pt")

model.train(
    data="archive/data.yaml",
    epochs=30,
    imgsz=640,
    device="cpu"   # ⚡ quan trọng
)