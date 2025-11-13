"""
Gerador de Pulseiras Hospitalares - Aplicação Desktop

Refatorado para programação modular com separação clara de responsabilidades:
- core/config.py: Configurações e constantes
- core/models.py: Modelos de dados (dataclasses)
- utils/helpers.py: Funções utilitárias
- core/render.py: Renderização de pulseiras
- core/io_manager.py: Importação/exportação (CSV, PNG, PDF)
- ui/layout_editor.py: Editor visual de layout
- app.py: Interface gráfica principal (este arquivo)

Principais recursos:
- Editor de layout com arrastar-soltar (drag & drop)
- Propriedades por elemento: posição, tamanho, rotação, alinhamento, cor, fonte
- Fontes do sistema (varredura local); seleção por item
- Modelos (templates) salvos em JSON e reutilizáveis
- Importação de CSV com mapeamento
- Exportação PNG/PDF com renderização fiel ao layout

Tecnologias:
- GUI: tkinter + ttkbootstrap
- Render: PIL/Pillow
- QR Code: qrcode
- PDF: reportlab
"""

import os
import json
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from dataclasses import asdict

# Importações dos módulos refatorados
from core import (
    P_WIDTH, P_HEIGHT, EXPECTED_COLUMNS, PREFS_FILE,
    get_templates_dir, cm_to_px, LayoutModel, TextItem, QRItem,
    render_layout_to_image, IOManager
)
from utils import list_system_fonts, get_font
from utils.zebra_printer import ZebraPrinter, generate_bracelet_zpl, test_printer_connection
from ui import LayoutEditor, AtendimentoForm


class PulseiraApp:
    """Interface gráfica principal da aplicação Unipulso."""

    def __init__(self, root):
        self.root = root
        self.root.title('Gerador de Pulseiras Hospitalares')
        self.logo_image = None
        self.patients = []
        self.current_patient_index = 0
        self.prefs_file = PREFS_FILE
        self.io_manager = IOManager()
        
        # Inicializar variáveis de status antes de carregar logo
        self.status_var = tb.StringVar(value='Iniciando...')
        
        # Inicializar impressora Zebra
        self.zebra_printer = None
        self.printer_name = "Zebra ZD230"  # Nome padrão
        self._init_zebra_printer()
        
        # Inicializar formulário de atendimento
        self.atendimento_form = AtendimentoForm(root, diretorio_dados='data')
        
        # ✅ MÓDULO 4 - CORREÇÃO: Carregar logo automaticamente da pasta "logo"
        self._carregar_logo_padrao()

        # ========== BARRA DE MENU ==========
        menubar = tb.Menu(root)
        root.config(menu=menubar)
        
        # Menu Arquivo
        menu_arquivo = tb.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="📁 Arquivo", menu=menu_arquivo)
        menu_arquivo.add_command(label="Importar CSV", command=self.import_csv)
        menu_arquivo.add_separator()
        menu_arquivo.add_command(label="Baixar Exemplo CSV", command=self.save_example_csv)
        menu_arquivo.add_command(label="Baixar Modelo CSV (vazio)", command=self.save_empty_csv)
        menu_arquivo.add_separator()
        menu_arquivo.add_command(label="Sair", command=root.quit)
        
        # Menu Exportar
        menu_exportar = tb.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="💾 Exportar", menu=menu_exportar)
        menu_exportar.add_command(label="Exportar PNG", command=self.export_png)
        menu_exportar.add_command(label="Exportar PDF", command=self.export_pdf)
        
        # Menu Impressão
        menu_print = tb.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="🖨️ Impressão", menu=menu_print)
        menu_print.add_command(label="Imprimir Pulseira Atual", command=self.print_current_bracelet)
        menu_print.add_command(label="Imprimir Todas as Pulseiras", command=self.print_all_bracelets)
        menu_print.add_separator()
        menu_print.add_command(label="Teste de Impressão", command=self.print_test)
        menu_print.add_command(label="Configurar Impressora", command=self.configure_printer)
        menu_print.add_separator()
        menu_print.add_command(label="Status da Impressora", command=self.show_printer_status)
        
        # Menu Layout
        menu_layout = tb.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="🎨 Layout", menu=menu_layout)
        menu_layout.add_command(label="Editor de Layout", command=self.open_layout_editor)
        menu_layout.add_command(label="Configurar Fonte Global", command=self.open_font_dialog)
        menu_layout.add_separator()
        menu_layout.add_command(label="Salvar Modelo", command=self.save_template)
        menu_layout.add_command(label="Carregar Modelo", command=self.load_template)
        
        # Menu Configurações
        menu_config = tb.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="⚙️ Configurações", menu=menu_config)
        menu_config.add_command(label="Upload Logotipo", command=self.upload_logo)

        # ========== FRAME PRINCIPAL COM SIDEBAR ==========
        main_container = tb.Frame(root)
        main_container.pack(fill=BOTH, expand=YES)
        
        # Painel lateral esquerdo (informações)
        sidebar = tb.Labelframe(main_container, text="ℹ️ Informações", width=250, bootstyle="info")
        sidebar.pack(side=LEFT, fill=Y, padx=5, pady=5)
        sidebar.pack_propagate(False)
        
        # Informações do CSV
        csv_info_frame = tb.Labelframe(sidebar, text="📊 CSV", bootstyle="primary")
        csv_info_frame.pack(fill=X, padx=5, pady=5)
        
        self.csv_info_var = tb.StringVar(value="Nenhum arquivo importado")
        tb.Label(csv_info_frame, textvariable=self.csv_info_var, wraplength=220).pack(padx=5, pady=5)
        
        # Informações da Logo
        logo_info_frame = tb.Labelframe(sidebar, text="🖼️ Logotipo", bootstyle="primary")
        logo_info_frame.pack(fill=X, padx=5, pady=5)
        
        self.logo_info_var = tb.StringVar(value="Logo padrão")
        tb.Label(logo_info_frame, textvariable=self.logo_info_var, wraplength=220).pack(padx=5, pady=5)
        
        # Informações da Fonte
        font_info_frame = tb.Labelframe(sidebar, text="🔤 Fonte", bootstyle="primary")
        font_info_frame.pack(fill=X, padx=5, pady=5)
        
        self.font_info_var = tb.StringVar(value="Carregando...")
        tb.Label(font_info_frame, textvariable=self.font_info_var, wraplength=220).pack(padx=5, pady=5)
        
        # Informações da Impressora
        printer_info_frame = tb.Labelframe(sidebar, text="🖨️ Impressora", bootstyle="primary")
        printer_info_frame.pack(fill=X, padx=5, pady=5)
        
        self.printer_info_var = tb.StringVar(value="Verificando...")
        tb.Label(printer_info_frame, textvariable=self.printer_info_var, wraplength=220).pack(padx=5, pady=5)
        
        # Ações rápidas na sidebar
        actions_frame = tb.Labelframe(sidebar, text="⚡ Ações Rápidas", bootstyle="success")
        actions_frame.pack(fill=X, padx=5, pady=5)
        
        tb.Button(actions_frame, text="🏥 Novo Atendimento", command=self.iniciar_atendimento, 
                 bootstyle="success").pack(fill=X, padx=5, pady=3)
        tb.Button(actions_frame, text="📥 Importar CSV", command=self.import_csv,
                 bootstyle="primary").pack(fill=X, padx=5, pady=3)
        tb.Button(actions_frame, text="🎨 Editor Layout", command=self.open_layout_editor,
                 bootstyle="info").pack(fill=X, padx=5, pady=3)
        tb.Button(actions_frame, text="🖨️ Imprimir Atual", command=self.print_current_bracelet,
                 bootstyle="warning").pack(fill=X, padx=5, pady=3)
        
        # Área principal (direita) com abas
        self.main_frame = tb.Frame(main_container)
        self.main_frame.pack(side=RIGHT, fill=BOTH, expand=YES, padx=5, pady=5)
        
        # Notebook (abas)
        notebook = tb.Notebook(self.main_frame)
        notebook.pack(fill=BOTH, expand=YES)
        
        # Aba 1: Pré-visualização
        preview_tab = tb.Frame(notebook)
        notebook.add(preview_tab, text="👁️ Pré-visualização")
        
        preview_frame = tb.Labelframe(preview_tab, text='Primeira pulseira do CSV', bootstyle="info")
        preview_frame.pack(fill=BOTH, expand=YES, padx=10, pady=10)

        self.canvas_preview = tb.Canvas(preview_frame, width=int(P_WIDTH/2), height=int(P_HEIGHT/2), 
                                       background='white', relief='sunken', borderwidth=2)
        self.canvas_preview.pack(padx=10, pady=10)
        
        # Controles de navegação
        nav_frame = tb.Frame(preview_frame)
        nav_frame.pack(fill=X, padx=10, pady=5)
        
        tb.Button(nav_frame, text="◀ Anterior", command=self.prev_patient, 
                 bootstyle="secondary").pack(side=LEFT, padx=5)
        self.patient_index_var = tb.StringVar(value="0 / 0")
        tb.Label(nav_frame, textvariable=self.patient_index_var, font=("Segoe UI", 10, "bold")).pack(side=LEFT, padx=20)
        tb.Button(nav_frame, text="Próximo ▶", command=self.next_patient,
                 bootstyle="secondary").pack(side=LEFT, padx=5)
        
        # Aba 2: Exportação
        export_tab = tb.Frame(notebook)
        notebook.add(export_tab, text="💾 Exportação")
        
        export_container = tb.Frame(export_tab)
        export_container.pack(expand=YES)
        
        tb.Label(export_container, text="Exportar Pulseiras", 
                font=("Segoe UI", 16, "bold")).pack(pady=20)
        
        export_buttons_frame = tb.Frame(export_container)
        export_buttons_frame.pack(pady=10)
        
        tb.Button(export_buttons_frame, text="📄 Exportar PNG", command=self.export_png,
                 bootstyle="success-outline", width=25).pack(pady=10)
        tb.Label(export_buttons_frame, text="Gera arquivos PNG individuais", 
                font=("Segoe UI", 9), foreground="gray").pack()
        
        tb.Button(export_buttons_frame, text="📑 Exportar PDF", command=self.export_pdf,
                 bootstyle="danger-outline", width=25).pack(pady=10)
        tb.Label(export_buttons_frame, text="Gera um único arquivo PDF com todas as pulseiras",
                font=("Segoe UI", 9), foreground="gray").pack()
        
        # Aba 3: Impressão
        print_tab = tb.Frame(notebook)
        notebook.add(print_tab, text="🖨️ Impressão")
        
        print_container = tb.Frame(print_tab)
        print_container.pack(expand=YES)
        
        tb.Label(print_container, text="Impressão Direta Zebra ZD230", 
                font=("Segoe UI", 16, "bold")).pack(pady=20)
        
        # Status da impressora
        self.printer_status_frame = tb.Labelframe(print_container, text="Status da Impressora", 
                                                  bootstyle="info")
        self.printer_status_frame.pack(fill=X, padx=40, pady=10)
        
        self.printer_status_label = tb.Label(self.printer_status_frame, text="Verificando...", 
                                            font=("Segoe UI", 10))
        self.printer_status_label.pack(padx=10, pady=10)
        
        # Botões de impressão
        print_buttons_frame = tb.Frame(print_container)
        print_buttons_frame.pack(pady=10)
        
        tb.Button(print_buttons_frame, text="🖨️ Imprimir Pulseira Atual", 
                 command=self.print_current_bracelet,
                 bootstyle="success", width=30).pack(pady=8)
        tb.Label(print_buttons_frame, text="Imprime a pulseira exibida na pré-visualização", 
                font=("Segoe UI", 9), foreground="gray").pack()
        
        tb.Button(print_buttons_frame, text="🖨️ Imprimir Todas as Pulseiras", 
                 command=self.print_all_bracelets,
                 bootstyle="primary", width=30).pack(pady=8)
        tb.Label(print_buttons_frame, text="Imprime todas as pulseiras do CSV carregado",
                font=("Segoe UI", 9), foreground="gray").pack()
        
        tb.Button(print_buttons_frame, text="🧪 Teste de Impressão", 
                 command=self.print_test,
                 bootstyle="warning-outline", width=30).pack(pady=8)
        tb.Label(print_buttons_frame, text="Imprime uma etiqueta de teste",
                font=("Segoe UI", 9), foreground="gray").pack()
        
        tb.Button(print_buttons_frame, text="⚙️ Configurar Impressora", 
                 command=self.configure_printer,
                 bootstyle="info-outline", width=30).pack(pady=8)
        tb.Label(print_buttons_frame, text="Escolhe a impressora e testa conexão",
                font=("Segoe UI", 9), foreground="gray").pack()

        # Barra de status inferior
        status_frame = tb.Frame(root, relief='sunken', borderwidth=1)
        status_frame.pack(side=BOTTOM, fill=X)
        
        self.status_var = tb.StringVar(value='Aguardando importação de CSV...')
        self.status = tb.Label(status_frame, textvariable=self.status_var, anchor='w')
        self.status.pack(side=LEFT, fill=X, expand=YES, padx=5, pady=2)

        # Inicializa fontes e configurações
        self.fonts_map = list_system_fonts()
        families = sorted(self.fonts_map.keys())
        default_size = int(cm_to_px(0.35) * 1.5)
        
        self.font_family = families[0] if families else 'Default'
        self.font_size = default_size
        self.name_font_size = 50
        self.font_bold_flag = False
        self.font_italic_flag = False
        self.auto_fit_enabled = False
        self.current_patient_index = 0
        self._load_prefs()
        
        self.font_regular = None
        self.font_bold = None
        self.font_reg_path = None
        self.font_bold_path = None
        self.update_fonts()

        # Modelo de layout padrão
        self.layout = self._default_layout()
        self.templates_dir = get_templates_dir(os.path.dirname(os.path.abspath(__file__)))
        
        # Atualizar informações da sidebar
        self._update_sidebar_info()

    def _update_sidebar_info(self):
        """Atualiza as informações exibidas na sidebar."""
        # Info CSV
        if self.patients:
            self.csv_info_var.set(f"✓ {len(self.patients)} paciente(s) carregado(s)")
        else:
            self.csv_info_var.set("Nenhum arquivo importado")
        
        # Info Logo
        if self.logo_image:
            self.logo_info_var.set("✓ Logo carregada")
        else:
            self.logo_info_var.set("Sem logo")
        
        # Info Fonte
        self.font_info_var.set(f"{self.font_family}\nTamanho: {self.font_size}px\nNome: {self.name_font_size}px")
        
        # Info Impressora
        if self.zebra_printer and self.zebra_printer.is_printer_available():
            self.printer_info_var.set(f"✓ {self.printer_name}\nConectada")
        else:
            self.printer_info_var.set("✗ Não conectada")
    
    def prev_patient(self):
        """Navega para o paciente anterior."""
        if not self.patients:
            return
        self.current_patient_index = (self.current_patient_index - 1) % len(self.patients)
        self.update_preview()
    
    def next_patient(self):
        """Navega para o próximo paciente."""
        if not self.patients:
            return
        self.current_patient_index = (self.current_patient_index + 1) % len(self.patients)
        self.update_preview()

    def _carregar_logo_padrao(self):
        """
        ✅ MÓDULO 4 - CORREÇÃO: Carrega automaticamente a logo da pasta "logo"
        Não precisa mais fazer upload toda vez - usa a logo padrão do projeto
        """
        try:
            # Caminho da pasta logo
            logo_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logo')
            
            if not os.path.isdir(logo_dir):
                print(f"[WARN] Pasta 'logo' não encontrada em: {logo_dir}")
                return
            
            # Procurar arquivos de imagem na pasta
            for filename in os.listdir(logo_dir):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                    logo_path = os.path.join(logo_dir, filename)
                    
                    # Carregar a logo
                    img = Image.open(logo_path).convert('RGBA')
                    self.logo_image = img
                    
                    print(f"[INFO] ✓ Logo padrão carregada automaticamente: {filename}")
                    self.status_var.set(f'✓ Logo padrão carregada: {filename}')
                    
                    # Usar a primeira imagem encontrada
                    break
            
            if not self.logo_image:
                print(f"[WARN] Nenhuma imagem encontrada na pasta 'logo'")
                
        except Exception as e:
            print(f"[WARN] Erro ao carregar logo padrão: {e}")

    def upload_logo(self):
        """
        Upload e carregamento de logotipo (opcional - sobrescreve a logo padrão).
        A logo padrão já é carregada automaticamente da pasta "logo".
        """
        path = filedialog.askopenfilename(
            filetypes=[('Image files', ('*.png', '*.jpg', '*.jpeg', '*.bmp', '*.gif')), ('All files', '*.*')]
        )
        if not path:
            return
        try:
            img = Image.open(path).convert('RGBA')
            self.logo_image = img
            self.status_var.set(f'✓ Logotipo personalizado carregado: {os.path.basename(path)}')
            self._update_sidebar_info()
            self.update_preview()
        except IOError:
            messagebox.showerror('Erro', 'O arquivo de imagem não pôde ser aberto. Verifique o formato.')
        except Exception as e:
            messagebox.showerror('Erro', f'Não foi possível abrir a imagem: {e}')

    def save_example_csv(self):
        """Salva arquivo CSV de exemplo."""
        self.io_manager.save_example_csv()

    def save_empty_csv(self):
        """Salva arquivo CSV vazio."""
        self.io_manager.save_empty_csv()

    def import_csv(self):
        """Importa dados de arquivo CSV."""
        self.patients = self.io_manager.import_csv()
        if self.patients:
            self.current_patient_index = 0
            self.status_var.set(f'✓ CSV importado: {len(self.patients)} registros')
            self._update_sidebar_info()
            self.update_preview()

    def update_preview(self):
        """Atualiza pré-visualização da pulseira atual."""
        self.canvas_preview.delete('all')
        cw = int(self.canvas_preview['width'])
        ch = int(self.canvas_preview['height'])
        
        if not self.patients:
            dummy = {}
            img = render_layout_to_image(self.layout, dummy, self.fonts_map, logo_image=self.logo_image)
            img_thumb = img.resize((cw, ch), Image.LANCZOS)
            self.tkimg = ImageTk.PhotoImage(img_thumb)
            self.canvas_preview.create_image(0, 0, image=self.tkimg, anchor='nw')
            self.canvas_preview.create_text(cw//2, ch//2, text='Sem dados. Importe um CSV.', 
                                          anchor='center', fill='#333333', font=('Segoe UI', 12))
            self.patient_index_var.set("0 / 0")
            return
        
        # Garantir que o índice está dentro dos limites
        if self.current_patient_index >= len(self.patients):
            self.current_patient_index = 0
        
        patient = self.patients[self.current_patient_index]
        img = render_layout_to_image(self.layout, patient, self.fonts_map, logo_image=self.logo_image)
        img_thumb = img.resize((cw, ch), Image.LANCZOS)
        self.tkimg = ImageTk.PhotoImage(img_thumb)
        self.canvas_preview.create_image(0, 0, image=self.tkimg, anchor='nw')
        
        # Atualizar contador
        self.patient_index_var.set(f"{self.current_patient_index + 1} / {len(self.patients)}")
        
        # Atualizar info da sidebar
        self._update_sidebar_info()

    def export_png(self):
        """Exporta pulseiras como PNG."""
        self.io_manager.export_png(self.patients, self.layout, self.fonts_map, self.logo_image)

    def export_pdf(self):
        """Exporta pulseiras como PDF."""
        self.io_manager.export_pdf(self.patients, self.layout, self.fonts_map, self.logo_image)

    def update_fonts(self):
        """Carrega as fontes PIL a partir da família/tamanho/estilo selecionados."""
        try:
            self.font_regular = get_font(
                self.fonts_map, 
                self.font_family, 
                self.font_size, 
                bold=False, 
                italic=self.font_italic_flag
            )
            self.font_bold = get_font(
                self.fonts_map, 
                self.font_family, 
                self.font_size, 
                bold=self.font_bold_flag, 
                italic=self.font_italic_flag
            )
            
            self.status_var.set(
                f'✓ Fonte: {self.font_family} {self.font_size}px '
                f'(bold={self.font_bold_flag}, italic={self.font_italic_flag})'
            )
            
            # Atualizar sidebar se existir
            if hasattr(self, 'font_info_var'):
                self._update_sidebar_info()
        except Exception as e:
            print(f"[DEBUG] Error updating fonts: {e}")
            from PIL import ImageFont
            self.font_regular = ImageFont.load_default()
            self.font_bold = ImageFont.load_default()
            self.status_var.set('Fonte: fallback (default)')

    def open_font_dialog(self):
        """Abre diálogo para escolher família, tamanho e estilos."""
        from tkinter import Toplevel, BooleanVar, Spinbox
        
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

        tb.Label(dlg, text='Tamanho do Nome (px):').grid(row=2, column=0, sticky='w', padx=6, pady=6)
        name_size_sb = tb.Spinbox(dlg, from_=6, to=800, increment=1, width=8)
        name_size_sb.set(str(self.name_font_size))
        name_size_sb.grid(row=2, column=1, sticky='w', padx=6, pady=6)

        bold_var = tb.BooleanVar(value=self.font_bold_flag)
        italic_var = tb.BooleanVar(value=self.font_italic_flag)
        save_default_var = tb.BooleanVar(value=True)
        
        cb_bold = tb.Checkbutton(dlg, text='Negrito (bold)', variable=bold_var)
        cb_bold.grid(row=3, column=0, padx=6, pady=6)
        cb_italic = tb.Checkbutton(dlg, text='Itálico (italic)', variable=italic_var)
        cb_italic.grid(row=3, column=1, padx=6, pady=6)
        cb_save = tb.Checkbutton(dlg, text='Salvar como padrão', variable=save_default_var)
        cb_save.grid(row=4, column=0, columnspan=2, padx=6, pady=6, sticky='w')

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
            self.update_fonts()
            
            # Aplica a fonte global aos itens de texto do layout
            try:
                for it in self.layout.items:
                    if it.get('type') == 'text':
                        it['font_family'] = self.font_family
                        it['font_size'] = self.font_size if it['id'] != 'nome' else self.name_font_size
                        it['bold'] = self.font_bold_flag
                        it['italic'] = self.font_italic_flag
            except Exception as e:
                print(f"[DEBUG] Error applying global font settings: {e}")
            
            self.update_preview()
            
            # salva como padrão, se marcado
            try:
                if save_default_var.get():
                    self._save_prefs()
            except Exception:
                pass
            
            dlg.destroy()

        btn_frame = tb.Frame(dlg)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=8)
        tb.Button(btn_frame, text='Aplicar', command=apply_and_close).pack(side=LEFT, padx=6)
        tb.Button(btn_frame, text='Cancelar', command=dlg.destroy).pack(side=LEFT, padx=6)

    def _load_prefs(self):
        """Carrega preferências do usuário."""
        try:
            if os.path.isfile(self.prefs_file):
                with open(self.prefs_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.font_family = data.get('font_family', self.font_family)
                self.font_size = int(data.get('font_size', self.font_size))
                self.font_bold_flag = bool(data.get('font_bold_flag', self.font_bold_flag))
                self.font_italic_flag = bool(data.get('font_italic_flag', self.font_italic_flag))
                self.name_font_size = int(data.get('name_font_size', self.name_font_size or self.font_size))
                self.auto_fit_enabled = bool(data.get('auto_fit_enabled', self.auto_fit_enabled))
        except Exception:
            pass

    def _save_prefs(self):
        """Salva preferências do usuário."""
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

    def _default_layout(self) -> LayoutModel:
        """
        ✅ MÓDULO 3 - CORREÇÃO: Layout padrão com nome e observação CENTRALIZADOS
        Nome e Observação posicionados exatamente no centro da área imprimível
        """
        from core import NP_START_PX, PRINTABLE_W_PX, SPACING_PX
        
        items = []
        
        # ========== ÁREA IMPRIMÍVEL ==========
        # A pulseira tem 29.5cm total
        # Primeiros 2.5cm são NÃO imprimíveis
        # Próximos 10cm são imprimíveis (onde colocamos QR + info)
        # Últimos 17cm (de 12.5cm a 29.5cm) também são NÃO imprimíveis
        printable_area_start = NP_START_PX  # 2.5cm em pixels
        printable_area_end = printable_area_start + PRINTABLE_W_PX  # até 12.5cm
        
        # ✅ MÓDULO 3: Calcular o CENTRO da área imprimível
        printable_width = PRINTABLE_W_PX  # Largura da área imprimível (10cm)
        printable_center_x = printable_area_start + (printable_width // 2)  # Centro absoluto
        
        # ========== QR CODE (LADO ESQUERDO) ==========
        qr_size = int(P_HEIGHT - 2 * cm_to_px(0.1))  # ~1.8cm
        qr_x = printable_area_start + cm_to_px(0.1)  # Início da área imprimível + 0.1cm
        
        items.append(
            asdict(QRItem(
                id='qr1',
                x=qr_x,
                y=cm_to_px(0.1),
                size=qr_size,
                binding='Número da carteirinha'
            ))
        )
        
        # ========== INFORMAÇÕES DO PACIENTE (LADO DIREITO) ==========
        # Começam após o QR Code, ainda dentro da área imprimível
        info_x_start = qr_x + qr_size + cm_to_px(0.1)  # Gap de 0.1cm após QR
        info_available_width = printable_area_end - info_x_start - cm_to_px(0.1)  # Até fim da imprimível - margem
        info_center_x = info_x_start + (info_available_width // 2)  # Centro da área de informações
        
        # ✅ MÓDULO 3: Nome CENTRALIZADO no meio da área imprimível
        items.append(
            asdict(TextItem(
                id='nome',
                x=printable_center_x,  # ✅ Centro absoluto da área imprimível
                y=cm_to_px(0.1),
                width=printable_width,  # ✅ Largura total da área imprimível
                text='{Nome do paciente}',
                font_size=32,
                bold=True,
                align='center'  # ✅ Alinhamento centralizado
            ))
        )
        
        # Carteirinha (centralizada também)
        items.append(
            asdict(TextItem(
                id='carteirinha',
                x=info_center_x,
                y=cm_to_px(0.1) + 38,  # 0.3cm abaixo do nome (~38px)
                width=info_available_width,
                text='Carteirinha: {Número da carteirinha}',
                font_size=20,
                bold=True,
                align='center'
            ))
        )
        
        # ========== CAMPOS EM 3 COLUNAS (ABAIXO DO NOME/CARTEIRINHA) ==========
        # Começam em 0.8cm (depois de nome + carteirinha)
        col_y_start = cm_to_px(0.8)
        line_height = cm_to_px(0.3)  # EXATAMENTE 0.3cm entre linhas
        
        # Ajustar espaçamento entre colunas e margens
        col_gap = cm_to_px(0.2)  # Aumenta o espaçamento entre colunas
        col_width = (info_available_width - 2 * col_gap) // 3  # Recalcula largura das colunas

        # Garantir que os campos não ultrapassem a área imprimível
        for item in items:
            if isinstance(item, dict) and 'x' in item and 'width' in item:
                if item['x'] + item['width'] > printable_area_end:
                    item['x'] = printable_area_end - item['width']

        # Coluna 1 (Nasc, Mãe, Conv)
        col1_x = info_x_start
        items.append(
            asdict(TextItem(
                id='data_nasc',
                x=col1_x,
                y=col_y_start,
                width=col_width,
                text='Nasc: {Data de nascimento}',
                font_size=16,
                bold=False,
                align='left'
            ))
        )
        items.append(
            asdict(TextItem(
                id='mae',
                x=col1_x,
                y=col_y_start + line_height,
                width=col_width,
                text='Mãe: {Nome da mãe}',
                font_size=16,
                bold=False,
                align='left'
            ))
        )
        items.append(
            asdict(TextItem(
                id='convenio',
                x=col1_x,
                y=col_y_start + 2 * line_height,
                width=col_width,
                text='Conv: {Convênio}',
                font_size=16,
                bold=False,
                align='left'
            ))
        )
        
        # Coluna 2 (Med, Sex, Adm)
        col2_x = col1_x + col_width + col_gap
        items.append(
            asdict(TextItem(
                id='medico',
                x=col2_x,
                y=col_y_start,
                width=col_width,
                text='Med: {Médico responsável}',
                font_size=16,
                bold=False,
                align='left'
            ))
        )
        items.append(
            asdict(TextItem(
                id='sexo',
                x=col2_x,
                y=col_y_start + line_height,
                width=col_width,
                text='Sex: {Sexo}',
                font_size=16,
                bold=False,
                align='left'
            ))
        )
        items.append(
            asdict(TextItem(
                id='data_admissao',
                x=col2_x,
                y=col_y_start + 2 * line_height,
                width=col_width,
                text='Adm: {Data de admissão}',
                font_size=16,
                bold=False,
                align='left'
            ))
        )
        
        # Coluna 3 (Hora de admissão, e espaço para mais)
        col3_x = col2_x + col_width + col_gap
        items.append(
            asdict(TextItem(
                id='hora_admissao',
                x=col3_x,
                y=col_y_start,
                width=col_width,
                text='Hora: {Hora de admissão}',
                font_size=16,
                bold=False,
                align='left'
            ))
        )
        
        # ✅ MÓDULO 3: Observação CENTRALIZADA no meio da área imprimível
        obs_y = col_y_start + cm_to_px(1.2)  # Bem abaixo das 3 colunas
        items.append(
            asdict(TextItem(
                id='observacao',
                x=printable_center_x,  # ✅ Centro absoluto da área imprimível
                y=obs_y,
                width=printable_width,  # ✅ Largura total da área imprimível
                text='{Observação}',
                font_size=14,
                bold=False,
                align='center'  # ✅ Alinhamento centralizado
            ))
        )
        
        return LayoutModel(items=items)

    def open_layout_editor(self):
        """Abre o editor visual de layout."""
        editor = LayoutEditor(self.root, self.layout, self.fonts_map, self.logo_image)
        editor.open(on_close_callback=self.update_preview)

    def save_template(self):
        """Salva layout como modelo (template)."""
        path = filedialog.asksaveasfilename(
            defaultextension='.json',
            filetypes=[('JSON', '*.json')],
            initialdir=self.templates_dir,
            initialfile='modelo.json'
        )
        if not path:
            return
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(self.layout.to_dict(), f, ensure_ascii=False, indent=2)
            messagebox.showinfo('Modelo', f'Modelo salvo em {path}')
        except Exception as e:
            messagebox.showerror('Erro', f'Não foi possível salvar o modelo: {e}')

    def load_template(self):
        """Carrega um modelo (template) salvo."""
        path = filedialog.askopenfilename(filetypes=[('JSON', '*.json')], initialdir=self.templates_dir)
        if not path:
            return
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.layout = LayoutModel.from_dict(data)
            self.update_preview()
            messagebox.showinfo('Modelo', f'Modelo carregado de {path}')
        except Exception as e:
            messagebox.showerror('Erro', f'Não foi possível carregar o modelo: {e}')
    
    # ========== MÉTODOS DE IMPRESSÃO ZEBRA ==========
    
    def _init_zebra_printer(self):
        """Inicializa a conexão com a impressora Zebra."""
        try:
            self.zebra_printer = ZebraPrinter(self.printer_name)
            
            # Atualizar status na aba de impressão (se já foi criada)
            if hasattr(self, 'printer_status_label'):
                if self.zebra_printer.is_printer_available():
                    self.printer_status_label.config(
                        text=f"✓ Impressora '{self.printer_name}' conectada e pronta",
                        foreground="green"
                    )
                else:
                    available = self.zebra_printer.list_printers()
                    msg = f"✗ Impressora '{self.printer_name}' não encontrada\n"
                    if available:
                        msg += f"Disponíveis: {', '.join(available[:3])}"
                    else:
                        msg += "Nenhuma impressora Zebra detectada"
                    self.printer_status_label.config(text=msg, foreground="red")
        except ImportError as e:
            self.zebra_printer = None
            if hasattr(self, 'printer_status_label'):
                self.printer_status_label.config(
                    text="✗ Módulo win32print não instalado\nExecute: pip install pywin32",
                    foreground="red"
                )
        except Exception as e:
            self.zebra_printer = None
            if hasattr(self, 'printer_status_label'):
                self.printer_status_label.config(
                    text=f"✗ Erro ao conectar: {str(e)}",
                    foreground="red"
                )
    
    def print_current_bracelet(self):
        """Imprime a pulseira atual exibida na pré-visualização."""
        if not self.patients:
            messagebox.showwarning("Aviso", "Nenhum paciente carregado. Importe um CSV primeiro.")
            return
        
        if not self.zebra_printer:
            messagebox.showerror("Erro", "Impressora Zebra não configurada. Configure em Menu > Impressão > Configurar Impressora")
            return
        
        if not self.zebra_printer.is_printer_available():
            messagebox.showerror("Erro", f"Impressora '{self.printer_name}' não está disponível. Verifique a conexão.")
            return
        
        try:
            patient = self.patients[self.current_patient_index]
            nome = patient.get('Nome do paciente', 'Sem nome')
            
            # Gerar ZPL
            zpl = generate_bracelet_zpl(patient)
            
            # Enviar para impressora
            if self.zebra_printer.send_zpl(zpl):
                self.status_var.set(f"✓ Pulseira de {nome} enviada para impressão")
                messagebox.showinfo("Sucesso", f"Pulseira de {nome} enviada para impressão com sucesso!")
            else:
                messagebox.showerror("Erro", "Falha ao enviar pulseira para impressão. Verifique a impressora.")
        
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao imprimir pulseira: {str(e)}")
    
    def print_all_bracelets(self):
        """Imprime todas as pulseiras do CSV carregado."""
        if not self.patients:
            messagebox.showwarning("Aviso", "Nenhum paciente carregado. Importe um CSV primeiro.")
            return
        
        if not self.zebra_printer:
            messagebox.showerror("Erro", "Impressora Zebra não configurada. Configure em Menu > Impressão > Configurar Impressora")
            return
        
        if not self.zebra_printer.is_printer_available():
            messagebox.showerror("Erro", f"Impressora '{self.printer_name}' não está disponível. Verifique a conexão.")
            return
        
        # Confirmar impressão
        total = len(self.patients)
        resposta = messagebox.askyesno(
            "Confirmar Impressão",
            f"Deseja imprimir {total} pulseira(s)?\n\nEsta operação enviará todas as pulseiras para a impressora."
        )
        
        if not resposta:
            return
        
        try:
            success_count = 0
            error_count = 0
            
            for i, patient in enumerate(self.patients):
                nome = patient.get('Nome do paciente', f'Paciente {i+1}')
                self.status_var.set(f"Imprimindo {i+1}/{total}: {nome}...")
                self.root.update()
                
                # Gerar ZPL
                zpl = generate_bracelet_zpl(patient)
                
                # Enviar para impressora
                if self.zebra_printer.send_zpl(zpl):
                    success_count += 1
                else:
                    error_count += 1
            
            # Relatório final
            if error_count == 0:
                messagebox.showinfo(
                    "Sucesso",
                    f"✓ Todas as {total} pulseiras foram enviadas para impressão com sucesso!"
                )
                self.status_var.set(f"✓ {total} pulseiras impressas com sucesso")
            else:
                messagebox.showwarning(
                    "Atenção",
                    f"Impressão concluída:\n✓ {success_count} sucesso\n✗ {error_count} falhas"
                )
                self.status_var.set(f"Impressão finalizada: {success_count} OK, {error_count} erros")
        
        except Exception as e:
            messagebox.showerror("Erro", f"Erro durante impressão em lote: {str(e)}")
    
    def print_test(self):
        """Imprime uma etiqueta de teste."""
        if not self.zebra_printer:
            messagebox.showerror("Erro", "Impressora Zebra não configurada. Configure em Menu > Impressão > Configurar Impressora")
            return
        
        if not self.zebra_printer.is_printer_available():
            messagebox.showerror("Erro", f"Impressora '{self.printer_name}' não está disponível. Verifique a conexão.")
            return
        
        try:
            if self.zebra_printer.print_test():
                messagebox.showinfo("Sucesso", "Etiqueta de teste enviada para impressão!")
                self.status_var.set("✓ Teste de impressão enviado")
            else:
                messagebox.showerror("Erro", "Falha ao enviar etiqueta de teste.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao imprimir teste: {str(e)}")
    
    def configure_printer(self):
        """Abre diálogo para configurar a impressora."""
        dlg = tb.Toplevel(self.root)
        dlg.title("Configurar Impressora Zebra")
        dlg.transient(self.root)
        dlg.grab_set()
        
        tb.Label(dlg, text="Configuração da Impressora Zebra", 
                font=("Segoe UI", 14, "bold")).pack(pady=15, padx=20)
        
        # Listar impressoras disponíveis
        tb.Label(dlg, text="Impressoras disponíveis:", 
                font=("Segoe UI", 10)).pack(anchor="w", padx=20)
        
        try:
            temp_printer = ZebraPrinter()
            available_printers = temp_printer.list_printers()
        except:
            available_printers = []
        
        if not available_printers:
            tb.Label(dlg, text="Nenhuma impressora encontrada", 
                    foreground="red").pack(padx=20, pady=5)
        else:
            printer_list = tb.Frame(dlg)
            printer_list.pack(fill=BOTH, expand=YES, padx=20, pady=10)
            
            selected_printer = tb.StringVar(value=self.printer_name)
            
            for printer in available_printers:
                rb = tb.Radiobutton(
                    printer_list,
                    text=printer,
                    variable=selected_printer,
                    value=printer,
                    bootstyle="info"
                )
                rb.pack(anchor="w", pady=2)
        
        # Botões
        btn_frame = tb.Frame(dlg)
        btn_frame.pack(pady=15)
        
        def test_and_save():
            if available_printers:
                self.printer_name = selected_printer.get()
                self._init_zebra_printer()
                
                if self.zebra_printer and self.zebra_printer.is_printer_available():
                    messagebox.showinfo("Sucesso", f"Impressora '{self.printer_name}' configurada com sucesso!")
                    self._update_sidebar_info()
                    dlg.destroy()
                else:
                    messagebox.showerror("Erro", f"Não foi possível conectar à impressora '{self.printer_name}'")
        
        tb.Button(btn_frame, text="Testar e Salvar", command=test_and_save,
                 bootstyle="success").pack(side=LEFT, padx=5)
        tb.Button(btn_frame, text="Cancelar", command=dlg.destroy,
                 bootstyle="secondary").pack(side=LEFT, padx=5)
    
    def show_printer_status(self):
        """Exibe o status detalhado da impressora."""
        result = test_printer_connection(self.printer_name)
        
        msg = f"Impressora configurada: {result['printer_name']}\n\n"
        msg += f"Status: {'✓ Conectada' if result['connected'] else '✗ Não conectada'}\n\n"
        
        if result['available_printers']:
            msg += "Impressoras disponíveis no sistema:\n"
            for p in result['available_printers']:
                msg += f"  • {p}\n"
        else:
            msg += "Nenhuma impressora encontrada no sistema.\n"
        
        if result['error']:
            msg += f"\nErro: {result['error']}"
        
        messagebox.showinfo("Status da Impressora", msg)

    def iniciar_atendimento(self):
        """
        ✅ MÓDULO 1 - CORREÇÃO: Inicia novo atendimento ZERANDO dados anteriores
        Remove TODOS os dados do paciente anterior.
        Não inclui nada automaticamente (exceto data/hora de admissão).
        """
        # ✅ ZERAR dados do paciente anterior COMPLETAMENTE
        self.patients = []
        self.status_var.set('🔄 Aguardando preenchimento do formulário de atendimento...')
        self.update_preview()  # Limpa preview antes de abrir formulário
        
        # Abrir formulário completamente limpo
        self.atendimento_form.abrir_formulario()
        
        # Aguardar fechamento do formulário para carregar dados
        self.root.wait_window(self.atendimento_form.window)
        
        # Carregar dados APENAS se novo paciente foi salvo
        self._carrega_dados_atendimento()

    def _carrega_dados_atendimento(self):
        """
        ✅ ATUALIZADO: Carrega paciente(s) do CSV após fechar formulário
        - Se usou "Salvar": carrega APENAS o último paciente
        - Se usou "Salvar e Adicionar Outro": carrega TODOS os pacientes do CSV
        """
        try:
            # Verificar se há formulário aberto
            if self.atendimento_form.window and self.atendimento_form.window.winfo_exists():
                return  # Formulário ainda está aberto, não carregar
            
            # Ler arquivo CSV atual
            dados = self.atendimento_form.obter_dados_csv()
            
            if dados and len(dados) > 0:
                # ✅ CARREGAR TODOS os pacientes do CSV
                # (Isso permite múltiplos pacientes se usou "Salvar e Adicionar Outro")
                self.patients = dados
                
                if len(dados) == 1:
                    # Um único paciente
                    nome_paciente = dados[0].get('Nome do paciente', 'Sem nome')
                    carteirinha = dados[0].get('Número da carteirinha', 'Sem número')
                    self.status_var.set(f'✓ Atendimento: {nome_paciente} (Carteirinha: {carteirinha})')
                else:
                    # Múltiplos pacientes cadastrados
                    self.status_var.set(f'✓ {len(dados)} pacientes cadastrados. Preview: último paciente.')
                
                self.update_preview()
            else:
                # Nenhum dado no CSV ou usuário cancelou
                self.patients = []
                self.status_var.set('⚠️ Nenhum atendimento ativo. Clique em "Iniciar Atendimento" para começar.')
                self.update_preview()
        except Exception as e:
            self.patients = []
            self.status_var.set('⚠️ Erro ao carregar dados. Inicie um novo atendimento.')
            print(f"[ERRO] Erro ao carregar dados: {str(e)}")


if __name__ == '__main__':
    app = tb.Window(themename='flatly')
    PulseiraApp(app)
    app.mainloop()
