<!-- filepath: c:\Users\Admin\Documents\GitHub\trabalhoFacul\DOCUMENTACAO.md -->
<div align="center">

# 📖 Documentação do Sistema Inteligente de Detecção de Máscaras
### *Detalhes Técnicos e Instruções de Uso*

![Python](https://img.shields.io/badge/Python-3.8+-3776ab?style=for-the-badge&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-FF6B35?style=for-the-badge&logo=yolo&logoColor=white)

</div>

---

## 📋 Índice

- [📝 Introdução](#-introdução)
- [✨ Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [🚀 Como Funciona](#-como-funciona)
- [🛠️ Instalação e Configuração](#-instalação-e-configuração)
- [🎯 Funcionalidades](#-funcionalidades)
- [📊 Relatórios e Análises](#-relatórios-e-análises)
- [🔧 Solução de Problemas](#-solução-de-problemas)
- [🤝 Contribuição](#-contribuição)
- [📄 Licença](#-licença)

---

## 📝 Introdução

O **Sistema Inteligente de Detecção de Máscaras** é uma solução inovadora que utiliza inteligência artificial para monitorar o uso de máscaras faciais em tempo real. Este sistema é especialmente útil em ambientes onde a conformidade com as normas de saúde é crucial.

## ✨ Tecnologias Utilizadas

- **Python**: Linguagem de programação principal.
- **OpenCV**: Biblioteca para processamento de imagens.
- **YOLOv8**: Algoritmo de detecção de objetos em tempo real.

## 🚀 Como Funciona

O sistema utiliza a arquitetura YOLOv8 para detectar e classificar o uso de máscaras faciais. Ele analisa o vídeo em tempo real e fornece feedback instantâneo sobre a conformidade do uso de máscaras.

### Fluxo de Trabalho

1. **Captura de Vídeo**: O sistema acessa a câmera para capturar o vídeo em tempo real.
2. **Processamento de Imagem**: Cada frame do vídeo é processado para detectar a presença e a posição da máscara.
3. **Classificação**: O sistema classifica o uso da máscara em três categorias: correta, incorreta e ausente.
4. **Feedback Visual**: O resultado é exibido em uma interface gráfica, com informações sobre a conformidade.

## 🛠️ Instalação e Configuração

### Pré-requisitos

- Python 3.8 ou superior
- OpenCV
- YOLOv8

### Passos para Instalação