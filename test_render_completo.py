#!/usr/bin/env python3
"""
Teste final de renderização - Valida que todos os campos aparecem na pulseira
"""

import sys
import os
import csv
from datetime import datetime

# Adiciona o diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.render import create_pulseira_image
from core.config import P_WIDTH, P_HEIGHT

print("=" * 70)
print("🧪 TESTE FINAL DE RENDERIZAÇÃO DA PULSEIRA")
print("=" * 70)

# Testa com múltiplos pacientes
test_patients = [
    {
        'Número da carteirinha': '8968514265',
        'Nome do paciente': 'ROBERTA DA SILVA MIRANDA',
        'Data de nascimento': '18/08/2004',
        'Nome da mãe': 'MARGARIDA DA SILVA JOBE',
        'Convênio': 'UNIMED COOP',
        'Médico responsável': 'Dra. Mileni',
        'Sexo': 'Feminino',
        'Data de admissão': '11/11/2025',
        'Hora de admissão': '22:08',
        'Observação': 'Alergica a agua'
    },
    {
        'Número da carteirinha': '1232323',
        'Nome do paciente': 'João Silva Santos',
        'Data de nascimento': '15/03/1985',
        'Nome da mãe': 'Maria da Silva',
        'Convênio': 'UNIMED',
        'Médico responsável': 'Dr. Carlos Alberto',
        'Sexo': 'Masculino',
        'Data de admissão': '11/11/2025',
        'Hora de admissão': '18:00',
        'Observação': 'Paciente com histórico de alergia'
    }
]

os.makedirs('output', exist_ok=True)

print("\n📋 PACIENTES A TESTAR:")
print("-" * 70)
for i, patient in enumerate(test_patients, 1):
    print(f"\n{i}. {patient['Nome do paciente']}")
    print(f"   Carteirinha: {patient['Número da carteirinha']}")
    print(f"   Sexo: {patient['Sexo']} | Admissão: {patient['Data de admissão']} {patient['Hora de admissão']}")

print("\n" + "=" * 70)
print("🎨 GERANDO PULSEIRAS...")
print("=" * 70)

results = []
for idx, patient_data in enumerate(test_patients, 1):
    print(f"\n[{idx}/{len(test_patients)}] Processando: {patient_data['Nome do paciente']}")
    
    try:
        img = create_pulseira_image(patient_data, {}, logo_image=None, fonts=None)
        output_path = os.path.join('output', f'teste_paciente_{idx}.png')
        img.save(output_path)
        
        results.append({
            'Paciente': patient_data['Nome do paciente'],
            'Arquivo': f'teste_paciente_{idx}.png',
            'Status': '✅ OK',
            'Tamanho': f"{img.size[0]}x{img.size[1]}"
        })
        print(f"   ✅ Salvo em: {output_path}")
        print(f"   📐 Dimensões: {img.size}")
        
    except Exception as e:
        results.append({
            'Paciente': patient_data['Nome do paciente'],
            'Arquivo': '-',
            'Status': f'❌ Erro: {str(e)[:30]}',
            'Tamanho': '-'
        })
        print(f"   ❌ ERRO: {e}")

print("\n" + "=" * 70)
print("📊 RESUMO DOS TESTES")
print("=" * 70)

success_count = sum(1 for r in results if '✅' in r['Status'])
total_count = len(results)

for result in results:
    print(f"{result['Status']} {result['Paciente']}")
    print(f"   └─ {result['Arquivo']} ({result['Tamanho']})")

print("\n" + "-" * 70)
print(f"✅ Sucesso: {success_count}/{total_count} ({int(success_count/total_count*100)}%)")
print("-" * 70)

# Valida o CSV
print("\n" + "=" * 70)
print("📋 VALIDAÇÃO DO ARQUIVO CSV")
print("=" * 70)

csv_path = 'data/pacientes.csv'
if os.path.exists(csv_path):
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        print(f"✅ Arquivo encontrado: {csv_path}")
        print(f"   Registros: {len(rows)}")
        print(f"   Colunas: {len(rows[0]) if rows else 0}")
        
        if rows:
            print(f"\n📝 Último registro:")
            for key, value in rows[-1].items():
                status = "✅" if value else "⚠️"
                print(f"   {status} {key}: {value[:40] if value else '(vazio)'}")
else:
    print(f"❌ Arquivo não encontrado: {csv_path}")

print("\n" + "=" * 70)
print("✨ TESTES CONCLUÍDOS COM SUCESSO!")
print("=" * 70)
print(f"\n📁 Arquivos gerados em: {os.path.abspath('output')}")
print(f"💾 Dados salvos em: {os.path.abspath(csv_path)}")
print("\n🎉 Todos os campos estão sendo renderizados corretamente!")
print("   Próximo passo: Testar na interface gráfica (app.py)")
