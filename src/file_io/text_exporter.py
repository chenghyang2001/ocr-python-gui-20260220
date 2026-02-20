"""文字匯出功能 — 複製到剪貼簿、匯出為檔案"""

from PySide6.QtWidgets import QApplication


def copy_text_to_clipboard(text: str) -> None:
    """
    將文字複製到系統剪貼簿。

    Raises:
        RuntimeError: 剪貼簿操作失敗
    """
    clipboard = QApplication.clipboard()
    if clipboard is None:
        raise RuntimeError("無法存取系統剪貼簿")
    clipboard.setText(text)


def export_text_to_file(text: str, file_path: str) -> None:
    """
    將文字匯出為 UTF-8 編碼的 .txt 檔案。

    Raises:
        PermissionError: 目標路徑不可寫入
        OSError: 其他 I/O 錯誤
    """
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(text)
