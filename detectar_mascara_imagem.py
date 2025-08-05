from ultralytics import YOLO
import cv2
import os

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

def detectar_mascara_imagem(caminho_imagem):
    """
    Função para detectar máscaras em uma imagem específica
    """
    if not os.path.exists(caminho_imagem):
        print(f"❌ Erro: Imagem não encontrada: {caminho_imagem}")
        return
    
    # Carregar imagem
    frame = cv2.imread(caminho_imagem)
    if frame is None:
        print(f"❌ Erro: Não foi possível carregar a imagem: {caminho_imagem}")
        return
    
    print(f"🔍 Analisando imagem: {os.path.basename(caminho_imagem)}")
    
    # Fazer predição
    results = model(frame)
    
    deteccoes_encontradas = False
    
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
                
                # Processar apenas se confiança > 0.5
                if conf > 0.5:
                    deteccoes_encontradas = True
                    cor = cores_classes[cls]
                    
                    # Desenhar retângulo
                    cv2.rectangle(frame, (x1, y1), (x2, y2), cor, 3)
                    
                    # Preparar texto
                    mensagem = mensagens_mascara[cls]
                    texto_conf = f"Confiança: {conf:.2f}"
                    
                    # Calcular tamanho do texto para ajustar fundo
                    (w_msg, h_msg), _ = cv2.getTextSize(mensagem, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)
                    (w_conf, h_conf), _ = cv2.getTextSize(texto_conf, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
                    
                    # Desenhar fundo para o texto
                    cv2.rectangle(frame, (x1, y1-70), (x1+max(w_msg, w_conf)+10, y1), cor, -1)
                    
                    # Desenhar texto da mensagem
                    cv2.putText(frame, mensagem, (x1+5, y1-40), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                    
                    # Desenhar confiança
                    cv2.putText(frame, texto_conf, (x1+5, y1-15), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
                    
                    # Imprimir resultado no console
                    print(f"  👤 Pessoa detectada: {mensagem} (Confiança: {conf:.2f})")
    
    if not deteccoes_encontradas:
        print("  ℹ️ Nenhuma pessoa detectada na imagem")
        # Adicionar texto na imagem
        cv2.putText(frame, "Nenhuma pessoa detectada", (50, 50), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    # Mostrar resultado
    cv2.imshow(f'Detecção de Máscaras - {os.path.basename(caminho_imagem)}', frame)
    print("  💡 Pressione qualquer tecla para fechar a janela")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def detectar_mascara_pasta(caminho_pasta):
    """
    Função para detectar máscaras em todas as imagens de uma pasta
    """
    if not os.path.exists(caminho_pasta):
        print(f"❌ Erro: Pasta não encontrada: {caminho_pasta}")
        return
    
    # Extensões de imagem suportadas
    extensoes_suportadas = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif')
    
    # Listar todas as imagens na pasta
    imagens = [f for f in os.listdir(caminho_pasta) 
               if f.lower().endswith(extensoes_suportadas)]
    
    if not imagens:
        print(f"❌ Nenhuma imagem encontrada na pasta: {caminho_pasta}")
        return
    
    print(f"📁 Processando {len(imagens)} imagens da pasta: {caminho_pasta}")
    print("=" * 60)
    
    for i, nome_imagem in enumerate(imagens, 1):
        caminho_completo = os.path.join(caminho_pasta, nome_imagem)
        print(f"\n[{i}/{len(imagens)}]")
        detectar_mascara_imagem(caminho_completo)

if __name__ == "__main__":
    print("🎭 Sistema de Detecção de Máscaras em Imagens")
    print("=" * 50)
    
    while True:
        print("\n📋 Escolha uma opção:")
        print("1. Detectar em uma imagem específica")
        print("2. Detectar em todas as imagens de uma pasta")
        print("3. Testar com imagens do dataset (pasta test)")
        print("4. Sair")
        
        opcao = input("\n👉 Digite sua opção (1-4): ").strip()
        
        if opcao == '1':
            caminho = input("📸 Digite o caminho da imagem: ").strip()
            detectar_mascara_imagem(caminho)
            
        elif opcao == '2':
            caminho = input("📁 Digite o caminho da pasta: ").strip()
            detectar_mascara_pasta(caminho)
            
        elif opcao == '3':
            pasta_test = r"c:\Users\Admin\Documents\GitHub\trabalhoFacul\test\images"
            print(f"🧪 Testando com imagens do dataset...")
            detectar_mascara_pasta(pasta_test)
            
        elif opcao == '4':
            print("👋 Saindo do programa...")
            break
            
        else:
            print("❌ Opção inválida! Tente novamente.")
