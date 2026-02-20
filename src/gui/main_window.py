"""主視窗 — OCR 圖片文字辨識桌面應用程式"""

from datetime import datetime

from PySide6.QtCore import QObject, Qt, QThread, Signal
from PySide6.QtGui import QImage, QKeySequence, QPixmap, QShortcut
from PySide6.QtWidgets import (
    QCheckBox,
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from src.file_io.image_loader import load_image_from_file
from src.file_io.text_exporter import copy_text_to_clipboard, export_text_to_file
from src.models import ImageSource, SourceType
from src.ocr_engine.engine import OcrEngine


class OcrWorker(QObject):
    """背景 OCR 辨識工作線程"""

    finished = Signal(object)  # RecognitionResult or Exception
    started = Signal()

    def __init__(self, engine: OcrEngine, image_source: ImageSource, languages: list[str]):
        super().__init__()
        self._engine = engine
        self._image_source = image_source
        self._languages = languages

    def run(self):
        self.started.emit()
        try:
            result = self._engine.recognize(self._image_source.image_data, self._languages)
            self.finished.emit(result)
        except Exception as e:
            self.finished.emit(e)


class MainWindow(QMainWindow):
    """主視窗"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("OCR 圖片文字辨識")
        self.setMinimumSize(800, 600)

        self._engine = OcrEngine()
        self._current_source: ImageSource | None = None
        self._worker_thread: QThread | None = None

        self._setup_ui()
        self._setup_shortcuts()
        self._update_button_states()

    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)

        # ── 左側：圖片預覽與來源按鈕 ──
        left_panel = QVBoxLayout()

        # 來源按鈕
        source_layout = QHBoxLayout()
        self._btn_load_file = QPushButton("載入圖片")
        self._btn_load_file.clicked.connect(self._on_load_file)
        source_layout.addWidget(self._btn_load_file)

        self._btn_paste_clipboard = QPushButton("從剪貼簿貼上")
        self._btn_paste_clipboard.clicked.connect(self._on_paste_clipboard)
        source_layout.addWidget(self._btn_paste_clipboard)
        left_panel.addLayout(source_layout)

        # 圖片預覽
        self._image_preview = QLabel("尚未載入圖片")
        self._image_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._image_preview.setMinimumSize(350, 300)
        self._image_preview.setStyleSheet("border: 1px solid #ccc; background: #f9f9f9;")
        left_panel.addWidget(self._image_preview, stretch=1)

        main_layout.addLayout(left_panel, stretch=1)

        # ── 右側：設定、結果、操作按鈕 ──
        right_panel = QVBoxLayout()

        # 語言選擇
        lang_group = QGroupBox("辨識語言")
        lang_layout = QHBoxLayout(lang_group)
        self._cb_ch_tra = QCheckBox("繁體中文")
        self._cb_ch_tra.setChecked(True)
        self._cb_ch_sim = QCheckBox("簡體中文")
        self._cb_en = QCheckBox("英文")
        lang_layout.addWidget(self._cb_ch_tra)
        lang_layout.addWidget(self._cb_ch_sim)
        lang_layout.addWidget(self._cb_en)
        right_panel.addWidget(lang_group)

        # 辨識按鈕
        self._btn_recognize = QPushButton("辨識")
        self._btn_recognize.clicked.connect(self._on_recognize)
        self._btn_recognize.setMinimumHeight(40)
        right_panel.addWidget(self._btn_recognize)

        # 狀態標籤
        self._status_label = QLabel("")
        right_panel.addWidget(self._status_label)

        # 結果區域
        self._result_text = QTextEdit()
        self._result_text.setReadOnly(True)
        self._result_text.setPlaceholderText("辨識結果將顯示在這裡...")
        right_panel.addWidget(self._result_text, stretch=1)

        # 操作按鈕
        action_layout = QHBoxLayout()
        self._btn_copy = QPushButton("複製到剪貼簿")
        self._btn_copy.clicked.connect(self._on_copy)
        action_layout.addWidget(self._btn_copy)

        self._btn_export = QPushButton("匯出")
        self._btn_export.clicked.connect(self._on_export)
        action_layout.addWidget(self._btn_export)
        right_panel.addLayout(action_layout)

        main_layout.addLayout(right_panel, stretch=1)

    def _setup_shortcuts(self):
        paste_shortcut = QShortcut(QKeySequence.StandardKey.Paste, self)
        paste_shortcut.activated.connect(self._on_paste_clipboard)

    def _update_button_states(self):
        has_image = self._current_source is not None
        is_processing = self._worker_thread is not None and self._worker_thread.isRunning()
        has_result = bool(self._result_text.toPlainText())

        self._btn_recognize.setEnabled(has_image and not is_processing)
        self._btn_copy.setEnabled(has_result)
        self._btn_export.setEnabled(has_result)

    def _get_selected_languages(self) -> list[str]:
        langs = []
        if self._cb_ch_tra.isChecked():
            langs.append("ch_tra")
        if self._cb_ch_sim.isChecked():
            langs.append("ch_sim")
        if self._cb_en.isChecked():
            langs.append("en")
        return langs

    def _display_image(self, image_source: ImageSource):
        """在預覽區域顯示圖片"""
        self._current_source = image_source
        img = image_source.image_data

        # PIL Image → QPixmap
        if img.mode != "RGB":
            img = img.convert("RGB")
        data = img.tobytes("raw", "RGB")
        qimg = QImage(data, img.width, img.height, img.width * 3, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg)

        scaled = pixmap.scaled(
            self._image_preview.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self._image_preview.setPixmap(scaled)
        self._result_text.clear()
        self._status_label.setText("")
        self._update_button_states()

    # ── 事件處理 ──

    def _on_load_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "選擇圖片檔案",
            "",
            "圖片檔案 (*.png *.jpg *.jpeg *.bmp *.tiff *.tif);;所有檔案 (*)",
        )
        if not file_path:
            return
        try:
            source = load_image_from_file(file_path)
            self._display_image(source)
        except (FileNotFoundError, ValueError) as e:
            QMessageBox.warning(self, "載入失敗", str(e))

    def _on_paste_clipboard(self):
        from src.file_io.image_loader import load_image_from_clipboard

        try:
            source = load_image_from_clipboard()
            self._display_image(source)
        except ValueError as e:
            QMessageBox.information(self, "剪貼簿", str(e))

    def _on_recognize(self):
        if self._current_source is None:
            return

        languages = self._get_selected_languages()
        if not languages:
            QMessageBox.warning(self, "語言選擇", "請至少選擇一種辨識語言")
            return

        self._btn_recognize.setEnabled(False)
        self._status_label.setText("辨識中...")

        self._worker_thread = QThread()
        self._worker = OcrWorker(self._engine, self._current_source, languages)
        self._worker.moveToThread(self._worker_thread)
        self._worker_thread.started.connect(self._worker.run)
        self._worker.finished.connect(self._on_recognize_done)
        self._worker.finished.connect(self._worker_thread.quit)
        self._worker_thread.start()

    def _on_recognize_done(self, result):
        if isinstance(result, Exception):
            QMessageBox.critical(self, "辨識失敗", str(result))
            self._status_label.setText("辨識失敗")
        else:
            if result.text:
                self._result_text.setPlainText(result.text)
                confidence_str = (
                    f"（信心度: {result.confidence:.0%}）" if result.confidence else ""
                )
                self._status_label.setText(
                    f"辨識完成 — {result.elapsed_time:.1f} 秒{confidence_str}"
                )
            else:
                self._result_text.setPlainText("")
                self._status_label.setText("未偵測到文字")
        self._update_button_states()

    def _on_copy(self):
        text = self._result_text.toPlainText()
        if not text:
            return
        try:
            copy_text_to_clipboard(text)
            self._status_label.setText("已複製到剪貼簿")
        except RuntimeError as e:
            QMessageBox.warning(self, "複製失敗", str(e))

    def _on_export(self):
        text = self._result_text.toPlainText()
        if not text:
            return

        # 預設檔名
        if self._current_source and self._current_source.source_type == SourceType.FILE:
            import os

            base = os.path.splitext(self._current_source.file_name or "result")[0]
            default_name = f"{base}.txt"
        else:
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            default_name = f"ocr-result-{timestamp}.txt"

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "匯出辨識結果",
            default_name,
            "文字檔 (*.txt);;所有檔案 (*)",
        )
        if not file_path:
            return
        try:
            export_text_to_file(text, file_path)
            self._status_label.setText(f"已匯出至: {file_path}")
        except (PermissionError, OSError) as e:
            QMessageBox.warning(self, "匯出失敗", str(e))
