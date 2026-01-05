"""
Módulo de renderização de pulseiras
"""

from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

from .config import (
    P_WIDTH, P_HEIGHT, NP_START_PX, SPACING_PX,
    cm_to_px, EXPECTED_COLUMNS, PRINTABLE_W_PX  # Importa a largura da área imprimível
)
from .models import TextItem, QRItem, LayoutModel
from utils import generate_qr_image, get_font, wrap_text


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
        PIL Image da pulseira
    """
    from utils import choose_font_file_for_family
    
    print(f"[DEBUG] Fonts received: {fonts}")
    
    # Cria a imagem base da pulseira (fundo branco, modo RGB para cores)
    base = Image.new('RGB', (P_WIDTH, P_HEIGHT), (255, 255, 255))
    draw = ImageDraw.Draw(base)  # Objeto para desenhar formas e textos na imagem

    # Define a largura da área imprimível (área útil onde os dados são renderizados)
    PRINTABLE_WIDTH_CM = 11  # 11cm é o padrão para pulseiras Zebra ZD230
    PRINTABLE_W_PX = cm_to_px(PRINTABLE_WIDTH_CM)  # Converte de cm para pixels (1299px)

    # Calcula os limites da área imprimível (região onde dados serão renderizados)
    printable_left = NP_START_PX  # Margem esquerda (295px = 2.5cm)
    printable_top = 0  # Começa no topo da pulseira
    printable_right = printable_left + PRINTABLE_W_PX  # Fim da área útil (295 + 1299 = 1594px)
    
    # Desenha borda retangular ao redor da área imprimível (referência visual)
    try:
        border_width = 3  # Borda de 3 pixels de espessura
        draw.rectangle(
            [(printable_left, printable_top), (printable_right - 1, P_HEIGHT - 1)],
            outline=(0, 0, 0), width=border_width  # Borda preta
        )
    except Exception as e:
        print(f"[ERROR] Falha ao desenhar a borda da área imprimível: {e}")

    # ============================================================
    # ÁREA 1 (ESQUERDA): QR CODE com número da carteirinha
    # ============================================================
    # Tamanho do QR: altura da pulseira menos margens superior/inferior (0.1cm cada)
    qr_side_px = int(P_HEIGHT - 2 * cm_to_px(0.1))  # ~216 pixels (quadrado)
    # Gera QR code com o número da carteirinha do paciente
    qr_img = generate_qr_image(patient_data.get('Número da carteirinha', ''), qr_side_px)
    # Posiciona QR: margem de 0.1cm da borda esquerda da área imprimível
    qr_x = printable_left + cm_to_px(0.1)
    qr_y = int((P_HEIGHT - qr_side_px) / 2)  # Centralizado verticalmente
    base.paste(qr_img, (qr_x, qr_y))  # Cola o QR code na imagem base

    # ============================================================
    # ÁREA 2 (CENTRO): Informações do Paciente (nome, dados, etc.)
    # ============================================================
    # Calcula área central disponível entre QR code e logo
    centro_left = qr_x + qr_side_px + cm_to_px(0.3)  # 0.3cm de margem após o QR
    centro_right = printable_right - cm_to_px(0.3)  # 0.3cm de margem antes da logo/borda
    
    # ============================================================
    # ÁREA 3 (DIREITA): LOGO do hospital/instituição
    # ============================================================
    if logo_image:  # Se um logotipo foi fornecido  # Se um logotipo foi fornecido
        # Define dimensões máximas para o logo (canto direito da pulseira)
        logo_width = int(cm_to_px(2.5))  # Largura máxima: 2.5cm (~295px)
        logo_height = int(P_HEIGHT - cm_to_px(0.2))  # Altura: total menos margens (0.1cm × 2)
        
        # Redimensiona logo mantendo proporção (thumbnail não distorce)
        logo_resized = logo_image.copy()
        logo_resized.thumbnail((logo_width, logo_height), Image.Resampling.LANCZOS)  # LANCZOS = alta qualidade
        
        # Posiciona logo no canto direito da área imprimível
        logo_x = printable_right - logo_width - cm_to_px(0.1)  # 0.1cm da borda direita
        logo_y = int((P_HEIGHT - logo_resized.height) / 2)  # Centralizado verticalmente
        base.paste(logo_resized, (logo_x, logo_y))  # Cola o logo na imagem
        
        # Ajusta área central para não sobrepor o logo (reduz largura disponível)
        centro_right = logo_x - cm_to_px(0.2)  # 0.2cm de margem entre texto e logo
    
    centro_width = centro_right - centro_left
    
    # Centro ABSOLUTO da área central (onde nome e observação ficam)
    centro_absolute_x = int(centro_left + (centro_width // 2))
    
    # Compatibilidade com código antigo
    text_x = centro_left
    text_max_w = centro_width

    print(f"[DEBUG] Centro width: {centro_width}px | Centro absoluto X: {centro_absolute_x}px")

    # Campos do layout - TODOS os campos importantes
    # Labels abreviados para economizar espaço
    fields = [
        ('Nasc', 'Data de nascimento'),
        ('Mãe', 'Nome da mãe'),
        ('Conv', 'Convênio'),
        ('Med', 'Médico responsável'),
        ('Sex', 'Sexo'),
        ('Adm', 'Data de admissão'),
        ('Hora', 'Hora de admissão')
    ]

    # Seleciona fontes locais
    if fonts and isinstance(fonts[0], str):
        reg_path = fonts[0]
        bold_path = fonts[1] if len(fonts) > 1 else None
        base_size = fonts[2] if len(fonts) > 2 else int(cm_to_px(0.35))
        name_size = fonts[4] if len(fonts) > 4 and isinstance(fonts[4], int) else base_size
        no_auto_fit = len(fonts) > 3 and str(fonts[3]).lower() in ("no", "false", "0", "off", "nofit")

        def fits_two_columns(test_font_reg, test_font_bold, test_font_name_bold):
            top_margin = cm_to_px(0.05)
            bottom_margin = cm_to_px(0.05)
            
            name_text = str(patient_data.get('Nome do paciente', '')).strip()
            bbox_name = draw.textbbox((0, 0), name_text, font=test_font_name_bold)
            name_h = bbox_name[3] - bbox_name[1]
            
            number_text = str(patient_data.get('Número da carteirinha', '')).strip()
            number_h = test_font_reg.getbbox('Hg')[3] - test_font_reg.getbbox('Hg')[1] if number_text else 0
            
            extra_text = patient_data.get('Texto adicional') or patient_data.get('Texto Adicional')
            extra_text = str(extra_text).strip() if extra_text else ''
            extra_factor = 2.0
            extra_h = int((test_font_reg.getbbox('Hg')[3] - test_font_reg.getbbox('Hg')[1]) * extra_factor) if extra_text else 0

            avail_h = P_HEIGHT - top_margin - bottom_margin - name_h - SPACING_PX
            if number_h:
                avail_h -= (number_h + SPACING_PX)
            if extra_h:
                avail_h -= (extra_h + SPACING_PX)

            if avail_h <= 0:
                return False

            col_gap = cm_to_px(0.1)
            col_w = int((text_max_w - col_gap) / 2)
            if col_w <= 20:
                return False

            line_h = test_font_reg.getbbox('Hg')[3] - test_font_reg.getbbox('Hg')[1]
            y = 0
            col = 0
            for label, key in fields:
                value = patient_data.get(key, '')
                text = f"{label}: {value}"
                lines = wrap_text(draw, text, test_font_reg, col_w)
                for _ in lines:
                    if y + line_h > avail_h:
                        col += 1
                        y = 0
                        if col >= 2:
                            return False
                    y += line_h + SPACING_PX
            return True

        try:
            NAME_FONT_BOLD_LOCAL = ImageFont.truetype(bold_path or reg_path, size=name_size)
        except Exception:
            NAME_FONT_BOLD_LOCAL = ImageFont.load_default()

        if no_auto_fit:
            try:
                FONT_REGULAR_LOCAL = ImageFont.truetype(reg_path, size=base_size)
                FONT_BOLD_LOCAL = ImageFont.truetype(bold_path or reg_path, size=base_size)
            except Exception:
                FONT_REGULAR_LOCAL = ImageFont.load_default()
                FONT_BOLD_LOCAL = FONT_REGULAR_LOCAL
            print(f"[DEBUG] Applied font size (no auto-fit exact): {base_size}; name={name_size}")
        else:
            size = base_size
            while size >= 6:
                try:
                    fr_try = ImageFont.truetype(reg_path, size=size)
                    fb_try = ImageFont.truetype(bold_path or reg_path, size=size)
                    fb_name_try = NAME_FONT_BOLD_LOCAL
                except Exception:
                    fr_try = ImageFont.load_default()
                    fb_try = fr_try
                    fb_name_try = NAME_FONT_BOLD_LOCAL

                if fits_two_columns(fr_try, fb_try, fb_name_try):
                    FONT_REGULAR_LOCAL = fr_try
                    FONT_BOLD_LOCAL = fb_try
                    print(f"[DEBUG] Applied font size (auto-fit): {size}; name={name_size}")
                    break
                size -= 1
            else:
                FONT_REGULAR_LOCAL = ImageFont.load_default()
                FONT_BOLD_LOCAL = FONT_REGULAR_LOCAL

        try:
            _ = NAME_FONT_BOLD_LOCAL
        except NameError:
            try:
                NAME_FONT_BOLD_LOCAL = ImageFont.truetype(bold_path or reg_path, size=name_size)
            except Exception:
                NAME_FONT_BOLD_LOCAL = ImageFont.load_default()
    else:
        if fonts and not isinstance(fonts[0], str):
            FONT_REGULAR_LOCAL = fonts[0]
            FONT_BOLD_LOCAL = fonts[1] if len(fonts) > 1 else fonts[0]
        else:
            from .config import FONT_REGULAR, FONT_BOLD
            FONT_REGULAR_LOCAL = FONT_REGULAR
            FONT_BOLD_LOCAL = FONT_BOLD
        NAME_FONT_BOLD_LOCAL = FONT_BOLD_LOCAL

    # ============================================================
    # RENDERIZAÇÃO DO NOME (centralizado na área central)
    # ============================================================
    top_margin = cm_to_px(0.1)
    
    name_text = str(patient_data.get('Nome do paciente', '')).strip()
    name_bbox = draw.textbbox((0, 0), name_text, font=NAME_FONT_BOLD_LOCAL)
    name_w = name_bbox[2] - name_bbox[0]
    name_h = name_bbox[3] - name_bbox[1]
    
    # ✅ Nome CENTRALIZADO na área CENTRAL (não na área imprimível total)
    name_x = int(centro_absolute_x - (name_w // 2))
    name_y = top_margin
    
    # Garantir que não ultrapasse limites da área central
    if name_x < centro_left:
        name_x = centro_left
    elif name_x + name_w > centro_right:
        name_x = int(centro_right - name_w)
    
    draw.text((name_x, name_y), name_text, font=NAME_FONT_BOLD_LOCAL, fill=(0, 0, 0))
    
    print(f"[DEBUG] Centro width: {centro_width}px | Centro X: {centro_absolute_x}px | Nome X: {name_x}px")

    # ============================================================
    # OBSERVAÇÃO (logo abaixo do nome, também centralizada)
    # ============================================================
    observacao = patient_data.get('Observação') or patient_data.get('Texto adicional') or patient_data.get('Texto Adicional')
    observacao = str(observacao).strip() if observacao else ''
    obs_h = 0
    
    if observacao:
        obs_bbox = draw.textbbox((0, 0), observacao, font=FONT_REGULAR_LOCAL)
        obs_w = obs_bbox[2] - obs_bbox[0]
        obs_h = obs_bbox[3] - obs_bbox[1]
        
        # ✅ Observação CENTRALIZADA na área central
        obs_x = int(centro_absolute_x - (obs_w // 2))
        obs_y = name_y + name_h + cm_to_px(0.1)
        
        # Garantir limites
        if obs_x < centro_left:
            obs_x = centro_left
        elif obs_x + obs_w > centro_right:
            obs_x = int(centro_right - obs_w)
        
        draw.text((obs_x, obs_y), observacao, font=FONT_REGULAR_LOCAL, fill=(0, 0, 0))
        y_cursor = obs_y + obs_h + cm_to_px(0.2)
    else:
        y_cursor = name_y + name_h + cm_to_px(0.2)

    # ============================================================
    # CAMPOS DE INFORMAÇÃO (layout do PDF)
    # ============================================================
    bottom_margin = cm_to_px(0.1)
    line_height = FONT_REGULAR_LOCAL.getbbox('Hg')[3] - FONT_REGULAR_LOCAL.getbbox('Hg')[1]
    
    # Campos principais (lado esquerdo)
    campos_esquerda = [
        ('Carteirinha', 'Número da carteirinha'),
        ('Convênio', 'Convênio'),
        ('Médico', 'Médico responsável')
    ]
    
    # Campos do lado direito
    campos_direita = [
        ('Mãe', 'Nome da mãe'),
        ('Data/Hora', None)  # Campo especial para juntar data e hora
    ]
    
    # Renderiza campos do lado esquerdo
    y_left = y_cursor
    fields_rendered = []
    for label, key in campos_esquerda:
        value = patient_data.get(key, '')
        if value:
            text = f"{label}: {str(value).strip()}"
            draw.text((centro_left, y_left), text, font=FONT_REGULAR_LOCAL, fill=(0, 0, 0))
            y_left += line_height + cm_to_px(0.05)
            fields_rendered.append(label)
    
    # Renderiza campos do lado direito (alinhados à direita)
    y_right = y_cursor
    for label, key in campos_direita:
        if label == 'Data/Hora':
            # Junta data e hora de admissão
            data = patient_data.get('Data de admissão', '')
            hora = patient_data.get('Hora de admissão', '')
            if data or hora:
                text = f"{data} {hora}".strip()
                if text:
                    bbox = draw.textbbox((0, 0), text, font=FONT_REGULAR_LOCAL)
                    text_w = bbox[2] - bbox[0]
                    x_pos = centro_right - text_w
                    draw.text((x_pos, y_right), text, font=FONT_REGULAR_LOCAL, fill=(0, 0, 0))
                    y_right += line_height + cm_to_px(0.05)
                    fields_rendered.append('Data/Hora')
        else:
            value = patient_data.get(key, '')
            if value:
                text = f"{label}: {str(value).strip()}"
                bbox = draw.textbbox((0, 0), text, font=FONT_REGULAR_LOCAL)
                text_w = bbox[2] - bbox[0]
                x_pos = centro_right - text_w
                draw.text((x_pos, y_right), text, font=FONT_REGULAR_LOCAL, fill=(0, 0, 0))
                y_right += line_height + cm_to_px(0.05)
                fields_rendered.append(label)
    
    print(f"[DEBUG] Campos renderizados: {', '.join(fields_rendered)}")

    # ============================================================
    # ÁREA DA LOGO (já renderizada no início)
    # ============================================================
    # A logo já foi posicionada no início do código

    return base


def render_layout_to_image(
    layout: LayoutModel,
    row: Dict[str, Any],
    fonts_map: Dict[str, List[Tuple[str, str]]],
    logo_image: Optional[Image.Image] = None
) -> Image.Image:
    """
    Renderiza o layout em uma imagem PIL utilizando dados de uma linha CSV.
    
    Args:
        layout: Modelo de layout
        row: Dados de uma linha (dict)
        fonts_map: Mapa de fontes do sistema
        logo_image: Imagem do logotipo (opcional)
        
    Returns:
        PIL Image renderizada
    """
    from utils import choose_font_file_for_family
    
    img = Image.new('RGBA', (layout.width, layout.height), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Área imprimível
    printable_left = NP_START_PX
    printable_right = printable_left + PRINTABLE_W_PX
    draw.rectangle(
        [(printable_left, 0), (printable_right - 1, layout.height - 1)],
        outline=(0, 0, 0), width=3
    )

    def resolve_placeholders(text: str) -> str:
        try:
            return text.format(**row)
        except Exception:
            return text

    # Renderiza itens do layout
    for it in layout.items:
        if it.get('type') == 'text':
            t = TextItem(**{k: it.get(k) for k in TextItem.__dataclass_fields__.keys() if k in it})
            value = ''
            if t.binding and str(t.binding) in row:
                value = str(row.get(str(t.binding), ''))
            elif t.text:
                value = resolve_placeholders(str(t.text))
            
            font = get_font(fonts_map, t.font_family, t.font_size, t.bold, t.italic)
            
            # Quebra de linha se width definido
            if t.width and t.width > 0:
                def wrap_line(text, max_w):
                    words = text.split()
                    if not words:
                        return ['']
                    lines = []
                    cur = words[0]
                    for w in words[1:]:
                        test = cur + ' ' + w
                        bbox = draw.textbbox((0, 0), test, font=font)
                        if bbox[2] - bbox[0] <= max_w:
                            cur = test
                        else:
                            lines.append(cur)
                            cur = w
                    lines.append(cur)
                    return lines
                
                lines = wrap_line(value, t.width)
                line_h = font.getbbox('Hg')[3] - font.getbbox('Hg')[1]
                x = t.x
                for i, ln in enumerate(lines):
                    line_img = Image.new('RGBA', (layout.width, layout.height), (0, 0, 0, 0))
                    line_draw = ImageDraw.Draw(line_img)
                    bbox = line_draw.textbbox((0, 0), ln, font=font)
                    w = bbox[2] - bbox[0]
                    
                    if t.align == 'center' and t.width:
                        x = t.x + max(0, int((t.width - w) / 2))
                    elif t.align == 'right' and t.width:
                        x = t.x + max(0, t.width - w)
                    else:
                        x = t.x
                    
                    y = t.y + i * (line_h + 2)
                    line_draw.text((x, y), ln, font=font, fill=t.color)
                    if t.rotation:
                        line_img = line_img.rotate(-t.rotation, resample=Image.BICUBIC, center=(x, y))
                    img.alpha_composite(line_img)
            else:
                timg = Image.new('RGBA', (layout.width, layout.height), (0, 0, 0, 0))
                tdraw = ImageDraw.Draw(timg)
                bbox = tdraw.textbbox((0, 0), value, font=font)
                w = bbox[2] - bbox[0]
                x = t.x
                if t.align == 'center':
                    x = t.x - w // 2
                elif t.align == 'right':
                    x = t.x - w
                tdraw.text((x, t.y), value, font=font, fill=t.color)
                if t.rotation:
                    timg = timg.rotate(-t.rotation, resample=Image.BICUBIC, center=(t.x, t.y))
                img.alpha_composite(timg)
        
        elif it.get('type') == 'qr':
            q = QRItem(**{k: it.get(k) for k in QRItem.__dataclass_fields__.keys() if k in it})
            data = ''
            if q.binding and str(q.binding) in row:
                data = str(row.get(str(q.binding), ''))
            elif q.data_text:
                data = resolve_placeholders(str(q.data_text))
            if data:
                qr_img = generate_qr_image(data, q.size)
                img.paste(qr_img, (q.x, q.y))

    # Logotipo opcional
    if logo_image:
        logo_area_left = NP_START_PX + PRINTABLE_W_PX
        logo_area_right = layout.width
        logo_area_w = logo_area_right - logo_area_left
        logo_area_h = layout.height
        max_w = int((logo_area_w - cm_to_px(0.2)) * 1.2)
        max_h = int((logo_area_h - cm_to_px(0.2)) * 1.2)
        logo = logo_image.copy()
        logo.thumbnail((max_w, max_h), Image.LANCZOS)
        lx = logo_area_left + cm_to_px(0.05)
        ly = int((logo_area_h - logo.height) / 2)
        img.paste(logo, (lx, ly), logo if logo.mode == 'RGBA' else None)

    return img.convert('RGB')
