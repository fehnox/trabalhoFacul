from ultralytics import YOLO
import cv2
import os
from datetime import datetime
import json

# Caminho correto para o modelo treinado
model = YOLO(r"c:\Users\Admin\Documents\GitHub\trabalhoFacul\runs\detect\train\weights\best.pt")

# Dicionário com as mensagens para cada classe
mensagens_mascara = {
    0: "Máscara Incorreta",
    1: "Está usando máscara",
    2: "Não está usando máscara"
}

def gerar_relatorio_deteccoes(caminho_pasta, salvar_relatorio=True):
    """
    Gera um relatório detalhado das detecções de máscaras em uma pasta
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
    
    print(f"📊 Gerando relatório para {len(imagens)} imagens...")
    print("=" * 60)
    
    # Estatísticas
    total_deteccoes = 0
    estatisticas = {
        0: {"nome": "Máscara Incorreta", "count": 0, "imagens": []},
        1: {"nome": "Está usando máscara", "count": 0, "imagens": []},
        2: {"nome": "Não está usando máscara", "count": 0, "imagens": []}
    }
    
    resultados_detalhados = []
    imagens_sem_deteccao = []
    
    for i, nome_imagem in enumerate(imagens, 1):
        caminho_completo = os.path.join(caminho_pasta, nome_imagem)
        
        # Mostrar progresso
        if i % 10 == 0:
            print(f"📈 Processando... {i}/{len(imagens)} imagens")
        
        # Carregar imagem
        frame = cv2.imread(caminho_completo)
        if frame is None:
            continue
        
        # Fazer predição
        results = model(frame)
        
        deteccoes_imagem = []
        
        # Processar resultados
        for r in results:
            boxes = r.boxes
            if boxes is not None:
                for box in boxes:
                    # Obter classe e confiança
                    cls = int(box.cls[0].cpu().numpy())
                    conf = float(box.conf[0].cpu().numpy())
                    
                    # Processar apenas se confiança > 0.5
                    if conf > 0.5:
                        total_deteccoes += 1
                        estatisticas[cls]["count"] += 1
                        estatisticas[cls]["imagens"].append(nome_imagem)
                        
                        deteccoes_imagem.append({
                            "classe": cls,
                            "mensagem": mensagens_mascara[cls],
                            "confianca": round(conf, 3)
                        })
        
        if deteccoes_imagem:
            resultados_detalhados.append({
                "imagem": nome_imagem,
                "deteccoes": deteccoes_imagem
            })
        else:
            imagens_sem_deteccao.append(nome_imagem)
    
    # Gerar relatório
    print("\n" + "="*60)
    print("📋 RELATÓRIO DE DETECÇÃO DE MÁSCARAS")
    print("="*60)
    print(f"📅 Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"📁 Pasta analisada: {caminho_pasta}")
    print(f"🖼️ Total de imagens processadas: {len(imagens)}")
    print(f"👥 Total de pessoas detectadas: {total_deteccoes}")
    print(f"🚫 Imagens sem detecção: {len(imagens_sem_deteccao)}")
    
    print("\n📊 ESTATÍSTICAS POR CATEGORIA:")
    print("-" * 40)
    
    for cls, dados in estatisticas.items():
        porcentagem = (dados["count"] / total_deteccoes * 100) if total_deteccoes > 0 else 0
        emoji = "✅" if cls == 1 else ("⚠️" if cls == 0 else "❌")
        print(f"{emoji} {dados['nome']}: {dados['count']} pessoas ({porcentagem:.1f}%)")
    
    # Análise de conformidade
    pessoas_com_mascara = estatisticas[1]["count"]
    pessoas_sem_mascara = estatisticas[2]["count"]
    pessoas_mascara_incorreta = estatisticas[0]["count"]
    
    if total_deteccoes > 0:
        taxa_conformidade = (pessoas_com_mascara / total_deteccoes) * 100
        taxa_nao_conformidade = ((pessoas_sem_mascara + pessoas_mascara_incorreta) / total_deteccoes) * 100
        
        print(f"\n🎯 ANÁLISE DE CONFORMIDADE:")
        print("-" * 40)
        print(f"✅ Taxa de conformidade: {taxa_conformidade:.1f}%")
        print(f"❌ Taxa de não conformidade: {taxa_nao_conformidade:.1f}%")
        
        if taxa_conformidade >= 80:
            print("🟢 SITUAÇÃO: BOA - Alta taxa de uso correto de máscaras")
        elif taxa_conformidade >= 60:
            print("🟡 SITUAÇÃO: MODERADA - Taxa razoável de uso de máscaras")
        else:
            print("🔴 SITUAÇÃO: CRÍTICA - Baixa taxa de uso correto de máscaras")
    
    # Salvar relatório em arquivo
    if salvar_relatorio:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"relatorio_mascaras_{timestamp}.json"
        
        relatorio_completo = {
            "metadata": {
                "data_hora": datetime.now().isoformat(),
                "pasta_analisada": caminho_pasta,
                "total_imagens": len(imagens),
                "total_deteccoes": total_deteccoes
            },
            "estatisticas": estatisticas,
            "resultados_detalhados": resultados_detalhados,
            "imagens_sem_deteccao": imagens_sem_deteccao,
            "taxa_conformidade": taxa_conformidade if total_deteccoes > 0 else 0
        }
        
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            json.dump(relatorio_completo, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 Relatório detalhado salvo em: {nome_arquivo}")
    
    return estatisticas, resultados_detalhados

def exibir_deteccoes_problematicas(resultados_detalhados):
    """
    Exibe apenas as imagens com pessoas sem máscara ou com máscara incorreta
    """
    print("\n⚠️ IMAGENS COM PROBLEMAS DE CONFORMIDADE:")
    print("="*50)
    
    problemas_encontrados = False
    
    for resultado in resultados_detalhados:
        imagem = resultado["imagem"]
        tem_problema = False
        
        for deteccao in resultado["deteccoes"]:
            if deteccao["classe"] in [0, 2]:  # Máscara incorreta ou sem máscara
                if not tem_problema:
                    print(f"\n📸 {imagem}:")
                    tem_problema = True
                    problemas_encontrados = True
                
                emoji = "⚠️" if deteccao["classe"] == 0 else "❌"
                print(f"   {emoji} {deteccao['mensagem']} (Confiança: {deteccao['confianca']})")
    
    if not problemas_encontrados:
        print("🎉 Parabéns! Nenhum problema de conformidade encontrado!")

if __name__ == "__main__":
    print("📊 Sistema de Relatórios - Detecção de Máscaras")
    print("=" * 50)
    
    while True:
        print("\n📋 Escolha uma opção:")
        print("1. Gerar relatório completo")
        print("2. Gerar relatório do dataset de teste")
        print("3. Exibir apenas problemas de conformidade")
        print("4. Sair")
        
        opcao = input("\n👉 Digite sua opção (1-4): ").strip()
        
        if opcao == '1':
            caminho = input("📁 Digite o caminho da pasta: ").strip()
            gerar_relatorio_deteccoes(caminho)
            
        elif opcao == '2':
            pasta_test = r"c:\Users\Admin\Documents\GitHub\trabalhoFacul\test\images"
            print(f"🧪 Gerando relatório do dataset de teste...")
            gerar_relatorio_deteccoes(pasta_test)
            
        elif opcao == '3':
            caminho = input("📁 Digite o caminho da pasta: ").strip()
            _, resultados = gerar_relatorio_deteccoes(caminho, salvar_relatorio=False)
            exibir_deteccoes_problematicas(resultados)
            
        elif opcao == '4':
            print("👋 Saindo do programa...")
            break
            
        else:
            print("❌ Opção inválida! Tente novamente.")
