from ultralytics import YOLO

# Caminho para o arquivo data.yaml do seu dataset
caminho_data = r"C:\Users\Pichau\Desktop\Faculdade Materias\projetos\Mask-Detection-YOLOv8.v1i.yolov8\data.yaml"

# Criação do modelo (YOLOv8n = leve, ideal para começar)
modelo = YOLO("yolov8n.yaml")

# Início do treinamento
modelo.train(
    data=caminho_data,
    epochs=50,
    imgsz=640,
    batch=8,
    device="cpu"  # Coloque "cpu" pois sua máquina não possui CUDA/GPU
)
