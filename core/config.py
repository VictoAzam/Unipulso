"""
Configurações globais da aplicação Unipulso
"""

import os
from PIL import Image, ImageFont

# ==============================
# Configurações de impressão
# ==============================
DPI = 300  # DPI para geração PNG de alta qualidade (300 é padrão profissional)
CM_TO_INCH = 1 / 2.54  # Fator de conversão: 1 cm = 0.3937 polegadas

# Dimensões físicas da pulseira em centímetros
PULSEIRA_W_CM = 29.5  # Largura total da pulseira hospitalar padrão
PULSEIRA_H_CM = 2.0   # Altura da pulseira (2cm é ideal para impressoras Zebra)
NON_PRINTABLE_START_CM = 2.5  # Início da área não-imprimível (margem esquerda)
PRINTABLE_WIDTH_CM = 11  # Largura útil para impressão de dados
SPACING_CM = 0.5  # Espaçamento padrão entre elementos

# ==============================
# Colunas esperadas CSV
# ==============================
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

# ==============================
# Configurações de fonte
# ==============================
FONT_SCALE = 12.5  # ajuste aqui (1.0 = 100%, 1.5 = +50%)

def cm_to_px(value_cm):
    """
    Converte centímetros para pixels baseado em DPI.
    
    Fórmula: pixels = cm × (1/2.54) × DPI
    Exemplo: 29.5cm × 0.3937 × 300 = 3484 pixels
    """
    return int(round(value_cm * CM_TO_INCH * DPI))

# Dimensões em pixels (calculadas automaticamente a partir das medidas em cm)
P_WIDTH = cm_to_px(PULSEIRA_W_CM)  # 3484 pixels (29.5cm × 300 DPI)
P_HEIGHT = cm_to_px(PULSEIRA_H_CM)  # 236 pixels (2cm × 300 DPI)
NP_START_PX = cm_to_px(NON_PRINTABLE_START_CM)  # 295 pixels (início da área não imprimível)
PRINTABLE_W_PX = cm_to_px(PRINTABLE_WIDTH_CM)  # 1299 pixels (área útil de impressão)
SPACING_PX = cm_to_px(SPACING_CM)  # 59 pixels (espaçamento entre elementos)

# Carrega fontes padrão do sistema
try:
    # Tenta carregar Noto Sans (fonte padrão) com tamanho calculado
    FONT_REGULAR = ImageFont.truetype("Noto Sans.ttf", size=int(cm_to_px(0.35) * FONT_SCALE))
    FONT_BOLD = ImageFont.truetype("Noto Sans-Bold.ttf", size=int(cm_to_px(0.38) * FONT_SCALE))
except Exception:
    # Fallback: se Noto Sans não estiver disponível, usa fonte padrão do PIL (bitmap, baixa qualidade)
    FONT_REGULAR = ImageFont.load_default()
    FONT_BOLD = ImageFont.load_default()

# ==============================
# Caminhos de arquivos
# ==============================
PREFS_FILE = os.path.join(os.path.expanduser('~'), '.unipulso_prefs.json')

def get_templates_dir(base_dir: str = None) -> str:
    """Retorna o diretório de templates."""
    if base_dir is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    tdir = os.path.join(base_dir, 'templates')
    os.makedirs(tdir, exist_ok=True)
    return tdir
