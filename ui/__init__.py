"""
UI module: Interface gráfica da aplicação Unipulso
Contém componentes de UI: editor, menu, sidebar, abas e preview.
"""

from .layout_editor import LayoutEditor
from .menu_manager import MenuManager
from .atendimento_form import AtendimentoForm

__all__ = [
    'LayoutEditor',
    'MenuManager',
    'AtendimentoForm'
]
