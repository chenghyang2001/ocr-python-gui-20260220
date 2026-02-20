"""檔案 I/O 模組的單元測試"""

import os
import tempfile

import pytest
from PIL import Image

from src.file_io.image_loader import load_image_from_file
from src.models import SourceType


class TestLoadImageFromFile:
    def _create_temp_image(self, suffix=".png"):
        """建立暫存圖片檔案"""
        img = Image.new("RGB", (100, 100), color="red")
        tmp = tempfile.NamedTemporaryFile(suffix=suffix, delete=False)
        img.save(tmp.name)
        tmp.close()
        return tmp.name

    def test_load_png(self):
        path = self._create_temp_image(".png")
        try:
            source = load_image_from_file(path)
            assert source.source_type == SourceType.FILE
            assert source.image_data is not None
            assert source.file_path == path
            assert source.file_name == os.path.basename(path)
        finally:
            os.unlink(path)

    def test_load_jpg(self):
        path = self._create_temp_image(".jpg")
        try:
            source = load_image_from_file(path)
            assert source.source_type == SourceType.FILE
        finally:
            os.unlink(path)

    def test_load_bmp(self):
        path = self._create_temp_image(".bmp")
        try:
            source = load_image_from_file(path)
            assert source.source_type == SourceType.FILE
        finally:
            os.unlink(path)

    def test_load_tiff(self):
        path = self._create_temp_image(".tiff")
        try:
            source = load_image_from_file(path)
            assert source.source_type == SourceType.FILE
        finally:
            os.unlink(path)

    def test_unsupported_format_raises(self):
        tmp = tempfile.NamedTemporaryFile(suffix=".gif", delete=False)
        tmp.write(b"fake gif data")
        tmp.close()
        try:
            with pytest.raises(ValueError, match="不支援"):
                load_image_from_file(tmp.name)
        finally:
            os.unlink(tmp.name)

    def test_missing_file_raises(self):
        with pytest.raises(FileNotFoundError):
            load_image_from_file("/nonexistent/path/image.png")
