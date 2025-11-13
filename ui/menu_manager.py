"""
Módulo para gerenciar menu bar e atalhos de teclado da aplicação UX melhorada.

Responsabilidades:
- Criação da barra de menu
- Configuração de atalhos de teclado
- Handlers de menu
"""

import os
import subprocess
import sys
from tkinter import filedialog, messagebox


class MenuManager:
    """Gerencia a barra de menu e atalhos de teclado."""

    def __init__(self, app):
        """
        Inicializa gerenciador de menu.
        
        Args:
            app: Referência à aplicação principal (PulseiraAppUX)
        """
        self.app = app
        self.root = app.root

    def create_menu_bar(self):
        """Cria barra de menu com atalhos."""
        import ttkbootstrap as tb
        
        menubar = tb.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menu Arquivo
        arquivo_menu = tb.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='📁 Arquivo', menu=arquivo_menu)
        arquivo_menu.add_command(label='Importar CSV (Ctrl+I)', command=self.app.import_csv)
        arquivo_menu.add_command(label='Exportar PNG (Ctrl+P)', command=self.app.export_png)
        arquivo_menu.add_command(label='Exportar PDF (Ctrl+D)', command=self.app.export_pdf)
        arquivo_menu.add_separator()
        arquivo_menu.add_command(label='Baixar Exemplo CSV', command=self.app.save_example_csv)
        arquivo_menu.add_command(label='Baixar Modelo Vazio', command=self.app.save_empty_csv)
        arquivo_menu.add_separator()
        arquivo_menu.add_command(label='Sair (Ctrl+Q)', command=self.root.quit)
        
        # Menu Editar
        editar_menu = tb.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='✏️ Editar', menu=editar_menu)
        editar_menu.add_command(label='Editor de Layout (Ctrl+L)', command=self.app.open_layout_editor)
        editar_menu.add_command(label='Configurar Fonte (Ctrl+F)', command=self.app.open_font_dialog)
        editar_menu.add_separator()
        editar_menu.add_command(label='Upload Logotipo', command=self.app.upload_logo)
        
        # Menu Modelos
        modelos_menu = tb.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='💾 Modelos', menu=modelos_menu)
        modelos_menu.add_command(label='Salvar Modelo Atual', command=self.app.save_template)
        modelos_menu.add_command(label='Carregar Modelo', command=self.app.load_template)
        modelos_menu.add_separator()
        modelos_menu.add_command(label='Abrir Pasta de Modelos', command=self.app.open_templates_folder)
        
        # Menu Ajuda
        ajuda_menu = tb.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='❓ Ajuda', menu=ajuda_menu)
        ajuda_menu.add_command(label='Sobre Unipulso', command=self.app.show_about)
        ajuda_menu.add_command(label='Guia CSV', command=self.app.show_csv_guide)

    def setup_keyboard_shortcuts(self):
        """Configura atalhos de teclado."""
        self.root.bind('<Control-i>', lambda e: self.app.import_csv())
        self.root.bind('<Control-p>', lambda e: self.app.export_png())
        self.root.bind('<Control-d>', lambda e: self.app.export_pdf())
        self.root.bind('<Control-l>', lambda e: self.app.open_layout_editor())
        self.root.bind('<Control-f>', lambda e: self.app.open_font_dialog())
        self.root.bind('<Control-q>', lambda e: self.root.quit())
        
        # Atalhos de navegação no carrossel
        self.root.bind('<Left>', lambda e: self.app.preview_previous_patient())
        self.root.bind('<Right>', lambda e: self.app.preview_next_patient())
