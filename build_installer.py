#!/usr/bin/env python3
"""
Script para criar o instalador Inno Setup do Unipulso
Requer Inno Setup instalado no Windows
"""

import os
import sys
import subprocess
from pathlib import Path

# Cores para output no terminal
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_step(message):
    """Imprime uma etapa do processo"""
    print(f"\n{Colors.OKBLUE}{'='*60}{Colors.ENDC}")
    print(f"{Colors.BOLD}{message}{Colors.ENDC}")
    print(f"{Colors.OKBLUE}{'='*60}{Colors.ENDC}\n")

def print_success(message):
    """Imprime mensagem de sucesso"""
    print(f"{Colors.OKGREEN}✓ {message}{Colors.ENDC}")

def print_error(message):
    """Imprime mensagem de erro"""
    print(f"{Colors.FAIL}✗ {message}{Colors.ENDC}")

def print_warning(message):
    """Imprime mensagem de aviso"""
    print(f"{Colors.WARNING}⚠ {message}{Colors.ENDC}")

def find_inno_setup():
    """Encontra o executável do Inno Setup"""
    print_step("Procurando Inno Setup")
    
    # Locais comuns de instalação do Inno Setup
    possible_paths = [
        r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
        r"C:\Program Files\Inno Setup 6\ISCC.exe",
        r"C:\Program Files (x86)\Inno Setup 5\ISCC.exe",
        r"C:\Program Files\Inno Setup 5\ISCC.exe",
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            print_success(f"Inno Setup encontrado: {path}")
            return path
    
    print_error("Inno Setup não encontrado!")
    print_warning("Por favor, instale o Inno Setup de: https://jrsoftware.org/isdl.php")
    return None

def verify_prerequisites():
    """Verifica se todos os pré-requisitos existem"""
    print_step("Verificando pré-requisitos")
    
    required_files = {
        'installer.iss': 'Script Inno Setup',
        'dist/Unipulso.exe': 'Executável (execute build_exe.py primeiro)',
    }
    
    all_ok = True
    for file_path, description in required_files.items():
        if Path(file_path).exists():
            print_success(f"{description}: {file_path}")
        else:
            print_error(f"{description} não encontrado: {file_path}")
            all_ok = False
    
    return all_ok

def create_installer(iscc_path):
    """Cria o instalador usando Inno Setup"""
    print_step("Criando instalador")
    
    try:
        # Criar diretório de saída se não existir
        os.makedirs('installer_output', exist_ok=True)
        
        # Executar Inno Setup Compiler
        cmd = [iscc_path, 'installer.iss']
        
        print(f"Executando: {' '.join(cmd)}")
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        print(result.stdout)
        print_success("Instalador criado com sucesso!")
        return True
        
    except subprocess.CalledProcessError as e:
        print_error(f"Erro ao criar instalador: {e}")
        if e.stdout:
            print(e.stdout)
        if e.stderr:
            print(e.stderr)
        return False

def verify_installer():
    """Verifica se o instalador foi criado"""
    print_step("Verificando instalador")
    
    installer_dir = Path('installer_output')
    
    if not installer_dir.exists():
        print_error("Diretório installer_output não encontrado")
        return False
    
    # Procurar arquivo .exe na pasta
    installers = list(installer_dir.glob('*.exe'))
    
    if installers:
        installer = installers[0]
        size_mb = installer.stat().st_size / (1024 * 1024)
        print_success(f"Instalador criado: {installer}")
        print_success(f"Tamanho: {size_mb:.2f} MB")
        return True
    else:
        print_error("Nenhum instalador .exe encontrado")
        return False

def main():
    """Função principal"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}")
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║        UNIPULSO - INSTALLER BUILDER v1.0                  ║")
    print("║    Gerador de Instalador para Windows                     ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    print(f"{Colors.ENDC}\n")
    
    try:
        # Encontrar Inno Setup
        iscc_path = find_inno_setup()
        if not iscc_path:
            print_error("\nNão é possível continuar sem o Inno Setup.")
            print_warning("Instale o Inno Setup e tente novamente.")
            sys.exit(1)
        
        # Verificar pré-requisitos
        if not verify_prerequisites():
            print_error("\nPré-requisitos não satisfeitos.")
            print_warning("Execute 'python build_exe.py' primeiro para gerar o executável.")
            sys.exit(1)
        
        # Criar instalador
        if not create_installer(iscc_path):
            sys.exit(1)
        
        # Verificar resultado
        if not verify_installer():
            sys.exit(1)
        
        # Sucesso!
        print(f"\n{Colors.OKGREEN}{Colors.BOLD}")
        print("╔═══════════════════════════════════════════════════════════╗")
        print("║          INSTALADOR CRIADO COM SUCESSO!                   ║")
        print("╚═══════════════════════════════════════════════════════════╝")
        print(f"{Colors.ENDC}")
        
        print(f"\n{Colors.OKCYAN}📦 Instalador disponível em: installer_output/{Colors.ENDC}")
        print(f"{Colors.OKCYAN}🚀 Distribua este arquivo para instalação em outros computadores{Colors.ENDC}\n")
        
    except KeyboardInterrupt:
        print(f"\n\n{Colors.WARNING}Processo cancelado pelo usuário{Colors.ENDC}")
        sys.exit(1)
    except Exception as e:
        print_error(f"Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
