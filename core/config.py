"""
Configurações globais da aplicação Unipulso
"""

import os
from PIL import Image, ImageFont

# ==============================
# Configurações de impressão
# ==============================
DPI = 300  # DPI para geração PNG de alta qualidade
CM_TO_INCH = 1 / 2.54

# Dimensões físicas
PULSEIRA_W_CM = 29.5
PULSEIRA_H_CM = 2.0
NON_PRINTABLE_START_CM = 2.5
PRINTABLE_WIDTH_CM = 11  # Largura da área imprimível em centímetros
SPACING_CM = 0.5

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
    """Converte centímetros para pixels baseado em DPI."""
    return int(round(value_cm * CM_TO_INCH * DPI))

# Dimensões em pixels
P_WIDTH = cm_to_px(PULSEIRA_W_CM)
P_HEIGHT = cm_to_px(PULSEIRA_H_CM)
NP_START_PX = cm_to_px(NON_PRINTABLE_START_CM)
PRINTABLE_W_PX = cm_to_px(PRINTABLE_WIDTH_CM)
SPACING_PX = cm_to_px(SPACING_CM)

# Carrega fontes padrão
try:
    FONT_REGULAR = ImageFont.truetype("Noto Sans.ttf", size=int(cm_to_px(0.35) * FONT_SCALE))
    FONT_BOLD = ImageFont.truetype("Noto Sans-Bold.ttf", size=int(cm_to_px(0.38) * FONT_SCALE))
except Exception:
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
