#!/usr/bin/env python3
"""
Script de teste para validar importação de CSV
Ajuda a diagnosticar problemas de colunas
"""

import csv
import sys
from pathlib import Path

# Adiciona o diretório current ao path
sys.path.insert(0, str(Path(__file__).parent))

from config import EXPECTED_COLUMNS
from io_manager import IOManager

def test_csv_structure(csv_file: str):
    """Analisa a estrutura de um arquivo CSV"""
    
    print("=" * 80)
    print("ANÁLISE DE ESTRUTURA DO CSV")
    print("=" * 80)
    print(f"\nArquivo: {csv_file}")
    print(f"\nColunas esperadas ({len(EXPECTED_COLUMNS)}):")
    for i, col in enumerate(EXPECTED_COLUMNS, 1):
        print(f"  {i:2d}. {col}")
    
    # Lê o CSV
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames
            
            print(f"\nColunas encontradas ({len(headers)}):")
            for i, col in enumerate(headers, 1):
                col_stripped = col.strip() if col else '[vazio]'
                status = "✓" if col_stripped in EXPECTED_COLUMNS else "✗"
                print(f"  {i:2d}. [{status}] {repr(col)}")
            
            # Verifica diferenças
            print("\n" + "-" * 80)
            print("DIAGNÓSTICO:")
            print("-" * 80)
            
            headers_normalized = [h.strip() if h else '' for h in headers]
            missing = [col for col in EXPECTED_COLUMNS if col not in headers_normalized]
            extra = [col for col in headers_normalized if col not in EXPECTED_COLUMNS]
            
            if missing:
                print(f"\n❌ COLUNAS FALTANDO ({len(missing)}):")
                for col in missing:
                    print(f"   - {col}")
            else:
                print(f"\n✓ Todas as colunas obrigatórias estão presentes!")
            
            if extra:
                print(f"\n⚠️  COLUNAS EXTRAS ({len(extra)}):")
                for col in extra:
                    print(f"   + {col}")
            else:
                print(f"\n✓ Sem colunas extras desnecessárias!")
            
            # Lê e mostra dados
            print("\n" + "-" * 80)
            print("DADOS (primeiros 3 pacientes):")
            print("-" * 80)
            
            f.seek(0)
            reader = csv.DictReader(f)
            for i, row in enumerate(reader, 1):
                if i > 3:
                    break
                print(f"\nPaciente #{i}:")
                for key, value in row.items():
                    if key and value:  # Só mostra não vazios
                        print(f"  {key.strip()}: {value.strip()}")
            
            # Resumo
            print("\n" + "=" * 80)
            if not missing:
                print("✅ CSV VÁLIDO - Pode ser importado sem problemas!")
            else:
                print("❌ CSV INVÁLIDO - Faltam colunas obrigatórias!")
            print("=" * 80)
            
    except FileNotFoundError:
        print(f"❌ Arquivo não encontrado: {csv_file}")
    except Exception as e:
        print(f"❌ Erro ao ler CSV: {e}")

def main():
    """Principal"""
    
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "  UTILITÁRIO DE TESTE - VALIDAÇÃO DE CSV".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "=" * 78 + "╝")
    print()
    
    # Se passou argumento, usa esse arquivo
    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
        test_csv_structure(csv_file)
    else:
        print("USO: python test_csv_import.py <caminho_do_csv>")
        print("\nExemplo:")
        print("  python test_csv_import.py dados.csv")
        print("  python test_csv_import.py C:\\Users\\seu_usuario\\dados_pacientes.csv")
        
        # Tenta com um arquivo de exemplo se existir
        exemplo_path = Path(__file__).parent / 'exemplo.csv'
        if exemplo_path.exists():
            print(f"\n📁 Encontrado: {exemplo_path}")
            print("Analisando...\n")
            test_csv_structure(str(exemplo_path))

if __name__ == '__main__':
    main()
