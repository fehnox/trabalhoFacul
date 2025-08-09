<!-- filepath: c:\Users\Admin\Documents\GitHub\trabalhoFacul\DOCUMENTACAO_TECNICA.md -->
<div align="center">

# 📚 Documentação Técnica do Sistema Inteligente de Detecção de Máscaras

### *Uma visão detalhada sobre a arquitetura e funcionamento do sistema*

![Python](https://img.shields.io/badge/Python-3.8+-3776ab?style=for-the-badge&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-FF6B35?style=for-the-badge&logo=yolo&logoColor=white)

</div>

---

## 🛠️ Arquitetura do Sistema

O sistema é composto por várias camadas que interagem entre si para realizar a detecção de máscaras faciais em tempo real. Abaixo está uma visão geral da arquitetura:

1. **Camada de Entrada**:
   - Captura de vídeo em tempo real através de uma webcam ou processamento de imagens estáticas.

2. **Camada de Processamento**:
   - Utiliza a biblioteca OpenCV para manipulação de imagens e vídeos.
   - Implementa o modelo YOLOv8 para detecção de objetos, especificamente para identificar o uso de máscaras.

3. **Camada de Saída**:
   - Exibe os resultados em uma interface gráfica, mostrando as detecções em tempo real com feedback visual.

## 📊 Fluxo de Dados

O fluxo de dados no sistema é o seguinte:

1. **Captura de Imagem**:
   - O sistema captura frames da webcam ou de uma imagem estática.

2. **Pré-processamento**:
   - As imagens são redimensionadas e normalizadas para serem compatíveis com o modelo YOLOv8.

3. **Detecção**:
   - O modelo YOLOv8 processa a imagem e retorna as classes detectadas (máscara correta, máscara incorreta, sem máscara).

4. **Pós-processamento**:
   - Os resultados são filtrados com base em um limiar de confiança e as detecções são anotadas na imagem.

5. **Exibição**:
   - A imagem processada é exibida em uma janela, mostrando as detecções e suas respectivas classes.

## 📋 Detalhes Técnicos

### Dependências

As principais bibliotecas utilizadas no projeto incluem:

- **Python 3.8+**
- **OpenCV**: Para manipulação de imagens e vídeos.
- **Ultralytics YOLOv8**: Para detecção de objetos.
- **NumPy**: Para operações numéricas.
- **Matplotlib**: Para visualização de dados.

### Estrutura de Diretórios

A estrutura do projeto é organizada da seguinte forma: