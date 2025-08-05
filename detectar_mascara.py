from ultralytics import YOLO
import cv2
import numpy as np

# Caminho correto para o modelo treinado
model = YOLO(r"c:\Users\Admin\Documents\GitHub\trabalhoFacul\runs\detect\train\weights\best.pt")

# Dicionário com as mensagens para cada classe
mensagens_mascara = {
    0: "⚠️ MÁSCARA INCORRETA - Ajuste sua máscara!",
    1: "✅ ESTÁ USANDO MÁSCARA - Muito bem!",
    2: "❌ NÃO ESTÁ USANDO MÁSCARA - Coloque sua máscara!"
}

# Cores para cada classe (BGR)
cores_classes = {
    0: (0, 165, 255),    # Laranja para máscara incorreta
    1: (0, 255, 0),      # Verde para com máscara
    2: (0, 0, 255)       # Vermelho para sem máscara
}

def detectar_mascara_webcam():
    """
    Função para detectar máscaras na webcam com mensagens personalizadas
    """
    print("🔍 Procurando câmeras disponíveis...")
    
    # Tentar diferentes índices e backends
    backends_para_testar = [
        (cv2.CAP_DSHOW, "DirectShow (Windows)"),
        (cv2.CAP_MSMF, "Media Foundation (Windows)"),
        (cv2.CAP_ANY, "Qualquer backend")
    ]
    
    cap = None
    camera_encontrada = False
    
    # Primeiro, tentar diferentes índices com backend padrão
    for camera_index in range(5):
        print(f"  Testando câmera índice {camera_index}...")
        test_cap = cv2.VideoCapture(camera_index)
        if test_cap.isOpened():
            # Verificar se realmente consegue ler frames
            ret, frame = test_cap.read()
            if ret and frame is not None:
                print(f"  ✅ Câmera encontrada no índice {camera_index}!")
                cap = test_cap
                camera_encontrada = True
                break
        test_cap.release()
    
    # Se não encontrou, tentar backends específicos
    if not camera_encontrada:
        print("🔄 Tentando backends específicos...")
        for backend, nome_backend in backends_para_testar:
            print(f"  Testando {nome_backend}...")
            for camera_index in range(3):
                try:
                    test_cap = cv2.VideoCapture(camera_index, backend)
                    if test_cap.isOpened():
                        ret, frame = test_cap.read()
                        if ret and frame is not None:
                            print(f"  ✅ Câmera encontrada com {nome_backend} no índice {camera_index}!")
                            cap = test_cap
                            camera_encontrada = True
                            break
                    test_cap.release()
                except Exception as e:
                    continue
            if camera_encontrada:
                break
    
    if not camera_encontrada:
        print("❌ ERRO: Nenhuma câmera foi encontrada!")
        print("\n🔧 Possíveis soluções:")
        print("   1. Verifique se a webcam está conectada")
        print("   2. Certifique-se de que a câmera não está sendo usada por outro programa")
        print("   3. Verifique as permissões de câmera no Windows")
        print("   4. Tente reiniciar o computador")
        print("   5. Teste com outros programas (como a aplicação Câmera do Windows)")
        return
    
    print("🎥 Câmera inicializada com sucesso!")
    print("📋 Pressione 'q' para sair")
    print("📋 Pressione 's' para salvar screenshot")
    
    screenshot_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Erro ao capturar frame da câmera!")
            break
        
        # Fazer predição
        results = model(frame)
        
        # Processar resultados
        for r in results:
            boxes = r.boxes
            if boxes is not None:
                for box in boxes:
                    # Obter coordenadas da caixa
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
                    
                    # Obter classe e confiança
                    cls = int(box.cls[0].cpu().numpy())
                    conf = float(box.conf[0].cpu().numpy())
                    
                    # Desenhar caixa apenas se confiança > 0.5
                    if conf > 0.5:
                        cor = cores_classes[cls]
                        
                        # Desenhar retângulo
                        cv2.rectangle(frame, (x1, y1), (x2, y2), cor, 2)
                        
                        # Preparar texto
                        mensagem = mensagens_mascara[cls]
                        texto_conf = f"Confiança: {conf:.2f}"
                        
                        # Desenhar fundo para o texto
                        cv2.rectangle(frame, (x1, y1-60), (x1+400, y1), cor, -1)
                        
                        # Desenhar texto da mensagem
                        cv2.putText(frame, mensagem, (x1+5, y1-35), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                        
                        # Desenhar confiança
                        cv2.putText(frame, texto_conf, (x1+5, y1-10), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Adicionar instruções na tela
        cv2.putText(frame, "Pressione 'q' para sair | 's' para screenshot", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Mostrar frame
        cv2.imshow('Detecção de Máscaras - Trabalho Faculdade', frame)
        
        # Verificar teclas pressionadas
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            screenshot_count += 1
            filename = f"screenshot_mascara_{screenshot_count}.jpg"
            cv2.imwrite(filename, frame)
            print(f"📸 Screenshot salvo: {filename}")
    
    # Limpar recursos
    cap.release()
    cv2.destroyAllWindows()
    print("👋 Câmera desconectada com sucesso!")

if __name__ == "__main__":
    print("🎭 Sistema de Detecção de Máscaras")
    print("=" * 40)
    print("Classes detectadas:")
    for i, msg in mensagens_mascara.items():
        print(f"  {i}: {msg}")
    print("=" * 40)
    
    detectar_mascara_webcam()
