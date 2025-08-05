# 🎭 Sistema de Detecção de Máscaras - Trabalho Faculdade

## 📝 Descrição
Sistema inteligente de detecção de máscaras usando YOLOv8, capaz de identificar se uma pessoa está:
- ✅ **Usando máscara corretamente**
- ⚠️ **Usando máscara incorretamente** 
- ❌ **Não usando máscara**

## 🚀 Funcionalidades

### 1. 📹 Detecção em Tempo Real (webcam)
- **Arquivo:** `detectar_mascara.py`
- Detecta máscaras em tempo real através da webcam
- Exibe mensagens claras e coloridas para cada situação
- Interface intuitiva com instruções na tela

### 2. 📸 Detecção em Imagens
- **Arquivo:** `detectar_mascara_imagem.py`  
- Analisa imagens individuais ou pastas inteiras
- Interface de menu interativo
- Suporte a múltiplos formatos (JPG, PNG, BMP, TIFF)

### 3. 📊 Relatórios Detalhados
- **Arquivo:** `relatorio_mascaras.py`
- Gera estatísticas completas de conformidade
- Salva relatórios em formato JSON
- Análise de taxa de conformidade
- Identifica imagens problemáticas

## 🎯 Classes Detectadas

| Classe | Mensagem | Cor | Status |
|--------|----------|-----|---------|
| 0 | ⚠️ MÁSCARA INCORRETA - Ajuste sua máscara! | 🟠 Laranja | Atenção |
| 1 | ✅ ESTÁ USANDO MÁSCARA - Muito bem! | 🟢 Verde | Correto |
| 2 | ❌ NÃO ESTÁ USANDO MÁSCARA - Coloque sua máscara! | 🔴 Vermelho | Incorreto |

## 🛠️ Como Usar

### Requisitos
```bash
pip install ultralytics opencv-python numpy
```

### 1. Detecção em Tempo Real
```bash
python detectar_mascara.py
```
- Pressione 'q' para sair

### 2. Análise de Imagens
```bash
python detectar_mascara_imagem.py
```
Opções disponíveis:
- Analisar uma imagem específica
- Analisar todas as imagens de uma pasta
- Testar com dataset de teste
- Sair

### 3. Relatórios
```bash
python relatorio_mascaras.py
```
Funcionalidades:
- Relatório completo com estatísticas
- Análise do dataset de teste
- Visualização de problemas de conformidade
- Exportação em JSON

## 📁 Estrutura do Projeto

```
trabalhoFacul/
├── detectar_mascara.py          # Detecção em tempo real
├── detectar_mascara_imagem.py   # Detecção em imagens
├── relatorio_mascaras.py        # Geração de relatórios
├── treinar_yolo.py             # Script de treinamento
├── data.yaml                   # Configuração do dataset
├── test/                       # Dataset de teste
│   ├── images/                # Imagens de teste
│   └── labels/                # Anotações de teste
├── train/                      # Dataset de treinamento
└── valid/                      # Dataset de validação
```

## 📊 Recursos dos Relatórios

### Estatísticas Geradas:
- 📈 Total de pessoas detectadas
- 📊 Distribuição por categoria
- 🎯 Taxa de conformidade
- ⚠️ Imagens problemáticas
- 📅 Timestamp e metadados

### Análise de Conformidade:
- 🟢 **BOA**: Taxa ≥ 80% de uso correto
- 🟡 **MODERADA**: Taxa entre 60-79%
- 🔴 **CRÍTICA**: Taxa < 60%

## 🎨 Interface Visual

### Cores das Detecções:
- **Verde**: Pessoa usando máscara corretamente
- **Laranja**: Máscara usada incorretamente  
- **Vermelho**: Pessoa sem máscara

### Informações Exibidas:
- Caixa delimitadora colorida
- Mensagem clara sobre o status
- Nível de confiança da detecção
- Instruções de uso

## 📈 Exemplo de Uso

```python
# Exemplo de detecção personalizada
from detectar_mascara_imagem import detectar_mascara_imagem

# Analisar uma imagem específica
detectar_mascara_imagem("caminho/para/sua/imagem.jpg")

# Gerar relatório de uma pasta
from relatorio_mascaras import gerar_relatorio_deteccoes
gerar_relatorio_deteccoes("caminho/para/pasta/imagens")
```

## 🔧 Configurações

### Limiar de Confiança
- Padrão: 0.5 (50%)
- Ajustável nos arquivos Python

### Modelo YOLO
- Localização configurada em cada arquivo
- Substitua o caminho conforme sua instalação

## 📝 Notas Importantes

1. **Webcam**: Certifique-se de que a câmera está conectada e funcionando
2. **Modelo**: Verifique se o caminho do modelo está correto
3. **Permissões**: Garanta acesso de leitura às pastas de imagens
4. **Performance**: Para muitas imagens, o processamento pode demorar

## 🎓 Trabalho Acadêmico

Este projeto foi desenvolvido como trabalho acadêmico para demonstrar:
- Aplicação de Deep Learning em problemas reais
- Uso do framework YOLOv8 para detecção de objetos
- Desenvolvimento de interfaces intuitivas
- Geração de relatórios e análises estatísticas
- Implementação de sistemas de monitoramento de saúde pública

---
*Desenvolvido com ❤️ para fins acadêmicos*
