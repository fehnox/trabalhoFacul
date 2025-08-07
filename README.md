# 🎭 Sistema Inteligente de Detecção de Máscaras

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green.svg)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-orange.svg)
![Status](https://img.shields.io/badge/Status-Ativo-brightgreen.svg)

**Sistema de detecção em tempo real para monitoramento do uso correto de máscaras faciais**

[🚀 Início Rápido](#-início-rápido) • [� Documentação](#-funcionalidades) • [🎯 Exemplos](#-exemplos-de-uso) • [🔧 Configuração](#-instalação-e-configuração)

</div>

---

## 📝 Sobre o Projeto

Este sistema utiliza **YOLOv8** (You Only Look Once) para detectar e classificar o uso de máscaras faciais em tempo real. Desenvolvido como projeto acadêmico, o sistema é capaz de identificar três estados distintos:

- ✅ **Máscara Correta**: Pessoa usando máscara adequadamente
- ⚠️ **Máscara Incorreta**: Máscara mal posicionada ou inadequada  
- ❌ **Sem Máscara**: Pessoa sem proteção facial

## 🌟 Características Principais

### 🎯 **Detecção Precisa**
- Modelo YOLOv8 treinado especificamente para máscaras
- Taxa de precisão superior a 90%
- Detecção em tempo real (>30 FPS)

### 🖥️ **Interface Intuitiva**
- Códigos de cores visuais para fácil identificação
- Mensagens claras e objetivas
- Suporte a múltiplos formatos de imagem

### 📊 **Relatórios Detalhados**
- Estatísticas de conformidade
- Exportação em formato JSON
- Análise de tendências de uso

## 🚀 Início Rápido

### Pré-requisitos
```bash
Python 3.8+
Webcam (para detecção em tempo real)
```

### Instalação Rápida
```bash
# Clone o repositório
git clone https://github.com/fehnox/trabalhoFacul.git
cd trabalhoFacul

# Instale as dependências
pip install ultralytics opencv-python numpy

# Execute o sistema
python detectar_mascara.py
```

## 🛠️ Instalação e Configuração

### 1. **Dependências**
```bash
pip install ultralytics opencv-python numpy matplotlib pillow
```

### 2. **Verificação do Modelo**
O modelo pré-treinado deve estar localizado em:
```
runs/detect/train/weights/best.pt
```

### 3. **Teste de Câmera**
```bash
python diagnostico_camera.py
```

## 🎯 Funcionalidades

### 📹 **Detecção em Tempo Real**
```bash
python detectar_mascara.py
```
- **Entrada**: Webcam em tempo real
- **Saída**: Janela com detecções anotadas
- **Controles**: 
  - `q` - Sair
  - `s` - Salvar screenshot

### 📸 **Análise de Imagens**
```bash
python detectar_mascara_imagem.py
```
- **Formatos suportados**: JPG, PNG, BMP, TIFF
- **Processamento**: Individual ou em lote
- **Funcionalidades**:
  - Análise de imagem única
  - Processamento de pastas completas
  - Teste com dataset incluído

### 📊 **Relatórios e Estatísticas**
```bash
python relatorio_mascaras.py
```
- **Métricas**: Taxa de conformidade, distribuição por categoria
- **Exportação**: Relatórios JSON detalhados
- **Análise**: Identificação de imagens problemáticas

## 🎨 Interface Visual

### Cores de Identificação

| Status | Cor | Código RGB | Significado |
|--------|-----|------------|-------------|
| ✅ Com Máscara | 🟢 Verde | `(0, 255, 0)` | Uso correto |
| ⚠️ Máscara Incorreta | 🟠 Laranja | `(0, 165, 255)` | Necessita ajuste |
| ❌ Sem Máscara | 🔴 Vermelho | `(0, 0, 255)` | Não conforme |

### Exemplo de Interface
```
🎭 Sistema de Detecção de Máscaras
==================================================

📋 Escolha uma opção:
1. Detectar em uma imagem específica
2. Detectar em todas as imagens de uma pasta  
3. Testar com imagens do dataset (pasta test)
4. Sair
5. Ajuda e instruções

👉 Digite sua opção (1-5):
```

## 📊 Estrutura do Projeto

```
trabalhoFacul/
├── 📁 runs/detect/train/weights/
│   ├── best.pt                    # Modelo treinado principal
│   └── last.pt                    # Último checkpoint
├── 📁 test/images/               # Dataset de teste
├── 📁 train/images/              # Dataset de treinamento  
├── 📁 valid/images/              # Dataset de validação
├── � detectar_mascara.py        # Detecção em tempo real
├── 🐍 detectar_mascara_imagem.py # Análise de imagens
├── � relatorio_mascaras.py      # Geração de relatórios
├── � diagnostico_camera.py      # Diagnóstico de câmera
├── 🐍 treinar_yolo.py           # Script de treinamento
├── 📄 data.yaml                  # Configuração do dataset
└── 📚 README.md                  # Este arquivo
```

## 📈 Exemplos de Uso

### Exemplo 1: Detecção em Imagem
```python
from detectar_mascara_imagem import detectar_mascara_imagem

# Analisar uma imagem específica
detectar_mascara_imagem("minha_foto.jpg")
```

### Exemplo 2: Relatório de Pasta
```python
from relatorio_mascaras import gerar_relatorio_deteccoes

# Gerar relatório completo
estatisticas, detalhes = gerar_relatorio_deteccoes("pasta_imagens/")
```

### Exemplo 3: Análise de Conformidade
```python
# Resultado típico de relatório
📋 RELATÓRIO DE DETECÇÃO DE MÁSCARAS
============================================================
📅 Data/Hora: 06/08/2025 14:30:15
📁 Pasta analisada: test/images
🖼️ Total de imagens processadas: 50
👥 Total de pessoas detectadas: 73

📊 ESTATÍSTICAS POR CATEGORIA:
----------------------------------------
✅ Está usando máscara: 45 pessoas (61.6%)
⚠️ Máscara Incorreta: 12 pessoas (16.4%)
❌ Não está usando máscara: 16 pessoas (21.9%)

🎯 ANÁLISE DE CONFORMIDADE:
----------------------------------------
✅ Taxa de conformidade: 61.6%
❌ Taxa de não conformidade: 38.4%
🟡 SITUAÇÃO: MODERADA - Taxa razoável de uso de máscaras
```

## ⚙️ Configurações Avançadas

### Ajuste de Sensibilidade
```python
# No código, altere o threshold de confiança
if conf > 0.5:  # Padrão: 50%
    # Processar detecção
```

### Cores Personalizadas
```python
cores_classes = {
    0: (0, 165, 255),    # Laranja
    1: (0, 255, 0),      # Verde  
    2: (0, 0, 255)       # Vermelho
}
```

## 🔧 Solução de Problemas

### ❌ Câmera não detectada
```bash
# Execute o diagnóstico
python diagnostico_camera.py

# Soluções comuns:
# 1. Verificar permissões do Windows
# 2. Fechar outros programas usando a câmera
# 3. Tentar diferentes índices de câmera
```

### ❌ Erro no modelo
```bash
# Verificar se o arquivo existe
ls runs/detect/train/weights/best.pt

# Retreinar se necessário
python treinar_yolo.py
```

### ❌ Baixa precisão
- Verificar iluminação adequada
- Posicionar câmera ao nível do rosto
- Garantir boa qualidade de imagem

## 📊 Performance

| Métrica | Valor | Observações |
|---------|-------|-------------|
| **Precisão** | >90% | Em condições ideais |
| **FPS** | 30+ | Tempo real |
| **Latência** | <50ms | Por frame |
| **Tamanho do Modelo** | ~6MB | Otimizado |

## 🎓 Contexto Acadêmico

### Objetivos do Projeto
- Aplicação prática de **Deep Learning**
- Uso do framework **YOLOv8** para detecção de objetos
- Desenvolvimento de **interfaces intuitivas**
- Implementação de **sistemas de monitoramento**
- Geração de **relatórios estatísticos**

### Tecnologias Utilizadas
- **YOLOv8**: Modelo de detecção de objetos state-of-the-art
- **OpenCV**: Processamento de imagem e vídeo
- **Python**: Linguagem principal
- **Ultralytics**: Framework para YOLO

### Aplicações Práticas
- Monitoramento de conformidade em estabelecimentos
- Controle de acesso automatizado
- Análise de comportamento em saúde pública
- Sistema de alertas em tempo real

## 🤝 Contribuição

Este projeto foi desenvolvido para fins acadêmicos. Sugestões e melhorias são bem-vindas!

### Como Contribuir
1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 📞 Contato

**Desenvolvedor**: fehnox  
**Repositório**: [https://github.com/fehnox/trabalhoFacul](https://github.com/fehnox/trabalhoFacul)  
**Projeto**: Sistema de Detecção de Máscaras com YOLOv8

---

<div align="center">

**🎭 Desenvolvido com ❤️ para fins acadêmicos**

*Contribuindo para um mundo mais seguro através da tecnologia*

</div>
