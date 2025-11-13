#!/usr/bin/env python3
"""
Script de verificação de layout - Garante que tudo fica na área imprimível
"""

import sys
sys.path.insert(0, '.')

from core.config import cm_to_px, NP_START_PX, PRINTABLE_W_PX, P_HEIGHT
from app import PulseiraApp

print("=" * 70)
print("VERIFICAÇÃO DE LAYOUT - ÁREA IMPRIMÍVEL")
print("=" * 70)

# Configuração de dimensões
print("\n📐 DIMENSÕES DA PULSEIRA:")
print(f"  Largura total: 29.5cm = {29.5 * 300 // 2.54:.0f}px")
print(f"  Altura: 2.0cm = {2.0 * 300 // 2.54:.0f}px")

print("\n📍 ÁREA NÃO IMPRIMÍVEL:")
print(f"  Início: 0.0cm")
print(f"  Fim: 2.5cm = {NP_START_PX}px")
print(f"  ⚠️  NÃO IMPRIMIR NADA AQUI!")

print("\n✅ ÁREA IMPRIMÍVEL:")
print(f"  Início: 2.5cm = {NP_START_PX}px")
print(f"  Fim: 12.5cm = {NP_START_PX + PRINTABLE_W_PX}px")
print(f"  Largura: 10.0cm = {PRINTABLE_W_PX}px")
print(f"  ✨ TODO CONTEÚDO DEVE ESTAR AQUI!")

# Criar instância fake para pegar o layout
class FakeTk:
    def mainloop(self): pass
    def destroy(self): pass
    def title(self, text): pass
    def geometry(self, size): pass
    def resizable(self, x, y): pass
    def pack(self, **kwargs): pass
    def bind(self, event, func): pass
    def update(self): pass

app = PulseiraApp(FakeTk())
layout = app._default_layout()

print("\n" + "=" * 70)
print("VERIFICAÇÃO DE ITENS DE LAYOUT")
print("=" * 70)

qr_item = None
all_inside = True

for item in layout.items:
    item_type = type(item).__name__ if hasattr(item, '__class__') else 'dict'
    
    if isinstance(item, dict):
        item_id = item.get('id', 'unknown')
        item_type = 'QRItem' if item.get('size') else 'TextItem'
    else:
        item_id = getattr(item, 'id', 'unknown')
    
    if item_type == 'QRItem' or (isinstance(item, dict) and item.get('size')):
        qr_item = item if isinstance(item, dict) else vars(item)
        x = qr_item.get('x')
        size = qr_item.get('size')
        x_end = x + size if size else x
        
        status = "✅ OK" if (x >= NP_START_PX and x_end <= NP_START_PX + PRINTABLE_W_PX) else "❌ ERRO"
        if "❌" in status:
            all_inside = False
        
        print(f"\n🔷 QR CODE (id={item_id})")
        print(f"   Posição X: {x}px ({x/300*2.54:.2f}cm) {status}")
        print(f"   Tamanho: {size}px ({size/300*2.54:.2f}cm)")
        print(f"   Fim X: {x_end}px ({x_end/300*2.54:.2f}cm)")
    
    elif item_type == 'TextItem' or (isinstance(item, dict) and 'text' in item):
        text_item = item if isinstance(item, dict) else vars(item)
        x = text_item.get('x')
        width = text_item.get('width', 0)
        x_end = x + width if width else x
        text = text_item.get('text', '')[:30]
        
        status = "✅ OK" if (x >= NP_START_PX and x_end <= NP_START_PX + PRINTABLE_W_PX) else "❌ ERRO"
        if "❌" in status:
            all_inside = False
        
        print(f"\n📝 {item_id}")
        print(f"   Texto: {text}")
        print(f"   Posição X: {x}px ({x/300*2.54:.2f}cm) {status}")
        print(f"   Fim X: {x_end}px ({x_end/300*2.54:.2f}cm)")

print("\n" + "=" * 70)
if all_inside:
    print("✅ SUCESSO! Todos os itens estão dentro da área imprimível!")
else:
    print("❌ ERRO! Alguns itens estão fora da área imprimível!")
print("=" * 70)
