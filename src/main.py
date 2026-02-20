"""OCR 圖片文字辨識桌面應用程式 — 入口點"""

import sys

from PySide6.QtWidgets import QApplication

from src.gui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("OCR 圖片文字辨識")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
