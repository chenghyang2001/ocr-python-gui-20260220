# Module Interfaces: OCR 圖片文字辨識桌面應用程式

**Date**: 2026-02-20
**Feature**: 002-ocr-file-clipboard

本專案依據憲法「模組化架構」原則，分為三個獨立模組。
以下定義各模組的公開介面（契約）。

## 模組一：OCR 引擎（ocr_engine）

OCR 核心邏輯，MUST 可在無 GUI 環境下獨立執行與測試。

```python
class OcrEngine:
    """OCR 辨識引擎封裝"""

    def __init__(self) -> None:
        """初始化 OCR 引擎（載入模型）"""
        ...

    def recognize(
        self,
        image: PIL.Image.Image,
        languages: list[str],
    ) -> RecognitionResult:
        """
        對圖片進行 OCR 辨識。

        Args:
            image: PIL Image 格式的圖片
            languages: 辨識語言列表
                       ("ch_tra", "ch_sim", "en")

        Returns:
            RecognitionResult 包含辨識文字、信心度、耗時

        Raises:
            ValueError: languages 為空或包含不支援的語言
        """
        ...

    def get_supported_languages(self) -> list[dict[str, str]]:
        """
        回傳支援的語言清單。

        Returns:
            [{"code": "ch_tra", "name": "繁體中文"}, ...]
        """
        ...
```

## 模組二：檔案 I/O（file_io）

圖片載入、剪貼簿讀取、結果匯出。

```python
def load_image_from_file(file_path: str) -> ImageSource:
    """
    從檔案路徑載入圖片。

    Args:
        file_path: 圖片檔案的絕對路徑

    Returns:
        ImageSource (source_type=FILE)

    Raises:
        FileNotFoundError: 檔案不存在
        ValueError: 不支援的檔案格式
    """
    ...

def load_image_from_clipboard() -> ImageSource:
    """
    從系統剪貼簿讀取圖片。

    Returns:
        ImageSource (source_type=CLIPBOARD)

    Raises:
        ValueError: 剪貼簿中沒有圖片
    """
    ...

def export_text_to_file(
    text: str,
    file_path: str,
) -> None:
    """
    將文字匯出為 UTF-8 編碼的 .txt 檔案。

    Args:
        text: 要匯出的文字內容
        file_path: 目標檔案的絕對路徑

    Raises:
        PermissionError: 目標路徑不可寫入
        OSError: 其他 I/O 錯誤
    """
    ...

def copy_text_to_clipboard(text: str) -> None:
    """
    將文字複製到系統剪貼簿。

    Args:
        text: 要複製的文字

    Raises:
        RuntimeError: 剪貼簿操作失敗
    """
    ...
```

## 模組三：GUI 介面（gui）

PySide6 桌面介面，依賴 ocr_engine 和 file_io 模組。

```python
class MainWindow:
    """主視窗"""

    # 使用者操作 → 呼叫 file_io / ocr_engine
    # OCR 在背景線程執行，透過 Qt 信號回傳結果
    # GUI 僅負責顯示與使用者互動
    ...
```

**GUI 模組 MUST NOT 直接存取**：
- OCR 引擎的內部實作細節
- 檔案系統操作（透過 file_io 模組間接操作）

## 模組依賴圖

```text
gui ──depends on──→ ocr_engine
gui ──depends on──→ file_io
ocr_engine ──independent──
file_io ──independent──
```

- `ocr_engine` 和 `file_io` 互不依賴
- `gui` 依賴兩者，但兩者不依賴 `gui`
- `ocr_engine` MUST 可在無 GUI 環境下測試
