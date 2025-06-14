# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules

hiddenimports = []
hiddenimports += collect_submodules('plyer')

a = Analysis(
    ['MiriMirim\\main.py'],
    pathex=[],
    binaries=[],
    datas=[('MiriMirim/source', 'source')],
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["pandas", "numpy", 'PyQt5.QtWebEngineWidgets', 'PyQt5.QtMultimedia', 'PyQt5.QtSql'],
    noarchive=False,
    optimize=0,
    upx_dir='C:\\upx',
    console=True, # 또는 False (GUI 앱의 경우)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Miri_Mirim',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
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
    name='Miri_Mirim',
)
