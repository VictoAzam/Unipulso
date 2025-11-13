"""
Módulo para gerenciar preview e carrossel de pacientes da interface UX melhorada.

Responsabilidades:
- Lógica de preview da pulseira
- Navegação no carrossel de pacientes
- Renderização e atualização de preview
- Dados do paciente na tela
"""

from PIL import Image, ImageTk
from render import render_layout_to_image


class PreviewManager:
    """Gerencia preview e carrossel de pacientes."""

    def __init__(self, app):
        """
        Inicializa gerenciador de preview.
        
        Args:
            app: Referência à aplicação principal (PulseiraAppUX)
        """
        self.app = app
        self.current_patient_index = 0
        self.tkimg = None  # Referência para PhotoImage

    def update_preview(self):
        """Atualiza pré-visualização com o paciente atual do carrossel."""
        canvas = self.app.tabs_manager.canvas_preview
        canvas.delete('all')
        cw = int(canvas['width'])
        ch = int(canvas['height'])
        
        try:
            # Se não há pacientes, mostra mensagem
            if not self.app.patients:
                # Renderiza pulseira vazia (sem dados)
                dummy = {}
                img = render_layout_to_image(
                    self.app.layout, 
                    dummy, 
                    self.app.fonts_map, 
                    logo_image=self.app.logo_image
                )
                img_thumb = img.resize((cw, ch), Image.LANCZOS)
                self.tkimg = ImageTk.PhotoImage(img_thumb)
                canvas.create_image(cw//2, ch//2, image=self.tkimg, anchor='center')
                
                # Atualiza informações
                self.app.tabs_manager.preview_info.config(
                    text='Nenhum paciente carregado',
                    foreground='#DC3545'
                )
                self._update_preview_data({})
                self.app.tabs_manager.btn_prev.config(state='disabled')
                self.app.tabs_manager.btn_next.config(state='disabled')
                return
            
            # Garante que o índice está válido
            if self.current_patient_index < 0:
                self.current_patient_index = 0
            elif self.current_patient_index >= len(self.app.patients):
                self.current_patient_index = len(self.app.patients) - 1
            
            # Pega o paciente atual
            patient = self.app.patients[self.current_patient_index]
            
            # Atualiza label de informação
            patient_num = self.current_patient_index + 1
            total = len(self.app.patients)
            nome = patient.get("Nome do paciente", "Paciente desconhecido")
            self.app.tabs_manager.preview_info.config(
                text=f'Paciente {patient_num}/{total} - {nome}',
                foreground='#28A745'
            )
            
            # Atualiza dados do paciente
            self._update_preview_data(patient)
            
            # Renderiza a pulseira
            img = render_layout_to_image(
                self.app.layout, 
                patient, 
                self.app.fonts_map, 
                logo_image=self.app.logo_image
            )
            
            # Redimensiona mantendo proporção (sem distorção)
            img_thumb = img.resize((cw, ch), Image.LANCZOS)
            self.tkimg = ImageTk.PhotoImage(img_thumb)
            canvas.create_image(cw//2, ch//2, image=self.tkimg, anchor='center')
            
            # Ativa/desativa botões de navegação
            self.app.tabs_manager.btn_prev.config(
                state='normal' if self.current_patient_index > 0 else 'disabled'
            )
            self.app.tabs_manager.btn_next.config(
                state='normal' if self.current_patient_index < len(self.app.patients) - 1 else 'disabled'
            )
            
        except Exception as e:
            print(f"[ERROR] Preview update failed: {e}")
            self.app.tabs_manager.preview_info.config(
                text=f'Erro na visualização: {str(e)[:50]}',
                foreground='#DC3545'
            )

    def _update_preview_data(self, patient):
        """Atualiza o texto com os dados do paciente."""
        preview_data_text = self.app.tabs_manager.preview_data_text
        
        if not patient:
            preview_data_text.config(
                text='Nenhum paciente para exibir',
                foreground='#6C757D'
            )
            return
        
        # Cria texto formatado com os dados
        data_lines = []
        
        # Extrai colunas importantes (se existirem)
        important_cols = [
            "Carteirinha do paciente",
            "Nome do paciente",
            "Convênio/Plano",
            "Médico responsável",
            "Data de nascimento",
            "Alergias",
            "Contato de emergência"
        ]
        
        for col in important_cols:
            value = patient.get(col, "")
            if value:
                # Formata: "Label: Valor"
                label = col.replace("do ", "").replace("da ", "").replace(" responsável", "").strip()
                # Trunca valores muito longos
                if len(str(value)) > 40:
                    value = str(value)[:37] + "..."
                data_lines.append(f"• {label}: {value}")
        
        if not data_lines:
            text = "Nenhum dado disponível"
            foreground = '#6C757D'
        else:
            text = "\n".join(data_lines)
            foreground = '#212529'
        
        preview_data_text.config(
            text=text,
            foreground=foreground
        )

    def next_patient(self):
        """Avança para o próximo paciente no carrossel."""
        if self.app.patients and self.current_patient_index < len(self.app.patients) - 1:
            self.current_patient_index += 1
            self.update_preview()

    def previous_patient(self):
        """Retrocede para o paciente anterior no carrossel."""
        if self.current_patient_index > 0:
            self.current_patient_index -= 1
            self.update_preview()

    def reset_index(self):
        """Reseta o índice para o primeiro paciente."""
        self.current_patient_index = 0
