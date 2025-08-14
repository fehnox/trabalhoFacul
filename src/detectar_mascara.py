import os
import time
import cv2
from ultralytics import YOLO
from .config import CONFIDENCIA_PADRAO, IMG_SIZE, MODELO_PADRAO, JANELA_TITULO


def carregar_modelo():
    if os.path.exists(MODELO_PADRAO):
        return YOLO(MODELO_PADRAO)
    return YOLO("yolov8n.pt")


def main():
    model = carregar_modelo()
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not cap.isOpened():
        print("❌ Não foi possível abrir a câmera (0).")
        return

    print("✅ Modelo carregado.")
    print(f"🧠 Classes: {getattr(model, 'names', {})}")

    last_save = 0.0
    while True:
        ok, frame = cap.read()
        if not ok:
            print("❌ Falha ao capturar frame da câmera.")
            break

        results = model.predict(
            frame,
            imgsz=IMG_SIZE,
            conf=CONFIDENCIA_PADRAO,
            verbose=False
        )
        annotated = results[0].plot()
        cv2.imshow(JANELA_TITULO, annotated)

        key = cv2.waitKey(1) & 0xFF
        if key in (ord("q"), 27):  # q ou ESC
            break
        if key == ord("s"):  # salvar screenshot (rate-limit 1s)
            now = time.time()
            if now - last_save > 1.0:
                os.makedirs("outputs/screenshots", exist_ok=True)
                caminho = os.path.join("outputs/screenshots", f"screenshot_{int(now)}.png")
                cv2.imwrite(caminho, annotated)
                print(f"💾 Screenshot salvo em: {caminho}")
                last_save = now

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()