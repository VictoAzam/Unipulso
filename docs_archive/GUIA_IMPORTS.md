# 📖 Guia Rápido de Importação - Projeto Unipulso

## Como importar elementos do projeto reorganizado

### Configuração e Modelos (Core)

```python
# Configurações
from core import P_WIDTH, P_HEIGHT, EXPECTED_COLUMNS, PREFS_FILE
from core import get_templates_dir, cm_to_px, DPI

# Modelos
from core import LayoutModel, TextItem, QRItem

# Renderização
from core import render_layout_to_image

# I/O (Importação/Exportação)
from core import IOManager
```

### Interface Gráfica (UI)

```python
# Editor de layout
from ui import LayoutEditor

# Menu
from ui.menu_manager import MenuManager
```

### Utilitários

```python
# Helpers
from utils import list_system_fonts, get_font, generate_qr_image
from utils import wrap_text, choose_font_file_for_family
```

### Testes

```python
# Para rodar testes
# pytest tests/
# ou
# python -m pytest tests/
```

## Estrutura de arquivos por responsabilidade

| Arquivo | Responsabilidade |
|---------|-------------------|
| `core/config.py` | Constantes, DPI, dimensões, fontes |
| `core/models.py` | Dataclasses: TextItem, QRItem, LayoutModel |
| `core/render.py` | Renderização de pulseiras em imagens |
| `core/io_manager.py` | Importar CSV, exportar PNG/PDF |
| `ui/layout_editor.py` | Editor WYSIWYG visual |
| `ui/menu_manager.py` | Barra de menu e atalhos teclado |
| `ui/sidebar.py` | Sidebar da interface |
| `ui/tabs.py` | Abas da interface |
| `ui/preview.py` | Pré-visualização de pulseiras |
| `utils/helpers.py` | QR codes, fontes, text wrapping |

## Executar a aplicação

```bash
# Do diretório raiz do projeto
python app.py
```

## Estrutura de pastas resumida

```
├── app.py              ← INICIE AQUI
├── core/               ← Lógica central
├── ui/                 ← Interface gráfica
├── utils/              ← Funções utilitárias
├── tests/              ← Testes
├── docs/               ← Documentação
├── data/               ← Dados de exemplo
└── templates/          ← Modelos salvos (JSON)
```

## Dicas

- 💡 Cada pasta tem um `__init__.py` que exporta os principais elementos
- 💡 Os imports estão estruturados de forma clara e lógica
- 💡 A documentação está em `docs/` para fácil referência
- 💡 Os testes estão em `tests/` e podem ser rodados com pytest
- 💡 Os dados de exemplo estão em `data/`

---

**Para mais detalhes**, veja `PROJETO_REORGANIZADO.md`
