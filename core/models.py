"""
Modelos de dados (dataclasses) para a aplicação Unipulso
"""

from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any
from .config import P_WIDTH, P_HEIGHT


@dataclass
class TextItem:
    """Representa um elemento de texto no layout."""
    type: str = 'text'
    id: str = ''
    x: int = 0
    y: int = 0
    width: int = 0  # 0 = sem limite
    rotation: float = 0.0
    text: str = ''  # pode conter placeholders {Coluna CSV}
    binding: Optional[str] = None  # se setado, usa o valor da coluna
    font_family: Optional[str] = None
    font_size: int = 32
    bold: bool = False
    italic: bool = False
    color: str = '#000000'
    align: str = 'left'  # left|center|right


@dataclass
class QRItem:
    """Representa um elemento QR code no layout."""
    type: str = 'qr'
    id: str = ''
    x: int = 0
    y: int = 0
    size: int = 100
    data_text: str = ''  # pode conter placeholders {Coluna}
    binding: Optional[str] = None


@dataclass
class LayoutModel:
    """Modelo de layout com lista de itens."""
    width: int = P_WIDTH
    height: int = P_HEIGHT
    items: List[dict] = field(default_factory=list)  # armazenado como dict para serialização

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'LayoutModel':
        """Cria LayoutModel a partir de dicionário."""
        lm = LayoutModel(
            width=data.get('width', P_WIDTH),
            height=data.get('height', P_HEIGHT)
        )
        lm.items = data.get('items', [])
        return lm

    def to_dict(self) -> Dict[str, Any]:
        """Converte LayoutModel para dicionário."""
        return {
            'width': self.width,
            'height': self.height,
            'items': self.items,
        }
