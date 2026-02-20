"""圖片載入功能 — 從檔案或剪貼簿讀取圖片"""

import os

from PIL import Image
from PySide6.QtGui import QImage
from PySide6.QtWidgets import QApplication

from src.models import ImageSource, SourceType

SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".tif"}


def load_image_from_file(file_path: str) -> ImageSource:
    """
    從檔案路徑載入圖片。

    Raises:
        FileNotFoundError: 檔案不存在
        ValueError: 不支援的檔案格式
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"檔案不存在: {file_path}")

    ext = os.path.splitext(file_path)[1].lower()
    if ext not in SUPPORTED_EXTENSIONS:
        supported = ", ".join(sorted(SUPPORTED_EXTENSIONS))
        raise ValueError(f"不支援的檔案格式: {ext}（支援: {supported}）")

    image = Image.open(file_path).convert("RGB")

    return ImageSource(
        source_type=SourceType.FILE,
        image_data=image,
        file_path=file_path,
        file_name=os.path.basename(file_path),
    )


def load_image_from_clipboard() -> ImageSource:
    """
    從系統剪貼簿讀取圖片。

    Raises:
        ValueError: 剪貼簿中沒有圖片
    """
    clipboard = QApplication.clipboard()
    qimage = clipboard.image()

    if qimage.isNull():
        raise ValueError("剪貼簿中沒有圖片")

    # QImage → PIL Image
    qimage = qimage.convertToFormat(QImage.Format.Format_RGB888)
    width = qimage.width()
    height = qimage.height()
    bytes_per_line = qimage.bytesPerLine()
    raw_data = qimage.bits().tobytes()

    # 處理 stride（每行可能有 padding）
    if bytes_per_line == width * 3:
        pil_image = Image.frombytes("RGB", (width, height), raw_data)
    else:
        pil_image = Image.frombytes("RGB", (width, height), raw_data, "raw", "RGB", bytes_per_line)

    return ImageSource(
        source_type=SourceType.CLIPBOARD,
        image_data=pil_image,
    )
