<!--
Sync Impact Report
===================
Version change: N/A → 1.0.0 (initial ratification)
Modified principles: N/A (first version)
Added sections:
  - Core Principles (3 principles)
  - Technology Constraints
  - Development Workflow
  - Governance
Removed sections:
  - [SECTION_2_NAME] and [SECTION_3_NAME] placeholders replaced
Templates requiring updates:
  - .specify/templates/plan-template.md ✅ no changes needed (generic)
  - .specify/templates/spec-template.md ✅ no changes needed (generic)
  - .specify/templates/tasks-template.md ✅ no changes needed (generic)
Follow-up TODOs: None
-->

# OCR Python GUI 專案憲法

## Core Principles

### I. 模組化架構

- OCR 引擎邏輯、GUI 介面、檔案 I/O 必須（MUST）分離為獨立模組
- 各模組之間透過明確定義的介面溝通，禁止直接跨層存取
- OCR 核心功能 MUST 可在無 GUI 環境下獨立執行與測試
- 新增功能時 MUST 先確認歸屬模組，不得建立無明確職責的模組

**理由**：OCR 應用的核心價值在辨識引擎，GUI 只是展示層。
分離後可獨立替換 OCR 引擎（如 Tesseract → PaddleOCR），
也方便日後擴展為 CLI 或 API 服務。

### II. 測試先行

- 所有 OCR 核心邏輯 MUST 有對應的單元測試
- 測試流程：撰寫測試 → 確認測試失敗（Red）→ 實作功能（Green）→ 重構（Refactor）
- GUI 互動邏輯 SHOULD 透過整合測試驗證關鍵使用者流程
- 未通過測試的程式碼禁止合併至主分支

**理由**：OCR 辨識結果的正確性直接影響使用者體驗，
測試先行確保每次修改都不會破壞既有的辨識能力。

### III. 簡單易用

- GUI 設計 MUST 遵循「最少操作步驟」原則——常見任務不超過 3 次點擊
- 不得為假設性需求預先建構功能（YAGNI）
- 新增抽象層 MUST 有具體的重複消除或解耦需求佐證
- 偏好直接、可讀的實作，而非過度工程化的設計模式

**理由**：OCR 工具的目標使用者可能不具技術背景，
介面與程式碼都應追求簡潔，降低使用與維護門檻。

## 技術約束

- **語言**：Python 3.11+
- **GUI 框架**：待定（依功能規格確認後決定）
- **OCR 引擎**：待定（依功能規格確認後決定）
- **測試框架**：pytest
- **目標平台**：Windows 桌面應用（優先），跨平台為次要目標
- **程式碼風格**：遵循 PEP 8，使用 ruff 進行 lint 與格式化

## 開發工作流

- 所有變更 MUST 透過功能分支（feature branch）進行
- 合併前 MUST 通過所有既有測試
- 提交訊息使用繁體中文，格式遵循 Conventional Commits
- 每個提交 SHOULD 聚焦單一邏輯變更

## Governance

- 本憲法為專案最高開發規範，所有 spec、plan、task 皆 MUST 遵守
- 修訂本憲法需記錄變更理由、影響範圍，並更新版本號
- 版本號遵循語義化版本：MAJOR（原則刪除或重新定義）、MINOR（新增原則或重大擴充）、PATCH（文字修正、澄清）
- 所有 PR 審查 MUST 驗證是否符合本憲法的原則

**Version**: 1.0.0 | **Ratified**: 2026-02-20 | **Last Amended**: 2026-02-20
