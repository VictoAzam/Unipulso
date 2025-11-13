"""
Módulo para gerenciar painel lateral (sidebar) da aplicação UX melhorada.

Responsabilidades:
- Criação do painel lateral
- Atualização de status e informações
- Componentes do sidebar (badges, separadores, etc)
"""

from ttkbootstrap import Frame, Label, Separator
from ttkbootstrap.constants import LEFT, X, Y, BOTH, CENTER


class SidebarManager:
    """Gerencia painel lateral com status e informações."""

    def __init__(self, app, sidebar_frame):
        """
        Inicializa gerenciador de sidebar.
        
        Args:
            app: Referência à aplicação principal (PulseiraAppUX)
            sidebar_frame: Frame do tkinter para o sidebar
        """
        self.app = app
        self.sidebar = sidebar_frame
        self.csv_status = None
        self.pulseira_status = None
        self.font_status = None
        self.logo_status = None

    def create_sidebar(self):
        """Cria painel lateral com status e informações."""
        # Título
        title = Label(self.sidebar, text='ℹ️ Informações', font=('Arial', 12, 'bold'))
        title.pack(fill=X, pady=(0, 10))
        
        # Separador
        sep1 = Separator(self.sidebar, orient='horizontal')
        sep1.pack(fill=X, pady=5)
        
        # Status do CSV
        csv_label = Label(self.sidebar, text='📊 CSV', font=('Arial', 10, 'bold'))
        csv_label.pack(fill=X, pady=(10, 5))
        
        self.csv_status = Label(
            self.sidebar, 
            text='Nenhum CSV importado',
            wraplength=220,
            justify=LEFT,
            foreground='#FF6B6B'
        )
        self.csv_status.pack(fill=X, padx=4, pady=2)
        
        # Separador
        sep2 = Separator(self.sidebar, orient='horizontal')
        sep2.pack(fill=X, pady=5)
        
        # Status da Pulseira
        pulseira_label = Label(self.sidebar, text='🏥 Pulseira', font=('Arial', 10, 'bold'))
        pulseira_label.pack(fill=X, pady=(10, 5))
        
        self.pulseira_status = Label(
            self.sidebar,
            text='Pré-visualização vazia',
            wraplength=220,
            justify=LEFT,
            foreground='#868E96'
        )
        self.pulseira_status.pack(fill=X, padx=4, pady=2)
        
        # Separador
        sep3 = Separator(self.sidebar, orient='horizontal')
        sep3.pack(fill=X, pady=5)
        
        # Status de Fonte
        fonte_label = Label(self.sidebar, text='🔤 Fonte', font=('Arial', 10, 'bold'))
        fonte_label.pack(fill=X, pady=(10, 5))
        
        self.font_status = Label(
            self.sidebar,
            text='Arial 48px',
            wraplength=220,
            justify=LEFT,
            foreground='#4C6EF5'
        )
        self.font_status.pack(fill=X, padx=4, pady=2)
        
        # Separador
        sep4 = Separator(self.sidebar, orient='horizontal')
        sep4.pack(fill=X, pady=5)
        
        # Status de Logotipo
        logo_label = Label(self.sidebar, text='🖼️ Logotipo', font=('Arial', 10, 'bold'))
        logo_label.pack(fill=X, pady=(10, 5))
        
        self.logo_status = Label(
            self.sidebar,
            text='Não carregado',
            wraplength=220,
            justify=LEFT,
            foreground='#FFA94D'
        )
        self.logo_status.pack(fill=X, padx=4, pady=2)
        
        # Espaço em branco
        spacer = Frame(self.sidebar)
        spacer.pack(fill=BOTH, expand=True)
        
        # Rodapé com versão
        sep5 = Separator(self.sidebar, orient='horizontal')
        sep5.pack(fill=X, pady=5)
        
        footer = Label(
            self.sidebar,
            text='Unipulso v2.0\nRefatorado\n',
            font=('Arial', 9),
            foreground='#868E96',
            justify=CENTER
        )
        footer.pack(fill=X, pady=(10, 0))

    def update_csv_status(self, patient_count):
        """Atualiza status de CSV importado."""
        if patient_count > 0:
            self.csv_status.config(
                text=f'✓ {patient_count} pacientes importados',
                foreground='#51CF66'
            )
        else:
            self.csv_status.config(
                text='✗ Falha ao importar',
                foreground='#FF6B6B'
            )

    def update_font_status(self, font_family, font_size):
        """Atualiza status de fonte."""
        self.font_status.config(
            text=f'{font_family}\n{font_size}px'
        )

    def update_logo_status(self, logo_name=None):
        """Atualiza status de logotipo."""
        if logo_name:
            self.logo_status.config(
                text=f'✓ {logo_name}',
                foreground='#51CF66'
            )
        else:
            self.logo_status.config(
                text='Não carregado',
                foreground='#FFA94D'
            )

    def update_pulseira_status(self, status_text, is_success=False):
        """Atualiza status de pulseira."""
        color = '#51CF66' if is_success else '#868E96'
        self.pulseira_status.config(
            text=status_text,
            foreground=color
        )
