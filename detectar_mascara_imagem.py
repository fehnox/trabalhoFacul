from ultralytics import YOLO
import cv2
import os
import time
from datetime import datetime
import json

# Caminho correto para o modelo treinado
try:
    model = YOLO(r"c:\Users\Admin\Documents\GitHub\trabalhoFacul\runs\detect\train\weights\best.pt")
    print("✅ Modelo carregado com sucesso!")
except Exception as e:
    print(f"❌ Erro ao carregar modelo: {e}")
    print("🔧 Verifique se o arquivo 'best.pt' existe em 'runs/detect/train/weights/'")
    exit(1)

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

# Configurações globais
CONFIANCA_MINIMA = 0.5
TAMANHO_FONTE_PRINCIPAL = 0.8
TAMANHO_FONTE_SECUNDARIA = 0.6
ESPESSURA_LINHA = 3

def redimensionar_imagem(imagem, max_width=1200, max_height=800):
    """
    Redimensiona imagem mantendo proporção se ela for muito grande
    """
    height, width = imagem.shape[:2]
    
    if width > max_width or height > max_height:
        # Calcular o fator de escala
        scale_w = max_width / width
        scale_h = max_height / height
        scale = min(scale_w, scale_h)
        
        # Novo tamanho
        new_width = int(width * scale)
        new_height = int(height * scale)
        
        # Redimensionar
        imagem_redimensionada = cv2.resize(imagem, (new_width, new_height))
        print(f"  📏 Imagem redimensionada de {width}x{height} para {new_width}x{new_height}")
        return imagem_redimensionada, scale
    
    return imagem, 1.0

def detectar_mascara_imagem(caminho_imagem, salvar_automatico=False, mostrar_imagem=True):
    """
    Função para detectar máscaras em uma imagem específica
    
    Args:
        caminho_imagem (str): Caminho para a imagem
        salvar_automatico (bool): Se True, salva automaticamente a imagem anotada
        mostrar_imagem (bool): Se True, exibe a imagem na tela
    
    Returns:
        dict: Resultado da detecção com estatísticas
    """
    if not os.path.exists(caminho_imagem):
        print(f"❌ Erro: Imagem não encontrada: {caminho_imagem}")
        return None

    # Carregar imagem
    frame_original = cv2.imread(caminho_imagem)
    if frame_original is None:
        print(f"❌ Erro: Não foi possível carregar a imagem: {caminho_imagem}")
        return None

    print(f"🔍 Analisando imagem: {os.path.basename(caminho_imagem)}")
    
    # Redimensionar se necessário
    frame, escala = redimensionar_imagem(frame_original.copy())
    
    # Medir tempo de processamento
    inicio = time.time()

    # Fazer predição
    try:
        results = model(frame)
    except Exception as e:
        print(f"❌ Erro ao rodar o modelo: {e}")
        return None

    tempo_processamento = time.time() - inicio
    
    deteccoes_encontradas = False
    estatisticas = {
        'total_pessoas': 0,
        'com_mascara': 0,
        'sem_mascara': 0,
        'mascara_incorreta': 0,
        'tempo_processamento': tempo_processamento,
        'deteccoes': []
    }

    # Processar resultados
    for r in results:
        boxes = getattr(r, 'boxes', None)
        if boxes is not None:
            for box in boxes:
                # Obter coordenadas da caixa (ajustar para escala original se necessário)
                coords = box.xyxy[0].cpu().numpy().astype(int)
                if escala != 1.0:
                    coords = (coords / escala).astype(int)
                x1, y1, x2, y2 = coords

                # Obter classe e confiança
                cls = int(box.cls[0].cpu().numpy())
                conf = float(box.conf[0].cpu().numpy())

                # Processar apenas se confiança > threshold
                if conf > CONFIANCA_MINIMA:
                    deteccoes_encontradas = True
                    estatisticas['total_pessoas'] += 1
                    
                    # Contar por categoria
                    if cls == 0:
                        estatisticas['mascara_incorreta'] += 1
                    elif cls == 1:
                        estatisticas['com_mascara'] += 1
                    elif cls == 2:
                        estatisticas['sem_mascara'] += 1
                    
                    # Armazenar detecção
                    estatisticas['deteccoes'].append({
                        'classe': cls,
                        'confianca': conf,
                        'coordenadas': [x1, y1, x2, y2]
                    })
                    
                    cor = cores_classes.get(cls, (255, 255, 255))

                    # Desenhar no frame original
                    cv2.rectangle(frame_original, (x1, y1), (x2, y2), cor, ESPESSURA_LINHA)

                    # Preparar texto
                    mensagem = mensagens_mascara.get(cls, f"Classe {cls}")
                    texto_conf = f"Confiança: {conf:.1%}"

                    # Calcular tamanho do texto para ajustar fundo
                    (w_msg, h_msg), _ = cv2.getTextSize(mensagem, cv2.FONT_HERSHEY_SIMPLEX, TAMANHO_FONTE_PRINCIPAL, 2)
                    (w_conf, h_conf), _ = cv2.getTextSize(texto_conf, cv2.FONT_HERSHEY_SIMPLEX, TAMANHO_FONTE_SECUNDARIA, 1)

                    # Ajustar posição do texto se estiver muito no topo
                    texto_y = max(y1, 70)
                    
                    # Desenhar fundo para o texto
                    cv2.rectangle(frame_original, (x1, texto_y-70), (x1+max(w_msg, w_conf)+20, texto_y), cor, -1)

                    # Desenhar texto da mensagem
                    cv2.putText(frame_original, mensagem, (x1+10, texto_y-40),
                                cv2.FONT_HERSHEY_SIMPLEX, TAMANHO_FONTE_PRINCIPAL, (255, 255, 255), 2)

                    # Desenhar confiança
                    cv2.putText(frame_original, texto_conf, (x1+10, texto_y-15),
                                cv2.FONT_HERSHEY_SIMPLEX, TAMANHO_FONTE_SECUNDARIA, (255, 255, 255), 1)

                    # Imprimir resultado no console
                    print(f"  👤 Pessoa detectada: {mensagem} (Confiança: {conf:.1%})")

    # Adicionar informações de resumo na imagem
    if deteccoes_encontradas:
        resumo = f"Pessoas: {estatisticas['total_pessoas']} | Tempo: {tempo_processamento:.2f}s"
        cv2.putText(frame_original, resumo, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        print(f"  📊 Resumo: {estatisticas['total_pessoas']} pessoa(s) detectada(s) em {tempo_processamento:.2f}s")
    else:
        print("  ℹ️ Nenhuma pessoa detectada na imagem")
        # Adicionar texto na imagem
        cv2.putText(frame_original, "Nenhuma pessoa detectada", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Salvar automaticamente se solicitado
    if salvar_automatico:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_saida = f"anotada_{timestamp}_{os.path.basename(caminho_imagem)}"
        cv2.imwrite(nome_saida, frame_original)
        print(f"  💾 Imagem anotada salva automaticamente: {nome_saida}")

    # Mostrar resultado se solicitado
    if mostrar_imagem:
        # Redimensionar para exibição se muito grande
        frame_display, _ = redimensionar_imagem(frame_original.copy())
        
        cv2.imshow(f'Detecção de Máscaras - {os.path.basename(caminho_imagem)}', frame_display)
        print("  💡 Pressione 's' para salvar, 'ESC' para sair, ou qualquer tecla para continuar")
        
        key = cv2.waitKey(0)
        if key == ord('s'):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_saida = f"anotada_{timestamp}_{os.path.basename(caminho_imagem)}"
            cv2.imwrite(nome_saida, frame_original)
            print(f"  💾 Imagem anotada salva como: {nome_saida}")
        elif key == 27:  # ESC key
            cv2.destroyAllWindows()
            return estatisticas
        
        cv2.destroyAllWindows()
    
    return estatisticas

def detectar_mascara_pasta(caminho_pasta, salvar_todas=False):
    """
    Função para detectar máscaras em todas as imagens de uma pasta
    
    Args:
        caminho_pasta (str): Caminho da pasta com imagens
        salvar_todas (bool): Se True, salva todas as imagens anotadas automaticamente
    
    Returns:
        dict: Estatísticas consolidadas de toda a pasta
    """
    if not os.path.exists(caminho_pasta):
        print(f"❌ Erro: Pasta não encontrada: {caminho_pasta}")
        return None
    
    # Extensões de imagem suportadas
    extensoes_suportadas = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif')
    
    # Listar todas as imagens na pasta
    imagens = [f for f in os.listdir(caminho_pasta) 
               if f.lower().endswith(extensoes_suportadas)]
    
    if not imagens:
        print(f"❌ Nenhuma imagem encontrada na pasta: {caminho_pasta}")
        return None
    
    print(f"📁 Processando {len(imagens)} imagens da pasta: {caminho_pasta}")
    print("=" * 60)
    
    # Estatísticas consolidadas
    estatisticas_totais = {
        'total_imagens': len(imagens),
        'imagens_processadas': 0,
        'total_pessoas': 0,
        'com_mascara': 0,
        'sem_mascara': 0,
        'mascara_incorreta': 0,
        'tempo_total': 0,
        'imagens_sem_deteccao': 0,
        'detalhes_por_imagem': []
    }
    
    inicio_total = time.time()
    
    for i, nome_imagem in enumerate(imagens, 1):
        caminho_completo = os.path.join(caminho_pasta, nome_imagem)
        print(f"\n[{i}/{len(imagens)}] {nome_imagem}")
        
        # Processar imagem (não mostrar se estiver processando em lote)
        mostrar = not salvar_todas  # Só mostrar se não estiver salvando todas
        resultado = detectar_mascara_imagem(caminho_completo, 
                                          salvar_automatico=salvar_todas, 
                                          mostrar_imagem=mostrar)
        
        if resultado:
            estatisticas_totais['imagens_processadas'] += 1
            estatisticas_totais['total_pessoas'] += resultado['total_pessoas']
            estatisticas_totais['com_mascara'] += resultado['com_mascara']
            estatisticas_totais['sem_mascara'] += resultado['sem_mascara']
            estatisticas_totais['mascara_incorreta'] += resultado['mascara_incorreta']
            estatisticas_totais['tempo_total'] += resultado['tempo_processamento']
            
            if resultado['total_pessoas'] == 0:
                estatisticas_totais['imagens_sem_deteccao'] += 1
                
            estatisticas_totais['detalhes_por_imagem'].append({
                'nome': nome_imagem,
                'pessoas': resultado['total_pessoas'],
                'deteccoes': resultado['deteccoes']
            })
    
    tempo_total = time.time() - inicio_total
    
    # Exibir resumo final
    print(f"\n" + "="*60)
    print(f"📋 RESUMO FINAL - PASTA: {os.path.basename(caminho_pasta)}")
    print(f"="*60)
    print(f"🖼️ Imagens processadas: {estatisticas_totais['imagens_processadas']}/{estatisticas_totais['total_imagens']}")
    print(f"👥 Total de pessoas detectadas: {estatisticas_totais['total_pessoas']}")
    print(f"🚫 Imagens sem detecção: {estatisticas_totais['imagens_sem_deteccao']}")
    print(f"⏱️ Tempo total: {tempo_total:.2f}s")
    print(f"⚡ Tempo médio por imagem: {tempo_total/len(imagens):.2f}s")
    
    if estatisticas_totais['total_pessoas'] > 0:
        print(f"\n📊 DISTRIBUIÇÃO:")
        print(f"✅ Com máscara: {estatisticas_totais['com_mascara']} ({estatisticas_totais['com_mascara']/estatisticas_totais['total_pessoas']*100:.1f}%)")
        print(f"⚠️ Máscara incorreta: {estatisticas_totais['mascara_incorreta']} ({estatisticas_totais['mascara_incorreta']/estatisticas_totais['total_pessoas']*100:.1f}%)")
        print(f"❌ Sem máscara: {estatisticas_totais['sem_mascara']} ({estatisticas_totais['sem_mascara']/estatisticas_totais['total_pessoas']*100:.1f}%)")
        
        # Taxa de conformidade
        taxa_conformidade = (estatisticas_totais['com_mascara'] / estatisticas_totais['total_pessoas']) * 100
        print(f"\n🎯 Taxa de conformidade: {taxa_conformidade:.1f}%")
        
        if taxa_conformidade >= 80:
            print("🟢 Situação: EXCELENTE")
        elif taxa_conformidade >= 60:
            print("🟡 Situação: BOA")
        else:
            print("🔴 Situação: NECESSITA ATENÇÃO")
    
    # Salvar relatório da pasta
    if estatisticas_totais['imagens_processadas'] > 0:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_relatorio = f"relatorio_pasta_{timestamp}.json"
        
        with open(nome_relatorio, 'w', encoding='utf-8') as f:
            json.dump(estatisticas_totais, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 Relatório salvo: {nome_relatorio}")
    
    return estatisticas_totais

def configurar_sistema():
    """
    Permite configurar parâmetros do sistema
    """
    global CONFIANCA_MINIMA
    
    print("\n⚙️ CONFIGURAÇÕES DO SISTEMA")
    print("=" * 40)
    print(f"Confiança mínima atual: {CONFIANCA_MINIMA:.1%}")
    
    try:
        nova_confianca = float(input("Nova confiança mínima (0.1 a 0.9): "))
        if 0.1 <= nova_confianca <= 0.9:
            CONFIANCA_MINIMA = nova_confianca
            print(f"✅ Confiança atualizada para: {CONFIANCA_MINIMA:.1%}")
        else:
            print("❌ Valor inválido! Mantendo configuração atual.")
    except ValueError:
        print("❌ Entrada inválida! Mantendo configuração atual.")

if __name__ == "__main__":
    print("🎭 Sistema Avançado de Detecção de Máscaras em Imagens")
    print(f"🤖 Modelo: YOLOv8 | 🎯 Confiança mínima: {CONFIANCA_MINIMA:.1%}")
    print("=" * 60)

    while True:
        print("\n📋 MENU PRINCIPAL:")
        print("1. 📸 Detectar em uma imagem específica")
        print("2. 📁 Detectar em todas as imagens de uma pasta")
        print("3. 🧪 Testar com imagens do dataset (pasta test)")
        print("4. 📦 Processar pasta e salvar todas as imagens anotadas")
        print("5. ⚙️ Configurações do sistema")
        print("6. ℹ️ Ajuda e instruções")
        print("7. 🚪 Sair")

        opcao = input("\n👉 Digite sua opção (1-7): ").strip()

        if opcao == '1':
            caminho = input("📸 Digite o caminho da imagem: ").strip().strip('"')
            if caminho:
                detectar_mascara_imagem(caminho)

        elif opcao == '2':
            caminho = input("📁 Digite o caminho da pasta: ").strip().strip('"')
            if caminho:
                detectar_mascara_pasta(caminho)

        elif opcao == '3':
            pasta_test = r"c:\Users\Admin\Documents\GitHub\trabalhoFacul\test\images"
            print(f"🧪 Testando com imagens do dataset...")
            detectar_mascara_pasta(pasta_test)

        elif opcao == '4':
            caminho = input("� Digite o caminho da pasta para processamento em lote: ").strip().strip('"')
            if caminho:
                print("🔄 Processando todas as imagens e salvando automaticamente...")
                detectar_mascara_pasta(caminho, salvar_todas=True)

        elif opcao == '5':
            configurar_sistema()

        elif opcao == '6':
            print("\n" + "="*60)
            print("ℹ️ INSTRUÇÕES E AJUDA")
            print("="*60)
            print("📋 FORMATOS SUPORTADOS:")
            print("   • JPG, JPEG, PNG, BMP, TIFF")
            print("\n🎯 CLASSES DETECTADAS:")
            print("   • ✅ Verde: Pessoa usando máscara corretamente")
            print("   • ⚠️ Laranja: Máscara usada incorretamente")
            print("   • ❌ Vermelho: Pessoa sem máscara")
            print("\n⌨️ CONTROLES NA VISUALIZAÇÃO:")
            print("   • 's': Salvar imagem anotada")
            print("   • ESC: Sair da visualização")
            print("   • Qualquer tecla: Continuar para próxima imagem")
            print("\n🔧 CONFIGURAÇÕES:")
            print(f"   • Confiança mínima atual: {CONFIANCA_MINIMA:.1%}")
            print("   • Use a opção 5 para alterar configurações")
            print("\n📊 FUNCIONALIDADES:")
            print("   • Redimensionamento automático de imagens grandes")
            print("   • Medição de tempo de processamento")
            print("   • Estatísticas detalhadas por pasta")
            print("   • Relatórios em formato JSON")
            print("   • Processamento em lote com salvamento automático")
            print("\n❓ PROBLEMAS COMUNS:")
            print("   • Se nenhuma pessoa for detectada, verifique:")
            print("     - Qualidade da imagem")
            print("     - Iluminação adequada")
            print("     - Presença de rostos visíveis")
            print("   • Para ajustar sensibilidade, altere a confiança mínima")

        elif opcao == '7':
            print("👋 Saindo do sistema...")
            print("🎓 Obrigado por usar o Sistema de Detecção de Máscaras!")
            break

        else:
            print("❌ Opção inválida! Digite um número de 1 a 7.")
