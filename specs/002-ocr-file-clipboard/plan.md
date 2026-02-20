# Implementation Plan: OCR 圖片文字辨識桌面應用程式（檔案／剪貼簿來源）

**Branch**: `002-ocr-file-clipboard` | **Date**: 2026-02-20 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-ocr-file-clipboard/spec.md`

## Summary

建構一個 Python 桌面 GUI 應用程式，支援從檔案路徑或系統剪貼簿載入圖片，透過離線 OCR 引擎辨識繁體中文、簡體中文、英文文字。使用者可複製辨識結果到剪貼簿或匯出為 .txt 檔案。使用 PySide6 作為 GUI 框架、RapidOCR 作為 OCR 引擎。

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: PySide6 (GUI)、rapidocr-onnxruntime (OCR)、Pillow (圖片處理)
**Storage**: N/A（無持久化需求，僅檔案匯出）
**Testing**: pytest
**Target Platform**: Windows 桌面應用（優先）
**Project Type**: Single project
**Performance Goals**: 單張 A4 300DPI 圖片辨識 < 10 秒
**Constraints**: 離線運作、記憶體 < 1GB、介面不凍結
**Scale/Scope**: 單一桌面應用、每次處理一張圖片

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### I. 模組化架構 ✅

| 規則 | 遵守方式 |
|------|---------|
| OCR 引擎、GUI、檔案 I/O 分離 | 三個獨立模組：`src/ocr_engine/`、`src/gui/`、`src/file_io/` |
| 模組間透過明確介面溝通 | 見 contracts/module-interfaces.md |
| OCR 可在無 GUI 下獨立測試 | `ocr_engine` 不依賴 `gui` 或 PySide6 |
| 新功能先確認歸屬模組 | 三個模組職責明確：辨識、介面、I/O |

### II. 測試先行 ✅

| 規則 | 遵守方式 |
|------|---------|
| OCR 核心邏輯有單元測試 | `tests/unit/test_ocr_engine.py` |
| Red-Green-Refactor 流程 | tasks 將按照先測試後實作排序 |
| GUI 整合測試 | `tests/integration/test_gui_workflow.py` |

### III. 簡單易用 ✅

| 規則 | 遵守方式 |
|------|---------|
| 常見任務 ≤ 3 次點擊 | 檔案：載入→辨識→複製（3 次）；剪貼簿：貼上→辨識（2 次） |
| YAGNI | 不實作批次處理、不預留擴充介面 |
| 抽象層有具體理由 | 模組分離有憲法明確要求 |

**Gate Result**: PASS — 無違規項目

## Project Structure

### Documentation (this feature)

```text
specs/002-ocr-file-clipboard/
├── plan.md              # 本檔案
├── spec.md              # 功能規格
├── research.md          # Phase 0 研究成果
├── data-model.md        # 資料模型
├── quickstart.md        # 快速開始指南
├── contracts/           # 模組介面契約
│   └── module-interfaces.md
└── tasks.md             # 由 /speckit.tasks 產生
```

### Source Code (repository root)

```text
src/
├── main.py              # 應用程式入口
├── ocr_engine/          # OCR 引擎模組
│   ├── __init__.py
│   └── engine.py        # OcrEngine 類別
├── file_io/             # 檔案 I/O 模組
│   ├── __init__.py
│   ├── image_loader.py  # load_image_from_file, load_image_from_clipboard
│   └── text_exporter.py # export_text_to_file, copy_text_to_clipboard
└── gui/                 # GUI 介面模組
    ├── __init__.py
    └── main_window.py   # MainWindow 主視窗

tests/
├── unit/
│   ├── test_ocr_engine.py    # OCR 引擎單元測試
│   └── test_file_io.py       # 檔案 I/O 單元測試
└── integration/
    └── test_gui_workflow.py   # GUI 工作流程整合測試
```

**Structure Decision**: 採用 Single project 結構。本專案為獨立桌面應用，
無 frontend/backend 分離需求。三個模組以 Python package 形式組織在 `src/` 下。

## Complexity Tracking

> 無違規項目，此區段不適用。
