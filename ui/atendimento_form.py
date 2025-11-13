"""
Módulo de Formulário de Atendimento
Responsável por coletar dados de novos pacientes via formulário interativo
"""

import csv
import os
from datetime import datetime
from typing import Dict, Optional
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox, filedialog
from pathlib import Path


class AtendimentoForm:
    """Formulário interativo para iniciar atendimento de novos pacientes"""

    # Campos do formulário com suas configurações
    CAMPOS = {
        'Número da carteirinha': {'obrigatorio': True, 'tipo': 'entry'},
        'Nome do paciente': {'obrigatorio': True, 'tipo': 'entry'},
        'Data de nascimento': {'obrigatorio': True, 'tipo': 'entry', 'placeholder': 'DD/MM/AAAA'},
        'Nome da mãe': {'obrigatorio': True, 'tipo': 'entry'},
        'Convênio': {'obrigatorio': True, 'tipo': 'entry'},
        'Médico responsável': {'obrigatorio': True, 'tipo': 'entry'},
        'Sexo': {'obrigatorio': True, 'tipo': 'combobox', 'opcoes': ['Masculino', 'Feminino', 'Outro']},
        'Data de admissão': {'obrigatorio': True, 'tipo': 'entry', 'placeholder': 'DD/MM/AAAA'},
        'Hora de admissão': {'obrigatorio': True, 'tipo': 'entry', 'placeholder': 'HH:MM'},
        'Observação': {'obrigatorio': False, 'tipo': 'text'},
    }

    # Mapeamento para nomes de colunas CSV (em inglês para compatibilidade)
    COLUNAS_CSV = [
        'Número da carteirinha',
        'Nome do paciente',
        'Data de nascimento',
        'Nome da mãe',
        'Convênio',
        'Médico responsável',
        'Sexo',
        'Data de admissão',
        'Hora de admissão',
        'Observação'
    ]

    def __init__(self, parent_root, diretorio_dados: str = 'data'):
        """
        Inicializa o formulário de atendimento
        
        Args:
            parent_root: Janela pai da aplicação
            diretorio_dados: Diretório onde armazenar CSVs
        """
        self.parent_root = parent_root
        self.diretorio_dados = diretorio_dados
        self.arquivo_csv = os.path.join(diretorio_dados, 'pacientes.csv')
        self.campos_entrada = {}
        self.window = None
        
        # Criar diretório de dados se não existir
        Path(diretorio_dados).mkdir(parents=True, exist_ok=True)
        
        # Garantir que o CSV existe com cabeçalho
        self._garantir_csv_existe()

    def _garantir_csv_existe(self):
        """Cria arquivo CSV com cabeçalho se não existir"""
        if not os.path.exists(self.arquivo_csv):
            try:
                with open(self.arquivo_csv, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(self.COLUNAS_CSV)
            except Exception as e:
                messagebox.showerror('Erro', f'Erro ao criar arquivo CSV: {str(e)}')

    def abrir_formulario(self):
        """Abre a janela do formulário de atendimento"""
        self.window = tb.Toplevel(self.parent_root)
        self.window.title('Iniciar Atendimento')
        self.window.geometry('600x700')
        self.window.resizable(False, False)

        # Frame principal com scroll
        main_frame = tb.Frame(self.window)
        main_frame.pack(fill=BOTH, expand=YES, padx=10, pady=10)

        # Título
        titulo = tb.Label(
            main_frame,
            text='Formulário de Atendimento',
            font=('Arial', 14, 'bold')
        )
        titulo.pack(pady=10)

        # Frame para scroll
        canvas_frame = tb.Frame(main_frame)
        canvas_frame.pack(fill=BOTH, expand=YES)

        canvas = tb.Canvas(canvas_frame, highlightthickness=0)
        scrollbar = tb.Scrollbar(canvas_frame, orient='vertical', command=canvas.yview)
        scrollable_frame = tb.Frame(canvas)

        scrollable_frame.bind(
            '<Configure>',
            lambda e: canvas.configure(scrollregion=canvas.bbox('all'))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side='left', fill=BOTH, expand=YES)
        scrollbar.pack(side='right', fill='y')

        # Criar campos do formulário
        self._criar_campos(scrollable_frame)

        # Frame dos botões
        btn_frame = tb.Frame(main_frame)
        btn_frame.pack(fill=X, pady=10)

        btn_salvar = tb.Button(
            btn_frame,
            text='💾 Salvar',
            command=self._salvar_atendimento,
            bootstyle='success',
            width=15
        )
        btn_salvar.pack(side=LEFT, padx=5)

        btn_salvar_novo = tb.Button(
            btn_frame,
            text='💾➕ Salvar e Adicionar Outro',
            command=self._salvar_e_adicionar_outro,
            bootstyle='success-outline',
            width=25
        )
        btn_salvar_novo.pack(side=LEFT, padx=5)

        btn_limpar = tb.Button(
            btn_frame,
            text='🔄 Limpar',
            command=self._limpar_campos,
            bootstyle='info',
            width=12
        )
        btn_limpar.pack(side=LEFT, padx=5)

        btn_cancelar = tb.Button(
            btn_frame,
            text='❌ Cancelar',
            command=self._cancelar_formulario,
            bootstyle='danger',
            width=12
        )
        btn_cancelar.pack(side=LEFT, padx=5)

        # Centralizar janela
        self.window.transient(self.parent_root)
        self.window.grab_set()
        
        # ✅ CORREÇÃO MÓDULO 2: Limpeza TOTAL de todos os campos (sem dados do paciente anterior)
        self.window.after(50, self._limpar_campos_completo)
        
        # ✅ CORREÇÃO MÓDULO 2: Preencher APENAS data/hora de admissão (horário do sistema)
        self.window.after(100, self._preencher_data_hora_automatica)

    def _criar_campos(self, parent_frame):
        """Cria os campos do formulário dinamicamente"""
        for nome_campo, config in self.CAMPOS.items():
            # Frame do campo
            field_frame = tb.Frame(parent_frame)
            field_frame.pack(fill=X, pady=8)

            # Label
            label_text = nome_campo
            if config['obrigatorio']:
                label_text += ' *'
            
            label = tb.Label(
                field_frame,
                text=label_text,
                font=('Arial', 10)
            )
            label.pack(anchor='w')

            # Widget de entrada
            if config['tipo'] == 'entry':
                entrada = tb.Entry(field_frame, width=50)
                entrada.pack(fill=X, pady=2)
                
                # Placeholder
                if 'placeholder' in config:
                    entrada.insert(0, config['placeholder'])
                    entrada.bind('<FocusIn>', lambda e, w=entrada, p=config['placeholder']: self._limpar_placeholder(w, p))
                    entrada.bind('<FocusOut>', lambda e, w=entrada, p=config['placeholder']: self._restaurar_placeholder(w, p))
                
                self.campos_entrada[nome_campo] = entrada

            elif config['tipo'] == 'combobox':
                combo = tb.Combobox(
                    field_frame,
                    values=config['opcoes'],
                    state='readonly',
                    width=47
                )
                combo.pack(fill=X, pady=2)
                self.campos_entrada[nome_campo] = combo

            elif config['tipo'] == 'text':
                text = tb.Text(field_frame, height=4, width=50)
                text.pack(fill=X, pady=2)
                self.campos_entrada[nome_campo] = text

    def _limpar_placeholder(self, widget, placeholder):
        """Remove placeholder ao focar no campo"""
        if widget.get() == placeholder:
            widget.delete(0, 'end')
            widget.config(foreground='black')

    def _restaurar_placeholder(self, widget, placeholder):
        """Restaura placeholder se campo vazio"""
        if widget.get() == '':
            widget.insert(0, placeholder)
            widget.config(foreground='gray')

    def _validar_campos(self) -> bool:
        """Valida se todos os campos obrigatórios foram preenchidos"""
        for nome_campo, config in self.CAMPOS.items():
            if config['obrigatorio']:
                widget = self.campos_entrada[nome_campo]
                
                if config['tipo'] == 'text':
                    valor = widget.get('1.0', 'end-1c').strip()
                else:
                    valor = widget.get().strip()
                
                # Verificar placeholder
                if 'placeholder' in config and valor == config['placeholder']:
                    valor = ''
                
                if not valor:
                    messagebox.showwarning(
                        'Campo Obrigatório',
                        f'Preencha o campo: {nome_campo}'
                    )
                    return False
        
        return True

    def _validar_datas(self) -> bool:
        """Valida formato das datas"""
        try:
            data_nasc = self.campos_entrada['Data de nascimento'].get().strip()
            data_admissao = self.campos_entrada['Data de admissão'].get().strip()
            hora_admissao = self.campos_entrada['Hora de admissão'].get().strip()
            
            # Validar datas (DD/MM/AAAA)
            if data_nasc and data_nasc != 'DD/MM/AAAA':
                datetime.strptime(data_nasc, '%d/%m/%Y')
            
            if data_admissao and data_admissao != 'DD/MM/AAAA':
                datetime.strptime(data_admissao, '%d/%m/%Y')
            
            # Validar hora (HH:MM)
            if hora_admissao and hora_admissao != 'HH:MM':
                datetime.strptime(hora_admissao, '%H:%M')
            
            return True
        except ValueError as e:
            messagebox.showerror(
                'Erro de Validação',
                f'Formato de data/hora inválido. Use:\n'
                f'Datas: DD/MM/AAAA\n'
                f'Hora: HH:MM'
            )
            return False

    def _coletar_dados(self) -> Dict[str, str]:
        """Coleta dados do formulário"""
        dados = {}
        for nome_campo, widget in self.campos_entrada.items():
            if isinstance(widget, tb.Text):
                valor = widget.get('1.0', 'end-1c').strip()
            else:
                valor = widget.get().strip()
            
            # Remover placeholder
            for config in self.CAMPOS.values():
                if 'placeholder' in config and valor == config['placeholder']:
                    valor = ''
                    break
            
            dados[nome_campo] = valor
        
        return dados

    def _salvar_atendimento(self):
        """Salva o atendimento no CSV e fecha o formulário"""
        if not self._validar_campos():
            return
        
        if not self._validar_datas():
            return
        
        try:
            dados = self._coletar_dados()
            self._gerar_csv(dados)
            
            messagebox.showinfo(
                'Sucesso',
                'Atendimento iniciado com sucesso!\n\n'
                f'Paciente: {dados["Nome do paciente"]}\n'
                f'Carteirinha: {dados["Número da carteirinha"]}'
            )
            
            # Fechar o formulário após salvar
            self.window.destroy()
            
        except Exception as e:
            messagebox.showerror('Erro', f'Erro ao salvar atendimento: {str(e)}')

    def _salvar_e_adicionar_outro(self):
        """
        🚀 NOVA FUNCIONALIDADE: Salva o paciente atual e prepara para cadastrar outro
        Ideal para dias com muitos atendimentos - agiliza o processo!
        """
        if not self._validar_campos():
            return
        
        if not self._validar_datas():
            return
        
        try:
            dados = self._coletar_dados()
            
            # Adicionar ao CSV (modo append para acumular múltiplos pacientes)
            self._adicionar_ao_csv(dados)
            
            # Mostrar mensagem de sucesso rápida (sem bloquear)
            nome = dados["Nome do paciente"]
            carteirinha = dados["Número da carteirinha"]
            
            # Toast notification (mensagem rápida)
            messagebox.showinfo(
                'Paciente Salvo ✓',
                f'Paciente cadastrado com sucesso!\n\n'
                f'{nome} (Carteirinha: {carteirinha})\n\n'
                f'O formulário será limpo para o próximo paciente.',
                parent=self.window
            )
            
            # Limpar completamente o formulário para novo paciente
            self._limpar_campos_completo()
            
            # Preencher novamente data/hora (atualizadas)
            self.window.after(100, self._preencher_data_hora_automatica)
            
            # Focar no primeiro campo para agilizar
            self.window.after(200, self._focar_primeiro_campo)
            
            print(f"[INFO] ✓ Paciente salvo: {nome}. Formulário limpo para próximo paciente.")
            
        except Exception as e:
            messagebox.showerror('Erro', f'Erro ao salvar atendimento: {str(e)}', parent=self.window)

    def _gerar_csv(self, dados: Dict[str, str]):
        """
        ✅ MÓDULO 1 - CORREÇÃO: Salva APENAS o novo paciente
        Limpa o CSV anterior e adiciona APENAS os novos dados
        
        Args:
            dados: Dicionário com dados do paciente
        """
        try:
            # ✅ LIMPAR CSV anterior e criar novo com APENAS este paciente
            with open(self.arquivo_csv, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=self.COLUNAS_CSV)
                writer.writeheader()  # Escrever cabeçalho
                writer.writerow(dados)  # Escrever APENAS o novo paciente
                
            print(f"[INFO] ✓ CSV atualizado com APENAS o novo paciente: {dados.get('Nome do paciente', 'Sem nome')}")
                
        except Exception as e:
            raise Exception(f'Erro ao escrever no CSV: {str(e)}')

    def _adicionar_ao_csv(self, dados: Dict[str, str]):
        """
        🚀 NOVA FUNCIONALIDADE: Adiciona paciente ao CSV (modo append)
        Usado pelo botão "Salvar e Adicionar Outro" para acumular múltiplos pacientes
        
        Args:
            dados: Dicionário com dados do paciente
        """
        try:
            # Garantir que arquivo existe com cabeçalho
            self._garantir_csv_existe()
            
            # ✅ ADICIONAR paciente ao CSV existente (modo append)
            with open(self.arquivo_csv, 'a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=self.COLUNAS_CSV)
                writer.writerow(dados)
                
            print(f"[INFO] ✓ Paciente adicionado ao CSV: {dados.get('Nome do paciente', 'Sem nome')}")
                
        except Exception as e:
            raise Exception(f'Erro ao adicionar paciente no CSV: {str(e)}')

    def _limpar_campos_completo(self):
        """
        ✅ MÓDULO 1 - CORREÇÃO: Limpeza TOTAL de TODOS os campos
        Remove TODOS os dados do paciente anterior.
        NENHUM campo deve conter informações antigas.
        """
        for nome_campo, widget in self.campos_entrada.items():
            config = self.CAMPOS[nome_campo]
            
            try:
                if isinstance(widget, tb.Text):
                    # Text widgets (Observação) - limpar completamente
                    widget.delete('1.0', 'end')
                elif config['tipo'] == 'combobox':
                    # Combobox (Sexo) - remover seleção
                    widget.set('')
                elif config['tipo'] == 'entry':
                    # Entry widgets - LIMPEZA TOTAL (remove dados anteriores)
                    widget.delete(0, 'end')
                    widget.config(foreground='black')
                else:
                    # Fallback genérico
                    try:
                        widget.delete(0, 'end')
                    except:
                        pass
            except Exception as e:
                print(f"[WARN] Erro ao limpar campo {nome_campo}: {e}")
        
        # Forçar atualização da interface
        self.window.update_idletasks()
        print("[INFO] ✓ Todos os campos do paciente anterior foram limpos")

    def _limpar_campos(self):
        """Limpa todos os campos do formulário (COMPLETAMENTE, sem placeholder)"""
        for nome_campo, widget in self.campos_entrada.items():
            config = self.CAMPOS[nome_campo]
            
            try:
                if isinstance(widget, tb.Text):
                    # Para Text widgets
                    widget.delete('1.0', 'end')
                elif config['tipo'] == 'combobox':
                    # Para Combobox - setar vazio
                    widget.set('')
                elif config['tipo'] == 'entry':
                    # Para Entry widgets - LIMPAR COMPLETAMENTE
                    widget.delete(0, 'end')
                    # NÃO restaurar placeholder para evitar confusão
                    widget.config(foreground='black')
                else:
                    # Fallback genérico
                    widget.delete(0, 'end')
            except Exception as e:
                print(f"[WARN] Erro ao limpar campo {nome_campo}: {e}")

    def _preencher_data_hora_automatica(self):
        """
        ✅ MÓDULO 2 - CORREÇÃO: Preenche APENAS Data e Hora de Admissão
        Única informação preenchida automaticamente = horário do sistema
        Todos os outros campos permanecem vazios (limpos)
        """
        try:
            from datetime import datetime
            
            # Obter data e hora atual do sistema
            agora = datetime.now()
            data_str = agora.strftime('%d/%m/%Y')  # DD/MM/AAAA
            hora_str = agora.strftime('%H:%M')      # HH:MM
            
            # ✅ Preencher APENAS "Data de admissão" (horário do sistema)
            widget_data = self.campos_entrada.get('Data de admissão')
            if widget_data and isinstance(widget_data, tb.Entry):
                widget_data.delete(0, 'end')
                widget_data.insert(0, data_str)
                widget_data.config(foreground='black')
            
            # ✅ Preencher APENAS "Hora de admissão" (horário do sistema)
            widget_hora = self.campos_entrada.get('Hora de admissão')
            if widget_hora and isinstance(widget_hora, tb.Entry):
                widget_hora.delete(0, 'end')
                widget_hora.insert(0, hora_str)
                widget_hora.config(foreground='black')
            
            print(f"[INFO] ✓ Data/Hora de admissão preenchidas automaticamente: {data_str} {hora_str}")
            print(f"[INFO] ✓ Todos os outros campos permanecem vazios (aguardando entrada manual)")
            
        except Exception as e:
            print(f"[WARN] Erro ao preencher data/hora automáticas: {e}")

    def _cancelar_formulario(self):
        """
        ✅ MÓDULO 1 - CORREÇÃO: Cancelar formulário sem salvar
        Fecha o formulário sem adicionar dados ao CSV
        """
        resposta = messagebox.askyesno(
            'Cancelar Atendimento',
            'Deseja realmente cancelar este atendimento?\n\n'
            'Os dados preenchidos não serão salvos.'
        )
        if resposta:
            print("[INFO] ✓ Atendimento cancelado pelo usuário")
            self.window.destroy()

    def _focar_primeiro_campo(self):
        """
        🚀 NOVA FUNCIONALIDADE: Foca automaticamente no primeiro campo
        Agiliza o cadastro após salvar e adicionar outro paciente
        """
        try:
            # Pegar o primeiro campo (Número da carteirinha)
            primeiro_campo = self.campos_entrada.get('Número da carteirinha')
            if primeiro_campo:
                primeiro_campo.focus_set()
                print("[INFO] ✓ Foco no primeiro campo para agilizar cadastro")
        except Exception as e:
            print(f"[WARN] Erro ao focar primeiro campo: {e}")

    def obter_dados_csv(self) -> list:
        """
        Retorna os dados do arquivo CSV como lista de dicionários
        
        Returns:
            Lista com dados dos pacientes
        """
        if not os.path.exists(self.arquivo_csv):
            return []
        
        try:
            dados = []
            with open(self.arquivo_csv, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row:
                        dados.append(row)
            return dados
        except Exception as e:
            messagebox.showerror('Erro', f'Erro ao ler CSV: {str(e)}')
            return []

    def exportar_csv(self, destino: str = None) -> bool:
        """
        Exporta dados para um novo arquivo CSV
        
        Args:
            destino: Caminho do arquivo de destino
            
        Returns:
            True se sucesso, False caso contrário
        """
        if destino is None:
            destino = filedialog.asksaveasfilename(
                defaultextension='.csv',
                filetypes=[('CSV files', '*.csv'), ('All files', '*.*')]
            )
        
        if not destino:
            return False
        
        try:
            dados = self.obter_dados_csv()
            with open(destino, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=self.COLUNAS_CSV)
                writer.writeheader()
                writer.writerows(dados)
            
            messagebox.showinfo('Sucesso', f'Dados exportados para:\n{destino}')
            return True
        except Exception as e:
            messagebox.showerror('Erro', f'Erro ao exportar: {str(e)}')
            return False
