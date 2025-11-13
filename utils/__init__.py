"""
Utils module: Funções utilitárias da aplicação Unipulso
Contém helpers para fonts, QR codes e outras operações.
"""

from .helpers import (
    list_system_fonts, get_font, generate_qr_image,
    wrap_text, choose_font_file_for_family
)

try:
    from .zebra_printer import ZebraPrinter, generate_bracelet_zpl, test_printer_connection
    ZEBRA_AVAILABLE = True
except ImportError:
    ZEBRA_AVAILABLE = False
    ZebraPrinter = None
    generate_bracelet_zpl = None
    test_printer_connection = None

__all__ = [
    'list_system_fonts', 'get_font', 'generate_qr_image',
    'wrap_text', 'choose_font_file_for_family',
    'ZebraPrinter', 'generate_bracelet_zpl', 'test_printer_connection',
    'ZEBRA_AVAILABLE'
]
