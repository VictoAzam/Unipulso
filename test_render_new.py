#!/usr/bin/env python3
"""
Script para testar a renderização da pulseira com os novos campos
"""

import sys
import os

# Adiciona o diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.render import create_pulseira_image
from core.config import P_WIDTH, P_HEIGHT

# Dados do paciente da primeira linha do CSV (que estava visível na imagem)
patient_data = {
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
}

# Fonts padrão
fonts = None

# Gera a imagem
print("Gerando pulseira com TODOS os campos visíveis...")
img = create_pulseira_image(patient_data, {}, logo_image=None, fonts=fonts)

# Salva
output_path = os.path.join('output', 'pulseira_teste_completa.png')
os.makedirs('output', exist_ok=True)
img.save(output_path)
print(f"✓ Pulseira salva em: {output_path}")
print(f"  Dimensões: {img.size}")
print("\n📋 Dados renderizados:")
for key, value in patient_data.items():
    print(f"   {key}: {value}")
