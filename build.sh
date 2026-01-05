#!/bin/bash

# Script para instalar dependências e gerar o executável Windows

echo "=================================================="
echo "🔧 Instalando PyInstaller..."
echo "=================================================="
pip install pyinstaller

echo ""
echo "=================================================="
echo "🔨 Gerando executável Windows..."
echo "=================================================="
python build_exe.py

echo ""
echo "=================================================="
echo "✅ Processo concluído!"
echo "=================================================="
echo ""
echo "📁 Seu executável está em: dist/GeradorPulseiras.exe"
echo ""
echo "💡 Para testar no Windows:"
echo "   1. Copie o arquivo 'dist/GeradorPulseiras.exe' para o Windows"
echo "   2. Execute-o (não precisa instalar nada!)"
echo ""
