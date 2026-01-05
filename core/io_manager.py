"""
Módulo de Importação e Exportação de dados
"""

import os
import io
import csv
from typing import List, Dict, Any, Optional
from PIL import Image
from tkinter import filedialog, messagebox

from .config import EXPECTED_COLUMNS, DPI, P_WIDTH, P_HEIGHT
from .render import render_layout_to_image
from .models import LayoutModel


class IOManager:
    """Gerencia importação e exportação de CSV, PNG e PDF."""

    @staticmethod
    def import_csv(filepath: Optional[str] = None) -> List[Dict[str, str]]:
        """
        Importa dados de arquivo CSV.
        
        Detecta automaticamente o delimitador (vírgula, ponto-e-vírgula ou tab).
        Aceita CSVs com colunas em qualquer ordem e remove espaços em branco.
        
        Args:
            filepath: Caminho do arquivo (se None, abre diálogo)
            
        Returns:
            Lista de dicionários com dados
        """
        if filepath is None:
            # Se nenhum caminho foi fornecido, abre diálogo para usuário selecionar
            filepath = filedialog.askopenfilename(filetypes=[('CSV files', '*.csv')])
        
        if not filepath:
            return []  # Usuário cancelou a seleção
        
        try:
            # === ETAPA 1: Detecta automaticamente o delimitador usado no CSV ===
            # Lê uma amostra do arquivo (primeiros 4KB) para análise
            with open(filepath, 'r', encoding='utf-8') as f:
                sample = f.read(4096)  # Amostra suficiente para detectar o padrão
            
            # Tenta usar o Sniffer do Python para detectar o delimitador
            try:
                dialect = csv.Sniffer().sniff(sample, delimiters=',;\t')  # Vírgula, ponto-e-vírgula ou tab
                delimiter = dialect.delimiter
            except Exception:
                # Se o Sniffer falhar, usa heurística manual (verifica primeira linha)
                first_line = sample.split('\n')[0]
                if ';' in first_line:
                    delimiter = ';'  # Excel Brasil/Portugal usa ponto-e-vírgula
                elif '\t' in first_line:
                    delimiter = '\t'  # Arquivo separado por tabulação
                else:
                    delimiter = ','  # Padrão internacional (vírgula)
            
            # === ETAPA 2: Lê o CSV com o delimitador detectado ===
            with open(filepath, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f, delimiter=delimiter)  # Cria leitor de dicionário
                headers = reader.fieldnames  # Obtém nomes das colunas
                
                if not headers:
                    raise ValueError('CSV está vazio.')
                
                # Normaliza nomes de colunas (remove espaços extras que podem causar erros)
                headers_normalized = [h.strip() if h else '' for h in headers]
                
                # === ETAPA 3: Valida se todas as colunas obrigatórias estão presentes ===
                missing_cols = [col for col in EXPECTED_COLUMNS if col not in headers_normalized]
                if missing_cols:
                    # Mostra erro amigável ao usuário listando o que falta
                    msg = f'Colunas obrigatórias ausentes:\n{", ".join(missing_cols)}'
                    messagebox.showerror('Erro', msg)
                    return []
                
                # === ETAPA 4: Lê e limpa os dados de cada paciente ===
                patients = []  # Lista que armazenará todos os pacientes
                for row_dict in reader:  # Itera sobre cada linha do CSV
                    # Normaliza chaves e valores (remove espaços desnecessários)
                    clean_row = {}
                    for key, value in row_dict.items():
                        if key:  # Ignora colunas sem nome
                            # Remove espaços do nome da coluna
                            normalized_key = key.strip()
                            # Remove espaços nas extremidades do valor (trim)
                            clean_value = value.strip() if value else ''
                            clean_row[normalized_key] = clean_value
                    
                    # Só adiciona linha se tiver pelo menos algum dado (ignora linhas vazias)
                    if any(clean_row.values()):
                        patients.append(clean_row)
                
                # Verifica se encontrou pelo menos um paciente válido
                if not patients:
                    messagebox.showwarning('Aviso', 'Nenhum paciente válido encontrado.')
                    return []
                
                # Sucesso! Mostra quantos pacientes foram importados
                messagebox.showinfo('Sucesso', f'{len(patients)} paciente(s) importado(s).')
                return patients
                
        except ValueError as ve:
            messagebox.showerror('Erro', str(ve))
            return []
        except Exception as e:
            messagebox.showerror('Erro', f'Falha ao importar CSV: {e}')
            return []

    @staticmethod
    def save_example_csv(filepath: Optional[str] = None) -> bool:
        """
        Salva arquivo CSV de exemplo.
        
        Args:
            filepath: Caminho do arquivo (se None, abre diálogo)
            
        Returns:
            True se salvo com sucesso
        """
        example = [
            {
                'Número da carteirinha': '123456',
                'Nome do paciente': 'João Silva',
                'Data de nascimento': '1990-05-12',
                'Nome da mãe': 'Maria Silva',
                'Convênio': 'SUS',
                'Médico responsável': 'Dra. Aline',
                'Sexo': 'M',
                'Data de admissão': '2025-10-15',
                'Hora de admissão': '14:30',
                'Observação': 'Alergia: Penicilina'
            },
            {
                'Número da carteirinha': '987654',
                'Nome do paciente': 'Ana Pereira',
                'Data de nascimento': '1985-08-01',
                'Nome da mãe': 'Clara Pereira',
                'Convênio': 'Particular',
                'Médico responsável': 'Dr. Bruno',
                'Sexo': 'F',
                'Data de admissão': '2025-10-15',
                'Hora de admissão': '15:10',
                'Observação': 'Uso contínuo: Losartana'
            }
        ]
        
        if filepath is None:
            filepath = filedialog.asksaveasfilename(
                defaultextension='.csv',
                filetypes=[('CSV', '*.csv')],
                initialfile='exemplo.csv'
            )
        
        if not filepath:
            return False
        
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=EXPECTED_COLUMNS)
                writer.writeheader()
                for r in example:
                    writer.writerow(r)
            messagebox.showinfo('Sucesso', f'Exemplo salvo em {filepath}')
            return True
        except Exception as e:
            messagebox.showerror('Erro', str(e))
            return False

    @staticmethod
    def save_empty_csv(filepath: Optional[str] = None) -> bool:
        """
        Salva arquivo CSV vazio (apenas headers).
        
        Args:
            filepath: Caminho do arquivo (se None, abre diálogo)
            
        Returns:
            True se salvo com sucesso
        """
        if filepath is None:
            filepath = filedialog.asksaveasfilename(
                defaultextension='.csv',
                filetypes=[('CSV', '*.csv')],
                initialfile='modelo_vazio.csv'
            )
        
        if not filepath:
            return False
        
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(EXPECTED_COLUMNS)
            messagebox.showinfo('Sucesso', f'Modelo vazio salvo em {filepath}')
            return True
        except Exception as e:
            messagebox.showerror('Erro', str(e))
            return False

    @staticmethod
    def export_png(
        patients: List[Dict[str, str]],
        layout: LayoutModel,
        fonts_map: Dict[str, List],
        logo_image: Optional[Image.Image] = None,
        save_dir: Optional[str] = None
    ) -> bool:
        """
        Exporta pulseiras como PNG.
        
        Args:
            patients: Lista de dados de pacientes
            layout: Modelo de layout
            fonts_map: Mapa de fontes do sistema
            logo_image: Imagem do logotipo (opcional)
            save_dir: Diretório de saída (se None, abre diálogo)
            
        Returns:
            True se exportado com sucesso
        """
        if not patients:
            messagebox.showwarning('Aviso', 'Nenhum paciente importado.')
            return False
        
        if save_dir is None:
            save_dir = filedialog.askdirectory()
        
        if not save_dir:
            return False
        
        choice = messagebox.askquestion(
            'Formato PNG',
            'Deseja salvar cada pulseira como arquivo separado? (Sim = separado, Não = único arquivo grande)'
        )
        
        images = []
        for i, p in enumerate(patients):
            # Usa render_layout_to_image se layout tem items, senão usa create_pulseira_image
            if layout and layout.items:
                img = render_layout_to_image(layout, p, fonts_map, logo_image=logo_image)
            else:
                from .render import create_pulseira_image
                img = create_pulseira_image(p, fonts_map, logo_image=logo_image)
            
            images.append((p, img))
            if choice == 'yes':
                fname = os.path.join(save_dir, f"pulseira_{i+1}_{p.get('Número da carteirinha','')}.png")
                img.save(fname, dpi=(DPI, DPI))
        
        if choice == 'no':
            total_h = sum(img.height for _, img in images)
            w = images[0][1].width
            big = Image.new('RGB', (w, total_h), (255, 255, 255))
            y = 0
            for _, img in images:
                big.paste(img, (0, y))
                y += img.height
            fname = os.path.join(save_dir, 'pulseiras_todas.png')
            big.save(fname, dpi=(DPI, DPI))
        
        messagebox.showinfo('Sucesso', f'Exportação PNG concluída em {save_dir}')
        return True

    @staticmethod
    def export_pdf(
        patients: List[Dict[str, str]],
        layout: LayoutModel,
        fonts_map: Dict[str, List],
        logo_image: Optional[Image.Image] = None,
        save_path: Optional[str] = None
    ) -> bool:
        """
        Exporta pulseiras como PDF.
        
        Args:
            patients: Lista de dados de pacientes
            layout: Modelo de layout
            fonts_map: Mapa de fontes do sistema
            logo_image: Imagem do logotipo (opcional)
            save_path: Caminho do arquivo (se None, abre diálogo)
            
        Returns:
            True se exportado com sucesso
        """
        if not patients:
            messagebox.showwarning('Aviso', 'Nenhum paciente importado.')
            return False
        
        try:
            from reportlab.lib.utils import ImageReader
            from reportlab.pdfgen import canvas as pdfcanvas
        except ImportError:
            messagebox.showerror('Erro', 'ReportLab não está instalado.')
            return False
        
        choice = messagebox.askquestion(
            'Formato PDF',
            'Deseja salvar cada pulseira como PDF separado? (Sim = separados, Não = único PDF)'
        )
        
        try:
            if choice == 'yes':
                save_dir = filedialog.askdirectory()
                if not save_dir:
                    return False
                
                for i, p in enumerate(patients):
                    # Usa render_layout_to_image se layout tem items, senão usa create_pulseira_image
                    if layout and layout.items:
                        img = render_layout_to_image(layout, p, fonts_map, logo_image=logo_image)
                    else:
                        from .render import create_pulseira_image
                        img = create_pulseira_image(p, fonts_map, logo_image=logo_image)
                    
                    buf = io.BytesIO()
                    img.save(buf, format='PNG', dpi=(DPI, DPI))
                    buf.seek(0)
                    
                    pdf_path = os.path.join(save_dir, f"pulseira_{i+1}_{p.get('Número da carteirinha','')}.pdf")
                    c = pdfcanvas.Canvas(pdf_path, pagesize=(P_WIDTH * 72.0 / DPI, P_HEIGHT * 72.0 / DPI))
                    c.drawImage(ImageReader(buf), 0, 0, width=P_WIDTH * 72.0 / DPI, height=P_HEIGHT * 72.0 / DPI)
                    c.showPage()
                    c.save()
                
                messagebox.showinfo('Sucesso', f'PDFs separados salvos em {save_dir}')
            else:
                if save_path is None:
                    save_path = filedialog.asksaveasfilename(
                        defaultextension='.pdf',
                        filetypes=[('PDF', '*.pdf')],
                        initialfile='pulseiras.pdf'
                    )
                
                if not save_path:
                    return False
                
                c = pdfcanvas.Canvas(save_path, pagesize=(P_WIDTH * 72.0 / DPI, P_HEIGHT * 72.0 / DPI))
                for p in patients:
                    # Usa render_layout_to_image se layout tem items, senão usa create_pulseira_image
                    if layout and layout.items:
                        img = render_layout_to_image(layout, p, fonts_map, logo_image=logo_image)
                    else:
                        from .render import create_pulseira_image
                        img = create_pulseira_image(p, fonts_map, logo_image=logo_image)
                    
                    buf = io.BytesIO()
                    img.save(buf, format='PNG', dpi=(DPI, DPI))
                    buf.seek(0)
                    c.drawImage(ImageReader(buf), 0, 0, width=P_WIDTH * 72.0 / DPI, height=P_HEIGHT * 72.0 / DPI)
                    c.showPage()
                c.save()
                messagebox.showinfo('Sucesso', f'PDF salvo em {save_path}')
            
            return True
        except Exception as e:
            messagebox.showerror('Erro', f'Falha ao gerar PDF: {e}')
            return False
