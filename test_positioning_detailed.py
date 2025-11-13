#!/usr/bin/env python3
"""
Script detalhado de verificação de posicionamento
"""

import sys
sys.path.insert(0, '.')

from core.config import cm_to_px, NP_START_PX, PRINTABLE_W_PX, P_HEIGHT, P_WIDTH
from app import PulseiraApp
from dataclasses import asdict

print("=" * 90)
print("VERIFICAÇÃO DETALHADA DE POSICIONAMENTO - NOME E OBSERVAÇÕES")
print("=" * 90)

# Dimensões
printable_area_start = NP_START_PX
printable_area_end = printable_area_start + PRINTABLE_W_PX

qr_size = int(P_HEIGHT - 2 * cm_to_px(0.1))
qr_x = printable_area_start + cm_to_px(0.1)

info_x_start = qr_x + qr_size + cm_to_px(0.3)
info_available_width = printable_area_end - info_x_start - cm_to_px(0.1)
info_center_x = info_x_start + (info_available_width // 2)

print("\n📐 DIMENSÕES")
print(f"  Pulseira total: {P_WIDTH}px = 29.5cm")
print(f"  Pulseira altura: {P_HEIGHT}px = 2.0cm")

print("\n📍 ÁREA IMPRIMÍVEL")
print(f"  Início: {printable_area_start}px = {printable_area_start/300*2.54:.2f}cm")
print(f"  Fim: {printable_area_end}px = {printable_area_end/300*2.54:.2f}cm")
print(f"  Largura: {PRINTABLE_W_PX}px = 10.0cm")

print("\n🔷 QR CODE")
print(f"  X: {qr_x}px = {qr_x/300*2.54:.2f}cm")
print(f"  Tamanho: {qr_size}px = {qr_size/300*2.54:.2f}cm")
print(f"  Fim: {qr_x + qr_size}px = {(qr_x + qr_size)/300*2.54:.2f}cm")

print("\n📝 ÁREA DE INFORMAÇÕES")
print(f"  X início: {info_x_start}px = {info_x_start/300*2.54:.2f}cm")
print(f"  X centro: {info_center_x}px = {info_center_x/300*2.54:.2f}cm")
print(f"  X fim: {printable_area_end}px = {printable_area_end/300*2.54:.2f}cm")
print(f"  Largura: {info_available_width}px = {info_available_width/300*2.54:.2f}cm")

print("\n" + "=" * 90)
print("ITENS DO LAYOUT")
print("=" * 90)

# Simular o layout
items = []

# Nome
nome_x = info_center_x
nome_y = cm_to_px(0.1)
nome_width = info_available_width

print(f"\n📌 NOME")
print(f"  X: {nome_x}px = {nome_x/300*2.54:.2f}cm (CENTER)")
print(f"  Y: {nome_y}px = {nome_y/300*2.54:.2f}cm")
print(f"  Width: {nome_width}px = {nome_width/300*2.54:.2f}cm")
print(f"  Align: center")
print(f"  Font size: 32")
print(f"  Status: {('✅ OK' if (nome_x > info_x_start and nome_x < printable_area_end) else '❌ ERRO')}")
print(f"  Nota: O 'x' é o CENTER da área imprimível. O texto será centralizado a partir daqui.")

# Carteirinha
cart_x = info_center_x
cart_y = nome_y + 38
cart_width = info_available_width

print(f"\n📌 CARTEIRINHA")
print(f"  X: {cart_x}px = {cart_x/300*2.54:.2f}cm (CENTER)")
print(f"  Y: {cart_y}px = {cart_y/300*2.54:.2f}cm")
print(f"  Width: {cart_width}px = {cart_width/300*2.54:.2f}cm")
print(f"  Align: center")
print(f"  Font size: 20")
print(f"  Status: {('✅ OK' if (cart_x > info_x_start and cart_x < printable_area_end) else '❌ ERRO')}")

# Campos
col_y_start = cm_to_px(0.8)
line_height = cm_to_px(0.3)
col_width = (info_available_width - cm_to_px(0.2)) // 3
col_gap = cm_to_px(0.15)

col1_x = info_x_start
col2_x = col1_x + col_width + col_gap
col3_x = col2_x + col_width + col_gap

print(f"\n📌 CAMPOS (3 COLUNAS)")
print(f"\n  Coluna 1: X={col1_x}px ({col1_x/300*2.54:.2f}cm), Width={col_width}px ({col_width/300*2.54:.2f}cm)")
print(f"    ✓ Nasc: Y={col_y_start}px ({col_y_start/300*2.54:.2f}cm)")
print(f"    ✓ Mãe: Y={col_y_start + line_height}px ({(col_y_start + line_height)/300*2.54:.2f}cm)")
print(f"    ✓ Conv: Y={col_y_start + 2 * line_height}px ({(col_y_start + 2 * line_height)/300*2.54:.2f}cm)")

print(f"\n  Coluna 2: X={col2_x}px ({col2_x/300*2.54:.2f}cm), Width={col_width}px ({col_width/300*2.54:.2f}cm)")
print(f"    ✓ Med: Y={col_y_start}px ({col_y_start/300*2.54:.2f}cm)")
print(f"    ✓ Sex: Y={col_y_start + line_height}px ({(col_y_start + line_height)/300*2.54:.2f}cm)")
print(f"    ✓ Adm: Y={col_y_start + 2 * line_height}px ({(col_y_start + 2 * line_height)/300*2.54:.2f}cm)")

print(f"\n  Coluna 3: X={col3_x}px ({col3_x/300*2.54:.2f}cm), Width={col_width}px ({col_width/300*2.54:.2f}cm)")
print(f"    ✓ Hora: Y={col_y_start}px ({col_y_start/300*2.54:.2f}cm)")

# Observação
obs_y = col_y_start + cm_to_px(1.2)
obs_x = info_x_start
obs_width = info_available_width

print(f"\n📌 OBSERVAÇÃO")
print(f"  X: {obs_x}px = {obs_x/300*2.54:.2f}cm (INÍCIO)")
print(f"  Y: {obs_y}px = {obs_y/300*2.54:.2f}cm")
print(f"  Width: {obs_width}px = {obs_width/300*2.54:.2f}cm")
print(f"  Align: left")
print(f"  Font size: 14")
print(f"  Status: {('✅ OK' if (obs_x >= info_x_start and obs_x + obs_width <= printable_area_end) else '❌ ERRO')}")

print("\n" + "=" * 90)
print("ANÁLISE DE CENTALIZAÇÃO")
print("=" * 90)

# Nome deve estar centralizado
nome_text = "João Silva"  # Exemplo
nome_px_length = len(nome_text) * 16  # Aproximado (32 font size = ~16px por letra)

print(f"\n📊 NOME: '{nome_text}'")
print(f"  Comprimento estimado: ~{nome_px_length}px")
print(f"  Área disponível: {info_available_width}px")
print(f"  X posição do CENTER: {nome_x}px")
print(f"  X esquerdo estimado: {nome_x - nome_px_length//2}px")
print(f"  X direito estimado: {nome_x + nome_px_length//2}px")
print(f"  Status: {'✅ CENTRALIZADO' if (nome_x - nome_px_length//2 > info_x_start and nome_x + nome_px_length//2 < printable_area_end) else '⚠️  POSSÍVEL PROBLEMA'}")

print("\n" + "=" * 90)
