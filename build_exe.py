#!/usr/bin/env python3
"""
Script de Build do Unipulso
Automatiza a criação do executável usando PyInstaller
"""

import os
import sys
import shutil
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
    UNDERLINE = '\033[4m'

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

def check_dependencies():
    """Verifica se as dependências necessárias estão instaladas"""
    print_step("Verificando dependências")
    
    dependencies = ['pyinstaller']
    missing = []
    
    for dep in dependencies:
        try:
            __import__(dep)
            print_success(f"{dep} instalado")
        except ImportError:
            missing.append(dep)
            print_error(f"{dep} não encontrado")
    
    if missing:
        print_warning(f"Instalando dependências faltantes: {', '.join(missing)}")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing)
        print_success("Dependências instaladas")
    
    return True

def clean_build():
    """Limpa diretórios de build anteriores"""
    print_step("Limpando builds anteriores")
    
    dirs_to_clean = ['build', 'dist']
    files_to_clean = ['*.spec~', '__pycache__']
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print_success(f"Removido diretório {dir_name}")
    
    print_success("Limpeza concluída")

def create_icon():
    """Cria um ícone se não existir"""
    print_step("Verificando ícone")
    
    logo_dir = Path('logo')
    icon_path = logo_dir / 'icon.ico'
    
    if icon_path.exists():
        print_success(f"Ícone encontrado: {icon_path}")
        return True
    
    print_warning("Ícone não encontrado. O instalador será criado sem ícone personalizado.")
    
    # Você pode adicionar aqui código para converter uma imagem PNG em ICO
    # usando Pillow se necessário
    
    return False

def build_executable():
    """Constrói o executável usando PyInstaller"""
    print_step("Construindo executável")
    
    try:
        # Executar PyInstaller com o arquivo .spec
        cmd = [sys.executable, '-m', 'PyInstaller', 'unipulso.spec', '--clean']
        
        print(f"Executando: {' '.join(cmd)}")
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        print_success("Executável construído com sucesso")
        return True
        
    except subprocess.CalledProcessError as e:
        print_error(f"Erro ao construir executável: {e}")
        if e.stdout:
            print(e.stdout)
        if e.stderr:
            print(e.stderr)
        return False

def verify_build():
    """Verifica se o build foi bem-sucedido"""
    print_step("Verificando build")
    
    dist_dir = Path('dist')
    exe_path = dist_dir / 'Unipulso.exe'
    
    if exe_path.exists():
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print_success(f"Executável criado: {exe_path}")
        print_success(f"Tamanho: {size_mb:.2f} MB")
        return True
    else:
        print_error("Executável não encontrado em dist/")
        return False

def copy_readme():
    """Copia documentação para o diretório de distribuição"""
    print_step("Copiando documentação")
    
    dist_dir = Path('dist')
    docs_to_copy = ['README.md', 'LICENSE', 'GUIA_CSV.md']
    
    for doc in docs_to_copy:
        if Path(doc).exists():
            shutil.copy(doc, dist_dir / doc)
            print_success(f"Copiado: {doc}")

def main():
    """Função principal do script de build"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}")
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║          UNIPULSO - BUILD SCRIPT v1.0                     ║")
    print("║    Gerador de Executável para Windows                     ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    print(f"{Colors.ENDC}\n")
    
    try:
        # Verificar se estamos no diretório correto
        if not Path('app.py').exists():
            print_error("Erro: app.py não encontrado. Execute este script na raiz do projeto.")
            sys.exit(1)
        
        # Verificar se unipulso.spec existe
        if not Path('unipulso.spec').exists():
            print_error("Erro: unipulso.spec não encontrado.")
            sys.exit(1)
        
        # Etapas do build
        if not check_dependencies():
            sys.exit(1)
        
        clean_build()
        create_icon()
        
        if not build_executable():
            sys.exit(1)
        
        if not verify_build():
            sys.exit(1)
        
        copy_readme()
        
        # Sucesso!
        print(f"\n{Colors.OKGREEN}{Colors.BOLD}")
        print("╔═══════════════════════════════════════════════════════════╗")
        print("║               BUILD CONCLUÍDO COM SUCESSO!                ║")
        print("╚═══════════════════════════════════════════════════════════╝")
        print(f"{Colors.ENDC}")
        
        print(f"\n{Colors.OKCYAN}📦 Executável disponível em: dist/Unipulso.exe{Colors.ENDC}")
        print(f"{Colors.OKCYAN}📁 Próximo passo: Execute build_installer.py para criar o instalador{Colors.ENDC}\n")
        
    except KeyboardInterrupt:
        print(f"\n\n{Colors.WARNING}Build cancelado pelo usuário{Colors.ENDC}")
        sys.exit(1)
    except Exception as e:
        print_error(f"Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
