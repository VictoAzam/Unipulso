# 🏥 Unipulso - Gerador de Pulseiras Hospitalares Refatorado

## ✨ Nova Arquitetura Modular

Este projeto foi **refatorado para seguir princípios de programação modular**, com separação clara de responsabilidades e alta reutilização de código.

---

## 📚 Estrutura Modular

```
├── config.py           ⚙️  Constantes e configurações globais
├── models.py           📊 Modelos de dados (TextItem, QRItem, LayoutModel)
├── utils.py            🔧 Funções utilitárias reutilizáveis
├── render.py           🎨 Renderização de imagens PIL
├── io_manager.py       📤 Gerenciador de I/O (CSV, PNG, PDF)
├── layout_editor.py    ✏️  Editor visual WYSIWYG
└── app.py              🖥️  Interface gráfica principal (orquestrador)
```

### Benefícios da Arquitetura

✅ **Cada módulo tem responsabilidade única** - SRP (Single Responsibility Principle)  
✅ **Fácil de testar** - Módulos são independentes  
✅ **Reutilizável** - Pode usar módulos em scripts standalone  
✅ **Extensível** - Adicione novos formatos/recursos facilmente  
✅ **Manutenível** - Código claro e organizado  

---

## 🚀 Começar Rapidamente

### 1. Instalar dependências

```bash
cd Unipulso
pip install -r requirements.txt
```

### 2. Executar a aplicação

```bash
python app.py
```

### 3. Usar módulos individualmente

```python
# Exemplo 1: Renderizar pulseira sem GUI
from models import LayoutModel
from render import render_layout_to_image
from utils import list_system_fonts
import json

# Carregar modelo
with open('templates/modelo.json') as f:
    layout = LayoutModel.from_dict(json.load(f))

# Dados do paciente
patient = {
    'Número da carteirinha': '123456',
    'Nome do paciente': 'João Silva',
    'Data de nascimento': '1990-05-12',
    # ... outros dados
}

# Renderizar
fonts_map = list_system_fonts()
img = render_layout_to_image(layout, patient, fonts_map)
img.save('pulseira.png')
```

```python
# Exemplo 2: Processar CSV em batch
from io_manager import IOManager
from render import render_layout_to_image
from models import LayoutModel
from utils import list_system_fonts

# Importar CSV
io = IOManager()
patients = io.import_csv('dados.csv')

# Renderizar todas
layout = LayoutModel.from_dict({...})
fonts_map = list_system_fonts()

for patient in patients:
    img = render_layout_to_image(layout, patient, fonts_map)
    filename = f"pulseira_{patient['Número da carteirinha']}.png"
    img.save(filename)
```

---

## 📦 Descrição dos Módulos

### **config.py** - Configurações
Centraliza todas as constantes do sistema:
- DPI e conversão de unidades
- Dimensões da pulseira
- Colunas CSV esperadas
- Configurações de fontes

```python
from config import P_WIDTH, P_HEIGHT, DPI, cm_to_px

# Usar em qualquer lugar
width_px = cm_to_px(29.5)  # 29.5 cm → pixels
```

### **models.py** - Modelos de Dados
Define estruturas com type hints e dataclasses:

```python
from models import TextItem, QRItem, LayoutModel

# Criar item de texto
text = TextItem(
    id='titulo',
    x=100,
    y=50,
    text='Nome do Paciente',
    font_size=32,
    bold=True
)

# Serializar/desserializar
layout_dict = layout.to_dict()
layout = LayoutModel.from_dict(layout_dict)
```

### **utils.py** - Funções Utilitárias
Funções independentes e reutilizáveis:

```python
from utils import (
    generate_qr_image,
    list_system_fonts,
    get_font,
    wrap_text
)

# Gerar QR code
qr = generate_qr_image("123456", 100)

# Listar fontes disponíveis
fonts = list_system_fonts()

# Quebrar texto em linhas
lines = wrap_text(draw, "texto longo", font, max_width=200)
```

### **render.py** - Renderização
Gera imagens PIL das pulseiras:

```python
from render import render_layout_to_image, create_pulseira_image

# Renderizar com layout customizado
img = render_layout_to_image(layout, patient_data, fonts_map)

# Renderizar modo legado (compatibilidade)
img = create_pulseira_image(patient_data, logo, fonts)
```

### **io_manager.py** - I/O Manager
Gerencia importação/exportação:

```python
from io_manager import IOManager

io = IOManager()

# CSV
patients = io.import_csv('dados.csv')
io.save_example_csv('exemplo.csv')
io.save_empty_csv('template.csv')

# Exportação
io.export_png(patients, layout, fonts_map)
io.export_pdf(patients, layout, fonts_map)
```

### **layout_editor.py** - Editor Visual
Gerencia interface do editor WYSIWYG:

```python
from layout_editor import LayoutEditor

# Criar editor
editor = LayoutEditor(root, layout, fonts_map, logo_image)

# Abrir janela
editor.open(on_close_callback=update_preview)
```

### **app.py** - Interface Principal
Orquestra todos os módulos:

```python
# Importa e utiliza todos os módulos
from app import PulseiraApp

# Criar interface
app = PulseiraApp(root)
```

---

## 🧪 Exemplos de Uso Avançado

### Exemplo 1: Script de Processamento em Batch

```python
#!/usr/bin/env python3
"""
Script para processar múltiplas pulseiras sem GUI
"""

from io_manager import IOManager
from render import render_layout_to_image
from models import LayoutModel
from utils import list_system_fonts
import json
import sys

def main():
    if len(sys.argv) < 3:
        print("Uso: python batch_processor.py <csv_file> <template_json>")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    template_file = sys.argv[2]
    
    # Carregar dados
    io = IOManager()
    patients = io.import_csv(csv_file)
    
    # Carregar layout
    with open(template_file) as f:
        layout = LayoutModel.from_dict(json.load(f))
    
    # Renderizar
    fonts_map = list_system_fonts()
    
    for i, patient in enumerate(patients, 1):
        img = render_layout_to_image(layout, patient, fonts_map)
        filename = f"saida/pulseira_{i:04d}.png"
        img.save(filename)
        print(f"✅ {filename}")
    
    print(f"\n✨ {len(patients)} pulseiras processadas!")

if __name__ == '__main__':
    main()
```

### Exemplo 2: Criar Novo Formato de Exportação

```python
# Em io_manager.py, adicionar:

class IOManager:
    @staticmethod
    def export_svg(patients, layout, fonts_map, logo_image=None):
        """Exporta pulseiras como SVG"""
        from reportlab.graphics import renderSVG
        from reportlab.lib.units import px
        
        for i, patient in enumerate(patients):
            img = render_layout_to_image(layout, patient, fonts_map, logo_image)
            # Converter para SVG
            filename = f"pulseira_{i}.svg"
            # ... implementação
```

### Exemplo 3: Transformar Layout

```python
# transformers.py
from models import LayoutModel

class LayoutTransformer:
    @staticmethod
    def scale_layout(layout, factor):
        """Escala layout por um fator"""
        new_layout = LayoutModel(
            width=int(layout.width * factor),
            height=int(layout.height * factor)
        )
        
        for item in layout.items:
            scaled = item.copy()
            for coord in ['x', 'y', 'width', 'height', 'size']:
                if coord in scaled:
                    scaled[coord] = int(scaled[coord] * factor)
            new_layout.items.append(scaled)
        
        return new_layout

# Usar
original = LayoutModel.from_dict(json.load(open('modelo.json')))
larger = LayoutTransformer.scale_layout(original, 1.5)
```

---

## 🧬 Padrões de Design Utilizados

| Padrão | Módulo | Descrição |
|--------|--------|-----------|
| **Single Responsibility** | Todos | Cada módulo tem uma razão para mudar |
| **Factory** | `io_manager.py` | Cria diferentes tipos de arquivo |
| **Strategy** | `render.py` | Múltiplos modos de renderização |
| **Observer** | `layout_editor.py` | Callbacks para atualizar preview |
| **Dependency Injection** | `app.py` | Recebe dependências ao inicializar |

---

## 📝 Adicionando Novos Recursos

### Adicionar Novo Tipo de Item

1. **Adicionar em `models.py`:**
```python
@dataclass
class CircleItem:
    type: str = 'circle'
    x: int = 0
    y: int = 0
    radius: int = 50
    color: str = '#000000'
```

2. **Implementar em `render.py`:**
```python
elif it.get('type') == 'circle':
    circle = CircleItem(...)
    draw.ellipse(
        [(circle.x - circle.radius, circle.y - circle.radius),
         (circle.x + circle.radius, circle.y + circle.radius)],
        fill=circle.color
    )
```

3. **Editor atualiza automaticamente** (é genérico!)

---

## 🔒 Boas Práticas

- ✅ Cada arquivo < 500 linhas
- ✅ Funções < 50 linhas
- ✅ Docstrings em todas funções
- ✅ Type hints em parâmetros
- ✅ Tratamento de erros apropriado
- ✅ Sem imports circulares
- ✅ Configurações centralizadas

---

## 📖 Documentação Completa

Para análise detalhada da arquitetura, veja **[ARCHITECTURE.md](./ARCHITECTURE.md)**

---

## 💡 Próximas Melhorias Sugeridas

- [ ] Adicionar testes unitários com `pytest`
- [ ] Implementar logging estruturado
- [ ] Criar API REST com `Flask`
- [ ] Dockerizar a aplicação
- [ ] Adicionar validação de esquema JSON
- [ ] Suporte a plugins/extensões
- [ ] Exportação em mais formatos (SVG, DXF)
- [ ] Sincronização em nuvem

---

## 📞 Suporte

Para dúvidas sobre a arquitetura modular, consulte:
1. **ARCHITECTURE.md** - Documentação técnica
2. **Docstrings** - Comentários no código
3. **Exemplos** - Scripts de uso

---

**Parabéns! Você tem uma arquitetura de classe mundial! 🚀**
