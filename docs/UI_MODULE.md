# 📘 Documentação do Módulo UI (Interface do Usuário)

## Visão Geral

O módulo **ui** contém todos os componentes da interface gráfica do Unipulso. Utiliza **ttkbootstrap** (baseado em tkinter) para criar uma interface moderna e responsiva.

---

## 📁 Estrutura do Módulo

```
ui/
├── __init__.py              # Exportações do módulo
├── tabs.py                  # Gerenciamento de abas
├── sidebar.py               # Painel lateral de informações
├── preview.py               # Preview e carrossel de pacientes
├── layout_editor.py         # Editor WYSIWYG de layouts
├── menu_manager.py          # Barra de menu e atalhos
└── atendimento_form.py      # Formulário de cadastro
```

---

## 📑 tabs.py - Gerenciamento de Abas

### Classe: `TabsManager`

Responsável por criar e gerenciar as 5 abas principais da aplicação.

```python
class TabsManager:
    """Gerencia abas da interface."""
    
    def __init__(self, app, notebook):
        """
        Inicializa gerenciador de abas.
        
        Args:
            app: Referência à aplicação principal (PulseiraAppUX)
            notebook: Widget do tkinter notebook (abas)
        """
```

### Abas Disponíveis

#### 1. 📥 Aba de Importação

```python
def _create_import_tab(self, tab):
    """Aba de importação de CSV."""
```

**Componentes**:
- Botão "Importar CSV"
- Botão "Baixar Exemplo"
- Botão "Baixar Modelo Vazio"
- TreeView com dados importados
- Label de status

**Funcionalidades**:
- Importar arquivo CSV
- Visualizar dados em tabela
- Download de CSV exemplo
- Download de CSV vazio (template)

#### 2. 👁️ Aba de Pré-visualização

```python
def _create_preview_tab(self, tab):
    """Aba de pré-visualização com carrossel."""
```

**Componentes**:
- Canvas para preview da pulseira
- Botões "Anterior" e "Próximo"
- Label com informações do paciente
- Frame com dados detalhados

**Funcionalidades**:
- Visualizar pulseira renderizada
- Navegar entre pacientes (carrossel)
- Ver dados do paciente atual
- Atalhos de teclado (← →)

**Layout**:
```
┌────────────────────────────────────┐
│   Preview da Pulseira (Canvas)     │
│                                    │
│  ┌──────────────────────────────┐ │
│  │     [Imagem da Pulseira]     │ │
│  └──────────────────────────────┘ │
│                                    │
│  ◄ Anterior    1/10    Próximo ►  │
│                                    │
│  Paciente 1/10 - João Silva        │
│  ┌──────────────────────────────┐ │
│  │ Nome: João Silva             │ │
│  │ Carteirinha: 123456          │ │
│  │ Convênio: SUS                │ │
│  └──────────────────────────────┘ │
└────────────────────────────────────┘
```

#### 3. ✏️ Aba do Editor

```python
def _create_editor_tab(self, tab):
    """Aba do editor de layout."""
```

**Componentes**:
- Botão "Abrir Editor de Layout"
- Instruções de uso
- Preview do layout atual

**Funcionalidades**:
- Abrir editor WYSIWYG em nova janela
- Criar layout customizado
- Arrastar elementos
- Configurar propriedades

#### 4. 📤 Aba de Exportação

```python
def _create_export_tab(self, tab):
    """Aba de exportação PNG/PDF."""
```

**Componentes**:
- Botão "Exportar PNG"
- Botão "Exportar PDF"
- Barra de progresso
- Label de status

**Funcionalidades**:
- Exportar todas as pulseiras como PNG
- Exportar todas as pulseiras como PDF
- Mostrar progresso da exportação
- Abrir pasta de saída

**Layout**:
```
┌────────────────────────────────────┐
│  Exportar Pulseiras                │
│                                    │
│  ┌──────────────┐  ┌────────────┐ │
│  │ Exportar PNG │  │ Export PDF │ │
│  └──────────────┘  └────────────┘ │
│                                    │
│  [▓▓▓▓▓▓▓▓▓▓░░░░░░] 60%          │
│  Exportando paciente 6/10...      │
│                                    │
│  ✓ 5 pulseiras exportadas         │
└────────────────────────────────────┘
```

#### 5. ⚙️ Aba de Configurações

```python
def _create_settings_tab(self, tab):
    """Aba de configurações."""
```

**Componentes**:
- Seletor de fonte
- Slider de tamanho de fonte
- Botão "Upload Logo"
- Preview do logo
- Botões de template

**Funcionalidades**:
- Escolher família de fontes
- Ajustar tamanho da fonte
- Carregar logotipo
- Salvar/carregar templates de layout

### Widgets Importantes

```python
# TreeView de dados importados
self.data_tree = ttk.Treeview(...)

# Canvas de preview
self.canvas_preview = tb.Canvas(...)

# Botões de navegação
self.btn_prev = tb.Button(text='◄ Anterior', ...)
self.btn_next = tb.Button(text='Próximo ►', ...)

# Label de status
self.import_status = tb.Label(text='...')
```

### Métodos de Atualização

```python
def update_import_table(self, patients: List[Dict]):
    """Atualiza TreeView com dados importados."""
    
def clear_import_table(self):
    """Limpa TreeView."""
    
def update_export_progress(self, current: int, total: int):
    """Atualiza barra de progresso de exportação."""
```

---

## 📊 sidebar.py - Painel Lateral

### Classe: `SidebarManager`

Gerencia o painel lateral com informações de status em tempo real.

```python
class SidebarManager:
    """Gerencia painel lateral com status e informações."""
    
    def __init__(self, app, sidebar_frame):
        """
        Inicializa gerenciador de sidebar.
        
        Args:
            app: Referência à aplicação principal
            sidebar_frame: Frame do tkinter para o sidebar
        """
```

### Status Exibidos

#### 1. 📊 Status do CSV

```python
self.csv_status = Label(
    text='Nenhum CSV importado',
    foreground='#FF6B6B'  # Vermelho
)
```

**Estados**:
- ❌ Nenhum CSV importado (vermelho)
- ✅ 10 pacientes carregados (verde)

#### 2. 🏥 Status da Pulseira

```python
self.pulseira_status = Label(
    text='Pré-visualização vazia',
    foreground='#868E96'  # Cinza
)
```

**Estados**:
- ⚪ Pré-visualização vazia (cinza)
- ✅ Paciente 1/10 - João Silva (verde)

#### 3. 🔤 Status de Fonte

```python
self.font_status = Label(
    text='Arial 48px',
    foreground='#4C6EF5'  # Azul
)
```

**Formato**: `[Família] [Tamanho]px`

#### 4. 🖼️ Status de Logotipo

```python
self.logo_status = Label(
    text='Não carregado',
    foreground='#868E96'  # Cinza
)
```

**Estados**:
- ❌ Não carregado (cinza)
- ✅ logo_hospital.png (verde)

### Métodos de Atualização

```python
def update_csv_status(self, count: int):
    """
    Atualiza status do CSV.
    
    Args:
        count: Número de pacientes carregados
    """
    if count == 0:
        self.csv_status.config(
            text='Nenhum CSV importado',
            foreground='#FF6B6B'
        )
    else:
        self.csv_status.config(
            text=f'{count} pacientes carregados',
            foreground='#28A745'
        )

def update_preview_status(self, patient_name: str):
    """Atualiza status do preview."""
    
def update_font_status(self, font_family: str, size: int):
    """Atualiza status da fonte."""
    
def update_logo_status(self, filename: str):
    """Atualiza status do logotipo."""
```

### Visual do Sidebar

```
┌─────────────────────┐
│ ℹ️ Informações      │
├─────────────────────┤
│ 📊 CSV              │
│ 10 pacientes        │
│ carregados          │
├─────────────────────┤
│ 🏥 Pulseira         │
│ Paciente 1/10       │
│ João Silva          │
├─────────────────────┤
│ 🔤 Fonte            │
│ Arial 48px          │
├─────────────────────┤
│ 🖼️ Logotipo         │
│ logo_hospital.png   │
└─────────────────────┘
```

---

## 🎬 preview.py - Preview e Carrossel

### Classe: `PreviewManager`

Gerencia a pré-visualização e navegação entre pacientes.

```python
class PreviewManager:
    """Gerencia preview e carrossel de pacientes."""
    
    def __init__(self, app):
        """
        Inicializa gerenciador de preview.
        
        Args:
            app: Referência à aplicação principal
        """
        self.app = app
        self.current_patient_index = 0
        self.tkimg = None  # Referência para PhotoImage
```

### Métodos Principais

#### `update_preview()`

```python
def update_preview(self):
    """
    Atualiza pré-visualização com o paciente atual do carrossel.
    
    Processo:
    1. Valida índice do paciente
    2. Renderiza pulseira do paciente atual
    3. Redimensiona para canvas
    4. Atualiza informações na tela
    5. Habilita/desabilita botões de navegação
    """
```

**Fluxo**:
```
┌─────────────────────┐
│ current_patient_idx │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ patients[idx]       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ render_layout_to_   │
│ image()             │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Resize para canvas  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ PhotoImage + paste  │
└─────────────────────┘
```

#### `next_patient()`

```python
def next_patient(self):
    """
    Navega para o próximo paciente.
    
    - Incrementa current_patient_index
    - Valida limites
    - Atualiza preview
    """
    if self.current_patient_index < len(self.app.patients) - 1:
        self.current_patient_index += 1
        self.update_preview()
```

#### `previous_patient()`

```python
def previous_patient(self):
    """
    Navega para o paciente anterior.
    
    - Decrementa current_patient_index
    - Valida limites
    - Atualiza preview
    """
    if self.current_patient_index > 0:
        self.current_patient_index -= 1
        self.update_preview()
```

#### `_update_preview_data(patient: Dict)`

```python
def _update_preview_data(self, patient: Dict):
    """
    Atualiza dados do paciente exibidos na tela.
    
    Args:
        patient: Dicionário com dados do paciente
        
    Exibe:
    - Nome do paciente
    - Número da carteirinha
    - Data de nascimento
    - Convênio
    - Médico responsável
    - Sexo
    - Data/hora de admissão
    - Observação
    """
```

### Atalhos de Teclado

| Tecla | Ação |
|-------|------|
| `←` | Paciente anterior |
| `→` | Próximo paciente |

### Estados do Carrossel

#### Sem Pacientes
```
┌────────────────────────────┐
│                            │
│  [Canvas vazio/dummy]      │
│                            │
│  ◄ (disabled)  ► (disabled)│
│  Nenhum paciente carregado │
└────────────────────────────┘
```

#### Primeiro Paciente (1/10)
```
┌────────────────────────────┐
│  [Pulseira João Silva]     │
│  ◄ (disabled)  ► (enabled) │
│  Paciente 1/10 - João Silva│
└────────────────────────────┘
```

#### Meio (5/10)
```
┌────────────────────────────┐
│  [Pulseira Ana Pereira]    │
│  ◄ (enabled)   ► (enabled) │
│  Paciente 5/10 - Ana ...   │
└────────────────────────────┘
```

#### Último Paciente (10/10)
```
┌────────────────────────────┐
│  [Pulseira Carlos Santos]  │
│  ◄ (enabled)   ► (disabled)│
│  Paciente 10/10 - Carlos...│
└────────────────────────────┘
```

---

## ✏️ layout_editor.py - Editor WYSIWYG

### Classe: `LayoutEditor`

Editor visual de layout (What You See Is What You Get).

```python
class LayoutEditor:
    """Editor visual de layout (WYSIWYG) para pulseiras."""
    
    def __init__(self, root, layout: LayoutModel, fonts_map: Dict, 
                 logo_image: Optional[Image.Image] = None):
        self.root = root
        self.layout = layout
        self.fonts_map = fonts_map
        self.logo_image = logo_image
        self._dragging = {'id': None, 'offset': (0, 0)}
        self._prop_entries: Dict[str, Any] = {}
```

### Interface do Editor

```
┌──────────────────────────────┬───────────────────┐
│                              │  Propriedades     │
│                              │  ┌─────────────┐  │
│      Canvas de Edição        │  │Item: [▼]    │  │
│                              │  └─────────────┘  │
│  ┌────────────────────────┐  │  Tipo: text      │
│  │ [QR]  Nome: João Silva │  │  ID: txt_nome    │
│  │                        │  │  X: 300          │
│  │  Conv: SUS  Nasc: ... │  │  Y: 50           │
│  │                        │  │  Largura: 0      │
│  └────────────────────────┘  │  Rotação: 0      │
│                              │  Texto: {Nome..} │
│  ┌──────────────────────┐    │  Binding: [▼]   │
│  │ Adicionar Texto      │    │  Fonte: Arial    │
│  │ Adicionar QR         │    │  Tamanho: 48     │
│  │ Remover Selecionado  │    │  Negrito: ☑      │
│  │ Aplicar Alterações   │    │  Cor: #000000    │
│  └──────────────────────┘    │  ┌─────────────┐ │
│                              │  │   Aplicar   │ │
└──────────────────────────────┴──┴─────────────┴─┘
```

### Métodos Principais

#### `open(on_close_callback=None)`

```python
def open(self, on_close_callback=None):
    """
    Abre a janela do editor.
    
    Args:
        on_close_callback: Função chamada ao fechar editor
    """
    win = tb.Toplevel(self.root)
    win.title('Editor de Layout')
    win.geometry('1000x500')
    # ... configuração da interface
```

#### `_editor_render()`

```python
def _editor_render(self):
    """
    Renderiza preview no canvas do editor.
    
    - Limpa canvas
    - Renderiza imagem base
    - Desenha retângulos de seleção
    - Mostra IDs dos itens
    """
```

#### Interação com Mouse

```python
def _editor_on_click(self, evt):
    """
    Handler de clique no canvas.
    
    - Detecta item clicado
    - Marca como selecionado
    - Carrega propriedades
    """

def _editor_on_drag(self, evt):
    """
    Handler de arrastar elemento.
    
    - Move item selecionado
    - Atualiza coordenadas X, Y
    - Renderiza novamente
    """

def _editor_on_release(self, evt):
    """
    Handler de soltar elemento.
    
    - Finaliza arrasto
    - Atualiza propriedades finais
    """
```

#### Gerenciamento de Itens

```python
def _add_text_item(self):
    """
    Adiciona novo item de texto.
    
    - Cria TextItem padrão
    - Adiciona ao layout
    - Renderiza novamente
    """

def _add_qr_item(self):
    """
    Adiciona novo item QR.
    
    - Cria QRItem padrão
    - Adiciona ao layout
    - Renderiza novamente
    """

def _remove_selected_item(self):
    """
    Remove item selecionado.
    
    - Remove do layout.items
    - Limpa seleção
    - Renderiza novamente
    """
```

#### Propriedades

```python
def _prop_load_from_selected(self):
    """
    Carrega propriedades do item selecionado nos campos.
    
    - Pega item atual
    - Preenche entries
    - Atualiza comboboxes
    """

def _prop_apply_to_selected(self):
    """
    Aplica propriedades dos campos ao item selecionado.
    
    - Lê valores dos entries
    - Atualiza item no layout
    - Renderiza novamente
    """
```

### Workflow de Edição

```
1. Usuário clica "Abrir Editor"
   ↓
2. Janela do editor abre
   ↓
3. Layout atual é renderizado no canvas
   ↓
4. Usuário pode:
   - Clicar em item para selecionar
   - Arrastar item para mover
   - Editar propriedades no painel direito
   - Adicionar novos itens (texto/QR)
   - Remover itens
   ↓
5. Ao fechar, layout atualizado é salvo
   ↓
6. Callback é chamado (atualiza preview principal)
```

---

## 📋 menu_manager.py - Menu e Atalhos

### Classe: `MenuManager`

Gerencia a barra de menu e atalhos de teclado.

```python
class MenuManager:
    """Gerencia a barra de menu e atalhos de teclado."""
    
    def __init__(self, app):
        """
        Inicializa gerenciador de menu.
        
        Args:
            app: Referência à aplicação principal
        """
        self.app = app
        self.root = app.root
```

### Estrutura do Menu

```
Barra de Menu
├── 📁 Arquivo
│   ├── Importar CSV (Ctrl+I)
│   ├── Exportar PNG (Ctrl+P)
│   ├── Exportar PDF (Ctrl+D)
│   ├── ─────────────
│   ├── Baixar Exemplo CSV
│   ├── Baixar Modelo Vazio
│   ├── ─────────────
│   └── Sair (Ctrl+Q)
│
├── ✏️ Editar
│   ├── Editor de Layout (Ctrl+L)
│   ├── Configurar Fonte (Ctrl+F)
│   ├── ─────────────
│   └── Upload Logotipo
│
├── 💾 Modelos
│   ├── Salvar Modelo Atual
│   ├── Carregar Modelo
│   ├── ─────────────
│   └── Abrir Pasta de Modelos
│
└── ❓ Ajuda
    ├── Sobre Unipulso
    └── Guia CSV
```

### Atalhos de Teclado

```python
def setup_keyboard_shortcuts(self):
    """Configura atalhos de teclado."""
    
    # Arquivo
    self.root.bind('<Control-i>', lambda e: self.app.import_csv())
    self.root.bind('<Control-p>', lambda e: self.app.export_png())
    self.root.bind('<Control-d>', lambda e: self.app.export_pdf())
    self.root.bind('<Control-q>', lambda e: self.root.quit())
    
    # Editar
    self.root.bind('<Control-l>', lambda e: self.app.open_layout_editor())
    self.root.bind('<Control-f>', lambda e: self.app.open_font_dialog())
    
    # Navegação
    self.root.bind('<Left>', lambda e: self.app.preview_previous_patient())
    self.root.bind('<Right>', lambda e: self.app.preview_next_patient())
```

### Tabela de Atalhos

| Atalho | Ação |
|--------|------|
| `Ctrl+I` | Importar CSV |
| `Ctrl+P` | Exportar PNG |
| `Ctrl+D` | Exportar PDF |
| `Ctrl+L` | Abrir Editor de Layout |
| `Ctrl+F` | Configurar Fonte |
| `Ctrl+Q` | Sair |
| `←` | Paciente Anterior |
| `→` | Próximo Paciente |

---

## 📝 atendimento_form.py - Formulário de Cadastro

### Classe: `AtendimentoForm`

Formulário interativo para cadastro de novos pacientes.

```python
class AtendimentoForm:
    """Formulário interativo para iniciar atendimento de novos pacientes"""
    
    def __init__(self, parent_root, diretorio_dados: str = 'data'):
        """
        Inicializa o formulário de atendimento.
        
        Args:
            parent_root: Janela pai da aplicação
            diretorio_dados: Diretório onde armazenar CSVs
        """
```

### Campos do Formulário

```python
CAMPOS = {
    'Número da carteirinha': {
        'obrigatorio': True, 
        'tipo': 'entry'
    },
    'Nome do paciente': {
        'obrigatorio': True, 
        'tipo': 'entry'
    },
    'Data de nascimento': {
        'obrigatorio': True, 
        'tipo': 'entry', 
        'placeholder': 'DD/MM/AAAA'
    },
    'Nome da mãe': {
        'obrigatorio': True, 
        'tipo': 'entry'
    },
    'Convênio': {
        'obrigatorio': True, 
        'tipo': 'entry'
    },
    'Médico responsável': {
        'obrigatorio': True, 
        'tipo': 'entry'
    },
    'Sexo': {
        'obrigatorio': True, 
        'tipo': 'combobox', 
        'opcoes': ['Masculino', 'Feminino', 'Outro']
    },
    'Data de admissão': {
        'obrigatorio': True, 
        'tipo': 'entry', 
        'placeholder': 'DD/MM/AAAA'
    },
    'Hora de admissão': {
        'obrigatorio': True, 
        'tipo': 'entry', 
        'placeholder': 'HH:MM'
    },
    'Observação': {
        'obrigatorio': False, 
        'tipo': 'text'
    }
}
```

### Interface do Formulário

```
┌──────────────────────────────────┐
│  Formulário de Atendimento       │
├──────────────────────────────────┤
│  Número da carteirinha *         │
│  [________________]              │
│                                  │
│  Nome do paciente *              │
│  [________________]              │
│                                  │
│  Data de nascimento *            │
│  [DD/MM/AAAA____]               │
│                                  │
│  Nome da mãe *                   │
│  [________________]              │
│                                  │
│  Convênio *                      │
│  [________________]              │
│                                  │
│  Médico responsável *            │
│  [________________]              │
│                                  │
│  Sexo *                          │
│  [Masculino ▼]                   │
│                                  │
│  Data de admissão *              │
│  [DD/MM/AAAA____]   [Auto]      │
│                                  │
│  Hora de admissão *              │
│  [HH:MM_________]   [Auto]      │
│                                  │
│  Observação                      │
│  [_______________                │
│   _______________]               │
│                                  │
│  ┌──────┐  ┌──────┐  ┌───────┐ │
│  │Salvar│  │Limpar│  │Cancelar│ │
│  └──────┘  └──────┘  └───────┘ │
└──────────────────────────────────┘
```

### Métodos Principais

#### `abrir_formulario()`

```python
def abrir_formulario(self):
    """
    Abre a janela do formulário de atendimento.
    
    - Cria janela Toplevel
    - Renderiza campos
    - Configura scrolling
    """
```

#### `_criar_campos(container)`

```python
def _criar_campos(self, container):
    """
    Cria campos de entrada dinâmicos baseados em CAMPOS.
    
    Args:
        container: Frame container para os campos
        
    Para cada campo:
    - Cria Label com nome (e * se obrigatório)
    - Cria widget apropriado (Entry, Combobox, Text)
    - Adiciona placeholder se houver
    - Armazena referência em self.campos_entrada
    """
```

#### `_validar_campos()`

```python
def _validar_campos(self) -> bool:
    """
    Valida campos obrigatórios.
    
    Returns:
        True se todos os campos obrigatórios estão preenchidos
        
    - Verifica cada campo obrigatório
    - Mostra mensagem de erro se vazio
    - Retorna False no primeiro erro
    """
```

#### `_salvar_paciente()`

```python
def _salvar_paciente(self):
    """
    Salva paciente no CSV.
    
    Processo:
    1. Valida campos
    2. Coleta dados dos widgets
    3. Adiciona linha no CSV
    4. Mostra confirmação
    5. Limpa formulário (opcional)
    6. Mantém aberto para próximo paciente
    """
```

#### `_limpar_formulario()`

```python
def _limpar_formulario(self):
    """
    Limpa todos os campos do formulário.
    
    - Limpa Entries
    - Reseta Comboboxes
    - Limpa Text widgets
    - Foca no primeiro campo
    """
```

#### `_preencher_data_hora_atual()`

```python
def _preencher_data_hora_atual(self):
    """
    Preenche automaticamente data e hora atuais.
    
    - Data de admissão: DD/MM/AAAA (hoje)
    - Hora de admissão: HH:MM (agora)
    """
```

### Salvamento Incremental

O formulário salva cada paciente diretamente no CSV, permitindo cadastro contínuo:

```python
# Cada salvamento adiciona uma linha
with open(self.arquivo_csv, 'a', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow([dados[col] for col in COLUNAS_CSV])
```

### Workflow de Uso

```
1. Usuário clica "Iniciar Atendimento"
   ↓
2. Formulário abre em nova janela
   ↓
3. Preencher campos obrigatórios (marcados com *)
   ↓
4. Opcional: Clicar "Auto" para data/hora atual
   ↓
5. Clicar "Salvar"
   ↓
6. Sistema valida e salva no CSV
   ↓
7. Confirma salvamento
   ↓
8. Formulário limpa (pronto para próximo)
   ↓
9. Repetir passos 3-8 para mais pacientes
   ↓
10. Fechar janela quando terminar
```

---

## 🎨 Temas e Estilos (ttkbootstrap)

### Tema Padrão

```python
app = tb.Window(themename='flatly')
```

### Bootstyles Disponíveis

| Bootstyle | Cor | Uso |
|-----------|-----|-----|
| `primary` | Azul | Ações principais |
| `success` | Verde | Confirmações |
| `info` | Azul claro | Informações |
| `warning` | Amarelo | Avisos |
| `danger` | Vermelho | Erros/Exclusões |
| `secondary` | Cinza | Ações secundárias |

### Exemplo de Uso

```python
# Botão de importar (ação principal)
btn = tb.Button(
    text='Importar CSV',
    bootstyle='primary',
    command=self.import_csv
)

# Botão de exportar (sucesso)
btn = tb.Button(
    text='Exportar PNG',
    bootstyle='success',
    command=self.export_png
)

# Label de erro
lbl = tb.Label(
    text='Erro ao carregar',
    bootstyle='danger'
)
```

---

## 🔗 Integração entre Componentes

### Fluxo de Dados

```
TabsManager ←→ PreviewManager
     ↓              ↓
     └──→ Aplicação Principal ←──┐
              ↓                    │
          IOManager               │
              ↓                    │
         render_layout         LayoutEditor
```

### Exemplo de Integração

```python
# Na aplicação principal
class PulseiraAppUX:
    def __init__(self, root):
        self.root = root
        self.patients = []
        self.layout = LayoutModel()
        
        # Criar gerenciadores
        self.tabs_manager = TabsManager(self, notebook)
        self.sidebar_manager = SidebarManager(self, sidebar)
        self.preview_manager = PreviewManager(self)
        self.menu_manager = MenuManager(self)
        
    def import_csv(self):
        # Importa dados
        self.patients = IOManager.import_csv()
        
        # Atualiza componentes
        self.tabs_manager.update_import_table(self.patients)
        self.sidebar_manager.update_csv_status(len(self.patients))
        self.preview_manager.update_preview()
```

---

## 📝 Boas Práticas

### 1. Separação de Responsabilidades

Cada classe UI tem uma responsabilidade específica:
- `TabsManager`: Apenas gerencia abas
- `PreviewManager`: Apenas preview/carrossel
- `SidebarManager`: Apenas status lateral

### 2. Comunicação via Callbacks

```python
# Editor notifica mudanças via callback
editor = LayoutEditor(root, layout, fonts_map)
editor.open(on_close_callback=self.on_layout_changed)

def on_layout_changed(self):
    self.preview_manager.update_preview()
```

### 3. Estado Centralizado

Todo o estado fica na aplicação principal:
```python
class PulseiraAppUX:
    self.patients = []        # Lista de pacientes
    self.layout = LayoutModel()  # Layout atual
    self.fonts_map = {}       # Fontes disponíveis
    self.logo_image = None    # Logo carregado
```

### 4. Validação de Dados

Sempre validar antes de processar:
```python
if not self.patients:
    messagebox.showwarning('Aviso', 'Nenhum paciente carregado')
    return
```

---

## 🔗 Links Relacionados

- [Documentação Técnica Completa](../DOCUMENTACAO_TECNICA_COMPLETA.md)
- [Documentação do Módulo Core](CORE_MODULE.md)
- [Guia de CSV](../GUIA_CSV.md)

---

**Versão**: 1.0.0  
**Última Atualização**: Janeiro 2026
