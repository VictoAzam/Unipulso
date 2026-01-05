"""
Funções utilitárias para a aplicação Unipulso
"""

import subprocess
import os
from typing import Dict, List, Tuple, Optional
from PIL import Image, ImageFont
import qrcode

from core.config import (
    P_HEIGHT, cm_to_px, FONT_SCALE, FONT_REGULAR, FONT_BOLD
)


def generate_qr_image(data: str, size_px: int) -> Image.Image:
    """
    Gera uma imagem PIL de QR code.
    
    Args:
        data: Dados para o QR code (ex: número da carteirinha)
        size_px: Tamanho final do QR em pixels (quadrado)
        
    Returns:
        PIL Image do QR code (RGB, pronto para colar)
    """
    qr = qrcode.QRCode(
        version=2,  # Versão do QR (1-40, maior = mais dados). 2 é suficiente para números
        error_correction=qrcode.constants.ERROR_CORRECT_M,  # Nível M = ~15% de correção de erros
        box_size=10,  # Tamanho de cada "quadradinho" do QR
        border=0,  # Sem borda ao redor (economiza espaço)
    )
    qr.add_data(data)  # Adiciona os dados a serem codificados
    qr.make(fit=True)  # Otimiza o tamanho automaticamente
    # Gera a imagem P&B e converte para RGB (compatível com cola)
    img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
    # Redimensiona para o tamanho exato solicitado (LANCZOS = melhor qualidade)
    img = img.resize((size_px, size_px), Image.LANCZOS)
    return img


def list_system_fonts() -> Dict[str, List[Tuple[str, str]]]:
    """
    ✅ MÓDULO 4 - CORREÇÃO: Retorna APENAS as fontes da pasta "fonte padrao"
    Não usa mais fontes do sistema - apenas as fontes obrigatórias do projeto
    
    Returns:
        Dicionário {família: [(caminho, estilo), ...]}
        Exemplo: {'Arial': [('/path/Arial-Regular.ttf', 'Regular'), ...]}
    """
    fonts = {}  # Dicionário que armazenará as fontes encontradas
    
    # ✅ Caminho obrigatório para fontes do projeto (pasta 'fonte padrao' na raiz)
    project_fonts_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'fonte padrao')
    
    # Verifica se a pasta existe
    if not os.path.isdir(project_fonts_dir):
        print(f"[WARN] Pasta 'fonte padrao' não encontrada em: {project_fonts_dir}")
        return fonts  # Retorna dicionário vazio
    
    # ✅ Carregar APENAS fontes da pasta "fonte padrao" (arquivos .ttf e .otf)
    for filename in os.listdir(project_fonts_dir):
        if filename.lower().endswith(('.ttf', '.otf')):  # Aceita TrueType e OpenType
            path = os.path.join(project_fonts_dir, filename)  # Caminho completo do arquivo
            
            # Extrair nome base do arquivo (sem extensão)
            name = os.path.splitext(filename)[0]  # Ex: "Arial-Bold.ttf" → "Arial-Bold"
            
            # Detectar estilo analisando o nome do arquivo (heurística)
            style = 'Regular'  # Padrão
            if 'bold' in name.lower():
                style = 'Bold'
            elif 'italic' in name.lower() or 'oblique' in name.lower():
                style = 'Italic'
            elif 'slab' in name.lower():
                style = 'Slab'
            
            # Extrair família base removendo sufixos de estilo
            # Ex: "Arial-Bold" → "Arial", "RobotoSlab" → "Roboto"
            family = name.replace('-Bold', '').replace('-Regular', '').replace('-Italic', '').replace('Slab', '').strip()
            
            # Adiciona à lista de fontes (setdefault cria lista vazia se família não existir)
            fonts.setdefault(family, []).append((path, style))
            
            print(f"[INFO] ✓ Fonte carregada: {family} ({style}) - {filename}")
    
    if not fonts:
        print(f"[WARN] Nenhuma fonte encontrada em 'fonte padrao'. Usando fonte padrão do sistema.")
    else:
        print(f"[INFO] ✓ Total de {len(fonts)} família(s) de fontes carregadas da pasta 'fonte padrao'")
    
    return fonts


def choose_font_file_for_family(
    fonts_map: Dict[str, List[Tuple[str, str]]],
    family: str,
    bold: bool = False,
    italic: bool = False
) -> Optional[str]:
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
    entries = fonts_map.get(family, [])
    
    # prioridades de busca
    targets = []
    if bold and italic:
        targets = ['bold italic', 'bolditalic', 'bold oblique']
    elif bold:
        targets = ['bold']
    elif italic:
        targets = ['italic', 'oblique']
    
    # procura correspondência de estilo
    for t in targets:
        for path, style in entries:
            if t in style.lower():
                return path
    
    # se não encontrou, retorna primeiro registro (fallback)
    if entries:
        return entries[0][0]
    
    return None


def get_font(
    fonts_map: Dict[str, List[Tuple[str, str]]],
    family: Optional[str],
    size: int,
    bold: bool = False,
    italic: bool = False
) -> ImageFont.FreeTypeFont:
    """
    Obtém um objeto ImageFont baseado em parâmetros.
    
    Args:
        fonts_map: Mapa de fontes do sistema
        family: Família de fontes (None = padrão)
        size: Tamanho em pixels
        bold: Se quer negrito
        italic: Se quer itálico
        
    Returns:
        Objeto ImageFont (TrueType ou default)
    """
    try:
        if not family:
            return ImageFont.load_default()
        
        path = choose_font_file_for_family(fonts_map, family, bold=bold, italic=italic) or \
               choose_font_file_for_family(fonts_map, family, bold=False, italic=False)
        
        if path:
            return ImageFont.truetype(path, size=size)
    except Exception:
        pass
    
    return ImageFont.load_default()


def wrap_text(
    draw,
    text: str,
    font: ImageFont.FreeTypeFont,
    max_width: int
) -> List[str]:
    """
    Quebra texto em múltiplas linhas para caber em max_width.
    
    Args:
        draw: Objeto PIL ImageDraw
        text: Texto a quebrar
        font: Font PIL
        max_width: Largura máxima em pixels
        
    Returns:
        Lista de linhas quebradas
    """
    words = text.split()
    if not words:
        return ['']
    
    lines = []
    cur = words[0]
    
    for w in words[1:]:
        test = cur + ' ' + w
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_width:
            cur = test
        else:
            lines.append(cur)
            cur = w
    
    lines.append(cur)
    
    # força corte para palavras muito longas
    for i, ln in enumerate(lines):
        bbox = draw.textbbox((0, 0), ln, font=font)
        if bbox[2] - bbox[0] > max_width:
            s = ln
            while draw.textbbox((0, 0), s + '...', font=font)[2] - \
                  draw.textbbox((0, 0), s + '...', font=font)[0] > max_width and len(s) > 1:
                s = s[:-1]
            lines[i] = s + '...'
    
    return lines
