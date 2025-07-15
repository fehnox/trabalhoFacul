from ultralytics import YOLO

# Caminho correto para o modelo treinado
model = YOLO(r"C:\Users\Pichau\Desktop\Faculdade Materias\projetos\Mask-Detection-YOLOv8.v1i.yolov8\runs\detect\train\weights\best.pt")

# Detectar com a webcam
model.predict(source=0, show=True)
