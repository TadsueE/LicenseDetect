from ultralytics import YOLO

model = YOLO('LicensePlateDetector.pt')
results = model(source="0", show=True, save_crop=True)