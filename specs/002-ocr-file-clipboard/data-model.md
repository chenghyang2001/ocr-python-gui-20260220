# Data Model: OCR 圖片文字辨識桌面應用程式

**Date**: 2026-02-20
**Feature**: 002-ocr-file-clipboard

## Entities

### ImageSource（圖片來源）

代表使用者提供的一張待辨識圖片。

| 屬性 | 型別 | 說明 |
|------|------|------|
| source_type | enum: FILE, CLIPBOARD | 圖片來源方式 |
| image_data | Image (PIL) | 圖片資料（統一為 PIL Image 格式） |
| file_path | str or None | 原始檔案路徑（僅 FILE 來源時有值） |
| file_name | str or None | 原始檔名（僅 FILE 來源時有值） |

**驗證規則**:
- FILE 來源時，file_path MUST 為存在且可讀的檔案
- FILE 來源時，副檔名 MUST 為 .png、.jpg、.jpeg、.bmp、.tiff 之一
- image_data MUST NOT 為空

**狀態轉換**: 無（靜態資料物件）

### RecognitionSettings（辨識設定）

使用者為本次辨識選擇的參數。

| 屬性 | 型別 | 說明 |
|------|------|------|
| languages | list[str] | 選擇的辨識語言列表 |

**驗證規則**:
- languages MUST 至少包含一個語言
- 語言值 MUST 為 "ch_tra"（繁體中文）、"ch_sim"（簡體中文）、"en"（英文）之一

### RecognitionResult（辨識結果）

一次辨識作業產生的結果。

| 屬性 | 型別 | 說明 |
|------|------|------|
| text | str | 辨識出的完整文字（各行以換行分隔） |
| confidence | float or None | 平均辨識信心度（0.0-1.0，如引擎提供） |
| elapsed_time | float | 辨識耗時（秒） |

**驗證規則**:
- text 可為空字串（代表未偵測到文字）
- confidence 若有值，MUST 在 0.0-1.0 範圍內

## Entity Relationships

```text
ImageSource ──→ RecognitionSettings ──→ RecognitionResult
   (1)              (1)                    (1)
```

每次辨識操作由一個 ImageSource + 一個 RecognitionSettings 產生一個 RecognitionResult。
應用程式僅維護當前作業狀態，不需要持久化歷史記錄。
