"""OCR 辨識引擎封裝 — 使用 RapidOCR (ONNX Runtime)"""

import time

import numpy as np
from PIL import Image
from rapidocr_onnxruntime import RapidOCR

from src.models import SUPPORTED_LANGUAGES, RecognitionResult


class OcrEngine:
    """OCR 辨識引擎，封裝 RapidOCR"""

    def __init__(self) -> None:
        self._engine = RapidOCR()

    def recognize(self, image: Image.Image, languages: list[str]) -> RecognitionResult:
        """
        對圖片進行 OCR 辨識。

        Args:
            image: PIL Image 格式的圖片
            languages: 辨識語言列表 ("ch_tra", "ch_sim", "en")

        Returns:
            RecognitionResult 包含辨識文字、信心度、耗時
        """
        if not languages:
            raise ValueError("languages 至少需包含一個語言")
        for lang in languages:
            if lang not in SUPPORTED_LANGUAGES:
                raise ValueError(f"不支援的語言代碼: {lang}")

        img_array = np.array(image)

        start_time = time.perf_counter()
        result, _ = self._engine(img_array)
        elapsed = time.perf_counter() - start_time

        if not result:
            return RecognitionResult(text="", confidence=None, elapsed_time=elapsed)

        lines = []
        scores = []
        for line in result:
            _box, text, score = line
            lines.append(text)
            scores.append(score)

        full_text = "\n".join(lines)
        avg_confidence = sum(scores) / len(scores) if scores else None

        return RecognitionResult(
            text=full_text,
            confidence=avg_confidence,
            elapsed_time=elapsed,
        )

    def get_supported_languages(self) -> list[dict[str, str]]:
        """回傳支援的語言清單"""
        return [
            {"code": "ch_tra", "name": "繁體中文"},
            {"code": "ch_sim", "name": "簡體中文"},
            {"code": "en", "name": "英文"},
        ]
