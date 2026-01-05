# 📘 Documentação do Módulo Core

## Visão Geral

O módulo **core** contém a lógica central do sistema Unipulso. É responsável por:

- Configurações globais
- Modelos de dados
- Renderização de pulseiras
- Gerenciamento de I/O (Importação/Exportação)

---

## 📁 Estrutura do Módulo

```
core/
├── __init__.py          # Exportações do módulo
├── config.py            # Configurações globais
├── models.py            # Dataclasses e modelos
├── render.py            # Motor de renderização
└── io_manager.py        # Importação/Exportação
```

---

## 🔧 config.py - Configurações Globais

### Constantes de Impressão

```python
DPI = 300                      # Resolução de impressão
CM_TO_INCH = 1 / 2.54          # Fator de conversão métrico
```

### Dimensões da Pulseira

```python
PULSEIRA_W_CM = 29.5           # Largura total: 29.5cm
PULSEIRA_H_CM = 2.0            # Altura: 2.0cm
NON_PRINTABLE_START_CM = 2.5   # Início área não imprimível
PRINTABLE_WIDTH_CM = 11        # Largura área imprimível
SPACING_CM = 0.5               # Espaçamento padrão
```

### Dimensões em Pixels (Calculadas)

```python
P_WIDTH = cm_to_px(PULSEIRA_W_CM)      # 3484 pixels
P_HEIGHT = cm_to_px(PULSEIRA_H_CM)     # 236 pixels
NP_START_PX = cm_to_px(NON_PRINTABLE_START_CM)  # 295 pixels
PRINTABLE_W_PX = cm_to_px(PRINTABLE_WIDTH_CM)   # 1299 pixels
```

### Colunas Esperadas do CSV

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

### Configurações de Fonte

```python
FONT_SCALE = 12.5              # Escala de ajuste de fonte
FONT_REGULAR = 'Arial'         # Fonte padrão regular
FONT_BOLD = 'Arial'            # Fonte padrão negrito
```

### Função: `cm_to_px(value_cm)`

Converte centímetros para pixels baseado no DPI configurado.

```python
def cm_to_px(value_cm: float) -> int:
    """
    Converte centímetros para pixels baseado em DPI.
    
    Fórmula:
        pixels = cm × (1/2.54) × DPI
    
    Args:
        value_cm: Valor em centímetros
        
    Returns:
        Valor em pixels (arredondado)
        
    Examples:
        >>> cm_to_px(29.5)
        3484
        >>> cm_to_px(2.0)
        236
        >>> cm_to_px(1.0)
        118
    """
    return int(round(value_cm * CM_TO_INCH * DPI))
```

#### Tabela de Conversão Comum

| Centímetros | Pixels (300 DPI) |
|-------------|------------------|
| 0.5 cm      | 59 px            |
| 1.0 cm      | 118 px           |
| 2.0 cm      | 236 px           |
| 2.5 cm      | 295 px           |
| 11.0 cm     | 1299 px          |
| 29.5 cm     | 3484 px          |

---

## 📊 models.py - Modelos de Dados

### Dataclass: `TextItem`

Representa um elemento de texto no layout da pulseira.

```python
@dataclass
class TextItem:
    """Representa um elemento de texto no layout."""
    
    type: str = 'text'                    # Tipo do item (sempre 'text')
    id: str = ''                          # Identificador único
    x: int = 0                            # Posição X (pixels)
    y: int = 0                            # Posição Y (pixels)
    width: int = 0                        # Largura máxima (0 = sem limite)
    rotation: float = 0.0                 # Rotação em graus
    text: str = ''                        # Texto (pode conter placeholders)
    binding: Optional[str] = None         # Nome da coluna CSV para binding
    font_family: Optional[str] = None     # Família da fonte
    font_size: int = 32                   # Tamanho da fonte em pixels
    bold: bool = False                    # Negrito
    italic: bool = False                  # Itálico
    color: str = '#000000'                # Cor em hex
    align: str = 'left'                   # Alinhamento (left|center|right)
```

#### Exemplo de Uso

```python
# Criar item de texto para nome do paciente
nome_item = TextItem(
    id='txt_nome',
    x=300,
    y=50,
    text='{Nome do paciente}',  # Placeholder
    binding='Nome do paciente',  # Coluna CSV
    font_family='Arial',
    font_size=48,
    bold=True,
    align='left'
)
```

#### Placeholders Suportados

O campo `text` pode conter placeholders que são substituídos pelos dados do CSV:

```python
text='{Nome do paciente}'           # → "João Silva"
text='Paciente: {Nome do paciente}' # → "Paciente: João Silva"
text='Cart: {Número da carteirinha}'# → "Cart: 123456"
```

### Dataclass: `QRItem`

Representa um QR code no layout.

```python
@dataclass
class QRItem:
    """Representa um elemento QR code no layout."""
    
    type: str = 'qr'                      # Tipo do item (sempre 'qr')
    id: str = ''                          # Identificador único
    x: int = 0                            # Posição X (pixels)
    y: int = 0                            # Posição Y (pixels)
    size: int = 100                       # Tamanho do QR (pixels)
    data_text: str = ''                   # Dados do QR (pode conter placeholders)
    binding: Optional[str] = None         # Nome da coluna CSV para binding
```

#### Exemplo de Uso

```python
# Criar QR code com número da carteirinha
qr_item = QRItem(
    id='qr_carteirinha',
    x=100,
    y=50,
    size=150,
    binding='Número da carteirinha'  # Vincula à coluna CSV
)
```

### Dataclass: `LayoutModel`

Modelo completo de layout contendo todos os itens.

```python
@dataclass
class LayoutModel:
    """Modelo de layout com lista de itens."""
    
    width: int = P_WIDTH                  # Largura do layout
    height: int = P_HEIGHT                # Altura do layout
    items: List[dict] = field(default_factory=list)  # Lista de itens
```

#### Métodos

##### `from_dict(data: Dict[str, Any]) -> LayoutModel`

Cria um LayoutModel a partir de um dicionário (deserialização).

```python
# Carregar de JSON
import json

with open('templates/custom.json') as f:
    data = json.load(f)
    
layout = LayoutModel.from_dict(data)
```

##### `to_dict() -> Dict[str, Any]`

Converte o LayoutModel para dicionário (serialização).

```python
# Salvar em JSON
layout = LayoutModel()
layout.items.append({
    'type': 'text',
    'id': 'nome',
    'x': 100,
    'y': 50,
    'binding': 'Nome do paciente'
})

with open('templates/custom.json', 'w') as f:
    json.dump(layout.to_dict(), f, indent=2)
```

#### Exemplo de Layout Completo

```python
layout = LayoutModel(
    width=3484,
    height=236,
    items=[
        {
            'type': 'qr',
            'id': 'qr_main',
            'x': 100,
            'y': 43,
            'size': 150,
            'binding': 'Número da carteirinha'
        },
        {
            'type': 'text',
            'id': 'txt_nome',
            'x': 300,
            'y': 50,
            'text': '{Nome do paciente}',
            'binding': 'Nome do paciente',
            'font_size': 48,
            'bold': True
        },
        {
            'type': 'text',
            'id': 'txt_convenio',
            'x': 300,
            'y': 120,
            'text': 'Convênio: {Convênio}',
            'binding': 'Convênio',
            'font_size': 32
        }
    ]
)
```

---

## 🎨 render.py - Motor de Renderização

### Função Principal: `create_pulseira_image`

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
        fonts: Tupla com informações de fonte (reg_path, bold_path, base_size, ...)
        
    Returns:
        PIL Image da pulseira (RGB, 300 DPI)
    """
```

#### Processo de Renderização

1. **Criar imagem base** (branco, P_WIDTH x P_HEIGHT)
2. **Calcular área imprimível**
3. **Determinar layout de colunas** (1 ou 2 colunas)
4. **Renderizar QR code**
5. **Renderizar nome do paciente**
6. **Renderizar campos em colunas**
7. **Renderizar observação**
8. **Aplicar logotipo** (se fornecido)

#### Exemplo de Uso

```python
from PIL import Image
from core import create_pulseira_image
from utils import list_system_fonts

# Dados do paciente
patient = {
    'Número da carteirinha': '123456',
    'Nome do paciente': 'João Silva',
    'Data de nascimento': '01/01/1990',
    'Convênio': 'SUS'
}

# Carregar fontes
fonts_map = list_system_fonts()

# Carregar logo
logo = Image.open('logo/hospital.png')

# Renderizar pulseira
image = create_pulseira_image(patient, fonts_map, logo)

# Salvar
image.save('output/pulseira.png', dpi=(300, 300))
```

### Função: `render_layout_to_image`

Renderiza um layout customizado (criado no editor WYSIWYG).

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
        layout: Modelo de layout com itens
        patient_data: Dados do paciente
        fonts_map: Mapa de fontes do sistema
        logo_image: Logo opcional
        
    Returns:
        PIL Image renderizada
    """
```

#### Exemplo de Uso

```python
# Criar layout customizado
layout = LayoutModel()
layout.items = [
    {
        'type': 'qr',
        'id': 'qr1',
        'x': 50,
        'y': 50,
        'size': 100,
        'binding': 'Número da carteirinha'
    },
    {
        'type': 'text',
        'id': 'nome',
        'x': 200,
        'y': 50,
        'binding': 'Nome do paciente',
        'font_size': 40
    }
]

# Renderizar
image = render_layout_to_image(layout, patient, fonts_map)
```

### Cálculo de Layout Dinâmico

O sistema calcula automaticamente se os campos cabem em 1 ou 2 colunas:

```python
def fits_two_columns(test_font_reg, test_font_bold, test_font_name_bold):
    """
    Verifica se todos os elementos cabem em layout de 2 colunas.
    
    Considera:
    - Altura do nome do paciente
    - Altura do número da carteirinha
    - Altura dos campos (7 campos em 2 colunas)
    - Margens superior e inferior
    - Espaçamentos entre elementos
    
    Returns:
        bool: True se cabe em 2 colunas, False se precisa 1 coluna
    """
```

### Ajuste Automático de Fonte

Se os elementos não cabem, o sistema reduz o tamanho da fonte automaticamente:

```python
# Tenta com tamanho base
font_size = base_size

while not fits_two_columns(...) and font_size > min_size:
    font_size -= 1  # Reduz 1px por vez
    # Recalcula com nova fonte
```

---

## 💾 io_manager.py - Gerenciamento de I/O

### Classe: `IOManager`

Gerencia toda a importação e exportação de dados.

### Método: `import_csv`

```python
@staticmethod
def import_csv(filepath: Optional[str] = None) -> List[Dict[str, str]]:
    """
    Importa dados de arquivo CSV.
    
    Detecta automaticamente o delimitador (vírgula, ponto-e-vírgula ou tab).
    Aceita CSVs com colunas em qualquer ordem e remove espaços em branco.
    
    Args:
        filepath: Caminho do arquivo (se None, abre diálogo)
        
    Returns:
        Lista de dicionários com dados dos pacientes
        
    Raises:
        ValueError: Se colunas obrigatórias estiverem faltando
    """
```

#### Detecção de Delimitador

```python
# Tenta sniffer do CSV
dialect = csv.Sniffer().sniff(sample, delimiters=',;\t')
delimiter = dialect.delimiter

# Se falhar, tenta na ordem:
delimiters = [',', ';', '\t']
for delim in delimiters:
    # Tenta ler com este delimitador
```

#### Validação de Colunas

```python
# Verifica colunas obrigatórias
required = ['Número da carteirinha', 'Nome do paciente']

missing = [col for col in required if col not in headers]
if missing:
    raise ValueError(f"Colunas obrigatórias faltando: {missing}")
```

### Método: `save_example_csv`

```python
@staticmethod
def save_example_csv(filepath: Optional[str] = None) -> bool:
    """
    Salva arquivo CSV de exemplo com 2 pacientes.
    
    Args:
        filepath: Caminho do arquivo (se None, abre diálogo)
        
    Returns:
        True se salvo com sucesso
    """
```

#### Dados do Exemplo

```python
example = [
    {
        'Número da carteirinha': '123456',
        'Nome do paciente': 'João Silva',
        'Data de nascimento': '1990-05-12',
        'Nome da mãe': 'Maria Silva',
        'Convênio': 'SUS',
        'Médico responsável': 'Dra. Aline',
        'Sexo': 'M',
        'Data de admissão': '2025-10-15',
        'Hora de admissão': '14:30',
        'Observação': 'Alergia: Penicilina'
    },
    # ... mais 1 paciente
]
```

### Método: `save_empty_csv`

```python
@staticmethod
def save_empty_csv(filepath: Optional[str] = None) -> bool:
    """
    Salva arquivo CSV vazio (apenas cabeçalho).
    
    Args:
        filepath: Caminho do arquivo (se None, abre diálogo)
        
    Returns:
        True se salvo com sucesso
    """
```

### Método: `export_png`

```python
@staticmethod
def export_png(
    patients: List[Dict[str, Any]],
    output_dir: str,
    layout: LayoutModel,
    fonts_map: Dict,
    logo_image: Optional[Image.Image] = None,
    progress_callback: Optional[callable] = None
) -> bool:
    """
    Exporta pulseiras como arquivos PNG individuais.
    
    Args:
        patients: Lista de pacientes
        output_dir: Diretório de saída
        layout: Layout a ser usado
        fonts_map: Mapa de fontes
        logo_image: Logo opcional
        progress_callback: Função de callback para progresso
        
    Returns:
        True se exportado com sucesso
    """
```

#### Formato de Saída

```
output/
├── paciente_001.png  (João Silva - 123456)
├── paciente_002.png  (Ana Pereira - 987654)
└── paciente_003.png  (...)
```

### Método: `export_pdf`

```python
@staticmethod
def export_pdf(
    patients: List[Dict[str, Any]],
    output_file: str,
    layout: LayoutModel,
    fonts_map: Dict,
    logo_image: Optional[Image.Image] = None,
    progress_callback: Optional[callable] = None
) -> bool:
    """
    Exporta pulseiras como arquivo PDF único.
    
    Cada pulseira ocupa uma página.
    
    Args:
        patients: Lista de pacientes
        output_file: Caminho do arquivo PDF
        layout: Layout a ser usado
        fonts_map: Mapa de fontes
        logo_image: Logo opcional
        progress_callback: Função de callback para progresso
        
    Returns:
        True se exportado com sucesso
    """
```

#### Estrutura do PDF

```
PDF (pulseiras.pdf)
├── Página 1: João Silva (123456)
├── Página 2: Ana Pereira (987654)
└── Página N: ...
```

---

## 🔄 Fluxo de Uso Típico

### 1. Importar Dados

```python
from core.io_manager import IOManager

patients = IOManager.import_csv('data/pacientes.csv')
print(f"Importados {len(patients)} pacientes")
```

### 2. Configurar Layout

```python
from core.models import LayoutModel

# Usar layout padrão ou carregar customizado
layout = LayoutModel()  # Layout padrão

# Ou carregar de arquivo
import json
with open('templates/custom.json') as f:
    layout = LayoutModel.from_dict(json.load(f))
```

### 3. Carregar Fontes e Logo

```python
from utils.helpers import list_system_fonts
from PIL import Image

fonts_map = list_system_fonts()
logo = Image.open('logo/hospital.png')
```

### 4. Renderizar Pulseira Individual

```python
from core.render import render_layout_to_image

patient = patients[0]
image = render_layout_to_image(layout, patient, fonts_map, logo)
image.show()  # Preview
```

### 5. Exportar Todas as Pulseiras

```python
# PNG
IOManager.export_png(
    patients, 
    'output/', 
    layout, 
    fonts_map, 
    logo
)

# PDF
IOManager.export_pdf(
    patients, 
    'output/pulseiras.pdf', 
    layout, 
    fonts_map, 
    logo
)
```

---

## 🧪 Testes e Validação

### Testar Importação de CSV

```python
# Arquivo de teste
test_csv = """Número da carteirinha,Nome do paciente,Convênio
123,João Silva,SUS
456,Ana Pereira,Particular"""

with open('test.csv', 'w') as f:
    f.write(test_csv)

patients = IOManager.import_csv('test.csv')
assert len(patients) == 2
assert patients[0]['Nome do paciente'] == 'João Silva'
```

### Testar Renderização

```python
patient = {'Número da carteirinha': '123', 'Nome do paciente': 'Teste'}
fonts_map = list_system_fonts()

image = create_pulseira_image(patient, fonts_map)
assert image.size == (3484, 236)
assert image.mode == 'RGB'
```

### Testar Exportação

```python
import os

patients = [{'Número da carteirinha': '123', 'Nome do paciente': 'Teste'}]
IOManager.export_png(patients, 'test_output/', layout, fonts_map)

assert os.path.exists('test_output/paciente_001.png')
```

---

## 📝 Notas de Implementação

### Performance

- **Renderização**: ~0.5s por pulseira em hardware médio
- **Exportação PNG**: ~1s por pulseira (inclui I/O)
- **Exportação PDF**: ~2s para 10 pulseiras

### Limitações

- Máximo de 1000 pacientes por exportação (limitação de memória)
- Fontes devem estar em `fonte padrao/`
- Imagens de logo devem ser PNG ou JPEG

### Boas Práticas

1. Sempre validar dados do CSV antes de renderizar
2. Usar callbacks de progresso para exportações longas
3. Testar layout com diferentes tamanhos de texto
4. Manter fontes em diretório dedicado

---

## 🔗 Links Relacionados

- [Documentação Técnica Completa](DOCUMENTACAO_TECNICA_COMPLETA.md)
- [Guia de CSV](GUIA_CSV.md)
- [Arquitetura do Sistema](ARCHITECTURE.md)

---

**Versão**: 1.0.0  
**Última Atualização**: Janeiro 2026
