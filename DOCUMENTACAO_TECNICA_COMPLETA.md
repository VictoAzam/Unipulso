# 📚 Documentação Técnica Completa - Unipulso

## 📋 Índice

1. [Visão Geral do Sistema](#visão-geral-do-sistema)
2. [Arquitetura do Projeto](#arquitetura-do-projeto)
3. [Módulos Principais](#módulos-principais)
4. [Componentes da Interface](#componentes-da-interface)
5. [Utilitários e Helpers](#utilitários-e-helpers)
6. [Fluxo de Dados](#fluxo-de-dados)
7. [Configurações](#configurações)
8. [Modelos de Dados](#modelos-de-dados)
9. [Sistema de Renderização](#sistema-de-renderização)
10. [Gerenciamento de I/O](#gerenciamento-de-io)
11. [Impressão Zebra](#impressão-zebra)
12. [Guia de Desenvolvimento](#guia-de-desenvolvimento)

---

## 🎯 Visão Geral do Sistema

**Unipulso** é um sistema completo para geração e impressão de pulseiras hospitalares. O sistema permite:

- ✅ Importação de dados via CSV
- ✅ Criação de layouts personalizados (WYSIWYG)
- ✅ Geração de QR codes
- ✅ Exportação em PNG e PDF
- ✅ Impressão direta em impressoras Zebra ZD230
- ✅ Formulário de atendimento integrado
- ✅ Interface moderna com ttkbootstrap

### Características Técnicas

- **Linguagem**: Python 3.8+
- **Framework GUI**: ttkbootstrap (baseado em tkinter)
- **Processamento de Imagens**: Pillow (PIL)
- **Formato de Exportação**: PNG, PDF
- **Impressão**: ZPL (Zebra Programming Language)
- **DPI**: 300 (alta qualidade)
- **Dimensões da Pulseira**: 29.5cm x 2.0cm

---

## 🏗️ Arquitetura do Projeto

### Estrutura de Diretórios

```
Unipulso/
├── app.py                    # Ponto de entrada (aplicação simplificada)
├── core/                     # Núcleo do sistema
│   ├── __init__.py
│   ├── config.py            # Configurações globais
│   ├── models.py            # Modelos de dados (dataclasses)
│   ├── render.py            # Motor de renderização
│   └── io_manager.py        # Importação/Exportação
├── ui/                      # Interface do usuário
│   ├── __init__.py
│   ├── tabs.py              # Gerenciamento de abas
│   ├── sidebar.py           # Painel lateral
│   ├── preview.py           # Preview e carrossel
│   ├── layout_editor.py     # Editor WYSIWYG
│   ├── menu_manager.py      # Menu e atalhos
│   └── atendimento_form.py  # Formulário de pacientes
├── utils/                   # Utilitários
│   ├── __init__.py
│   ├── helpers.py           # Funções auxiliares
│   └── zebra_printer.py     # Impressão Zebra
├── data/                    # Dados e CSVs
├── templates/               # Modelos de layout
├── output/                  # Saída de arquivos gerados
├── fonte padrao/            # Fontes do projeto
└── logo/                    # Logotipos
```

### Camadas da Aplicação

```
┌─────────────────────────────────────┐
│         Interface (UI)              │
│  tabs.py | sidebar.py | preview.py  │
└─────────────┬───────────────────────┘
              │
┌─────────────▼───────────────────────┐
│      Lógica de Negócio (Core)      │
│  render.py | models.py | config.py  │
└─────────────┬───────────────────────┘
              │
┌─────────────▼───────────────────────┐
│      Utilitários (Utils)            │
│   helpers.py | zebra_printer.py     │
└─────────────────────────────────────┘
```

---

## 📦 Módulos Principais

### 1. **app.py** - Aplicação Principal

Arquivo de entrada simplificado com funcionalidades mínimas:

```python
"""
Unipulso - Gerador de Pulseiras Hospitalares (versão limpa)
"""
```

**Responsabilidades**:
- Inicialização da aplicação
- Configuração da janela principal
- Funções básicas de geração de pulseiras
- Interface minimalista com ttkbootstrap

**Classes**:
- `PulseiraApp`: Classe principal da aplicação

**Funções Principais**:
- `cm_to_px(value_cm)`: Conversão cm → pixels
- `generate_qr_image(data, size_px)`: Geração de QR code
- `create_pulseira_image(patient_data, logo_image)`: Montagem da pulseira

---

### 2. **core/config.py** - Configurações Globais

Centraliza todas as configurações do sistema.

```python
DPI = 300                    # DPI para impressão
CM_TO_INCH = 1 / 2.54        # Conversão métrica
PULSEIRA_W_CM = 29.5         # Largura em cm
PULSEIRA_H_CM = 2.0          # Altura em cm
NON_PRINTABLE_START_CM = 2.5 # Área não imprimível
PRINTABLE_WIDTH_CM = 11      # Largura imprimível
```

**Colunas Esperadas do CSV**:
```python
EXPECTED_COLUMNS = [
    'Número da carteirinha',
    'Nome do paciente',
    'Data de nascimento',
    'Nome da mãe',
    'Convênio',
    'Médico responsável',
    'Sexo',
    'Data de admissão',
    'Hora de admissão',
    'Observação'
]
```

**Funções**:
- `cm_to_px(value_cm)`: Converte centímetros para pixels baseado em DPI

---

### 3. **core/models.py** - Modelos de Dados

Define as estruturas de dados usando dataclasses.

#### **TextItem**
Representa um elemento de texto no layout.

```python
@dataclass
class TextItem:
    type: str = 'text'
    id: str = ''
    x: int = 0
    y: int = 0
    width: int = 0           # 0 = sem limite
    rotation: float = 0.0
    text: str = ''           # Pode conter placeholders {Coluna CSV}
    binding: Optional[str] = None
    font_family: Optional[str] = None
    font_size: int = 32
    bold: bool = False
    italic: bool = False
    color: str = '#000000'
    align: str = 'left'      # left|center|right
```

#### **QRItem**
Representa um elemento QR code no layout.

```python
@dataclass
class QRItem:
    type: str = 'qr'
    id: str = ''
    x: int = 0
    y: int = 0
    size: int = 100
    data_text: str = ''      # Pode conter placeholders
    binding: Optional[str] = None
```

#### **LayoutModel**
Modelo de layout com lista de itens.

```python
@dataclass
class LayoutModel:
    width: int = P_WIDTH
    height: int = P_HEIGHT
    items: List[dict] = field(default_factory=list)
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'LayoutModel'
    
    def to_dict(self) -> Dict[str, Any]
```

---

### 4. **core/render.py** - Motor de Renderização

Responsável por gerar imagens das pulseiras.

#### Função Principal: `create_pulseira_image`

```python
def create_pulseira_image(
    patient_data: Dict[str, Any],
    fonts_map: Dict[str, List[Tuple[str, str]]],
    logo_image: Optional[Image.Image] = None,
    fonts: Optional[Tuple] = None
) -> Image.Image:
    """
    Gera uma PIL.Image da pulseira a partir dos dados do paciente.
    
    Args:
        patient_data: Dicionário com dados do paciente
        fonts_map: Mapa de fontes do sistema
        logo_image: Imagem do logotipo (opcional)
        fonts: Tupla com informações de fonte
        
    Returns:
        PIL Image da pulseira
    """
```

#### Funcionalidades:
- ✅ Renderização de texto com ajuste automático
- ✅ Geração e posicionamento de QR codes
- ✅ Inserção de logotipos
- ✅ Cálculo de área imprimível
- ✅ Suporte a múltiplas colunas
- ✅ Wrapping de texto
- ✅ Ajuste dinâmico de fonte

#### Função: `render_layout_to_image`

```python
def render_layout_to_image(
    layout: LayoutModel,
    patient_data: Dict[str, Any],
    fonts_map: Dict[str, List[Tuple[str, str]]],
    logo_image: Optional[Image.Image] = None
) -> Image.Image:
    """
    Renderiza layout customizado em imagem.
    
    Args:
        layout: Modelo de layout
        patient_data: Dados do paciente
        fonts_map: Mapa de fontes
        logo_image: Logo opcional
        
    Returns:
        PIL Image renderizada
    """
```

---

### 5. **core/io_manager.py** - Gerenciamento de I/O

Gerencia importação e exportação de dados.

#### Classe: `IOManager`

**Métodos Principais**:

##### `import_csv(filepath: Optional[str] = None) -> List[Dict[str, str]]`
```python
"""
Importa dados de arquivo CSV.

Detecta automaticamente o delimitador (vírgula, ponto-e-vírgula ou tab).
Aceita CSVs com colunas em qualquer ordem e remove espaços em branco.

Args:
    filepath: Caminho do arquivo (se None, abre diálogo)
    
Returns:
    Lista de dicionários com dados
"""
```

**Características**:
- Detecção automática de delimitador
- Suporte a múltiplos encodings (UTF-8, Latin-1)
- Validação de colunas obrigatórias
- Limpeza de dados (trimming)

##### `save_example_csv(filepath: Optional[str] = None) -> bool`
```python
"""
Salva arquivo CSV de exemplo com 2 pacientes demo.
"""
```

##### `save_empty_csv(filepath: Optional[str] = None) -> bool`
```python
"""
Salva arquivo CSV vazio (apenas cabeçalho).
"""
```

##### `export_png(patients: List[Dict], ...) -> bool`
```python
"""
Exporta pulseiras como arquivos PNG individuais.

Args:
    patients: Lista de pacientes
    output_dir: Diretório de saída
    layout: Layout a ser usado
    fonts_map: Mapa de fontes
    logo_image: Logo opcional
    
Returns:
    True se exportado com sucesso
"""
```

##### `export_pdf(patients: List[Dict], ...) -> bool`
```python
"""
Exporta pulseiras como arquivo PDF único.

Cada pulseira ocupa uma página.
"""
```

---

## 🖥️ Componentes da Interface

### 1. **ui/tabs.py** - Gerenciamento de Abas

#### Classe: `TabsManager`

Gerencia as 5 abas principais da aplicação.

**Abas**:
1. 📥 **Importação** - Importar/exportar CSV
2. 👁️ **Pré-visualização** - Carrossel de pacientes
3. ✏️ **Editor** - Editor visual de layout
4. 📤 **Exportação** - Gerar PNG/PDF
5. ⚙️ **Configurações** - Fontes, logotipo, etc.

**Métodos Principais**:
```python
def create_tabs(self):
    """Cria todas as abas."""

def _create_import_tab(self, tab):
    """Aba de importação de CSV."""

def _create_preview_tab(self, tab):
    """Aba de pré-visualização com carrossel."""

def _create_editor_tab(self, tab):
    """Aba do editor de layout."""

def _create_export_tab(self, tab):
    """Aba de exportação PNG/PDF."""

def _create_settings_tab(self, tab):
    """Aba de configurações."""
```

**Widgets Importantes**:
- `data_tree`: TreeView com dados importados
- `canvas_preview`: Canvas para preview da pulseira
- `btn_prev/btn_next`: Botões de navegação do carrossel

---

### 2. **ui/sidebar.py** - Painel Lateral

#### Classe: `SidebarManager`

Gerencia o painel lateral com informações de status.

**Status Exibidos**:
- 📊 **CSV**: Status da importação
- 🏥 **Pulseira**: Preview atual
- 🔤 **Fonte**: Fonte selecionada
- 🖼️ **Logotipo**: Status do logo

**Métodos**:
```python
def create_sidebar(self):
    """Cria painel lateral com status."""

def update_csv_status(self, count: int):
    """Atualiza status do CSV."""

def update_preview_status(self, patient_name: str):
    """Atualiza status do preview."""

def update_font_status(self, font_family: str, size: int):
    """Atualiza status da fonte."""

def update_logo_status(self, filename: str):
    """Atualiza status do logotipo."""
```

---

### 3. **ui/preview.py** - Preview e Carrossel

#### Classe: `PreviewManager`

Gerencia a pré-visualização e navegação entre pacientes.

**Atributos**:
- `current_patient_index`: Índice do paciente atual
- `tkimg`: Referência para PhotoImage (evita garbage collection)

**Métodos Principais**:
```python
def update_preview(self):
    """Atualiza pré-visualização com o paciente atual."""

def next_patient(self):
    """Navega para o próximo paciente."""

def previous_patient(self):
    """Navega para o paciente anterior."""

def _update_preview_data(self, patient: Dict):
    """Atualiza dados do paciente na tela."""
```

**Funcionalidades**:
- ✅ Navegação com botões
- ✅ Atalhos de teclado (← →)
- ✅ Contador de pacientes
- ✅ Exibição de dados detalhados
- ✅ Renderização em tempo real

---

### 4. **ui/layout_editor.py** - Editor WYSIWYG

#### Classe: `LayoutEditor`

Editor visual de layout (What You See Is What You Get).

**Funcionalidades**:
- ✅ Arrastar e soltar elementos
- ✅ Edição de propriedades em tempo real
- ✅ Adicionar/remover itens
- ✅ Preview instantâneo
- ✅ Salvamento de layout

**Estrutura**:
```
┌──────────────────┬─────────────────┐
│                  │  Propriedades   │
│                  │                 │
│    Canvas        │  - Tipo         │
│    (Preview)     │  - Posição X,Y  │
│                  │  - Tamanho      │
│                  │  - Fonte        │
│                  │  - Cor          │
│                  │  - Binding      │
└──────────────────┴─────────────────┘
```

**Métodos Principais**:
```python
def open(self, on_close_callback=None):
    """Abre a janela do editor."""

def _editor_render(self):
    """Renderiza preview no canvas."""

def _editor_on_click(self, evt):
    """Handler de clique no canvas."""

def _editor_on_drag(self, evt):
    """Handler de arrastar elemento."""

def _prop_load_from_selected(self):
    """Carrega propriedades do item selecionado."""

def _prop_apply_to_selected(self):
    """Aplica propriedades ao item selecionado."""

def _add_text_item(self):
    """Adiciona novo item de texto."""

def _add_qr_item(self):
    """Adiciona novo item QR."""

def _remove_selected_item(self):
    """Remove item selecionado."""
```

---

### 5. **ui/menu_manager.py** - Menu e Atalhos

#### Classe: `MenuManager`

Gerencia a barra de menu e atalhos de teclado.

**Menus**:

##### 📁 Arquivo
- Importar CSV (`Ctrl+I`)
- Exportar PNG (`Ctrl+P`)
- Exportar PDF (`Ctrl+D`)
- Baixar Exemplo CSV
- Baixar Modelo Vazio
- Sair (`Ctrl+Q`)

##### ✏️ Editar
- Editor de Layout (`Ctrl+L`)
- Configurar Fonte (`Ctrl+F`)
- Upload Logotipo

##### 💾 Modelos
- Salvar Modelo Atual
- Carregar Modelo
- Abrir Pasta de Modelos

##### ❓ Ajuda
- Sobre Unipulso
- Guia CSV

**Atalhos de Teclado**:
```python
Ctrl+I  → Importar CSV
Ctrl+P  → Exportar PNG
Ctrl+D  → Exportar PDF
Ctrl+L  → Editor de Layout
Ctrl+F  → Configurar Fonte
Ctrl+Q  → Sair
←       → Paciente anterior
→       → Próximo paciente
```

---

### 6. **ui/atendimento_form.py** - Formulário de Atendimento

#### Classe: `AtendimentoForm`

Formulário interativo para cadastro de novos pacientes.

**Campos do Formulário**:
```python
CAMPOS = {
    'Número da carteirinha': {'obrigatorio': True, 'tipo': 'entry'},
    'Nome do paciente': {'obrigatorio': True, 'tipo': 'entry'},
    'Data de nascimento': {'obrigatorio': True, 'tipo': 'entry'},
    'Nome da mãe': {'obrigatorio': True, 'tipo': 'entry'},
    'Convênio': {'obrigatorio': True, 'tipo': 'entry'},
    'Médico responsável': {'obrigatorio': True, 'tipo': 'entry'},
    'Sexo': {'obrigatorio': True, 'tipo': 'combobox'},
    'Data de admissão': {'obrigatorio': True, 'tipo': 'entry'},
    'Hora de admissão': {'obrigatorio': True, 'tipo': 'entry'},
    'Observação': {'obrigatorio': False, 'tipo': 'text'},
}
```

**Funcionalidades**:
- ✅ Validação de campos obrigatórios
- ✅ Máscaras de data/hora
- ✅ Auto-preenchimento de data/hora atual
- ✅ Salvamento incremental em CSV
- ✅ Interface scrollável

**Métodos Principais**:
```python
def abrir_formulario(self):
    """Abre a janela do formulário."""

def _criar_campos(self, container):
    """Cria campos de entrada dinâmicos."""

def _validar_campos(self) -> bool:
    """Valida campos obrigatórios."""

def _salvar_paciente(self):
    """Salva paciente no CSV."""

def _limpar_formulario(self):
    """Limpa todos os campos."""
```

---

## 🛠️ Utilitários e Helpers

### 1. **utils/helpers.py** - Funções Auxiliares

#### `generate_qr_image(data: str, size_px: int) -> Image.Image`
```python
"""
Gera uma imagem PIL de QR code.

Args:
    data: Dados para o QR code
    size_px: Tamanho em pixels
    
Returns:
    PIL Image do QR code
"""
```

#### `list_system_fonts() -> Dict[str, List[Tuple[str, str]]]`
```python
"""
Retorna APENAS as fontes da pasta "fonte padrao".
Não usa mais fontes do sistema - apenas fontes do projeto.

Returns:
    Dicionário {familia: [(path, estilo), ...]}
"""
```

**Características**:
- Carregamento exclusivo de fontes da pasta `fonte padrao/`
- Detecção automática de estilos (Regular, Bold, Italic)
- Logging detalhado de fontes carregadas

#### `choose_font_file_for_family(...) -> Optional[str]`
```python
"""
Escolhe um arquivo de fonte para a família com base em estilo solicitado.

Args:
    fonts_map: Mapa de fontes do sistema
    family: Família de fontes
    bold: Se quer negrito
    italic: Se quer itálico
    
Returns:
    Caminho do arquivo de fonte ou None
"""
```

#### `get_font(family: str, size: int, bold=False, italic=False) -> ImageFont`
```python
"""
Obtém uma fonte PIL ImageFont.

Tenta usar fonte do sistema, fallback para fonte padrão.

Args:
    family: Família de fontes
    size: Tamanho em pixels
    bold: Negrito
    italic: Itálico
    
Returns:
    ImageFont configurado
"""
```

#### `wrap_text(text: str, font: ImageFont, max_width: int) -> List[str]`
```python
"""
Quebra texto em múltiplas linhas para caber na largura máxima.

Args:
    text: Texto a ser quebrado
    font: Fonte PIL
    max_width: Largura máxima em pixels
    
Returns:
    Lista de linhas
"""
```

---

### 2. **utils/zebra_printer.py** - Impressão Zebra

#### Classe: `ZebraPrinter`

Gerencia impressão em impressoras Zebra via ZPL.

**Características**:
- ✅ Comunicação RAW com impressora
- ✅ Comandos ZPL (Zebra Programming Language)
- ✅ Suporte Windows (win32print) e Linux (CUPS)
- ✅ Conversão de imagens para formato Zebra
- ✅ Calibração automática

**Métodos Principais**:

##### `__init__(printer_name: str = "Zebra ZD230")`
```python
"""
Inicializa o gerenciador da impressora Zebra.

Args:
    printer_name: Nome da impressora instalada no sistema
"""
```

##### `list_printers() -> List[str]`
```python
"""
Lista todas as impressoras instaladas no sistema.

Returns:
    Lista com nomes das impressoras
"""
```

##### `is_printer_available() -> bool`
```python
"""
Verifica se a impressora configurada está disponível.

Returns:
    True se a impressora está disponível
"""
```

##### `send_zpl(zpl_command: str) -> bool`
```python
"""
Envia comandos ZPL diretamente para a impressora.

Args:
    zpl_command: Comando ZPL a ser enviado
    
Returns:
    True se enviado com sucesso
"""
```

##### `print_image(image: Image.Image, dpi: int = 300) -> bool`
```python
"""
Imprime uma imagem PIL na impressora Zebra.

Converte a imagem para formato Zebra e envia via ZPL.

Args:
    image: Imagem PIL a ser impressa
    dpi: DPI da imagem (default: 300)
    
Returns:
    True se impressão foi enviada com sucesso
"""
```

##### `calibrate() -> bool`
```python
"""
Executa calibração da impressora.

Envia comando ZPL de calibração automática.

Returns:
    True se calibração foi enviada
"""
```

**Exemplo de Uso**:
```python
# Criar instância
printer = ZebraPrinter("Zebra ZD230")

# Verificar disponibilidade
if printer.is_printer_available():
    # Imprimir imagem
    image = Image.open("pulseira.png")
    printer.print_image(image)
    
    # Ou enviar ZPL direto
    zpl = "^XA^FO50,50^A0N,50,50^FDTeste^FS^XZ"
    printer.send_zpl(zpl)
```

---

## 🔄 Fluxo de Dados

### 1. Fluxo de Importação CSV

```
┌─────────────┐
│ Usuário     │
│ clica em    │
│ Importar    │
└──────┬──────┘
       │
       ▼
┌─────────────────────────┐
│ IOManager.import_csv()  │
│ - Detecta delimitador   │
│ - Valida colunas        │
│ - Limpa dados           │
└──────┬──────────────────┘
       │
       ▼
┌─────────────────────────┐
│ app.patients = [...]    │
│ Armazena na aplicação   │
└──────┬──────────────────┘
       │
       ▼
┌─────────────────────────┐
│ TabsManager             │
│ - Atualiza TreeView     │
│ - Mostra contagem       │
└──────┬──────────────────┘
       │
       ▼
┌─────────────────────────┐
│ PreviewManager          │
│ - Renderiza 1º paciente │
│ - Habilita navegação    │
└─────────────────────────┘
```

### 2. Fluxo de Renderização

```
┌─────────────────────────┐
│ Dados do Paciente       │
│ {Nome, Carteirinha,...} │
└──────┬──────────────────┘
       │
       ▼
┌─────────────────────────┐
│ LayoutModel             │
│ Define posicionamento   │
└──────┬──────────────────┘
       │
       ▼
┌─────────────────────────┐
│ render_layout_to_image()│
│ - Cria imagem base      │
│ - Renderiza QR codes    │
│ - Renderiza textos      │
│ - Aplica logo           │
└──────┬──────────────────┘
       │
       ▼
┌─────────────────────────┐
│ PIL Image (300 DPI)     │
│ 29.5cm x 2.0cm          │
└──────┬──────────────────┘
       │
       ├─────────┬──────────┬─────────┐
       ▼         ▼          ▼         ▼
   Preview   Export PNG  Export PDF  Impressora
```

### 3. Fluxo de Exportação

```
┌─────────────────┐
│ Lista Pacientes │
└────────┬────────┘
         │
         ▼
┌────────────────────────┐
│ Para cada paciente:    │
│  1. Renderiza imagem   │
│  2. Salva PNG/PDF      │
└────────┬───────────────┘
         │
         ▼
┌────────────────────────┐
│ IOManager.export_png() │
│ ou export_pdf()        │
└────────┬───────────────┘
         │
         ▼
┌────────────────────────┐
│ Arquivos em output/    │
│ - paciente_001.png     │
│ - paciente_002.png     │
│ ou pulseiras.pdf       │
└────────────────────────┘
```

---

## ⚙️ Configurações

### Configurações de Dimensões

| Parâmetro | Valor | Descrição |
|-----------|-------|-----------|
| `DPI` | 300 | Resolução de impressão |
| `PULSEIRA_W_CM` | 29.5 | Largura total da pulseira |
| `PULSEIRA_H_CM` | 2.0 | Altura da pulseira |
| `NON_PRINTABLE_START_CM` | 2.5 | Início da área não imprimível |
| `PRINTABLE_WIDTH_CM` | 11 | Largura da área imprimível |
| `SPACING_CM` | 0.5 | Espaçamento entre elementos |

### Cálculo de Pixels

```python
def cm_to_px(value_cm):
    """
    Fórmula: pixels = cm × (1/2.54) × DPI
    
    Exemplo:
    29.5 cm × 0.3937 × 300 = 3484 pixels
    2.0 cm × 0.3937 × 300 = 236 pixels
    """
    return int(round(value_cm * CM_TO_INCH * DPI))
```

### Área Imprimível

```
┌──────────────────────────────────────────────────────┐
│ Pulseira Total: 29.5cm (3484px)                      │
│                                                      │
│ ┌──────┬─────────────────────────────────┬──────┐  │
│ │  NP  │      ÁREA IMPRIMÍVEL (11cm)     │  NP  │  │
│ │ 2.5cm│           1299px                │      │  │
│ └──────┴─────────────────────────────────┴──────┘  │
│                                                      │
│ NP = Non-Printable (área não imprimível)            │
└──────────────────────────────────────────────────────┘
```

---

## 📊 Modelos de Dados

### Estrutura de Paciente (CSV)

```python
{
    'Número da carteirinha': str,  # Identificador único
    'Nome do paciente': str,        # Nome completo
    'Data de nascimento': str,      # DD/MM/AAAA
    'Nome da mãe': str,             # Nome da mãe
    'Convênio': str,                # Plano de saúde
    'Médico responsável': str,      # Nome do médico
    'Sexo': str,                    # M/F/Outro
    'Data de admissão': str,        # DD/MM/AAAA
    'Hora de admissão': str,        # HH:MM
    'Observação': str               # Campo livre
}
```

### Estrutura de Layout (JSON)

```json
{
  "width": 3484,
  "height": 236,
  "items": [
    {
      "type": "qr",
      "id": "qr_carteirinha",
      "x": 100,
      "y": 50,
      "size": 150,
      "binding": "Número da carteirinha"
    },
    {
      "type": "text",
      "id": "txt_nome",
      "x": 300,
      "y": 50,
      "width": 0,
      "text": "{Nome do paciente}",
      "binding": "Nome do paciente",
      "font_family": "Arial",
      "font_size": 48,
      "bold": true,
      "color": "#000000",
      "align": "left"
    }
  ]
}
```

---

## 🎨 Sistema de Renderização

### Pipeline de Renderização

```
Input: Patient Data + Layout
        │
        ▼
┌───────────────────────┐
│ 1. Create Base Image  │
│    (White, P_WIDTH x  │
│     P_HEIGHT)         │
└───────┬───────────────┘
        │
        ▼
┌───────────────────────┐
│ 2. Calculate Areas    │
│    - QR Area          │
│    - Text Area        │
│    - Logo Area        │
└───────┬───────────────┘
        │
        ▼
┌───────────────────────┐
│ 3. Render QR Codes    │
│    - Generate QR      │
│    - Paste at X,Y     │
└───────┬───────────────┘
        │
        ▼
┌───────────────────────┐
│ 4. Render Text Items  │
│    - Apply binding    │
│    - Load font        │
│    - Draw text        │
│    - Wrap if needed   │
└───────┬───────────────┘
        │
        ▼
┌───────────────────────┐
│ 5. Apply Logo         │
│    - Resize           │
│    - Paste w/ alpha   │
└───────┬───────────────┘
        │
        ▼
    Output: PIL Image
```

### Placeholders Suportados

Textos e QR codes podem usar placeholders que são substituídos pelos dados do paciente:

```python
# Exemplo de uso de placeholders
text_item = {
    "text": "Paciente: {Nome do paciente}",
    "binding": "Nome do paciente"  # Também pode ser usado
}

# Resultado renderizado:
# "Paciente: João Silva"
```

### Ajuste Automático de Fonte

O sistema tenta ajustar automaticamente o tamanho da fonte para caber no espaço disponível:

```python
def fits_two_columns(test_font_reg, test_font_bold, test_font_name_bold):
    """
    Verifica se todos os elementos cabem no espaço disponível.
    
    Considera:
    - Altura do nome do paciente
    - Altura do número da carteirinha
    - Altura de campos em 2 colunas
    - Margens e espaçamentos
    
    Returns:
        True se cabe, False se precisa reduzir fonte
    """
```

---

## 💾 Gerenciamento de I/O

### Formatos de Exportação

#### PNG (Individual)
- Um arquivo por paciente
- Nome: `paciente_001.png`, `paciente_002.png`, etc.
- Resolução: 300 DPI
- Formato: RGB

#### PDF (Único)
- Todas as pulseiras em um arquivo
- Uma pulseira por página
- Mantém resolução de 300 DPI
- Formato: A4 landscape (opcional)

### Importação de CSV

#### Delimitadores Suportados
- `,` (vírgula)
- `;` (ponto-e-vírgula)
- `\t` (tab)

#### Encodings Suportados
- UTF-8
- Latin-1 (ISO-8859-1)

#### Validação de Dados

```python
# Colunas obrigatórias
REQUIRED_COLUMNS = [
    'Número da carteirinha',
    'Nome do paciente'
]

# Validação automática:
- Remove espaços em branco (trim)
- Valida presença de colunas obrigatórias
- Alerta sobre colunas extras/faltantes
```

---

## 🖨️ Impressão Zebra

### Comandos ZPL Básicos

```zpl
^XA           ; Início do comando
^FO50,50      ; Posição (Field Origin)
^A0N,50,50    ; Fonte (tipo, altura, largura)
^FDTexto^FS   ; Dados do campo (Field Data)
^XZ           ; Fim do comando
```

### Exemplo de Impressão de Imagem

```python
printer = ZebraPrinter("Zebra ZD230")

# Carregar imagem
image = Image.open("pulseira.png")

# Converter para P&B (1-bit)
image = image.convert("1")

# Imprimir
printer.print_image(image, dpi=300)
```

### Calibração da Impressora

```python
printer.calibrate()
# Envia: ~JC (Calibrate Media)
```

### Troubleshooting de Impressão

| Problema | Solução |
|----------|---------|
| Impressora não encontrada | Verificar nome exato com `printer.list_printers()` |
| Impressão cortada | Calibrar mídia com `printer.calibrate()` |
| Imagem muito clara | Ajustar densidade de impressão |
| Imagem espelhada | Usar `^POI` (Print Orientation Invert) |

---

## 🧑‍💻 Guia de Desenvolvimento

### Instalação de Dependências

```bash
pip install -r requirements.txt
```

**Dependências Principais**:
```
ttkbootstrap>=1.10.0
Pillow>=9.0.0
qrcode>=7.3.1
reportlab>=3.6.0  # Para PDF
pywin32>=300      # Para impressão Windows
```

### Executar a Aplicação

```bash
# Versão simples
python app.py

# Versão completa (se houver)
python main.py
```

### Estrutura de Desenvolvimento

```python
# 1. Inicializar aplicação
app = PulseiraApp(root)

# 2. Carregar dados
patients = IOManager.import_csv("data.csv")

# 3. Renderizar pulseira
image = render_layout_to_image(layout, patient, fonts_map)

# 4. Exportar
IOManager.export_png(patients, "output/", layout, fonts_map)
```

### Adicionar Novo Campo ao CSV

1. **Atualizar `config.py`**:
```python
EXPECTED_COLUMNS.append('Novo Campo')
```

2. **Atualizar `atendimento_form.py`**:
```python
CAMPOS['Novo Campo'] = {'obrigatorio': False, 'tipo': 'entry'}
```

3. **Atualizar layout** (se necessário):
```json
{
  "type": "text",
  "binding": "Novo Campo",
  "text": "{Novo Campo}"
}
```

### Adicionar Nova Fonte

1. Copiar arquivo `.ttf` ou `.otf` para `fonte padrao/`
2. Reiniciar a aplicação
3. Fonte estará disponível no editor de layout

### Criar Novo Template de Layout

```python
# Via código
layout = LayoutModel(width=P_WIDTH, height=P_HEIGHT)
layout.items.append({
    'type': 'text',
    'id': 'nome',
    'x': 100,
    'y': 50,
    'binding': 'Nome do paciente',
    'font_size': 48
})

# Salvar
import json
with open('templates/custom.json', 'w') as f:
    json.dump(layout.to_dict(), f, indent=2)
```

### Debug e Logging

```python
# Ativar debug no render.py
print(f"[DEBUG] Renderizando paciente: {patient_data}")
print(f"[DEBUG] Área imprimível: {PRINTABLE_W_PX}px")
```

---

## 📝 Convenções de Código

### Nomenclatura

- **Classes**: PascalCase (`LayoutEditor`, `IOManager`)
- **Funções**: snake_case (`create_pulseira_image`, `cm_to_px`)
- **Constantes**: UPPER_SNAKE_CASE (`P_WIDTH`, `DPI`)
- **Variáveis**: snake_case (`patient_data`, `fonts_map`)

### Docstrings

```python
def funcao_exemplo(param1: str, param2: int) -> bool:
    """
    Descrição breve da função.
    
    Descrição detalhada (opcional).
    
    Args:
        param1: Descrição do parâmetro 1
        param2: Descrição do parâmetro 2
        
    Returns:
        Descrição do valor retornado
        
    Raises:
        ExceptionType: Quando ocorre X
    """
```

### Type Hints

```python
from typing import Dict, List, Optional, Tuple

def process_patients(
    patients: List[Dict[str, str]],
    layout: LayoutModel
) -> Optional[Image.Image]:
    pass
```

---

## 🔍 Referências e Links Úteis

### Documentação Oficial

- **Pillow (PIL)**: https://pillow.readthedocs.io/
- **ttkbootstrap**: https://ttkbootstrap.readthedocs.io/
- **QRCode**: https://pypi.org/project/qrcode/
- **ReportLab (PDF)**: https://www.reportlab.com/docs/reportlab-userguide.pdf

### ZPL (Zebra Programming Language)

- **ZPL Manual**: https://www.zebra.com/content/dam/zebra/manuals/printers/common/programming/zpl-zbi2-pm-en.pdf
- **ZPL Designer**: http://labelary.com/viewer.html

### Arquitetura do Projeto

- Ver: `ARCHITECTURE.md`
- Ver: `BUILD_SYSTEM_INDEX.md`

---

## 📞 Suporte e Contribuição

### Reportar Bugs

Crie um issue com:
1. Descrição do problema
2. Passos para reproduzir
3. Comportamento esperado vs. atual
4. Logs/screenshots

### Contribuir

1. Fork do repositório
2. Criar branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push (`git push origin feature/nova-funcionalidade`)
5. Pull Request

---

## 📄 Licença

Ver arquivo `LICENSE` no diretório raiz do projeto.

---

## 🎉 Conclusão

Esta documentação cobre todos os aspectos técnicos do sistema **Unipulso**. Para dúvidas específicas, consulte os arquivos individuais de cada módulo ou entre em contato com a equipe de desenvolvimento.

**Versão da Documentação**: 1.0.0  
**Data**: Janeiro 2026  
**Autor**: Equipe Unipulso
