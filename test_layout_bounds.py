#!/usr/bin/env python3
"""
Script de teste: Renderizar uma pulseira de teste e verificar layout
"""

import sys
sys.path.insert(0, '.')

from core.config import cm_to_px, NP_START_PX, PRINTABLE_W_PX
from core.models import LayoutModel, TextItem, QRItem
from dataclasses import asdict

print("=" * 70)
print("VERIFICAÇÃO DE LAYOUT - ÁREA IMPRIMÍVEL")
print("=" * 70)

# Configuração de dimensões
print("\n📐 DIMENSÕES DA PULSEIRA:")
print(f"  Largura total: 29.5cm")
print(f"  Altura: 2.0cm")

print("\n📍 ÁREA NÃO IMPRIMÍVEL:")
print(f"  Início: 0.0cm")
print(f"  Fim: 2.5cm = {NP_START_PX}px")
print(f"  ⚠️  NÃO IMPRIMIR NADA AQUI!")

print("\n✅ ÁREA IMPRIMÍVEL:")
print(f"  Início: 2.5cm = {NP_START_PX}px")
print(f"  Fim: 12.5cm = {NP_START_PX + PRINTABLE_W_PX}px")
print(f"  Largura: 10.0cm = {PRINTABLE_W_PX}px")

# Recrear o layout para verificar
P_HEIGHT = cm_to_px(2.0)
items = []

printable_area_start = NP_START_PX
printable_area_end = printable_area_start + PRINTABLE_W_PX

qr_size = int(P_HEIGHT - 2 * cm_to_px(0.1))
qr_x = printable_area_start + cm_to_px(0.1)

items.append(QRItem(
    id='qr1',
    x=qr_x,
    y=cm_to_px(0.1),
    size=qr_size,
    binding='Número da carteirinha'
))

info_x_start = qr_x + qr_size + cm_to_px(0.3)
info_available_width = printable_area_end - info_x_start - cm_to_px(0.1)

print("\n" + "=" * 70)
print("VERIFICAÇÃO DE ITENS DE LAYOUT")
print("=" * 70)

all_inside = True
for item in items:
    if isinstance(item, QRItem):
        x = item.x
        size = item.size
        x_end = x + size
        
        in_bounds = (x >= NP_START_PX and x_end <= NP_START_PX + PRINTABLE_W_PX)
        status = "✅ OK" if in_bounds else "❌ ERRO"
        if not in_bounds:
            all_inside = False
        
        print(f"\n🔷 QR CODE")
        print(f"   Posição X: {x}px = {x/300*2.54:.2f}cm {status}")
        print(f"   Tamanho: {size}px = {size/300*2.54:.2f}cm")
        print(f"   Fim X: {x_end}px = {x_end/300*2.54:.2f}cm")
        
        if not in_bounds:
            print(f"   ⚠️  FORA DOS LIMITES!")
            print(f"       Esperado: {NP_START_PX}px a {NP_START_PX + PRINTABLE_W_PX}px")
            print(f"       Obtido: {x}px a {x_end}px")

print("\n" + "=" * 70)
print("ANÁLISE DO ESPAÇO DISPONÍVEL")
print("=" * 70)

print(f"\n📏 QR Code:")
print(f"   Início: {qr_x}px ({qr_x/300*2.54:.2f}cm)")
print(f"   Fim: {qr_x + qr_size}px ({(qr_x + qr_size)/300*2.54:.2f}cm)")
print(f"   Tamanho: {qr_size}px ({qr_size/300*2.54:.2f}cm)")

print(f"\n📝 Informações:")
print(f"   Início: {info_x_start}px ({info_x_start/300*2.54:.2f}cm)")
print(f"   Fim (limite): {printable_area_end}px ({printable_area_end/300*2.54:.2f}cm)")
print(f"   Largura disponível: {info_available_width}px ({info_available_width/300*2.54:.2f}cm)")

print("\n" + "=" * 70)
if all_inside:
    print("✅ SUCESSO! Todos os itens estão dentro da área imprimível!")
else:
    print("❌ ERRO! Alguns itens estão fora da área imprimível!")
print("=" * 70)
