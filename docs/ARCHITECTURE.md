# 📋 Guia de Arquitetura Modular - Unipulso

## 📁 Estrutura do Projeto Refatorado

```
Unipulso/
├── config.py              # ⚙️  Configurações globais
├── models.py              # 📊 Modelos de dados (dataclasses)
├── utils.py               # 🔧 Funções utilitárias
├── render.py              # 🎨 Renderização de pulseiras
├── io_manager.py          # 📤 Importação/Exportação
├── layout_editor.py       # ✏️  Editor visual de layout
├── app.py                 # 🖥️  Interface gráfica principal
├── requirements.txt       # 📦 Dependências
└── templates/             # 💾 Modelos salvos (JSON)
```

---

## 📖 Descrição dos Módulos

### 1️⃣ **config.py** - Configurações e Constantes
**Responsabilidade:** Centralizar todas as configurações do sistema

```python
# Inclui:
- DPI e conversão cm→px
- Dimensões físicas da pulseira
- Colunas CSV esperadas
- Configurações de fontes
- Funções auxiliares (cm_to_px, get_templates_dir)
```

**Por que é importante:**
- ✅ Mudanças em constantes em um único lugar
- ✅ Evita "magic numbers" espalhados no código
- ✅ Facilita testes com diferentes configurações

---

### 2️⃣ **models.py** - Modelos de Dados
**Responsabilidade:** Definir estruturas de dados usando dataclasses

```python
@dataclass
class TextItem:
    """Elemento de texto no layout"""
    type: str = 'text'
    id: str = ''
    x: int = 0
    # ... outros campos

@dataclass
class QRItem:
    """Elemento QR code no layout"""
    type: str = 'qr'
    # ... campos específicos

@dataclass
class LayoutModel:
    """Modelo de layout com lista de itens"""
    width: int = P_WIDTH
    height: int = P_HEIGHT
    items: List[dict] = field(default_factory=list)
```

**Benefícios:**
- ✅ Type hints para melhor IDE support
- ✅ Serialização/desserialização automática
- ✅ Validação de tipos em tempo de desenvolvimento

---

### 3️⃣ **utils.py** - Funções Utilitárias
**Responsabilidade:** Funções reutilizáveis e independentes

```python
Funções principais:
- generate_qr_image()          # Gera QR codes
- list_system_fonts()          # Escaneia fontes do sistema
- choose_font_file_for_family()# Seleciona font file
- get_font()                   # Obtém ImageFont
- wrap_text()                  # Quebra texto em linhas
```

**Vantagens:**
- ✅ Funções puras (sem efeitos colaterais)
- ✅ Fácil de testar unitariamente
- ✅ Reutilizáveis em outros contextos

---

### 4️⃣ **render.py** - Renderização
**Responsabilidade:** Gerar imagens PIL das pulseiras

```python
Funções principais:
- create_pulseira_image()      # Renderiza pulseira (modo legado)
- render_layout_to_image()     # Renderiza com layout customizado
```

**Separação de responsabilidades:**
- ✅ Renderização desacoplada da GUI
- ✅ Pode ser usado em scripts batch
- ✅ Testável independentemente

---

### 5️⃣ **io_manager.py** - Importação/Exportação
**Responsabilidade:** Gerenciar operações de I/O

```python
class IOManager:
    Métodos principais:
    - import_csv()              # Importa dados CSV
    - save_example_csv()        # Gera CSV de exemplo
    - save_empty_csv()          # Gera template CSV
    - export_png()              # Exporta como PNG
    - export_pdf()              # Exporta como PDF
```

**Vantagens:**
- ✅ Todas as operações de arquivo em um lugar
- ✅ Tratamento de erros centralizado
- ✅ Fácil adicionar novos formatos

---

### 6️⃣ **layout_editor.py** - Editor Visual
**Responsabilidade:** Gerenciar a interface do editor de layout

```python
class LayoutEditor:
    Recursos principais:
    - Editor visual WYSIWYG (drag & drop)
    - Edição de propriedades de itens
    - Adição/remoção de elementos
    - Preview em tempo real
```

**Padrão de design:**
- ✅ Separação entre lógica e apresentação
- ✅ Callback para comunicação com app.py
- ✅ Reutilizável em múltiplas janelas

---

### 7️⃣ **app.py** - Interface Gráfica Principal
**Responsabilidade:** Orquestrar os módulos

```python
class PulseiraApp:
    - Inicializa GUI com ttkbootstrap
    - Orquestra interações entre módulos
    - Gerencia estado da aplicação
    - Carrega/salva preferências do usuário
```

**Responsabilidades Delegadas:**
```
app.py delegam para:
├── config.py        → constantes e configs
├── models.py        → estrutura de dados
├── utils.py         → funções auxiliares
├── render.py        → geração de imagens
├── io_manager.py    → operações de arquivo
└── layout_editor.py → editor visual
```

---

## 🔄 Fluxo de Dados

```
┌─────────────────────────────────────────────────────────┐
│                    app.py (GUI)                         │
│               (Orquestrador Principal)                   │
├─────────────────────────────────────────────────────────┤
│                                                           │
├─→ [config.py]      ← Constantes & Configs              │
├─→ [models.py]      ← Estruturas de Dados               │
├─→ [utils.py]       ← Funções Utilitárias               │
├─→ [io_manager.py]  ← I/O (CSV, PNG, PDF)              │
│    │                                                      │
│    └─→ [render.py] ← Renderização                       │
│         │                                                 │
│         └─→ [utils.py] ← Fontes & QR codes             │
│                                                           │
├─→ [layout_editor.py] ← Editor Visual                    │
│    │                                                      │
│    └─→ [render.py] ← Preview em Tempo Real             │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

---

## ✨ Benefícios da Arquitetura Modular

### 1. **Manutenibilidade** 🔧
- Cada módulo tem responsabilidade única
- Mudanças isoladas não afetam outros módulos
- Código mais legível e documentado

### 2. **Testabilidade** ✅
```python
# Fácil testar cada módulo isoladamente
def test_generate_qr_image():
    img = generate_qr_image("123456", 100)
    assert img.size == (100, 100)

def test_wrap_text():
    lines = wrap_text(draw, "texto longo", font, 100)
    assert len(lines) > 0
```

### 3. **Reusabilidade** ♻️
```python
# Pode usar render.py em scripts batch
from render import render_layout_to_image
from models import LayoutModel

layout = LayoutModel.from_dict(json.load(open('modelo.json')))
img = render_layout_to_image(layout, patient_data, fonts_map)
img.save('pulseira.png')
```

### 4. **Extensibilidade** 🚀
```python
# Adicionar novo formato de exportação:
# Apenas estender IOManager
class IOManager:
    def export_svg(self, ...):  # Novo formato
        pass
```

### 5. **Escalabilidade** 📈
```python
# Processar múltiplas pulseiras em paralelo
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor() as executor:
    futures = [
        executor.submit(render_layout_to_image, layout, patient, fonts_map)
        for patient in patients
    ]
    images = [f.result() for f in futures]
```

---

## 📝 Como Estender o Projeto

### Adicionar Novo Tipo de Item no Layout

```python
# 1. Adicionar à models.py
@dataclass
class ImageItem:
    type: str = 'image'
    id: str = ''
    x: int = 0
    y: int = 0
    width: int = 100
    height: int = 100
    path: str = ''  # Caminho da imagem

# 2. Adicionar rendering em render.py
def render_layout_to_image(...):
    # ... código existente ...
    elif it.get('type') == 'image':
        img_item = ImageItem(...)
        image = Image.open(img_item.path)
        img.paste(image, (img_item.x, img_item.y))

# 3. Editor atualiza automaticamente
# (layout_editor.py já é genérico o suficiente)
```

### Adicionar Novo Formato de Exportação

```python
# Em io_manager.py
class IOManager:
    @staticmethod
    def export_svg(patients, layout, fonts_map, save_path=None):
        """Novo formato SVG"""
        # implementação...
```

### Adicionar Novo Módulo

```
# Criar novo arquivo: transformers.py

from typing import Dict, List
from models import LayoutModel, TextItem

class LayoutTransformer:
    @staticmethod
    def scale_layout(layout: LayoutModel, factor: float) -> LayoutModel:
        """Escala todos os itens do layout"""
        new_layout = LayoutModel(
            width=int(layout.width * factor),
            height=int(layout.height * factor)
        )
        for item in layout.items:
            scaled_item = item.copy()
            scaled_item['x'] = int(item.get('x', 0) * factor)
            scaled_item['y'] = int(item.get('y', 0) * factor)
            new_layout.items.append(scaled_item)
        return new_layout
```

---

## 🧪 Testes Unitários (Exemplo)

```python
# test_utils.py
import unittest
from utils import wrap_text, generate_qr_image, get_font
from PIL import Image, ImageDraw, ImageFont

class TestUtils(unittest.TestCase):
    def setUp(self):
        self.img = Image.new('RGB', (300, 300))
        self.draw = ImageDraw.Draw(self.img)
        self.font = ImageFont.load_default()
    
    def test_generate_qr_image(self):
        qr_img = generate_qr_image("123456", 100)
        self.assertEqual(qr_img.size, (100, 100))
    
    def test_wrap_text_short(self):
        lines = wrap_text(self.draw, "hello", self.font, 1000)
        self.assertEqual(len(lines), 1)
    
    def test_wrap_text_long(self):
        long_text = "palavra " * 50
        lines = wrap_text(self.draw, long_text, self.font, 100)
        self.assertGreater(len(lines), 1)

if __name__ == '__main__':
    unittest.main()
```

---

## 🎯 Próximos Passos Sugeridos

1. **Adicionar Testes Unitários** ✅
   ```bash
   pytest tests/
   ```

2. **Adicionar Logging** 📝
   ```python
   import logging
   logger = logging.getLogger(__name__)
   ```

3. **Criar API REST** 🌐
   ```python
   from flask import Flask
   app = Flask(__name__)
   ```

4. **Dockerizar a Aplicação** 🐳
   ```dockerfile
   FROM python:3.11
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   CMD ["python", "app.py"]
   ```

---

## 📚 Referências de Design Patterns

- **Single Responsibility Principle (SRP)**: Cada módulo tem uma razão para mudar
- **Dependency Injection**: Módulos recebem dependências ao invés de criá-las
- **Factory Pattern**: IOManager e LayoutEditor usam padrões de criação
- **Observer Pattern**: Callbacks entre módulos (layout_editor → app)

---

## ✅ Checklist de Boas Práticas

- ✅ Cada arquivo < 500 linhas
- ✅ Funções < 50 linhas
- ✅ Documentação com docstrings
- ✅ Type hints em funções
- ✅ Separação clara de responsabilidades
- ✅ Reutilização de código
- ✅ Tratamento de erros apropriado
- ✅ Configurações centralizadas

---

**Parabéns! Seu código está pronto para escalar! 🚀**
