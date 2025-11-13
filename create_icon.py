#!/usr/bin/env python3
"""
Script para criar ícone .ico a partir de imagem PNG
Útil para gerar icon.ico para o instalador
"""

import os
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("❌ Pillow não está instalado!")
    print("Execute: pip install Pillow")
    sys.exit(1)

def create_icon_from_image(input_path, output_path='logo/icon.ico'):
    """
    Cria um arquivo .ico multi-resolução a partir de uma imagem
    
    Args:
        input_path: Caminho para imagem de entrada (PNG, JPG, etc)
        output_path: Caminho para arquivo .ico de saída
    """
    try:
        # Criar diretório de saída se não existir
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Abrir imagem original
        print(f"📂 Abrindo imagem: {input_path}")
        img = Image.open(input_path)
        
        # Converter para RGB se necessário (remove transparência se tiver)
        if img.mode == 'RGBA':
            # Criar fundo branco
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3])  # Alpha channel como máscara
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Tamanhos padrão de ícone Windows
        icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
        
        # Salvar como .ico com múltiplas resoluções
        print(f"💾 Salvando ícone: {output_path}")
        img.save(output_path, format='ICO', sizes=icon_sizes)
        
        # Verificar tamanho do arquivo
        size_kb = os.path.getsize(output_path) / 1024
        
        print(f"✅ Ícone criado com sucesso!")
        print(f"   Resoluções: {', '.join([f'{w}x{h}' for w, h in icon_sizes])}")
        print(f"   Tamanho: {size_kb:.1f} KB")
        print(f"   Local: {output_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar ícone: {e}")
        return False

def find_logo_images():
    """Procura por imagens de logo no projeto"""
    logo_dir = Path('logo')
    
    if not logo_dir.exists():
        return []
    
    # Extensões de imagem suportadas
    extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.gif']
    
    images = []
    for ext in extensions:
        images.extend(logo_dir.glob(f'*{ext}'))
    
    return images

def main():
    """Função principal"""
    print("\n" + "="*60)
    print("    UNIPULSO - Criador de Ícone")
    print("="*60 + "\n")
    
    # Verificar se já existe icon.ico
    icon_path = Path('logo/icon.ico')
    if icon_path.exists():
        response = input("⚠️  icon.ico já existe. Sobrescrever? (s/n): ")
        if response.lower() != 's':
            print("Operação cancelada.")
            return
    
    # Procurar imagens disponíveis
    images = find_logo_images()
    
    if not images:
        print("❌ Nenhuma imagem encontrada na pasta logo/")
        print("\nColoque uma imagem PNG na pasta 'logo/' e tente novamente.")
        print("Sugestão: logo/logo.png (256x256 ou maior)")
        return
    
    # Listar imagens disponíveis
    print("Imagens disponíveis:\n")
    for i, img in enumerate(images, 1):
        size_kb = img.stat().st_size / 1024
        print(f"  {i}. {img.name} ({size_kb:.1f} KB)")
    
    # Selecionar imagem
    if len(images) == 1:
        selected = images[0]
        print(f"\n📌 Usando única imagem encontrada: {selected.name}")
    else:
        try:
            choice = int(input(f"\nEscolha uma imagem (1-{len(images)}): "))
            if 1 <= choice <= len(images):
                selected = images[choice - 1]
            else:
                print("❌ Escolha inválida.")
                return
        except ValueError:
            print("❌ Entrada inválida.")
            return
    
    # Criar ícone
    print()
    if create_icon_from_image(str(selected)):
        print("\n🎉 Pronto! Agora você pode usar o ícone no instalador.")
        print("   O arquivo unipulso.spec já está configurado para usá-lo.")
    else:
        print("\n❌ Falha ao criar ícone.")
        sys.exit(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Operação cancelada pelo usuário.")
        sys.exit(0)
