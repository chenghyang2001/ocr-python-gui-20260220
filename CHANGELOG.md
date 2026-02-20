# Changelog

本文件記錄專案的所有重要變更與開發歷程。

## [0.1.1] - 2026-02-20

### 打包與發布

- 建立 PyInstaller 設定檔 `ocr_app.spec`，自動收集 RapidOCR 的 ONNX 模型與 onnxruntime 動態庫
- 建立打包腳本 `build_exe.py`，產出單一 exe（約 128MB，含所有 OCR 模型，可獨立執行）
- 建立 GitHub Actions 工作流 `.github/workflows/release.yml`：
  - 推送 `v*` tag 時自動觸發
  - 在 `windows-latest` 環境建置 exe
  - 使用 `softprops/action-gh-release` 自動建立 Release 並附加 exe
- 建立一鍵發布腳本 `release.bat`：自動遞增 patch 版本、打包 exe、git commit/tag/push
- 更新 `.gitignore`：排除 `*.spec` 但保留 `ocr_app.spec`
- 更新 `README.md`：新增「打包與發布」章節（一鍵發布、手動打包、手動發布說明）
- 建立 `CHANGELOG.md` 記錄完整專案變更歷程
- 合併 `002-ocr-file-clipboard` 分支至 `main`
- 首次自動發布 Release v0.1.1，GitHub Actions 建置成功（build 2m49s + release 10s）

## [0.1.0] - 2026-02-20

### 階段一：專案初始化

- 從 Specify 模板建立專案骨架
- 建立 `README.md` 專案說明
- 建立 `.gitignore`（Python 專案規則）

### 階段二：專案治理

- 制定專案憲法 v1.0.0（`.specify/memory/constitution.md`），確立三大核心原則：
  1. **模組化架構**：各模組獨立開發、獨立測試
  2. **測試先行**：TDD 流程，先寫測試再實作
  3. **簡單易用**：直覺的使用者介面
- 定義技術約束（Python 3.11+、pytest、ruff、Windows 為主要平台）
- 新增貢獻者角色與職責、行為準則、衝突解決程序

### 階段三：功能規劃與設計

- 撰寫功能規格書 `specs/002-ocr-file-clipboard/spec.md`：
  - US1：從檔案載入圖片進行 OCR 辨識（P1）
  - US2：從系統剪貼簿擷取圖片進行 OCR 辨識（P1）
  - US3：匯出辨識結果為文字檔（P2）
- 完成技術研究 `research.md`：
  - OCR 引擎：選定 RapidOCR (ONNX)，相比 PaddleOCR 大幅減少依賴（~70MB vs 1.5GB+）
  - GUI 框架：選定 PySide6，原生剪貼簿支援、QThread 非阻塞 UI、LGPL 授權
  - 圖片處理：Pillow
- 建立資料模型 `data-model.md`：ImageSource、RecognitionSettings、RecognitionResult
- 定義模組介面合約 `contracts/module-interfaces.md`
- 建立實作計畫 `plan.md` 與任務清單 `tasks.md`（34 項任務、6 個階段）
- 建立需求品質檢查清單 `checklists/requirements.md`
- 建立快速上手指南 `quickstart.md`

### 階段四：核心功能實作（遵循 TDD）

**資料模型** (`src/models.py`)：
- `SourceType` 列舉（FILE、CLIPBOARD）
- `ImageSource`：圖片來源資料，含驗證邏輯
- `RecognitionSettings`：辨識設定，支援語言代碼驗證
- `RecognitionResult`：辨識結果（文字、信心度、耗時）

**OCR 引擎** (`src/ocr_engine/engine.py`)：
- 封裝 RapidOCR，提供 `recognize()` 與 `get_supported_languages()` 方法
- 支援繁體中文（ch_tra）、簡體中文（ch_sim）、英文（en）
- 自動計算平均信心度與辨識耗時

**檔案 I/O** (`src/file_io/`)：
- `image_loader.py`：從檔案載入圖片（PNG/JPG/BMP/TIFF），從剪貼簿擷取圖片（QImage → PIL Image，處理 stride/padding）
- `text_exporter.py`：複製文字到剪貼簿（QClipboard）、匯出為 UTF-8 文字檔

**主視窗 GUI** (`src/gui/main_window.py`)：
- 左側面板：圖片預覽區、「載入圖片」與「從剪貼簿貼上」按鈕
- 右側面板：語言選擇（繁中/簡中/英文 QCheckBox）、「辨識」按鈕、狀態標籤、結果顯示區（QTextEdit）、「複製到剪貼簿」與「匯出」按鈕
- `OcrWorker` + `QThread`：背景執行 OCR，避免 UI 凍結
- Ctrl+V 快捷鍵綁定剪貼簿貼上
- 匯出預設檔名：檔案來源用原始檔名、剪貼簿來源用 `ocr-result-YYYYMMDD-HHMMSS.txt`
- 完整錯誤處理：格式不支援、檔案不存在、辨識失敗、匯出權限錯誤

**應用程式入口** (`src/main.py`)：
- PySide6 QApplication 啟動、MainWindow 初始化

### 階段五：測試

- 28 項單元測試全數通過，遵循 TDD 流程（Red → Green）：
  - `tests/unit/test_models.py`（14 項）：資料模型建構、驗證規則、邊界情況
  - `tests/unit/test_ocr_engine.py`（8 項）：引擎初始化、語言清單、辨識功能、空白圖片、無效語言
  - `tests/unit/test_file_io.py`（6 項）：各格式檔案載入、不支援格式拒絕、缺少檔案處理
- 通過 ruff lint 檢查（src/ 與 tests/）

### 專案架構

```
ocr-python-gui-20260220/
├── src/
│   ├── main.py              # 應用程式入口
│   ├── models.py            # 共用資料模型
│   ├── ocr_engine/
│   │   └── engine.py        # OCR 引擎（RapidOCR 封裝）
│   ├── file_io/
│   │   ├── image_loader.py  # 圖片載入（檔案/剪貼簿）
│   │   └── text_exporter.py # 文字匯出（剪貼簿/檔案）
│   └── gui/
│       └── main_window.py   # PySide6 主視窗
├── tests/unit/              # 單元測試（28 項）
├── specs/002-ocr-file-clipboard/  # 功能規格與設計文件
├── .github/workflows/release.yml  # GitHub Actions 自動發布
├── ocr_app.spec             # PyInstaller 打包設定
├── build_exe.py             # 本機打包腳本
├── release.bat              # 一鍵發布腳本
├── requirements.txt         # Python 依賴
└── pyproject.toml           # 專案設定
```

### 技術棧

| 類別 | 技術 | 用途 |
|------|------|------|
| GUI | PySide6 | 桌面視窗、剪貼簿存取、背景執行緒 |
| OCR | RapidOCR (ONNX Runtime) | 離線文字辨識（繁中/簡中/英文） |
| 圖片處理 | Pillow | 圖片載入與格式轉換 |
| 打包 | PyInstaller | 產出單一 Windows exe |
| CI/CD | GitHub Actions | 自動建置與發布 Release |
| 測試 | pytest | 單元測試 |
| Lint | ruff | 程式碼品質檢查 |
