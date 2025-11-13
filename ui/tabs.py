"""
Módulo para gerenciar as abas (tabs) da interface UX melhorada.

Responsabilidades:
- Criação das abas de importação, pré-visualização, editor, exportação e configurações
- Controles dentro de cada aba
- Atualização de dados nas abas
"""

from tkinter import ttk, END, filedialog, messagebox
import ttkbootstrap as tb
from ttkbootstrap.constants import LEFT, RIGHT, BOTH, X, Y, YES


class TabsManager:
    """Gerencia abas da interface."""

    def __init__(self, app, notebook):
        """
        Inicializa gerenciador de abas.
        
        Args:
            app: Referência à aplicação principal (PulseiraAppUX)
            notebook: Widget do tkinter notebook (abas)
        """
        self.app = app
        self.notebook = notebook
        
        # Widgets que serão referenciados depois
        self.data_tree = None
        self.import_status = None
        self.preview_info = None
        self.preview_data_frame = None
        self.preview_data_text = None
        self.canvas_preview = None
        self.btn_prev = None
        self.btn_next = None

    def create_tabs(self):
        """Cria todas as abas."""
        # Aba 1: Importação
        tab_import = tb.Frame(self.notebook)
        self.notebook.add(tab_import, text='📥 Importação')
        self._create_import_tab(tab_import)
        
        # Aba 2: Pré-visualização
        tab_preview = tb.Frame(self.notebook)
        self.notebook.add(tab_preview, text='👁️ Pré-visualização')
        self._create_preview_tab(tab_preview)
        
        # Aba 3: Editor
        tab_editor = tb.Frame(self.notebook)
        self.notebook.add(tab_editor, text='✏️ Editor')
        self._create_editor_tab(tab_editor)
        
        # Aba 4: Exportação
        tab_export = tb.Frame(self.notebook)
        self.notebook.add(tab_export, text='📤 Exportação')
        self._create_export_tab(tab_export)
        
        # Aba 5: Configurações
        tab_settings = tb.Frame(self.notebook)
        self.notebook.add(tab_settings, text='⚙️ Configurações')
        self._create_settings_tab(tab_settings)

    def _create_import_tab(self, tab):
        """Aba de importação de CSV."""
        frame = tb.Frame(tab, padding=20)
        frame.pack(fill=BOTH, expand=YES)
        
        # Instrução
        instruction = tb.Label(
            frame,
            text='Importe um arquivo CSV com os dados dos pacientes',
            font=('Arial', 12)
        )
        instruction.pack(pady=(0, 20))
        
        # Botões de ação
        btn_frame = tb.Frame(frame)
        btn_frame.pack(fill=X, pady=10)
        
        btn_import = tb.Button(
            btn_frame,
            text='📥 Importar CSV',
            command=self.app.import_csv,
            width=20
        )
        btn_import.pack(side=LEFT, padx=5)
        
        btn_example = tb.Button(
            btn_frame,
            text='📄 Baixar Exemplo',
            command=self.app.save_example_csv,
            width=20
        )
        btn_example.pack(side=LEFT, padx=5)
        
        btn_empty = tb.Button(
            btn_frame,
            text='📝 Modelo Vazio',
            command=self.app.save_empty_csv,
            width=20
        )
        btn_empty.pack(side=LEFT, padx=5)
        
        # Tabela de dados
        sep = tb.Separator(frame, orient='horizontal')
        sep.pack(fill=X, pady=20)
        
        data_label = tb.Label(frame, text='Dados Importados', font=('Arial', 11, 'bold'))
        data_label.pack(fill=X, pady=(0, 10))
        
        # Frame com scrollbar
        tree_frame = tb.Frame(frame)
        tree_frame.pack(fill=BOTH, expand=YES)
        
        # Cria treeview
        self.data_tree = ttk.Treeview(
            tree_frame,
            columns=['Carteirinha', 'Nome', 'Convênio', 'Médico'],
            height=15,
            show='headings'
        )
        
        # Define colunas
        self.data_tree.column('Carteirinha', width=100, anchor='w')
        self.data_tree.column('Nome', width=200, anchor='w')
        self.data_tree.column('Convênio', width=150, anchor='w')
        self.data_tree.column('Médico', width=150, anchor='w')
        
        self.data_tree.heading('Carteirinha', text='Carteirinha')
        self.data_tree.heading('Nome', text='Nome do Paciente')
        self.data_tree.heading('Convênio', text='Convênio')
        self.data_tree.heading('Médico', text='Médico')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.data_tree.yview)
        self.data_tree.configure(yscroll=scrollbar.set)
        
        self.data_tree.pack(side=LEFT, fill=BOTH, expand=YES)
        scrollbar.pack(side=RIGHT, fill='y')
        
        # Status
        self.import_status = tb.Label(
            frame,
            text='Nenhum arquivo importado',
            foreground='#868E96',
            font=('Arial', 10)
        )
        self.import_status.pack(fill=X, pady=(10, 0))

    def _create_preview_tab(self, tab):
        """Aba de pré-visualização com carrossel de pacientes."""
        frame = tb.Frame(tab, padding=20)
        frame.pack(fill=BOTH, expand=YES)
        
        # === CONTROLE DE NAVEGAÇÃO (TOP) ===
        nav_frame = tb.Frame(frame)
        nav_frame.pack(fill=X, pady=(0, 15))
        
        # Botão anterior
        self.btn_prev = tb.Button(
            nav_frame,
            text='⬅️ Anterior',
            command=self.app.preview_previous_patient,
            width=15
        )
        self.btn_prev.pack(side=LEFT, padx=5)
        
        # Informação do paciente
        self.preview_info = tb.Label(
            nav_frame,
            text='Nenhum paciente',
            font=('Arial', 11, 'bold'),
            foreground='#4C6EF5'
        )
        self.preview_info.pack(side=LEFT, expand=YES, padx=20)
        
        # Botão próximo
        self.btn_next = tb.Button(
            nav_frame,
            text='Próximo ➡️',
            command=self.app.preview_next_patient,
            width=15
        )
        self.btn_next.pack(side=LEFT, padx=5)
        
        # === DADOS DO PACIENTE ===
        self.preview_data_frame = tb.Labelframe(frame, text='📋 Dados do Paciente', padding=10)
        self.preview_data_frame.pack(fill=X, pady=(0, 15))
        
        self.preview_data_text = tb.Label(
            self.preview_data_frame,
            text='Importe um CSV para ver os dados',
            font=('Arial', 10),
            foreground='#FFFFFF',
            justify='left'
        )
        self.preview_data_text.pack(fill=BOTH, expand=YES, padx=10, pady=10)
        
        # === CANVAS DE PREVIEW ===
        canvas_frame = tb.Labelframe(frame, text='🎨 Visualização da Pulseira', padding=10)
        canvas_frame.pack(fill=BOTH, expand=YES)
        
        # Cria canvas com proporção correta da pulseira
        # Pulseira padrão: 85.6mm x 32mm (proporção ~2.68:1)
        self.canvas_preview = tb.Canvas(
            canvas_frame,
            width=800,
            height=300,
            background='white',
            relief='sunken',
            bd=2,
            highlightthickness=1,
            highlightbackground='#DEE2E6'
        )
        self.canvas_preview.pack(fill=BOTH, expand=YES, padx=5, pady=5)

    def _create_editor_tab(self, tab):
        """Aba do editor de layout."""
        frame = tb.Frame(tab, padding=20)
        frame.pack(fill=BOTH, expand=YES)
        
        btn_frame = tb.Frame(frame)
        btn_frame.pack(fill=X, pady=(0, 20))
        
        btn_editor = tb.Button(
            btn_frame,
            text='🖌️ Abrir Editor de Layout',
            command=self.app.open_layout_editor,
            width=30
        )
        btn_editor.pack(side=LEFT, padx=5)
        
        label = tb.Label(
            frame,
            text='Clique no botão acima para abrir o editor visual de layout.\n\n'
                 'No editor você pode:\n'
                 '• Adicionar itens de texto\n'
                 '• Adicionar código QR\n'
                 '• Posicionar itens com arrastar e soltar\n'
                 '• Configurar fontes, cores e tamanhos\n'
                 '• Editar propriedades dos itens',
            font=('Arial', 11),
            justify='left',
            foreground='#495057'
        )
        label.pack(fill=BOTH, expand=YES, padx=10, pady=10)

    def _create_export_tab(self, tab):
        """Aba de exportação."""
        frame = tb.Frame(tab, padding=20)
        frame.pack(fill=BOTH, expand=YES)
        
        title = tb.Label(
            frame,
            text='Exportar Pulseiras',
            font=('Arial', 12, 'bold')
        )
        title.pack(pady=(0, 20))
        
        # Botões
        btn_frame = tb.Frame(frame)
        btn_frame.pack(fill=X, pady=10)
        
        btn_png = tb.Button(
            btn_frame,
            text='🖼️ Exportar PNG',
            command=self.app.export_png,
            width=25
        )
        btn_png.pack(side=LEFT, padx=10, pady=5)
        
        btn_pdf = tb.Button(
            btn_frame,
            text='📕 Exportar PDF',
            command=self.app.export_pdf,
            width=25
        )
        btn_pdf.pack(side=LEFT, padx=10, pady=5)
        
        # Informações
        info_frame = tb.Labelframe(frame, text='Informações de Exportação', padding=15)
        info_frame.pack(fill=BOTH, expand=YES, pady=20)
        
        info_text = tb.Label(
            info_frame,
            text='PNG:\n'
                 '• Salva cada pulseira como arquivo separado\n'
                 '• Resolução: 300 DPI (pronto para impressão)\n'
                 '• Formato: RGB\n\n'
                 'PDF:\n'
                 '• Todas as pulseiras em um único arquivo\n'
                 '• Fácil de compartilhar\n'
                 '• Pronto para impressão de múltiplas cópias\n\n'
                 'Dica: Importe um CSV antes de exportar!',
            justify='left',
            font=('Arial', 10),
            foreground='#495057'
        )
        info_text.pack(fill=BOTH, expand=YES)

    def _create_settings_tab(self, tab):
        """Aba de configurações."""
        frame = tb.Frame(tab, padding=20)
        frame.pack(fill=BOTH, expand=YES)
        
        # Logotipo
        logo_frame = tb.Labelframe(frame, text='🖼️ Logotipo', padding=15)
        logo_frame.pack(fill=X, pady=10)
        
        btn_upload = tb.Button(
            logo_frame,
            text='Upload Logotipo',
            command=self.app.upload_logo
        )
        btn_upload.pack(side=LEFT, padx=5)
        
        # Fonte
        font_frame = tb.Labelframe(frame, text='🔤 Configurações de Fonte', padding=15)
        font_frame.pack(fill=X, pady=10)
        
        btn_font = tb.Button(
            font_frame,
            text='Configurar Fonte Global',
            command=self.app.open_font_dialog
        )
        btn_font.pack(side=LEFT, padx=5)
        
        # Modelos
        models_frame = tb.Labelframe(frame, text='💾 Modelos', padding=15)
        models_frame.pack(fill=X, pady=10)
        
        btn_save = tb.Button(
            models_frame,
            text='Salvar Modelo',
            command=self.app.save_template
        )
        btn_save.pack(side=LEFT, padx=5)
        
        btn_load = tb.Button(
            models_frame,
            text='Carregar Modelo',
            command=self.app.load_template
        )
        btn_load.pack(side=LEFT, padx=5)
        
        btn_open_folder = tb.Button(
            models_frame,
            text='Abrir Pasta de Modelos',
            command=self.app.open_templates_folder
        )
        btn_open_folder.pack(side=LEFT, padx=5)

    def update_import_table(self, patients):
        """Atualiza tabela de dados importados."""
        # Limpa itens antigos
        for item in self.data_tree.get_children():
            self.data_tree.delete(item)
        
        # Adiciona novos itens
        for patient in patients[:100]:  # Limite de 100 linhas
            values = (
                patient.get('Número da carteirinha', ''),
                patient.get('Nome do paciente', ''),
                patient.get('Convênio', ''),
                patient.get('Médico responsável', '')
            )
            self.data_tree.insert('', END, values=values)
