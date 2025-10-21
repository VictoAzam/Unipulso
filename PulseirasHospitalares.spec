# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[('.venv/Lib/site-packages/ttkbootstrap/themes', 'ttkbootstrap/themes')],
    hiddenimports=['ttkbootstrap', 'PIL', 'PIL._tkinter_finder', 'qrcode', 'reportlab', 'reportlab.pdfgen.canvas', 'reportlab.lib.pagesizes', 'reportlab.lib.utils'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='PulseirasHospitalares',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
