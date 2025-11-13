#!/usr/bin/env python3
"""
Script de teste: Exportar uma pulseira de exemplo
"""

import sys
sys.path.insert(0, '.')

import csv
from core.io_manager import IOManager
from core.config import P_WIDTH, P_HEIGHT

# Dados de teste
dados_teste = {
    'Número da carteirinha': '12345678',
    'Nome do paciente': 'João Silva',
    'Data de nascimento': '15/03/1985',
    'Nome da mãe': 'Maria Silva',
    'Convênio': 'Unimed',
    'Médico responsável': 'Dr. Carlos',
    'Sexo': 'Masculino',
    'Data de admissão': '11/11/2025',
    'Hora de admissão': '14:30',
    'Observação': 'Alergia a penicilina'
}

# Adicionar ao CSV de teste
csv_teste = 'data/pacientes_teste.csv'
colunas = list(dados_teste.keys())

with open(csv_teste, 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.DictWriter(f, fieldnames=colunas)
    writer.writeheader()
    writer.writerow(dados_teste)

print("=" * 70)
print("EXPORTAR PULSEIRA DE TESTE")
print("=" * 70)
print(f"\n✅ CSV criado: {csv_teste}")
print(f"\n📊 Dados de teste:")
for chave, valor in dados_teste.items():
    print(f"   {chave}: {valor}")

# Renderizar diretamente
from core.render import render_layout_to_image
from core.models import LayoutModel
from core.config import FONT_REGULAR, FONT_BOLD

output_png = 'pulseira_teste.png'

try:
    # Não vamos usar layout complexo, apenas criar a imagem
    from app import PulseiraApp
    
    # Layout padrão da app
    class FakeRoot:
        pass
    
    # Renderizar a pulseira com o layout
    from core.render import create_pulseira_image
    fonts_map = {'regular': FONT_REGULAR, 'bold': FONT_BOLD}
    
    img = create_pulseira_image(dados_teste, fonts_map)
    img.save(output_png, dpi=(300, 300))
    
    print(f"\n✅ PNG exportado: {output_png}")
    print(f"   Dimensões: {P_WIDTH}px × {P_HEIGHT}px")
    print(f"   Tamanho físico: 29.5cm × 2.0cm")
except Exception as e:
    print(f"\n❌ Erro ao exportar PNG: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("VERIFICAÇÃO VISUAL:")
print("  1. Abra pulseira_teste.png em um editor de imagem")
print("  2. Verifique se:")
print("     ✓ QR Code está à esquerda, sem sobreposição de texto")
print("     ✓ Nenhum texto sai pela borda direita")
print("     ✓ Espaçamento entre linhas é consistente")
print("=" * 70)
