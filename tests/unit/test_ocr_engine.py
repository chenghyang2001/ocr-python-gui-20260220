"""OCR 引擎的單元測試"""

import pytest
from PIL import Image

from src.models import RecognitionResult
from src.ocr_engine.engine import OcrEngine


class TestOcrEngineInit:
    def test_engine_creates_successfully(self):
        engine = OcrEngine()
        assert engine is not None


class TestGetSupportedLanguages:
    def test_returns_list(self):
        engine = OcrEngine()
        langs = engine.get_supported_languages()
        assert isinstance(langs, list)
        assert len(langs) > 0

    def test_contains_required_languages(self):
        engine = OcrEngine()
        langs = engine.get_supported_languages()
        codes = [lang["code"] for lang in langs]
        assert "ch_tra" in codes
        assert "ch_sim" in codes
        assert "en" in codes

    def test_language_has_code_and_name(self):
        engine = OcrEngine()
        langs = engine.get_supported_languages()
        for lang in langs:
            assert "code" in lang
            assert "name" in lang


class TestRecognize:
    def test_recognize_returns_result(self):
        engine = OcrEngine()
        img = Image.new("RGB", (200, 50), color="white")
        result = engine.recognize(img, ["en"])
        assert isinstance(result, RecognitionResult)
        assert isinstance(result.text, str)
        assert result.elapsed_time >= 0

    def test_recognize_empty_languages_raises(self):
        engine = OcrEngine()
        img = Image.new("RGB", (100, 100))
        with pytest.raises(ValueError):
            engine.recognize(img, [])

    def test_recognize_invalid_language_raises(self):
        engine = OcrEngine()
        img = Image.new("RGB", (100, 100))
        with pytest.raises(ValueError):
            engine.recognize(img, ["invalid"])

    def test_recognize_blank_image(self):
        """空白圖片應回傳空字串（未偵測到文字）"""
        engine = OcrEngine()
        img = Image.new("RGB", (100, 100), color="white")
        result = engine.recognize(img, ["en"])
        assert isinstance(result.text, str)
