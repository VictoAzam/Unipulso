"""
Módulo para impressão direta em impressoras Zebra ZD230
Utiliza comandos ZPL (Zebra Programming Language) via comunicação RAW
"""

import os
import platform
from typing import Dict, Any, Optional, List
from PIL import Image
import io
import base64


class ZebraPrinter:
    """
    Classe para gerenciar impressão em impressoras Zebra via ZPL.
    
    ZPL (Zebra Programming Language) é uma linguagem de comandos
    usada para controlar impressoras Zebra. Permite impressão direta
    sem necessidade de drivers gráficos, resultando em melhor performance.
    """
    
    def __init__(self, printer_name: str = "Zebra ZD230"):
        """
        Inicializa o gerenciador da impressora Zebra.
        
        Args:
            printer_name: Nome exato da impressora como aparece no sistema
                         (ex: "Zebra ZD230", "ZDesigner ZD230-203dpi ZPL")
        """
        self.printer_name = printer_name
        self.system = platform.system()  # Detecta SO (Windows, Linux, Darwin)
        
        # === Inicializa biblioteca específica do sistema operacional ===
        if self.system == "Windows":
            try:
                import win32print  # Biblioteca de impressão Windows
                self.win32print = win32print
            except ImportError:
                # Se pywin32 não estiver instalado, levanta erro instrutivo
                raise ImportError(
                    "Módulo win32print não encontrado. "
                    "Instale com: pip install pywin32"
                )
    
    def list_printers(self) -> List[str]:
        """
        Lista todas as impressoras instaladas no sistema.
        Funciona em Windows (win32print) e Linux (CUPS).
        
        Returns:
            Lista com nomes exatos das impressoras como aparecem no sistema
        """
        if self.system == "Windows":
            printers = []
            # EnumPrinters(2) lista todas as impressoras locais e de rede
            for printer in self.win32print.EnumPrinters(2):
                # printer[2] contém o nome da impressora
                printers.append(printer[2])
            return printers
        else:
            # Para Linux/Unix, usa CUPS (Common Unix Printing System)
            try:
                import cups
                conn = cups.Connection()  # Conecta ao servidor CUPS
                # getPrinters() retorna dicionário {nome: info}
                return list(conn.getPrinters().keys())
            except ImportError:
                print("[WARN] Módulo cups não encontrado. Instale com: pip install pycups")
                return []
    
    def is_printer_available(self) -> bool:
        """
        Verifica se a impressora configurada está disponível.
        
        Returns:
            True se a impressora está disponível, False caso contrário
        """
        available_printers = self.list_printers()
        return self.printer_name in available_printers
    
    def send_zpl(self, zpl_command: str) -> bool:
        """
        Envia comandos ZPL diretamente para a impressora.
        
        ZPL (Zebra Programming Language) é uma linguagem de texto puro.
        Exemplo de comando: "^XA^FO50,50^A0N,50,50^FDTeste^FS^XZ"
        
        Args:
            zpl_command: String com comando(s) ZPL completo(s)
                        Deve iniciar com ^XA e terminar com ^XZ
            
        Returns:
            True se enviado com sucesso, False caso contrário
        """
        try:
            # Roteia para função específica do sistema operacional
            if self.system == "Windows":
                return self._send_zpl_windows(zpl_command)
            else:
                return self._send_zpl_linux(zpl_command)
        except Exception as e:
            print(f"[ERROR] Erro ao enviar ZPL: {e}")
            return False
    
    def _send_zpl_windows(self, zpl_command: str) -> bool:
        """
        Envia comandos ZPL via Windows usando win32print (impressão RAW).
        
        Impressão RAW envia dados diretamente à impressora sem processamento
        do driver gráfico, permitindo uso de comandos ZPL nativos.
        
        Args:
            zpl_command: Comando ZPL a ser enviado
            
        Returns:
            True se enviado com sucesso
        """
        try:
            # ETAPA 1: Abre conexão com a impressora pelo nome
            hprinter = self.win32print.OpenPrinter(self.printer_name)
            
            try:
                # ETAPA 2: Inicia um novo documento de impressão
                # Parâmetros: (handle_impressora, nível, (nome_doc, arquivo_saida, tipo_dados))
                hjob = self.win32print.StartDocPrinter(hprinter, 1, ("Pulseira", None, "RAW"))
                # "RAW" indica que os dados serão enviados sem processamento
                
                try:
                    # ETAPA 3: Inicia uma nova página
                    self.win32print.StartPagePrinter(hprinter)
                    
                    # ETAPA 4: Envia o comando ZPL (converte string para bytes UTF-8)
                    self.win32print.WritePrinter(hprinter, zpl_command.encode('utf-8'))
                    
                    # ETAPA 5: Finaliza a página (dispara impressão)
                    self.win32print.EndPagePrinter(hprinter)
                    
                finally:
                    # ETAPA 6: Finaliza o documento (sempre executado)
                    self.win32print.EndDocPrinter(hprinter)
            finally:
                # ETAPA 7: Fecha a conexão com a impressora (sempre executado)
                self.win32print.ClosePrinter(hprinter)
            
            return True  # Sucesso!
            
        except Exception as e:
            print(f"[ERROR] Erro ao imprimir (Windows): {e}")
            return False
    
    def _send_zpl_linux(self, zpl_command: str) -> bool:
        """
        Envia comandos ZPL via Linux (CUPS).
        
        Args:
            zpl_command: Comando ZPL a ser enviado
            
        Returns:
            True se enviado com sucesso
        """
        try:
            import cups
            
            # Conectar ao CUPS
            conn = cups.Connection()
            
            # Criar arquivo temporário com ZPL
            temp_file = "/tmp/zebra_zpl.txt"
            with open(temp_file, 'w') as f:
                f.write(zpl_command)
            
            # Enviar para impressora
            conn.printFile(self.printer_name, temp_file, "Pulseira", {})
            
            # Remover arquivo temporário
            os.remove(temp_file)
            
            return True
            
        except Exception as e:
            print(f"[ERROR] Erro ao imprimir (Linux): {e}")
            return False
    
    def print_test(self) -> bool:
        """
        Imprime uma etiqueta de teste.
        
        Returns:
            True se impressão foi bem-sucedida
        """
        zpl = """
^XA
^FO50,50^ADN,36,20^FDTeste de Impressao^FS
^FO50,100^ADN,24,12^FDImpressora Zebra ZD230^FS
^FO50,150^ADN,24,12^FDSistema Unipulso^FS
^XZ
"""
        return self.send_zpl(zpl.strip())


def generate_bracelet_zpl(patient_data: Dict[str, Any], qr_data: str = None) -> str:
    """
    Gera comandos ZPL para impressão de pulseira hospitalar.
    
    Layout da pulseira (11cm de largura útil):
    - QR Code à esquerda
    - Informações do paciente à direita
    
    Args:
        patient_data: Dicionário com dados do paciente
        qr_data: Dados para o QR Code (padrão: número da carteirinha)
        
    Returns:
        String com comandos ZPL
    """
    # Configurações da impressora Zebra ZD230
    # DPI: 203 (8 dots/mm)
    # Largura da pulseira: ~25mm (2 polegadas)
    # Comprimento útil: ~110mm (11cm)
    
    # Conversão: 203 DPI = 8 dots/mm
    # 11cm = 110mm = 880 dots
    # 2cm (altura) = 20mm = 160 dots
    
    # Dados do paciente
    nome = patient_data.get('Nome do paciente', '')
    carteirinha = patient_data.get('Número da carteirinha', '')
    data_nasc = patient_data.get('Data de nascimento', '')
    mae = patient_data.get('Nome da mãe', '')
    convenio = patient_data.get('Convênio', '')
    medico = patient_data.get('Médico responsável', '')
    sexo = patient_data.get('Sexo', '')
    data_adm = patient_data.get('Data de admissão', '')
    hora_adm = patient_data.get('Hora de admissão', '')
    observacao = patient_data.get('Observação', '')
    
    # QR Code data
    if not qr_data:
        qr_data = carteirinha
    
    # Montar comando ZPL
    # ^XA = Início do formato
    # ^FO = Field Origin (posição X,Y em dots)
    # ^A = Font (tipo, altura, largura)
    # ^FD = Field Data (dados a imprimir)
    # ^FS = Field Separator (fim do campo)
    # ^BQ = QR Code
    # ^XZ = Fim do formato
    
    zpl = f"""^XA
~TA000
~JSN
^LT0
^MNW
^MTT
^PON
^PMN
^LH0,0
^JMA
^PR4,4
~SD15
^JUS
^LRN
^CI27
^PA0,1,1,0

^MMT
^PW880
^LL160
^LS0

^FT30,30^BQN,2,4
^FH\\^FDQA,{qr_data}^FS

^FT200,30^A0N,24,24^FH\\^FD{nome[:30]}^FS
^FT200,60^A0N,16,16^FH\\^FDCart: {carteirinha}^FS

^FT200,90^A0N,14,14^FH\\^FDNasc: {data_nasc}^FS
^FT350,90^A0N,14,14^FH\\^FDConv: {convenio[:15]}^FS

^FT200,110^A0N,14,14^FH\\^FDMae: {mae[:25]}^FS

^FT200,130^A0N,14,14^FH\\^FDMed: {medico[:20]}^FS
^FT500,130^A0N,14,14^FH\\^FDSex: {sexo}^FS

^FT200,150^A0N,14,14^FH\\^FDAdm: {data_adm} {hora_adm}^FS

^FT200,180^A0N,12,12^FH\\^FDObs: {observacao[:40]}^FS

^PQ1,0,1,Y
^XZ
"""
    
    return zpl.strip()


def test_printer_connection(printer_name: str = "Zebra ZD230") -> Dict[str, Any]:
    """
    Testa a conexão com a impressora Zebra.
    
    Args:
        printer_name: Nome da impressora
        
    Returns:
        Dicionário com status da conexão
    """
    result = {
        'connected': False,
        'printer_name': printer_name,
        'available_printers': [],
        'error': None
    }
    
    try:
        printer = ZebraPrinter(printer_name)
        result['available_printers'] = printer.list_printers()
        result['connected'] = printer.is_printer_available()
        
        if not result['connected']:
            result['error'] = f"Impressora '{printer_name}' não encontrada no sistema"
    
    except Exception as e:
        result['error'] = str(e)
    
    return result


# Exemplo de uso
if __name__ == "__main__":
    # Testar conexão
    print("=" * 60)
    print("TESTE DE CONEXÃO COM IMPRESSORA ZEBRA ZD230")
    print("=" * 60)
    
    test_result = test_printer_connection()
    
    print(f"\nImpressoras disponíveis:")
    for p in test_result['available_printers']:
        print(f"  - {p}")
    
    print(f"\nImpressora configurada: {test_result['printer_name']}")
    print(f"Status: {'✓ Conectada' if test_result['connected'] else '✗ Não encontrada'}")
    
    if test_result['error']:
        print(f"Erro: {test_result['error']}")
    
    # Se conectada, fazer teste de impressão
    if test_result['connected']:
        print("\n" + "=" * 60)
        print("TESTE DE IMPRESSÃO")
        print("=" * 60)
        
        resposta = input("\nDeseja imprimir uma etiqueta de teste? (s/n): ")
        
        if resposta.lower() == 's':
            printer = ZebraPrinter(test_result['printer_name'])
            
            if printer.print_test():
                print("✓ Etiqueta de teste enviada com sucesso!")
            else:
                print("✗ Erro ao enviar etiqueta de teste")
