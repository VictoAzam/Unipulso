"""
Gerador de Pulseiras Hospitalares - Aplicação Desktop
Requisitos implementados:
- GUI com ttkbootstrap (tema bootstrap-like)
- Importação de CSV com colunas esperadas
- Upload de logotipo para área final não imprimível
- Geração de qrcode por número da carteirinha
- Montagem de imagem de pulseira nas dimensões 29.5 x 2 cm
- Respeito das áreas não imprimíveis e imprimível (10 cm) e espaçamento de 0.5 cm
- Exportação para PNG (cada pulseira separada ou todas em uma imagem) e PDF (todas em um arquivo)
- Botões para baixar exemplo.csv e modelo_vazio.csv

Dependências:
- ttkbootstrap
- pillow
- qrcode
- reportlab

Instalação (recomendado):
pip install ttkbootstrap pillow qrcode reportlab

Uso: execute `python gerador_pulseiras.py` e use a interface gráfica.
"""

import io
import csv
import math
import os
import json
from tkinter import filedialog, messagebox
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from PIL import Image, ImageDraw, ImageFont, ImageTk
from datetime import datetime
import qrcode
import textwrap
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas as pdfcanvas
import subprocess

# --- Configurações de impressão e conversão cm->px ---
DPI = 300  # DPI para geração PNG de alta qualidade
CM_TO_INCH = 1 / 2.54

def cm_to_px(value_cm):
    return int(round(value_cm * CM_TO_INCH * DPI))

# Dimensões físicas
PULSEIRA_W_CM = 29.5
PULSEIRA_H_CM = 2.0
NON_PRINTABLE_START_CM = 3.5
PRINTABLE_W_CM = 10.0
SPACING_CM = 0.5

# Conversões em pixels
P_WIDTH = cm_to_px(PULSEIRA_W_CM)
P_HEIGHT = cm_to_px(PULSEIRA_H_CM)
NP_START_PX = cm_to_px(NON_PRINTABLE_START_CM)
PRINTABLE_W_PX = cm_to_px(PRINTABLE_W_CM)
SPACING_PX = cm_to_px(SPACING_CM)

# Fonts (tente localizar fontes do sistema ou fallback)
FONT_SCALE = 12.5  # ajuste aqui (1.0 = 100%, 1.5 = +50%)

try:
    FONT_REGULAR = ImageFont.truetype("Noto Sans.ttf", size=int(cm_to_px(0.35) * FONT_SCALE))
    FONT_BOLD = ImageFont.truetype("Noto Sans-Bold.ttf", size=int(cm_to_px(0.38) * FONT_SCALE))
except Exception:
    FONT_REGULAR = ImageFont.load_default()
    FONT_BOLD = ImageFont.load_default()

# Colunas esperadas
EXPECTED_COLUMNS = [
    'Número da carteirinha',
    'Nome do paciente',
    'Data de nascimento',
    'Nome da mãe',
    'Convênio',
    'Médico responsável',
    'Sexo',
    'Data de admissão',
    'Hora de admissão'
]

# Funções utilitárias

def generate_qr_image(data, size_px):
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


def create_pulseira_image(patient_data, logo_image=None, fonts=None):
    """Gera uma PIL.Image da pulseira a partir dos dados do paciente.
    fonts pode ser:
      - (ImageFontRegular, ImageFontBold)  OR
      - (reg_path, bold_path, base_size_px)  -> nesse caso a função ajusta o tamanho até caber
    """
    print(f"[DEBUG] Fonts received: {fonts}")
    # Cria a imagem base (branco)
    base = Image.new('RGB', (P_WIDTH, P_HEIGHT), (255, 255, 255))
    draw = ImageDraw.Draw(base)

    # Área imprimível
    printable_left = NP_START_PX
    printable_top = 0
    printable_right = printable_left + PRINTABLE_W_PX
    # Borda da área imprimível (contorno)
    try:
        border_width = 3  # px
        # Ajusta -1 para não estourar os limites da imagem
        draw.rectangle(
            [(printable_left, printable_top), (printable_right - 1, P_HEIGHT - 1)],
            outline=(0, 0, 0), width=border_width
        )
    except Exception:
        pass

    # QR
    qr_side_px = int(P_HEIGHT - 2 * cm_to_px(0.1))
    qr_img = generate_qr_image(patient_data.get('Número da carteirinha', ''), qr_side_px)
    qr_x = printable_left + cm_to_px(0.1)
    qr_y = int((P_HEIGHT - qr_side_px) / 2)
    base.paste(qr_img, (qr_x, qr_y))

    # textos
    text_x = qr_x + qr_side_px + SPACING_PX
    text_max_w = printable_right - text_x - cm_to_px(0.1)

    print(f"[DEBUG] Text max width: {text_max_w}")
    # Evita acessar atributo .size em caso de paths (strings)
    try:
        if fonts:
            if isinstance(fonts[0], str):
                base_sz = fonts[2] if len(fonts) > 2 else 'N/A'
                print(f"[DEBUG] Fonts info: paths provided, base_size={base_sz}")
            else:
                # Pode não existir atributo size, então apenas informa o tipo
                print("[DEBUG] Fonts info: ImageFont objects provided")
        else:
            print("[DEBUG] Fonts info: using global defaults")
    except Exception as _e:
        print(f"[DEBUG] Fonts info: error reading fonts -> {_e}")

    # Campos: o Nome será tratado separadamente (centralizado)
    fields = [
        ('Nascimento', 'Data de nascimento'),
        ('Mãe', 'Nome da mãe'),
        ('Convênio', 'Convênio'),
        ('Médico', 'Médico responsável'),
        ('Sexo', 'Sexo'),
        ('Admissão', 'Data de admissão'),
        ('Hora', 'Hora de admissão')
    ]

    def wrap_text(draw_obj, text, font, max_width):
        """Quebra o texto em múltiplas linhas para caber em max_width usando medições do draw_obj."""
        words = text.split()
        if not words:
            return ['']
        lines = []
        cur = words[0]
        for w in words[1:]:
            test = cur + ' ' + w
            bbox = draw_obj.textbbox((0,0), test, font=font)
            if bbox[2] - bbox[0] <= max_width:
                cur = test
            else:
                lines.append(cur)
                cur = w
        lines.append(cur)
        # caso alguma palavra isolada seja maior que max_width, força corte
        for i, ln in enumerate(lines):
            bbox = draw_obj.textbbox((0,0), ln, font=font)
            if bbox[2] - bbox[0] > max_width:
                # corta caracteres até caber
                s = ln
                while draw_obj.textbbox((0,0), s + '...', font=font)[2] - draw_obj.textbbox((0,0), s + '...', font=font)[0] > max_width and len(s) > 1:
                    s = s[:-1]
                lines[i] = s + '...'
        return lines

    # Seleciona fontes locais. Suporta dois formatos em `fonts`.
    if fonts and isinstance(fonts[0], str):
        # caso receive (reg_path, bold_path, base_size)
        reg_path = fonts[0]
        bold_path = fonts[1] if len(fonts) > 1 else None
        base_size = fonts[2] if len(fonts) > 2 else int(cm_to_px(0.35))
        # Nome do paciente com tamanho independente (se fornecido)
        name_size = fonts[4] if len(fonts) > 4 and isinstance(fonts[4], int) else base_size
        # verifica se foi solicitado NÃO auto-ajustar
        no_auto_fit = len(fonts) > 3 and str(fonts[3]).lower() in ("no", "false", "0", "off", "nofit")
        # Função auxiliar para testar se cabe em duas colunas.
        def fits_two_columns(test_font_reg, test_font_bold, test_font_name_bold):
            # Alturas e larguras disponíveis
            top_margin = cm_to_px(0.05)
            bottom_margin = cm_to_px(0.05)
            # Primeiro desenhamos o nome em bold, centralizado na área de texto
            name_text = str(patient_data.get('Nome do paciente', '')).strip()
            name_text = name_text if name_text else ''
            bbox_name = draw.textbbox((0, 0), name_text, font=test_font_name_bold)
            name_h = bbox_name[3] - bbox_name[1]
            # Alturas de linhas adicionais acima das colunas: número + extra + timestamp (estimadas)
            number_text = str(patient_data.get('Número da carteirinha', '')).strip()
            number_text = number_text if number_text else ''
            number_h = test_font_reg.getbbox('Hg')[3] - test_font_reg.getbbox('Hg')[1] if number_text else 0
            extra_text = patient_data.get('Texto adicional') or patient_data.get('Texto Adicional')
            extra_text = str(extra_text).strip() if extra_text else ''
            # texto adicional com fonte aumentada (2.0x da base)
            extra_factor = 2.0
            extra_h = int((test_font_reg.getbbox('Hg')[3] - test_font_reg.getbbox('Hg')[1]) * extra_factor) if extra_text else 0
            ts_text = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            ts_h = test_font_reg.getbbox('Hg')[3] - test_font_reg.getbbox('Hg')[1]

            # Área disponível para demais campos abaixo do nome
            avail_h = P_HEIGHT - top_margin - bottom_margin - name_h - SPACING_PX
            # desconta linhas extras acima das colunas
            if number_h:
                avail_h -= (number_h + SPACING_PX)
            if extra_h:
                avail_h -= (extra_h + SPACING_PX)
            # timestamp ficará abaixo das colunas; não descontar aqui
            if avail_h <= 0:
                return False
            # Duas colunas dentro do espaço de texto
            col_gap = cm_to_px(0.1)
            col_w = int((text_max_w - col_gap) / 2)
            if col_w <= 20:
                return False
            # Simula o empacotamento
            line_h = test_font_reg.getbbox('Hg')[3] - test_font_reg.getbbox('Hg')[1]
            y = 0
            col = 0
            for label, key in fields:
                value = patient_data.get(key, '')
                text = f"{label}: {value}"
                lines = wrap_text(draw, text, test_font_reg, col_w)
                for _ in lines:
                    if y + line_h > avail_h:
                        # próxima coluna
                        col += 1
                        y = 0
                        if col >= 2:
                            return False
                    y += line_h + SPACING_PX
            return True

        # Escolhe tamanho: se no_auto_fit for True, usa exatamente base_size;
        # caso contrário, reduz até caber nas duas colunas.
        # preparar fonte do nome (bold) com tamanho específico
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
            # valida se cabe; se não, não reduz, apenas continuará podendo vazar (com duas colunas)
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
                # fallback
                FONT_REGULAR_LOCAL = ImageFont.load_default()
                FONT_BOLD_LOCAL = FONT_REGULAR_LOCAL
        # garante NAME_FONT_BOLD_LOCAL definido também no ramo no_auto_fit
        try:
            _ = NAME_FONT_BOLD_LOCAL
        except NameError:
            try:
                NAME_FONT_BOLD_LOCAL = ImageFont.truetype(bold_path or reg_path, size=name_size)
            except Exception:
                NAME_FONT_BOLD_LOCAL = ImageFont.load_default()
    else:
        # já recebeu ImageFont objects ou nada
        if fonts and not isinstance(fonts[0], str):
            FONT_REGULAR_LOCAL = fonts[0]
            FONT_BOLD_LOCAL = fonts[1] if len(fonts) > 1 else fonts[0]
        else:
            FONT_REGULAR_LOCAL = FONT_REGULAR
            FONT_BOLD_LOCAL = FONT_BOLD
        # para caso não haja paths, usa a mesma fonte bold para o nome
        NAME_FONT_BOLD_LOCAL = FONT_BOLD_LOCAL

    # Desenho final: nome centralizado e demais campos em duas colunas
    top_margin = cm_to_px(0.05)
    bottom_margin = cm_to_px(0.05)
    col_gap = cm_to_px(0.1)
    col_w = int((text_max_w - col_gap) / 2)
    # Nome (bold) centralizado horizontalmente na área de texto (à direita do QR)
    # Equivalente a uma 'classe CSS' .paciente-nome: estilização independente do restante dos textos
    name_text = str(patient_data.get('Nome do paciente', '')).strip()
    name_text = name_text if name_text else ''
    name_bbox = draw.textbbox((0, 0), name_text, font=NAME_FONT_BOLD_LOCAL)
    name_w = name_bbox[2] - name_bbox[0]
    name_h = name_bbox[3] - name_bbox[1]
    name_x = text_x + max(0, int((text_max_w - name_w) / 2))
    name_y = top_margin
    draw.text((name_x, name_y), name_text, font=NAME_FONT_BOLD_LOCAL, fill=(0, 0, 0))

    # Número da carteirinha (texto) abaixo do nome, destacado
    card_number = str(patient_data.get('Número da carteirinha', '')).strip()
    card_label = f"Carteirinha: {card_number}" if card_number else ''
    number_h = 0
    if card_label:
        nb = draw.textbbox((0, 0), card_label, font=FONT_BOLD_LOCAL)
        number_w = nb[2] - nb[0]
        number_h = nb[3] - nb[1]
        num_x = text_x + max(0, int((text_max_w - number_w) / 2))
        num_y = name_y + name_h + SPACING_PX
        draw.text((num_x, num_y), card_label, font=FONT_BOLD_LOCAL, fill=(0, 0, 0))
    else:
        num_y = name_y + name_h

    # Área para listas abaixo do nome
    # Texto adicional com fonte maior, se existir
    extra_text = patient_data.get('Texto adicional') or patient_data.get('Texto Adicional')
    extra_text = str(extra_text).strip() if extra_text else ''
    extra_factor = 2.0
    extra_h = 0
    y_cursor = (num_y + number_h + SPACING_PX) if card_label else (name_y + name_h + SPACING_PX)
    if extra_text:
        try:
            # criar fonte maior baseada na regular
            if isinstance(FONT_REGULAR_LOCAL, ImageFont.FreeTypeFont):
                size_reg = FONT_REGULAR_LOCAL.size
                extra_font = ImageFont.truetype(FONT_REGULAR_LOCAL.path, size=int(size_reg * extra_factor))
            else:
                extra_font = FONT_BOLD_LOCAL
        except Exception:
            extra_font = FONT_BOLD_LOCAL
        eb = draw.textbbox((0, 0), extra_text, font=extra_font)
        extra_w = eb[2] - eb[0]
        extra_h = eb[3] - eb[1]
        ex = text_x + max(0, int((text_max_w - extra_w) / 2))
        ey = y_cursor
        draw.text((ex, ey), extra_text, font=extra_font, fill=(0, 0, 0))
        y_cursor = ey + extra_h + SPACING_PX

    # Área para listas abaixo do nome/numero/extra
    y_start = y_cursor
    y = y_start
    line_height = FONT_REGULAR_LOCAL.getbbox('Hg')[3] - FONT_REGULAR_LOCAL.getbbox('Hg')[1]
    x_col = text_x  # primeira coluna
    max_y = P_HEIGHT - bottom_margin
    overflowed = False
    for label, key in fields:
        value = patient_data.get(key, '')
        text = f"{label}: {value}"
        lines = wrap_text(draw, text, FONT_REGULAR_LOCAL, col_w)
        for ln in lines:
            if y + line_height > max_y:
                # vai para a segunda coluna
                if x_col == text_x:
                    x_col = text_x + col_w + col_gap
                    y = y_start
                else:
                    overflowed = True
                    break
            draw.text((x_col, y), ln, font=FONT_REGULAR_LOCAL, fill=(0, 0, 0))
            y += line_height + SPACING_PX
        if overflowed:
            break

    # logotipo (não imprimível) — aumentar ~20% e alinhar mais à esquerda
    logo_area_left = printable_left + PRINTABLE_W_PX
    logo_area_right = P_WIDTH
    logo_area_w = logo_area_right - logo_area_left
    logo_area_h = P_HEIGHT

    if logo_image:
        max_w = int((logo_area_w - cm_to_px(0.2)) * 1.2)
        max_h = int((logo_area_h - cm_to_px(0.2)) * 1.2)
        logo = logo_image.copy()
        logo.thumbnail((max_w, max_h), Image.LANCZOS)
        # alinhar à esquerda, com pequena margem
        lx = logo_area_left + cm_to_px(0.05)
        ly = int((logo_area_h - logo.height)/2)
        base.paste(logo, (lx, ly), logo if logo.mode=='RGBA' else None)

    # Timestamp (data/hora da geração) abaixo das colunas, alinhado à direita da área de texto
    ts = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    ts_bbox = draw.textbbox((0, 0), ts, font=FONT_REGULAR_LOCAL)
    ts_w = ts_bbox[2] - ts_bbox[0]
    ts_h = ts_bbox[3] - ts_bbox[1]
    ts_x = text_x + text_max_w - ts_w
    ts_y = P_HEIGHT - bottom_margin - ts_h
    draw.text((ts_x, ts_y), ts, font=FONT_REGULAR_LOCAL, fill=(0, 0, 0))

    return base

def list_system_fonts():
    """Retorna dict: família -> list of (filepath, style)."""
    fonts = {}
    try:
        out = subprocess.check_output(
            ["fc-list", "--format", "%{file}||%{family}||%{style}\\n"],
            stderr=subprocess.DEVNULL
        ).decode('utf-8', errors='ignore')
        for line in out.splitlines():
            parts = line.split("||")
            if len(parts) >= 3:
                path = parts[0].strip()
                family = parts[1].strip()
                style = parts[2].strip()
                for fam in family.split(','):
                    fam = fam.strip()
                    fonts.setdefault(fam, []).append((path, style))
    except Exception:
        # fallback: procura arquivos .ttf/.otf em pastas comuns
        for root in ['/usr/share/fonts', '/usr/local/share/fonts', os.path.expanduser('~/.local/share/fonts'),
                     os.path.expanduser('~/Library/Fonts'), '/Library/Fonts', 'C:\\\\Windows\\\\Fonts']:
            if not os.path.isdir(root):
                continue
            for dirpath, _, files in os.walk(root):
                for f in files:
                    if f.lower().endswith(('.ttf', '.otf')):
                        path = os.path.join(dirpath, f)
                        name = os.path.splitext(f)[0]
                        fonts.setdefault(name, []).append((path, 'Regular'))
    return fonts


def choose_font_file_for_family(fonts_map, family, bold=False, italic=False):
    """Tenta escolher um arquivo de fonte para a família com base em estilo solicitado."""
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

# --- GUI Application ---
class PulseiraApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Gerador de Pulseiras Hospitalares')
        self.logo_image = None
        self.patients = []
        self.prefs_file = os.path.join(os.path.expanduser('~'), '.unipulso_prefs.json')

        # Frame principal
        self.main_frame = tb.Frame(root, padding=10)
        self.main_frame.pack(fill=BOTH, expand=YES)

        # Controles superiores
        ctrl_frame = tb.Frame(self.main_frame)
        ctrl_frame.pack(fill=X, pady=6)

        self.btn_upload_logo = tb.Button(ctrl_frame, text='Upload Logotipo', command=self.upload_logo)
        self.btn_upload_logo.pack(side=LEFT, padx=4)

        self.btn_download_example = tb.Button(ctrl_frame, text='Baixar Exemplo CSV', command=self.save_example_csv)
        self.btn_download_example.pack(side=LEFT, padx=4)

        self.btn_download_empty = tb.Button(ctrl_frame, text='Baixar Modelo CSV (vazio)', command=self.save_empty_csv)
        self.btn_download_empty.pack(side=LEFT, padx=4)

        self.btn_import_csv = tb.Button(ctrl_frame, text='Importar CSV', command=self.import_csv)
        self.btn_import_csv.pack(side=LEFT, padx=4)

        self.btn_export_png = tb.Button(ctrl_frame, text='Exportar PNG', command=self.export_png)
        self.btn_export_png.pack(side=LEFT, padx=4)

        self.btn_export_pdf = tb.Button(ctrl_frame, text='Exportar PDF', command=self.export_pdf)
        self.btn_export_pdf.pack(side=LEFT, padx=4)

        # Preview area
        preview_frame = tb.LabelFrame(self.main_frame, text='Pré-visualização (Primeira pulseira)')
        preview_frame.pack(fill=BOTH, expand=YES, pady=8)

        self.canvas_preview = tb.Canvas(preview_frame, width=int(P_WIDTH/2), height=int(P_HEIGHT/2), background='white')
        self.canvas_preview.pack(padx=6, pady=6)

        # Label status
        self.status_var = tb.StringVar(value='Aguardando importação de CSV...')
        self.status = tb.Label(self.main_frame, textvariable=self.status_var)
        self.status.pack(fill=X, pady=4)

        self.fonts_map = list_system_fonts()
        families = sorted(self.fonts_map.keys())
        # configurações padrão de fonte (tamanho em pixels)
        default_size = int(cm_to_px(0.35) * 1.5)  # ~50% maior por padrão
        # tenta carregar preferências
        self.font_family = families[0] if families else 'Default'
        self.font_size = default_size
        self.name_font_size = 50  # tamanho independente para o Nome (padrão solicitado)
        self.font_bold_flag = False
        self.font_italic_flag = False
        self.auto_fit_enabled = False
        self._load_prefs()
        # fontes PIL carregadas para uso
        self.font_regular = ImageFont.load_default()
        self.font_bold = ImageFont.load_default()
        # paths das fontes (usadas pelo render para auto-ajuste)
        self.font_reg_path = None
        self.font_bold_path = None
        self.update_fonts()

        # botão para configurar fonte
        self.btn_font_config = tb.Button(ctrl_frame, text='Configurar Fonte', command=self.open_font_dialog)
        self.btn_font_config.pack(side=LEFT, padx=4)

    def upload_logo(self):
        # Use tuple of patterns so o file chooser do sistema mostra arquivos corretamente
        path = filedialog.askopenfilename(filetypes=[('Image files', ('*.png','*.jpg','*.jpeg','*.bmp','*.gif')), ('All files', '*.*')])
        if not path:
            return
        try:
            img = Image.open(path).convert('RGBA')
            self.logo_image = img
            self.status_var.set(f'Logotipo carregado: {os.path.basename(path)}')
            self.update_preview()
        except IOError:
            messagebox.showerror('Erro', 'O arquivo de imagem não pôde ser aberto. Verifique o formato.')
        except Exception as e:
            messagebox.showerror('Erro', f'Não foi possível abrir a imagem: {e}')

    def save_example_csv(self):
        example = [
            {
                'Número da carteirinha':'123456',
                'Nome do paciente':'João Silva',
                'Data de nascimento':'1990-05-12',
                'Nome da mãe':'Maria Silva',
                'Convênio':'SUS',
                'Médico responsável':'Dra. Aline',
                'Sexo':'M',
                'Data de admissão':'2025-10-15',
                'Hora de admissão':'14:30'
            },
            {
                'Número da carteirinha':'987654',
                'Nome do paciente':'Ana Pereira',
                'Data de nascimento':'1985-08-01',
                'Nome da mãe':'Clara Pereira',
                'Convênio':'Particular',
                'Médico responsável':'Dr. Bruno',
                'Sexo':'F',
                'Data de admissão':'2025-10-15',
                'Hora de admissão':'15:10'
            }
        ]
        save_path = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV','*.csv')], initialfile='exemplo.csv')
        if not save_path:
            return
        try:
            with open(save_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=EXPECTED_COLUMNS)
                writer.writeheader()
                for r in example:
                    writer.writerow(r)
            messagebox.showinfo('Sucesso', f'Exemplo salvo em {save_path}')
        except Exception as e:
            messagebox.showerror('Erro', str(e))

    def save_empty_csv(self):
        save_path = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV','*.csv')], initialfile='modelo_vazio.csv')
        if not save_path:
            return
        try:
            with open(save_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(EXPECTED_COLUMNS)
            messagebox.showinfo('Sucesso', f'Modelo vazio salvo em {save_path}')
        except Exception as e:
            messagebox.showerror('Erro', str(e))

    def import_csv(self):
        path = filedialog.askopenfilename(filetypes=[('CSV files','*.csv')])
        if not path:
            return
        try:
            with open(path, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                headers = reader.fieldnames
                if not headers or any(col not in headers for col in EXPECTED_COLUMNS):
                    raise ValueError('CSV não contém todas as colunas esperadas.')
                self.patients = [row for row in reader]
            self.status_var.set(f'CSV importado: {os.path.basename(path)} - {len(self.patients)} registros')
            self.update_preview()
        except ValueError as ve:
            messagebox.showerror('Erro', str(ve))
        except Exception as e:
            messagebox.showerror('Erro', f'Falha ao importar CSV: {e}')

    def update_preview(self):
        self.canvas_preview.delete('all')
        if not self.patients:
            self.canvas_preview.create_text(int(self.canvas_preview['width'])//2, int(self.canvas_preview['height'])//2, text='Sem dados. Importe um CSV.', anchor='center')
            return
        patient = self.patients[0]
        # Passa caminhos + tamanho para enable auto-ajuste vertical
        if self.font_reg_path:
            # Quarto argumento: 'auto' habilita auto-fit; 'no' usa tamanho exato
            fonts_arg = (
                self.font_reg_path,
                self.font_bold_path,
                self.font_size,
                'auto' if self.auto_fit_enabled else 'no',
                self.name_font_size,
            )
        else:
            fonts_arg = (self.font_regular, self.font_bold)
        img = create_pulseira_image(patient, logo_image=self.logo_image, fonts=fonts_arg)
        cw = int(self.canvas_preview['width'])
        ch = int(self.canvas_preview['height'])
        img_thumb = img.resize((cw, ch), Image.LANCZOS)
        self.tkimg = ImageTk.PhotoImage(img_thumb)
        self.canvas_preview.create_image(0,0, image=self.tkimg, anchor='nw')

    def export_png(self):
        if not self.patients:
            messagebox.showwarning('Aviso', 'Nenhum paciente importado.')
            return
        save_dir = filedialog.askdirectory()
        if not save_dir:
            return
        # Pergunta se quer um arquivo por pulseira ou único
        choice = messagebox.askquestion('Formato PNG', 'Deseja salvar cada pulseira como arquivo separado? (Sim = separado, Não = único arquivo grande)')
        images = []
        for i, p in enumerate(self.patients):
            if self.font_reg_path:
                fonts_arg = (
                    self.font_reg_path,
                    self.font_bold_path,
                    self.font_size,
                    'auto' if self.auto_fit_enabled else 'no',
                    self.name_font_size,
                )
            else:
                fonts_arg = (self.font_regular, self.font_bold)
            img = create_pulseira_image(p, logo_image=self.logo_image, fonts=fonts_arg)
            images.append((p, img))
            if choice == 'yes':
                fname = os.path.join(save_dir, f"pulseira_{i+1}_{p.get('Número da carteirinha','')}.png")
                img.save(fname, dpi=(DPI,DPI))
        if choice == 'no':
            # junta verticalmente (ou horizontalmente) — faremos vertical stack
            total_h = sum(img.height for _,img in images)
            w = images[0][1].width
            big = Image.new('RGB', (w, total_h), (255,255,255))
            y = 0
            for _,img in images:
                big.paste(img, (0,y))
                y += img.height
            fname = os.path.join(save_dir, 'pulseiras_todas.png')
            big.save(fname, dpi=(DPI,DPI))
        messagebox.showinfo('Sucesso', f'Exportação PNG concluída em {save_dir}')

    def export_pdf(self):
        if not self.patients:
            messagebox.showwarning('Aviso', 'Nenhum paciente importado.')
            return
        # Pergunta se deseja salvar como um único PDF ou vários separados
        choice = messagebox.askquestion('Formato PDF', 'Deseja salvar cada pulseira como PDF separado? (Sim = separados, Não = único PDF)')
        try:
            from reportlab.lib.utils import ImageReader
            if choice == 'yes':
                # Vários arquivos separados
                save_dir = filedialog.askdirectory()
                if not save_dir:
                    return
                for i, p in enumerate(self.patients):
                    if self.font_reg_path:
                        fonts_arg = (
                            self.font_reg_path,
                            self.font_bold_path,
                            self.font_size,
                            'auto' if self.auto_fit_enabled else 'no',
                            self.name_font_size,
                        )
                    else:
                        fonts_arg = (self.font_regular, self.font_bold)
                    img = create_pulseira_image(p, logo_image=self.logo_image, fonts=fonts_arg)
                    buf = io.BytesIO()
                    img.save(buf, format='PNG', dpi=(DPI,DPI))
                    buf.seek(0)
                    pdf_path = os.path.join(save_dir, f"pulseira_{i+1}_{p.get('Número da carteirinha','')}.pdf")
                    c = pdfcanvas.Canvas(pdf_path, pagesize=(P_WIDTH * 72.0 / DPI, P_HEIGHT * 72.0 / DPI))
                    c.drawImage(ImageReader(buf), 0, 0, width=P_WIDTH * 72.0 / DPI, height=P_HEIGHT * 72.0 / DPI)
                    c.showPage()
                    c.save()
                messagebox.showinfo('Sucesso', f'PDFs separados salvos em {save_dir}')
            else:
                # Único arquivo PDF
                save_path = filedialog.asksaveasfilename(defaultextension='.pdf', filetypes=[('PDF','*.pdf')], initialfile='pulseiras.pdf')
                if not save_path:
                    return
                c = pdfcanvas.Canvas(save_path, pagesize=(P_WIDTH * 72.0 / DPI, P_HEIGHT * 72.0 / DPI))
                for p in self.patients:
                    if self.font_reg_path:
                        fonts_arg = (
                            self.font_reg_path,
                            self.font_bold_path,
                            self.font_size,
                            'auto' if self.auto_fit_enabled else 'no',
                            self.name_font_size,
                        )
                    else:
                        fonts_arg = (self.font_regular, self.font_bold)
                    img = create_pulseira_image(p, logo_image=self.logo_image, fonts=fonts_arg)
                    buf = io.BytesIO()
                    img.save(buf, format='PNG', dpi=(DPI,DPI))
                    buf.seek(0)
                    c.drawImage(ImageReader(buf), 0, 0, width=P_WIDTH * 72.0 / DPI, height=P_HEIGHT * 72.0 / DPI)
                    c.showPage()
                c.save()
                messagebox.showinfo('Sucesso', f'PDF salvo em {save_path}')
        except Exception as e:
            messagebox.showerror('Erro', f'Falha ao gerar PDF: {e}')

    def update_fonts(self):
        """Carrega as fontes PIL a partir da família/tamanho/estilo selecionados."""
        try:
            reg_path = choose_font_file_for_family(self.fonts_map, self.font_family, bold=False, italic=self.font_italic_flag)
            bold_path = choose_font_file_for_family(self.fonts_map, self.font_family, bold=self.font_bold_flag, italic=self.font_italic_flag)
            # armazena paths para uso em create_pulseira_image (auto-ajuste)
            self.font_reg_path = reg_path
            self.font_bold_path = bold_path or reg_path
            if reg_path:
                self.font_regular = ImageFont.truetype(reg_path, size=self.font_size)
            else:
                self.font_regular = ImageFont.load_default()
            if bold_path:
                self.font_bold = ImageFont.truetype(bold_path, size=self.font_size)
            else:
                # fallback para regular se não encontrou bold
                self.font_bold = self.font_regular
            # Atualiza status com info da fonte
            self.status_var.set(f'Fonte: {self.font_family} {self.font_size}px (bold={self.font_bold_flag}, italic={self.font_italic_flag})')
            print(f"[DEBUG] Font paths: Regular={self.font_reg_path}, Bold={self.font_bold_path}")
            print(f"[DEBUG] Font size: {self.font_size}, Bold={self.font_bold_flag}, Italic={self.font_italic_flag}")
        except Exception:
            self.font_regular = ImageFont.load_default()
            self.font_bold = ImageFont.load_default()
            self.font_reg_path = None
            self.font_bold_path = None
            self.status_var.set('Fonte: fallback (default)')

    def open_font_dialog(self):
        """Abre diálogo para escolher família, tamanho e estilos."""
        dlg = tb.Toplevel(self.root)
        dlg.title('Configurar fonte')
        dlg.transient(self.root)
        dlg.grab_set()

        tb.Label(dlg, text='Família:').grid(row=0, column=0, sticky='w', padx=6, pady=6)
        families = sorted(self.fonts_map.keys())
        fam_cb = tb.Combobox(dlg, values=families, width=40)
        fam_cb.set(self.font_family)
        fam_cb.grid(row=0, column=1, padx=6, pady=6)

        tb.Label(dlg, text='Tamanho (px):').grid(row=1, column=0, sticky='w', padx=6, pady=6)
        size_sb = tb.Spinbox(dlg, from_=6, to=600, increment=1, width=8)
        size_sb.set(str(self.font_size))
        size_sb.grid(row=1, column=1, sticky='w', padx=6, pady=6)

        # tamanho do nome (independente)
        tb.Label(dlg, text='Tamanho do Nome (px):').grid(row=2, column=0, sticky='w', padx=6, pady=6)
        name_size_sb = tb.Spinbox(dlg, from_=6, to=800, increment=1, width=8)
        name_size_sb.set(str(self.name_font_size))
        name_size_sb.grid(row=2, column=1, sticky='w', padx=6, pady=6)

        bold_var = tb.BooleanVar(value=self.font_bold_flag)
        italic_var = tb.BooleanVar(value=self.font_italic_flag)
        save_default_var = tb.BooleanVar(value=True)
        auto_fit_var = tb.BooleanVar(value=getattr(self, 'auto_fit_enabled', False))
        cb_bold = tb.Checkbutton(dlg, text='Negrito (bold)', variable=bold_var)
        cb_bold.grid(row=3, column=0, padx=6, pady=6)
        cb_italic = tb.Checkbutton(dlg, text='Itálico (italic)', variable=italic_var)
        cb_italic.grid(row=3, column=1, padx=6, pady=6)
        cb_auto = tb.Checkbutton(dlg, text='Auto-ajustar para caber', variable=auto_fit_var)
        cb_auto.grid(row=4, column=0, padx=6, pady=6, sticky='w')
        cb_save = tb.Checkbutton(dlg, text='Salvar como padrão', variable=save_default_var)
        cb_save.grid(row=4, column=1, padx=6, pady=6, sticky='w')

        def apply_and_close():
            self.font_family = fam_cb.get() or self.font_family
            try:
                self.font_size = int(size_sb.get())
            except Exception:
                pass
            try:
                self.name_font_size = int(name_size_sb.get())
            except Exception:
                self.name_font_size = self.font_size
            self.font_bold_flag = bool(bold_var.get())
            self.font_italic_flag = bool(italic_var.get())
            self.auto_fit_enabled = bool(auto_fit_var.get())
            self.update_fonts()
            self.update_preview()
            # salva como padrão, se marcado
            try:
                if save_default_var.get():
                    self._save_prefs()
            except Exception:
                pass
            dlg.destroy()

        btn_frame = tb.Frame(dlg)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=8)
        tb.Button(btn_frame, text='Aplicar', command=apply_and_close).pack(side=LEFT, padx=6)
        tb.Button(btn_frame, text='Cancelar', command=dlg.destroy).pack(side=LEFT, padx=6)

    def _load_prefs(self):
        try:
            if os.path.isfile(self.prefs_file):
                with open(self.prefs_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.font_family = data.get('font_family', self.font_family)
                self.font_size = int(data.get('font_size', self.font_size))
                self.font_bold_flag = bool(data.get('font_bold_flag', self.font_bold_flag))
                self.font_italic_flag = bool(data.get('font_italic_flag', self.font_italic_flag))
                # carrega tamanho do nome, se existir; fallback para font_size
                self.name_font_size = int(data.get('name_font_size', self.name_font_size or self.font_size))
                self.auto_fit_enabled = bool(data.get('auto_fit_enabled', self.auto_fit_enabled))
        except Exception:
            pass

    def _save_prefs(self):
        try:
            data = {
                'font_family': self.font_family,
                'font_size': self.font_size,
                'font_bold_flag': self.font_bold_flag,
                'font_italic_flag': self.font_italic_flag,
                'name_font_size': self.name_font_size,
                'auto_fit_enabled': self.auto_fit_enabled,
            }
            with open(self.prefs_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception:
            pass


if __name__ == '__main__':
    app = tb.Window(themename='flatly')
    PulseiraApp(app)
    app.mainloop()
