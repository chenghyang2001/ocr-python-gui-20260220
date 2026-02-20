# Tasks: OCR 圖片文字辨識桌面應用程式（檔案／剪貼簿來源）

**Input**: Design documents from `/specs/002-ocr-file-clipboard/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/

**Tests**: 憲法要求「測試先行」——OCR 核心邏輯 MUST 有單元測試，GUI SHOULD 有整合測試。每個 story 的測試任務排在實作之前。

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: 專案初始化、建立基本結構與開發環境

- [x] T001 Create project directory structure: `src/ocr_engine/`, `src/file_io/`, `src/gui/`, `tests/unit/`, `tests/integration/` with `__init__.py` files
- [x] T002 Create `requirements.txt` with dependencies: PySide6, rapidocr-onnxruntime, Pillow, pytest, ruff
- [x] T003 [P] Create `pyproject.toml` with project metadata, ruff configuration (line-length=100, target Python 3.11), and pytest settings
- [x] T004 [P] Create application entry point in `src/main.py` with minimal PySide6 QApplication bootstrap

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: 所有 User Story 共用的核心元件——資料模型與 OCR 引擎

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Tests for Foundational

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T005 [P] Write unit tests for data models (ImageSource, RecognitionSettings, RecognitionResult) in `tests/unit/test_models.py` — test construction, validation rules, edge cases (empty languages, invalid confidence)
- [x] T006 [P] Write unit tests for OcrEngine in `tests/unit/test_ocr_engine.py` — test recognize() with a sample image, get_supported_languages(), invalid language handling, empty image handling

### Implementation for Foundational

- [x] T007 Create shared data models (ImageSource, RecognitionSettings, RecognitionResult) in `src/models.py` per data-model.md — include SourceType enum (FILE, CLIPBOARD), validation logic
- [x] T008 Implement OcrEngine class in `src/ocr_engine/engine.py` per contracts/module-interfaces.md — wrap rapidocr-onnxruntime, implement recognize() and get_supported_languages(), map language codes to RapidOCR parameters
- [x] T009 Verify T005 and T006 tests pass (Green) after T007 and T008 implementation

**Checkpoint**: Data models and OCR engine are functional and tested. User story implementation can now begin.

---

## Phase 3: User Story 1 — 從檔案載入圖片進行 OCR 辨識 (Priority: P1) 🎯 MVP

**Goal**: 使用者透過檔案選擇器載入一張圖片，辨識後可複製結果到剪貼簿

**Independent Test**: 開啟應用 → 載入圖片 → 辨識 → 複製到剪貼簿 → 在記事本貼上驗證

### Tests for User Story 1

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T010 [P] [US1] Write unit tests for load_image_from_file() in `tests/unit/test_file_io.py` — test valid PNG/JPG/BMP/TIFF loading, invalid format rejection, missing file handling
- [x] T011 [P] [US1] Write unit tests for copy_text_to_clipboard() in `tests/unit/test_file_io.py` — test text copying to clipboard

### Implementation for User Story 1

- [x] T012 [US1] Implement load_image_from_file() in `src/file_io/image_loader.py` per contracts — validate file extension, load via Pillow, return ImageSource(source_type=FILE)
- [x] T013 [US1] Implement copy_text_to_clipboard() in `src/file_io/text_exporter.py` per contracts — use QClipboard.setText()
- [x] T014 [US1] Build MainWindow GUI layout in `src/gui/main_window.py` — image preview area (QLabel), language selector (QCheckBox group for 繁中/簡中/英文), action buttons (載入圖片/辨識/複製到剪貼簿), result text area (QTextEdit, read-only but selectable)
- [x] T015 [US1] Wire "載入圖片" button in `src/gui/main_window.py` — open QFileDialog with filter for PNG/JPG/BMP/TIFF, call load_image_from_file(), display image preview with QPixmap.scaled(KeepAspectRatio)
- [x] T016 [US1] Wire "辨識" button with background thread in `src/gui/main_window.py` — create QThread worker calling OcrEngine.recognize(), emit signal on completion, disable button during processing, show progress indicator (QProgressBar or busy cursor)
- [x] T017 [US1] Wire "複製到剪貼簿" button and display result in `src/gui/main_window.py` — populate QTextEdit with result text, enable copy button, call copy_text_to_clipboard() on click, show success tooltip. Handle "未偵測到文字" case.
- [x] T018 [US1] Add error handling for US1 in `src/gui/main_window.py` — show QMessageBox for unsupported format, file not found, OCR failure. Disable "辨識" button when no image loaded.
- [x] T019 [US1] Verify T010 and T011 tests pass (Green) after implementation

**Checkpoint**: 使用者可從檔案載入圖片、辨識文字、複製到剪貼簿。MVP 功能完成。

---

## Phase 4: User Story 2 — 從系統剪貼簿擷取圖片進行 OCR 辨識 (Priority: P1)

**Goal**: 使用者截圖後，透過「從剪貼簿貼上」按鈕或 Ctrl+V 直接辨識

**Independent Test**: Win+Shift+S 截圖 → 切換到應用 → Ctrl+V → 圖片出現在預覽區 → 辨識 → 確認結果

### Tests for User Story 2

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T020 [P] [US2] Write unit tests for load_image_from_clipboard() in `tests/unit/test_file_io.py` — test successful clipboard image read, test clipboard-no-image error case

### Implementation for User Story 2

- [x] T021 [US2] Implement load_image_from_clipboard() in `src/file_io/image_loader.py` per contracts — use QApplication.clipboard().image() to get QImage, convert to PIL Image, return ImageSource(source_type=CLIPBOARD). Raise ValueError if clipboard has no image.
- [x] T022 [US2] Add "從剪貼簿貼上" button to MainWindow in `src/gui/main_window.py` — call load_image_from_clipboard(), display image preview. Show "剪貼簿中沒有圖片" message if no image found.
- [x] T023 [US2] Add Ctrl+V keyboard shortcut in `src/gui/main_window.py` — bind QShortcut(QKeySequence.Paste) to same handler as "從剪貼簿貼上" button
- [x] T024 [US2] Verify T020 tests pass (Green) after implementation

**Checkpoint**: 使用者可從檔案或剪貼簿兩種方式載入圖片並辨識。兩個 P1 story 皆完成。

---

## Phase 5: User Story 3 — 匯出辨識結果為文字檔 (Priority: P2)

**Goal**: 使用者可將辨識結果匯出為 .txt 檔案

**Independent Test**: 辨識完成 → 點擊「匯出」→ 選擇儲存位置 → 確認 .txt 檔案內容正確

### Tests for User Story 3

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T025 [P] [US3] Write unit tests for export_text_to_file() in `tests/unit/test_file_io.py` — test UTF-8 encoding output, test permission error handling, verify file content matches input text

### Implementation for User Story 3

- [x] T026 [US3] Implement export_text_to_file() in `src/file_io/text_exporter.py` per contracts — write text with UTF-8 encoding, handle PermissionError
- [x] T027 [US3] Add "匯出" button to MainWindow in `src/gui/main_window.py` — open QFileDialog.getSaveFileName with .txt filter, default filename based on source (original filename for FILE source, "ocr-result-YYYYMMDD-HHMMSS.txt" for CLIPBOARD source), call export_text_to_file()
- [x] T028 [US3] Add error handling for export in `src/gui/main_window.py` — show QMessageBox on permission error, allow re-selecting path. Disable "匯出" button when no result available.
- [x] T029 [US3] Verify T025 tests pass (Green) after implementation

**Checkpoint**: 所有 3 個 User Story 皆完成，應用功能完整。

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: 改善整體品質、跨 story 的整合與優化

- [ ] T030 [P] Write integration test for full file→OCR→copy workflow in `tests/integration/test_gui_workflow.py`
- [ ] T031 [P] Write integration test for full clipboard→OCR→export workflow in `tests/integration/test_gui_workflow.py`
- [x] T032 Run ruff check and format on `src/` and `tests/`, fix any violations
- [x] T033 Run quickstart.md validation — verify all steps from quickstart.md work end-to-end
- [x] T034 Update `README.md` with project description, installation instructions, and usage guide

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion — BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational (Phase 2)
- **User Story 2 (Phase 4)**: Depends on Foundational (Phase 2). Can run in parallel with US1, but practically benefits from US1's GUI layout (T014-T017)
- **User Story 3 (Phase 5)**: Depends on Foundational (Phase 2). Requires US1 or US2 to have result to export, but implementation is independent
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Independent — builds GUI foundation
- **User Story 2 (P1)**: Adds to US1's GUI — extend MainWindow with clipboard button and Ctrl+V shortcut
- **User Story 3 (P2)**: Adds to US1/US2's GUI — extend MainWindow with export button

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Data models / I/O functions before GUI wiring
- Core implementation before error handling
- Story complete before moving to next priority

### Parallel Opportunities

- T003 and T004 can run in parallel (Setup phase)
- T005 and T006 can run in parallel (Foundational tests)
- T010 and T011 can run in parallel (US1 tests)
- T012 and T013 can run in parallel (US1 I/O functions)

---

## Parallel Example: Phase 2 (Foundational)

```bash
# Launch tests in parallel:
Task: "Write unit tests for data models in tests/unit/test_models.py"
Task: "Write unit tests for OcrEngine in tests/unit/test_ocr_engine.py"

# Then implement sequentially:
Task: "Create shared data models in src/models.py"
Task: "Implement OcrEngine in src/ocr_engine/engine.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (data models + OCR engine)
3. Complete Phase 3: User Story 1 (file load → OCR → copy)
4. **STOP and VALIDATE**: 開啟應用 → 載入圖片 → 辨識 → 複製到剪貼簿
5. Demo-ready MVP

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. Add User Story 1 → 檔案載入辨識 (MVP!)
3. Add User Story 2 → 剪貼簿擷取辨識 (P1 完成)
4. Add User Story 3 → 匯出文字檔 (全功能)
5. Polish → 品質與文件完善

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing (Red-Green-Refactor per constitution)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
