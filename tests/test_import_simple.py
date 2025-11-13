#!/usr/bin/env python3
"""
Script rápido para testar a importação de CSV
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from io_manager import IOManager

print("\n" + "="*60)
print("TESTE DE IMPORTAÇÃO DE CSV")
print("="*60 + "\n")

patients = IOManager.import_csv('teste_dados.csv')

if patients:
    print(f"✅ Importados {len(patients)} pacientes:\n")
    for i, p in enumerate(patients, 1):
        print(f"  {i}. {p.get('Nome do paciente', 'N/A')} ({p.get('Número da carteirinha', 'N/A')})")
        print(f"     Convênio: {p.get('Convênio', 'N/A')}")
        print(f"     Observação: {p.get('Observação', 'N/A')}")
        print()
else:
    print("❌ Nenhum paciente foi importado")

print("="*60 + "\n")
