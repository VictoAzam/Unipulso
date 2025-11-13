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
    """Classe para gerenciar impressão em impressoras Zebra via ZPL."""
    
    def __init__(self, printer_name: str = "Zebra ZD230"):
        """
        Inicializa o gerenciador da impressora Zebra.
        
        Args:
            printer_name: Nome da impressora instalada no sistema
        """
        self.printer_name = printer_name
        self.system = platform.system()
        
        # Verificar se estamos no Windows
        if self.system == "Windows":
            try:
                import win32print
                self.win32print = win32print
            except ImportError:
                raise ImportError(
                    "Módulo win32print não encontrado. "
                    "Instale com: pip install pywin32"
                )
    
    def list_printers(self) -> List[str]:
        """
        Lista todas as impressoras instaladas no sistema.
        
        Returns:
            Lista com nomes das impressoras
        """
        if self.system == "Windows":
            printers = []
            for printer in self.win32print.EnumPrinters(2):
                printers.append(printer[2])
            return printers
        else:
            # Para Linux, usar CUPS
            try:
                import cups
                conn = cups.Connection()
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
        
        Args:
            zpl_command: Comando ZPL a ser enviado
            
        Returns:
            True se enviado com sucesso, False caso contrário
        """
        try:
            if self.system == "Windows":
                return self._send_zpl_windows(zpl_command)
            else:
                return self._send_zpl_linux(zpl_command)
        except Exception as e:
            print(f"[ERROR] Erro ao enviar ZPL: {e}")
            return False
    
    def _send_zpl_windows(self, zpl_command: str) -> bool:
        """
        Envia comandos ZPL via Windows (win32print).
        
        Args:
            zpl_command: Comando ZPL a ser enviado
            
        Returns:
            True se enviado com sucesso
        """
        try:
            # Abrir impressora
            hprinter = self.win32print.OpenPrinter(self.printer_name)
            
            try:
                # Iniciar documento
                hjob = self.win32print.StartDocPrinter(hprinter, 1, ("Pulseira", None, "RAW"))
                
                try:
                    # Iniciar página
                    self.win32print.StartPagePrinter(hprinter)
                    
                    # Enviar comando ZPL
                    self.win32print.WritePrinter(hprinter, zpl_command.encode('utf-8'))
                    
                    # Finalizar página
                    self.win32print.EndPagePrinter(hprinter)
                    
                finally:
                    # Finalizar documento
                    self.win32print.EndDocPrinter(hprinter)
            finally:
                # Fechar impressora
                self.win32print.ClosePrinter(hprinter)
            
            return True
            
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
