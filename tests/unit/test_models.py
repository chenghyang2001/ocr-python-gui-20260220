"""資料模型的單元測試 — ImageSource, RecognitionSettings, RecognitionResult"""

import pytest
from PIL import Image

from src.models import ImageSource, RecognitionResult, RecognitionSettings, SourceType


class TestSourceType:
    def test_has_file_and_clipboard(self):
        assert SourceType.FILE.value == "file"
        assert SourceType.CLIPBOARD.value == "clipboard"


class TestImageSource:
    def test_create_file_source(self):
        img = Image.new("RGB", (100, 100))
        source = ImageSource(
            source_type=SourceType.FILE,
            image_data=img,
            file_path="/tmp/test.png",
            file_name="test.png",
        )
        assert source.source_type == SourceType.FILE
        assert source.file_path == "/tmp/test.png"
        assert source.file_name == "test.png"
        assert source.image_data is not None

    def test_create_clipboard_source(self):
        img = Image.new("RGB", (100, 100))
        source = ImageSource(
            source_type=SourceType.CLIPBOARD,
            image_data=img,
        )
        assert source.source_type == SourceType.CLIPBOARD
        assert source.file_path is None
        assert source.file_name is None

    def test_image_data_required(self):
        with pytest.raises((TypeError, ValueError)):
            ImageSource(source_type=SourceType.FILE, image_data=None)


class TestRecognitionSettings:
    def test_create_with_single_language(self):
        settings = RecognitionSettings(languages=["ch_tra"])
        assert settings.languages == ["ch_tra"]

    def test_create_with_multiple_languages(self):
        settings = RecognitionSettings(languages=["ch_tra", "en"])
        assert settings.languages == ["ch_tra", "en"]

    def test_empty_languages_raises(self):
        with pytest.raises(ValueError):
            RecognitionSettings(languages=[])

    def test_invalid_language_raises(self):
        with pytest.raises(ValueError):
            RecognitionSettings(languages=["invalid_lang"])

    def test_valid_language_codes(self):
        for code in ["ch_tra", "ch_sim", "en"]:
            settings = RecognitionSettings(languages=[code])
            assert code in settings.languages


class TestRecognitionResult:
    def test_create_with_text(self):
        result = RecognitionResult(text="辨識結果", confidence=0.95, elapsed_time=1.5)
        assert result.text == "辨識結果"
        assert result.confidence == 0.95
        assert result.elapsed_time == 1.5

    def test_create_empty_text(self):
        result = RecognitionResult(text="", confidence=None, elapsed_time=0.5)
        assert result.text == ""
        assert result.confidence is None

    def test_confidence_out_of_range_raises(self):
        with pytest.raises(ValueError):
            RecognitionResult(text="test", confidence=1.5, elapsed_time=1.0)

    def test_confidence_negative_raises(self):
        with pytest.raises(ValueError):
            RecognitionResult(text="test", confidence=-0.1, elapsed_time=1.0)

    def test_confidence_none_is_valid(self):
        result = RecognitionResult(text="test", confidence=None, elapsed_time=1.0)
        assert result.confidence is None
