# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['home_screen.py'],
    pathex=[],
    binaries=[('C:/Python312/tcl/tcl8.6', './tcl/tcl8.6'), ('C:/Python312/tcl/tk8.6', './tcl/tk8.6')],
    datas=[('Images', 'Images'), ('.env', '.'), ('linkedin_bot.py', '.'), ('get_job_titles.py', '.'), ('job_titles.py', '.')],
    hiddenimports=['PIL', 'dotenv', 'ttkbootstrap'],
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
    [],
    exclude_binaries=True,
    name='home_screen',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='home_screen',
)
