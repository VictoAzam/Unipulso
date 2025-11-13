"""
Core module: Núcleo da aplicação Unipulso
Contém modelos, configurações e lógica de renderização e I/O.
"""

from .config import (
    P_WIDTH, P_HEIGHT, EXPECTED_COLUMNS, PREFS_FILE,
    get_templates_dir, cm_to_px, DPI, NP_START_PX, PRINTABLE_W_PX, SPACING_PX
)
from .models import LayoutModel, TextItem, QRItem
from .render import render_layout_to_image
from .io_manager import IOManager

__all__ = [
    'P_WIDTH', 'P_HEIGHT', 'EXPECTED_COLUMNS', 'PREFS_FILE',
    'get_templates_dir', 'cm_to_px', 'DPI',
    'NP_START_PX', 'PRINTABLE_W_PX', 'SPACING_PX',
    'LayoutModel', 'TextItem', 'QRItem',
    'render_layout_to_image',
    'IOManager'
]
