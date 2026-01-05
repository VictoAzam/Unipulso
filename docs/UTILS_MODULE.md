# 📘 Documentação do Módulo Utils (Utilitários)

## Visão Geral

O módulo **utils** contém funções auxiliares e utilitários usados em todo o sistema Unipulso. Inclui funções para manipulação de fontes, geração de QR codes, e impressão em impressoras Zebra.

---

## 📁 Estrutura do Módulo

```
utils/
├── __init__.py          # Exportações do módulo
├── helpers.py           # Funções auxiliares gerais
└── zebra_printer.py     # Impressão em impressoras Zebra
```

---

## 🛠️ helpers.py - Funções Auxiliares

### Importações

```python
import subprocess
import os
from typing import Dict, List, Tuple, Optional
from PIL import Image, ImageFont
import qrcode
from core.config import P_HEIGHT, cm_to_px, FONT_SCALE
```

---

### Função: `generate_qr_image`

Gera uma imagem PIL de QR code.

```python
def generate_qr_image(data: str, size_px: int) -> Image.Image:
    """
    Gera uma imagem PIL de QR code.
    
    Args:
        data: Dados para o QR code (texto)
        size_px: Tamanho em pixels (quadrado)
        
    Returns:
        PIL Image do QR code (RGB)
        
    Examples:
        >>> qr = generate_qr_image("123456", 150)
        >>> qr.size
        (150, 150)
        >>> qr.mode
        'RGB'
    """
    qr = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=0,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
    img = img.resize((size_px, size_px), Image.LANCZOS)
    return img
```

#### Parâmetros do QRCode

| Parâmetro | Valor | Descrição |
|-----------|-------|-----------|
| `version` | 2 | Versão do QR (1-40, maior = mais dados) |
| `error_correction` | M | Nível de correção (L < M < Q < H) |
| `box_size` | 10 | Tamanho de cada "caixa" do QR |
| `border` | 0 | Bordas ao redor (em caixas) |

#### Níveis de Correção de Erro

| Nível | Constante | Recuperação |
|-------|-----------|-------------|
| L | `ERROR_CORRECT_L` | ~7% |
| M | `ERROR_CORRECT_M` | ~15% |
| Q | `ERROR_CORRECT_Q` | ~25% |
| H | `ERROR_CORRECT_H` | ~30% |

---

### Função: `list_system_fonts`

Lista fontes disponíveis da pasta `fonte padrao/`.

```python
def list_system_fonts() -> Dict[str, List[Tuple[str, str]]]:
    """
    Retorna APENAS as fontes da pasta "fonte padrao".
    Não usa mais fontes do sistema - apenas fontes do projeto.
    
    Returns:
        Dicionário {familia: [(path, estilo), ...]}
        
    Examples:
        >>> fonts = list_system_fonts()
        >>> 'Arial' in fonts
        True
        >>> fonts['Arial']
        [('/path/to/Arial-Regular.ttf', 'Regular'),
         ('/path/to/Arial-Bold.ttf', 'Bold')]
    """
    fonts = {}
    
    # Caminho obrigatório para fontes do projeto
    project_fonts_dir = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), 
        'fonte padrao'
    )
    
    if not os.path.isdir(project_fonts_dir):
        print(f"[WARN] Pasta 'fonte padrao' não encontrada")
        return fonts
    
    # Carregar APENAS fontes da pasta "fonte padrao"
    for filename in os.listdir(project_fonts_dir):
        if filename.lower().endswith(('.ttf', '.otf')):
            path = os.path.join(project_fonts_dir, filename)
            
            # Extrair nome da família da fonte
            name = os.path.splitext(filename)[0]
            
            # Detectar estilo pelo nome do arquivo
            style = 'Regular'
            if 'bold' in name.lower():
                style = 'Bold'
            elif 'italic' in name.lower() or 'oblique' in name.lower():
                style = 'Italic'
            elif 'slab' in name.lower():
                style = 'Slab'
            
            # Extrair família base
            family = name.replace('-Bold', '').replace('-Regular', '')\
                        .replace('-Italic', '').replace('Slab', '').strip()
            
            fonts.setdefault(family, []).append((path, style))
            print(f"[INFO] ✓ Fonte carregada: {family} ({style})")
    
    return fonts
```

#### Estrutura Retornada

```python
{
    'Arial': [
        ('C:/Unipulso/fonte padrao/Arial-Regular.ttf', 'Regular'),
        ('C:/Unipulso/fonte padrao/Arial-Bold.ttf', 'Bold')
    ],
    'RobotoSlab': [
        ('C:/Unipulso/fonte padrao/RobotoSlab.ttf', 'Slab')
    ]
}
```

#### Detecção de Estilos

A função detecta estilos baseado no nome do arquivo:

| Padrão no Nome | Estilo Detectado |
|----------------|------------------|
| `*bold*` | Bold |
| `*italic*` | Italic |
| `*oblique*` | Italic |
| `*slab*` | Slab |
| Outros | Regular |

---

### Função: `choose_font_file_for_family`

Escolhe um arquivo de fonte para a família com base no estilo solicitado.

```python
def choose_font_file_for_family(
    fonts_map: Dict[str, List[Tuple[str, str]]],
    family: str,
    bold: bool = False,
    italic: bool = False
) -> Optional[str]:
    """
    Escolhe um arquivo de fonte para a família com base em estilo.
    
    Args:
        fonts_map: Mapa de fontes do sistema (de list_system_fonts)
        family: Família de fontes desejada
        bold: Se quer negrito
        italic: Se quer itálico
        
    Returns:
        Caminho do arquivo de fonte ou None se não encontrado
        
    Examples:
        >>> fonts_map = list_system_fonts()
        >>> choose_font_file_for_family(fonts_map, 'Arial', bold=True)
        'C:/Unipulso/fonte padrao/Arial-Bold.ttf'
    """
    if family not in fonts_map:
        return None
    
    variants = fonts_map[family]
    
    # Procura por estilo específico
    if bold:
        for path, style in variants:
            if 'bold' in style.lower():
                return path
    
    if italic:
        for path, style in variants:
            if 'italic' in style.lower():
                return path
    
    # Fallback para Regular
    for path, style in variants:
        if 'regular' in style.lower():
            return path
    
    # Se não encontrar, retorna o primeiro
    return variants[0][0] if variants else None
```

#### Lógica de Seleção

```
1. Se bold=True:
   → Procura por variante com "bold" no estilo
   
2. Se italic=True:
   → Procura por variante com "italic" no estilo
   
3. Fallback:
   → Procura por "regular"
   → Se não encontrar, usa primeira disponível
```

---

### Função: `get_font`

Obtém uma fonte PIL ImageFont.

```python
def get_font(
    family: str, 
    size: int, 
    bold: bool = False, 
    italic: bool = False
) -> ImageFont:
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
        
    Examples:
        >>> font = get_font('Arial', 48, bold=True)
        >>> font.size
        48
    """
    fonts_map = list_system_fonts()
    
    font_path = choose_font_file_for_family(fonts_map, family, bold, italic)
    
    if font_path and os.path.exists(font_path):
        try:
            return ImageFont.truetype(font_path, size)
        except Exception as e:
            print(f"[WARN] Erro ao carregar fonte {font_path}: {e}")
    
    # Fallback para fonte padrão do sistema
    try:
        return ImageFont.truetype('arial.ttf', size)
    except Exception:
        return ImageFont.load_default()
```

#### Estratégia de Fallback

```
1. Tenta carregar fonte solicitada da pasta "fonte padrao/"
   ↓ (se falhar)
2. Tenta carregar Arial do sistema (arial.ttf)
   ↓ (se falhar)
3. Usa fonte padrão do PIL (bitmap, baixa qualidade)
```

---

### Função: `wrap_text`

Quebra texto em múltiplas linhas para caber na largura máxima.

```python
def wrap_text(text: str, font: ImageFont, max_width: int) -> List[str]:
    """
    Quebra texto em múltiplas linhas para caber na largura máxima.
    
    Args:
        text: Texto a ser quebrado
        font: Fonte PIL
        max_width: Largura máxima em pixels
        
    Returns:
        Lista de linhas
        
    Examples:
        >>> font = get_font('Arial', 32)
        >>> lines = wrap_text('Nome muito longo do paciente', font, 200)
        >>> lines
        ['Nome muito', 'longo do', 'paciente']
    """
    words = text.split()
    lines = []
    current_line = []
    
    for word in words:
        # Testa linha com palavra adicionada
        test_line = ' '.join(current_line + [word])
        bbox = font.getbbox(test_line)
        width = bbox[2] - bbox[0]
        
        if width <= max_width:
            current_line.append(word)
        else:
            # Linha cheia, inicia nova
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
    
    # Adiciona última linha
    if current_line:
        lines.append(' '.join(current_line))
    
    return lines
```

#### Algoritmo de Wrapping

```
Input: "Nome muito longo do paciente"
Max width: 200px
Font: Arial 32px

Processo:
1. words = ['Nome', 'muito', 'longo', 'do', 'paciente']
2. current_line = []

3. Testa "Nome" → 60px → OK
   current_line = ['Nome']

4. Testa "Nome muito" → 150px → OK
   current_line = ['Nome', 'muito']

5. Testa "Nome muito longo" → 230px → EXCEDE!
   → Salva "Nome muito"
   → current_line = ['longo']

6. Testa "longo do" → 120px → OK
   current_line = ['longo', 'do']

7. Testa "longo do paciente" → 210px → EXCEDE!
   → Salva "longo do"
   → current_line = ['paciente']

8. Fim → Salva "paciente"

Output: ['Nome muito', 'longo do', 'paciente']
```

---

## 🖨️ zebra_printer.py - Impressão Zebra

### Classe: `ZebraPrinter`

Gerencia impressão em impressoras Zebra ZD230 via ZPL.

```python
class ZebraPrinter:
    """Classe para gerenciar impressão em impressoras Zebra via ZPL."""
    
    def __init__(self, printer_name: str = "Zebra ZD230"):
        """
        Inicializa o gerenciador da impressora Zebra.
        
        Args:
            printer_name: Nome da impressora instalada no sistema
        """
        self.printer_name = printer_name
        self.system = platform.system()
        
        # Verificar se estamos no Windows
        if self.system == "Windows":
            try:
                import win32print
                self.win32print = win32print
            except ImportError:
                raise ImportError(
                    "Módulo win32print não encontrado. "
                    "Instale com: pip install pywin32"
                )
```

---

### Método: `list_printers`

```python
def list_printers(self) -> List[str]:
    """
    Lista todas as impressoras instaladas no sistema.
    
    Returns:
        Lista com nomes das impressoras
        
    Examples:
        >>> printer = ZebraPrinter()
        >>> printer.list_printers()
        ['Zebra ZD230', 'Microsoft Print to PDF', 'HP LaserJet']
    """
    if self.system == "Windows":
        printers = []
        for printer in self.win32print.EnumPrinters(2):
            printers.append(printer[2])
        return printers
    else:
        # Para Linux, usar CUPS
        try:
            import cups
            conn = cups.Connection()
            return list(conn.getPrinters().keys())
        except ImportError:
            print("[WARN] Módulo cups não encontrado")
            return []
```

---

### Método: `is_printer_available`

```python
def is_printer_available(self) -> bool:
    """
    Verifica se a impressora configurada está disponível.
    
    Returns:
        True se a impressora está disponível
        
    Examples:
        >>> printer = ZebraPrinter("Zebra ZD230")
        >>> printer.is_printer_available()
        True
    """
    available_printers = self.list_printers()
    return self.printer_name in available_printers
```

---

### Método: `send_zpl`

```python
def send_zpl(self, zpl_command: str) -> bool:
    """
    Envia comandos ZPL diretamente para a impressora.
    
    Args:
        zpl_command: Comando ZPL a ser enviado
        
    Returns:
        True se enviado com sucesso, False caso contrário
        
    Examples:
        >>> printer = ZebraPrinter("Zebra ZD230")
        >>> zpl = "^XA^FO50,50^A0N,50,50^FDHello^FS^XZ"
        >>> printer.send_zpl(zpl)
        True
    """
    try:
        if self.system == "Windows":
            return self._send_zpl_windows(zpl_command)
        else:
            return self._send_zpl_linux(zpl_command)
    except Exception as e:
        print(f"[ERROR] Erro ao enviar ZPL: {e}")
        return False
```

#### Comandos ZPL Básicos

```zpl
^XA           ; Início do comando
^FO50,50      ; Posição (Field Origin) X=50, Y=50
^A0N,50,50    ; Fonte (tipo 0, orientação N, altura 50, largura 50)
^FDTexto^FS   ; Dados do campo (Field Data)
^XZ           ; Fim do comando
```

---

### Método: `print_image`

```python
def print_image(self, image: Image.Image, dpi: int = 300) -> bool:
    """
    Imprime uma imagem PIL na impressora Zebra.
    
    Converte a imagem para formato Zebra e envia via ZPL.
    
    Args:
        image: Imagem PIL a ser impressa
        dpi: DPI da imagem (default: 300)
        
    Returns:
        True se impressão foi enviada com sucesso
        
    Examples:
        >>> from PIL import Image
        >>> img = Image.open('pulseira.png')
        >>> printer = ZebraPrinter("Zebra ZD230")
        >>> printer.print_image(img, dpi=300)
        True
    """
    # Converter para P&B (1-bit)
    image_bw = image.convert("1")
    
    # Converter para formato Zebra (GRF)
    grf_data = self._image_to_zebra_grf(image_bw)
    
    # Montar comando ZPL
    width, height = image_bw.size
    zpl = f"^XA^FO0,0^GFA,{len(grf_data)},{len(grf_data)},{width//8},"
    zpl += grf_data
    zpl += "^FS^XZ"
    
    # Enviar para impressora
    return self.send_zpl(zpl)
```

#### Processo de Conversão de Imagem

```
PIL Image (RGB)
    ↓
Convert to 1-bit (P&B)
    ↓
Convert to Zebra GRF format
    ↓
Build ZPL command
    ↓
Send to printer
```

---

### Método: `calibrate`

```python
def calibrate(self) -> bool:
    """
    Executa calibração da impressora.
    
    Envia comando ZPL de calibração automática.
    
    Returns:
        True se calibração foi enviada
        
    Examples:
        >>> printer = ZebraPrinter("Zebra ZD230")
        >>> printer.calibrate()
        True
    """
    # Comando de calibração
    zpl = "~JC"
    return self.send_zpl(zpl)
```

---

### Método Privado: `_image_to_zebra_grf`

```python
def _image_to_zebra_grf(self, image: Image.Image) -> str:
    """
    Converte imagem PIL (1-bit) para formato GRF da Zebra.
    
    Args:
        image: Imagem PIL em modo "1" (P&B)
        
    Returns:
        String com dados GRF em formato hexadecimal
    """
    width, height = image.size
    pixels = image.load()
    
    grf_data = []
    
    for y in range(height):
        row_data = []
        for x in range(0, width, 8):
            byte = 0
            for bit in range(8):
                if x + bit < width:
                    if pixels[x + bit, y] == 0:  # Pixel preto
                        byte |= (1 << (7 - bit))
            row_data.append(f"{byte:02X}")
        grf_data.append(''.join(row_data))
    
    return ''.join(grf_data)
```

#### Algoritmo de Conversão

```
Imagem 8x2 pixels (exemplo):
[■ □ ■ ■ □ □ ■ □]  → Byte: 10110010 → 0xB2
[□ ■ ■ □ ■ ■ □ ■]  → Byte: 01101101 → 0x6D

GRF Output: "B26D"

■ = pixel preto (1)
□ = pixel branco (0)
```

---

## 📊 Exemplos de Uso Completo

### Exemplo 1: Gerar e Salvar Pulseira

```python
from PIL import Image
from utils.helpers import generate_qr_image, get_font, list_system_fonts
from core.render import create_pulseira_image

# Dados do paciente
patient = {
    'Número da carteirinha': '123456',
    'Nome do paciente': 'João Silva',
    'Convênio': 'SUS'
}

# Carregar fontes
fonts_map = list_system_fonts()

# Gerar imagem
image = create_pulseira_image(patient, fonts_map)

# Salvar
image.save('pulseira.png', dpi=(300, 300))
```

### Exemplo 2: Imprimir em Zebra

```python
from PIL import Image
from utils.zebra_printer import ZebraPrinter

# Carregar imagem
image = Image.open('pulseira.png')

# Criar instância da impressora
printer = ZebraPrinter("Zebra ZD230")

# Verificar disponibilidade
if not printer.is_printer_available():
    print("Impressora não encontrada!")
    print("Impressoras disponíveis:")
    for p in printer.list_printers():
        print(f"  - {p}")
else:
    # Calibrar (opcional)
    printer.calibrate()
    
    # Imprimir
    if printer.print_image(image, dpi=300):
        print("Impressão enviada com sucesso!")
    else:
        print("Erro ao imprimir")
```

### Exemplo 3: Gerar QR Code Standalone

```python
from utils.helpers import generate_qr_image

# Gerar QR code
qr = generate_qr_image("123456789", 200)

# Salvar
qr.save('qrcode.png')

# Ou usar em composição
from PIL import Image
base = Image.new('RGB', (400, 400), 'white')
base.paste(qr, (100, 100))
base.save('qr_on_background.png')
```

### Exemplo 4: Wrap de Texto Longo

```python
from utils.helpers import get_font, wrap_text
from PIL import Image, ImageDraw

# Texto longo
text = "Nome muito longo do paciente que precisa quebrar em múltiplas linhas"

# Fonte
font = get_font('Arial', 32)

# Quebrar texto
lines = wrap_text(text, font, max_width=400)

# Desenhar
image = Image.new('RGB', (500, 200), 'white')
draw = ImageDraw.Draw(image)

y = 20
for line in lines:
    draw.text((10, y), line, fill='black', font=font)
    y += 40  # Espaçamento entre linhas

image.save('texto_quebrado.png')
```

---

## 🔧 Troubleshooting

### Problema: Fontes não carregam

**Sintoma**: `[WARN] Pasta 'fonte padrao' não encontrada`

**Solução**:
```python
# Verificar estrutura
import os
print(os.path.exists('fonte padrao/'))
print(os.listdir('fonte padrao/'))

# Adicionar fontes .ttf ou .otf na pasta
```

### Problema: QR Code não escaneia

**Sintoma**: QR code gerado mas não funciona

**Possíveis causas**:
1. Dados muito longos (use QR version maior)
2. Impressão de baixa qualidade (use DPI maior)
3. Correção de erro baixa (use ERROR_CORRECT_H)

**Solução**:
```python
qr = qrcode.QRCode(
    version=4,  # Aumentar versão
    error_correction=qrcode.constants.ERROR_CORRECT_H,  # Máxima correção
    box_size=12,  # Aumentar box_size
    border=4  # Adicionar borda
)
```

### Problema: Impressora Zebra não encontrada

**Sintoma**: `is_printer_available()` retorna `False`

**Solução**:
```python
# Listar impressoras instaladas
printer = ZebraPrinter()
print("Impressoras disponíveis:")
for p in printer.list_printers():
    print(f"  - {p}")

# Usar nome exato
printer = ZebraPrinter("Nome Exato Da Impressora")
```

### Problema: Texto não quebra corretamente

**Sintoma**: Texto sai da área designada

**Solução**:
```python
# Ajustar max_width
max_width = canvas_width - 20  # Margem de 10px de cada lado

# Usar fonte menor se necessário
font_size = 32
while True:
    font = get_font('Arial', font_size)
    lines = wrap_text(text, font, max_width)
    total_height = len(lines) * font_size
    if total_height <= available_height:
        break
    font_size -= 1
```

---

## 🔗 Links Relacionados

- [Documentação Técnica Completa](../DOCUMENTACAO_TECNICA_COMPLETA.md)
- [Documentação do Módulo Core](CORE_MODULE.md)
- [Documentação do Módulo UI](UI_MODULE.md)
- [ZPL Programming Guide](https://www.zebra.com/content/dam/zebra/manuals/printers/common/programming/zpl-zbi2-pm-en.pdf)

---

## 📝 Referências

### Bibliotecas Usadas

- **qrcode**: https://pypi.org/project/qrcode/
- **Pillow (PIL)**: https://pillow.readthedocs.io/
- **pywin32**: https://pypi.org/project/pywin32/ (Windows)
- **pycups**: https://pypi.org/project/pycups/ (Linux)

### ZPL Resources

- **ZPL Manual**: https://www.zebra.com/zpl
- **Online ZPL Viewer**: http://labelary.com/viewer.html
- **ZPL Designer**: https://www.zebra.com/zd

---

**Versão**: 1.0.0  
**Última Atualização**: Janeiro 2026
