import cv2
import platform
import sys

def diagnosticar_camera():
    """
    Função para diagnosticar problemas com a câmera
    """
    print("🔧 DIAGNÓSTICO DE CÂMERA - Sistema de Detecção de Máscaras")
    print("=" * 60)
    
    # Informações do sistema
    print("📊 INFORMAÇÕES DO SISTEMA:")
    print(f"   Sistema Operacional: {platform.system()} {platform.release()}")
    print(f"   Versão do Python: {sys.version}")
    print(f"   Versão do OpenCV: {cv2.__version__}")
    
    # Verificar backends disponíveis
    print(f"\n🔌 BACKENDS DISPONÍVEIS:")
    backends = []
    for backend_name in dir(cv2):
        if backend_name.startswith('CAP_'):
            try:
                backend_value = getattr(cv2, backend_name)
                if isinstance(backend_value, int):
                    backends.append((backend_name, backend_value))
            except:
                pass
    
    for name, value in backends[:10]:  # Mostrar os primeiros 10
        print(f"   {name}: {value}")
    
    # Testar câmeras
    print(f"\n📹 TESTANDO CÂMERAS:")
    cameras_encontradas = []
    
    # Teste básico
    print("   Teste básico (índices 0-4):")
    for i in range(5):
        try:
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                ret, frame = cap.read()
                if ret and frame is not None:
                    h, w = frame.shape[:2]
                    print(f"   ✅ Câmera {i}: OK - Resolução: {w}x{h}")
                    cameras_encontradas.append(i)
                else:
                    print(f"   ⚠️ Câmera {i}: Abriu mas não consegue ler frames")
                cap.release()
            else:
                print(f"   ❌ Câmera {i}: Não disponível")
        except Exception as e:
            print(f"   ❌ Câmera {i}: Erro - {str(e)}")
    
    # Teste com backends específicos (Windows)
    if platform.system() == "Windows":
        print("\n   Teste com backends específicos do Windows:")
        backends_windows = [
            (cv2.CAP_DSHOW, "DirectShow"),
            (cv2.CAP_MSMF, "Media Foundation"),
            (cv2.CAP_VFW, "Video for Windows")
        ]
        
        for backend, nome in backends_windows:
            print(f"\n   Testando {nome}:")
            for i in range(3):
                try:
                    cap = cv2.VideoCapture(i, backend)
                    if cap.isOpened():
                        ret, frame = cap.read()
                        if ret and frame is not None:
                            h, w = frame.shape[:2]
                            print(f"     ✅ Câmera {i}: OK - Resolução: {w}x{h}")
                            if i not in cameras_encontradas:
                                cameras_encontradas.append(f"{i} ({nome})")
                        cap.release()
                    else:
                        print(f"     ❌ Câmera {i}: Não disponível")
                except Exception as e:
                    print(f"     ❌ Câmera {i}: Erro - {str(e)}")
    
    # Resumo
    print(f"\n📋 RESUMO:")
    if cameras_encontradas:
        print(f"   ✅ {len(cameras_encontradas)} câmera(s) encontrada(s): {cameras_encontradas}")
        print("   🎥 Você pode usar o sistema de detecção de máscaras!")
        
        # Teste de demonstração
        print(f"\n🧪 TESTE DE DEMONSTRAÇÃO:")
        print("   Deseja testar a primeira câmera encontrada? (s/n)")
        resposta = input("   ").strip().lower()
        
        if resposta == 's':
            testar_camera_demo(cameras_encontradas[0])
    else:
        print("   ❌ Nenhuma câmera foi encontrada")
        print("\n🔧 POSSÍVEIS SOLUÇÕES:")
        print("   1. Conecte uma webcam USB")
        print("   2. Verifique se a câmera não está sendo usada por outro programa")
        print("   3. Atualize os drivers da câmera")
        print("   4. Verifique as permissões de câmera no Windows:")
        print("      - Configurações > Privacidade > Câmera")
        print("      - Permitir acesso de aplicativos da área de trabalho")
        print("   5. Tente executar como administrador")
        print("   6. Reinicie o computador")

def testar_camera_demo(camera_index):
    """
    Teste de demonstração da câmera
    """
    print(f"\n📹 Iniciando teste da câmera {camera_index}...")
    print("   Pressione 'q' para sair")
    
    try:
        # Se o índice contém informações do backend, usar apenas o número
        if isinstance(camera_index, str) and "(" in camera_index:
            camera_index = int(camera_index.split()[0])
        
        cap = cv2.VideoCapture(int(camera_index))
        
        if not cap.isOpened():
            print("   ❌ Erro: Não foi possível abrir a câmera")
            return
        
        print("   ✅ Câmera aberta com sucesso!")
        
        frame_count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                print("   ❌ Erro ao capturar frame")
                break
            
            frame_count += 1
            
            # Adicionar informações na tela
            cv2.putText(frame, f"Teste de Camera - Frame {frame_count}", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, "Pressione 'q' para sair", (10, 60), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            
            cv2.imshow('Teste de Camera - Diagnóstico', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        print("   ✅ Teste concluído com sucesso!")
        
    except Exception as e:
        print(f"   ❌ Erro durante o teste: {str(e)}")

def verificar_permissoes_windows():
    """
    Guia para verificar permissões no Windows
    """
    print("\n🔐 VERIFICANDO PERMISSÕES DO WINDOWS:")
    print("   1. Pressione Win + I para abrir Configurações")
    print("   2. Vá para Privacidade e segurança > Câmera")
    print("   3. Certifique-se de que 'Acesso à câmera' está ATIVADO")
    print("   4. Certifique-se de que 'Permitir que aplicativos acessem sua câmera' está ATIVADO")
    print("   5. Certifique-se de que 'Permitir que aplicativos da área de trabalho acessem sua câmera' está ATIVADO")

if __name__ == "__main__":
    try:
        diagnosticar_camera()
        
        print(f"\n❓ Precisa de mais ajuda com permissões? (s/n)")
        resposta = input("   ").strip().lower()
        if resposta == 's':
            verificar_permissoes_windows()
            
    except KeyboardInterrupt:
        print("\n\n👋 Diagnóstico interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro durante o diagnóstico: {str(e)}")
