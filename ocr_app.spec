# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec — OCR 圖片文字辨識桌面應用程式"""

import os
import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# 收集 RapidOCR 的 ONNX 模型與設定檔
rapidocr_datas = collect_data_files("rapidocr_onnxruntime")

# 收集 onnxruntime 動態庫
onnxruntime_datas = collect_data_files("onnxruntime")

a = Analysis(
    ["src/main.py"],
    pathex=["."],
    binaries=[],
    datas=rapidocr_datas + onnxruntime_datas,
    hiddenimports=[
        "rapidocr_onnxruntime",
        "onnxruntime",
        "PIL",
        "PySide6.QtCore",
        "PySide6.QtGui",
        "PySide6.QtWidgets",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["pytest", "ruff", "tkinter"],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="OCR-App",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # GUI 應用程式，不顯示 console 視窗
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
