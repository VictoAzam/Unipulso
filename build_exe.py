"""
Script para gerar executável Windows do Gerador de Pulseiras
Uso: python build_exe.py
"""
import PyInstaller.__main__
import os
import shutil

# Remove pastas antigas de build se existirem
if os.path.exists('build'):
    shutil.rmtree('build')
if os.path.exists('dist'):
    shutil.rmtree('dist')

# Configuração do PyInstaller
PyInstaller.__main__.run([
    'app.py',
    '--name=GeradorPulseiras',
    '--windowed',  # Sem console (GUI apenas)
    '--onefile',  # Um único arquivo executável
    '--icon=icon.ico' if os.path.exists('icon.ico') else '--noconfirm',
    '--add-data=requeriments.txt:.',
    '--hidden-import=PIL._tkinter_finder',
    '--hidden-import=ttkbootstrap',
    '--hidden-import=qrcode',
    '--hidden-import=reportlab',
    '--collect-all=ttkbootstrap',
    '--noconfirm',
])

print("\n" + "="*60)
print("✅ Executável gerado com sucesso!")
print("📁 Localização: dist/GeradorPulseiras.exe")
print("="*60)
