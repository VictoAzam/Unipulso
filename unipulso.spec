# -*- mode: python ; coding: utf-8 -*-
"""
Especificação PyInstaller para Unipulso
Cria executável com todas as dependências embutidas
"""

import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Coletar todos os submódulos necessários
hiddenimports = [
    'PIL._tkinter_finder',
    'ttkbootstrap',
    'ttkbootstrap.constants',
    'ttkbootstrap.themes',
    'reportlab.pdfbase',
    'reportlab.pdfbase.ttfonts',
    'reportlab.lib.pagesizes',
    'qrcode',
    'qrcode.image.pil',
    'win32print',
    'win32ui',
    'pywintypes',
]

# Coletar dados do ttkbootstrap (temas)
datas = collect_data_files('ttkbootstrap')

# Adicionar recursos do projeto
project_dir = os.path.abspath(SPECPATH)

# Pastas de recursos
datas += [
    (os.path.join(project_dir, 'logo'), 'logo'),
    (os.path.join(project_dir, 'fonte padrao'), 'fonte padrao'),
    (os.path.join(project_dir, 'templates'), 'templates'),
    (os.path.join(project_dir, 'data'), 'data'),
]

# Arquivos individuais importantes
if os.path.exists(os.path.join(project_dir, 'LICENSE')):
    datas += [(os.path.join(project_dir, 'LICENSE'), '.')]

a = Analysis(
    ['app.py'],
    pathex=[project_dir],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'pytest',
        'unittest',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Unipulso',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Aplicação GUI (sem console)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=os.path.join(project_dir, 'logo', 'icon.ico') if os.path.exists(os.path.join(project_dir, 'logo', 'icon.ico')) else None,
    version_file=None,
)
