"""共用資料模型 — ImageSource, RecognitionSettings, RecognitionResult"""

from dataclasses import dataclass, field
from enum import Enum

from PIL import Image


class SourceType(Enum):
    """圖片來源類型"""

    FILE = "file"
    CLIPBOARD = "clipboard"


SUPPORTED_LANGUAGES = {"ch_tra", "ch_sim", "en"}


@dataclass
class ImageSource:
    """使用者提供的圖片來源"""

    source_type: SourceType
    image_data: Image.Image
    file_path: str | None = None
    file_name: str | None = None

    def __post_init__(self):
        if self.image_data is None:
            raise ValueError("image_data 不可為空")


@dataclass
class RecognitionSettings:
    """辨識設定"""

    languages: list[str] = field(default_factory=list)

    def __post_init__(self):
        if not self.languages:
            raise ValueError("languages 至少需包含一個語言")
        for lang in self.languages:
            if lang not in SUPPORTED_LANGUAGES:
                raise ValueError(f"不支援的語言代碼: {lang}")


@dataclass
class RecognitionResult:
    """辨識結果"""

    text: str
    confidence: float | None
    elapsed_time: float

    def __post_init__(self):
        if self.confidence is not None:
            if not (0.0 <= self.confidence <= 1.0):
                raise ValueError(f"confidence 必須在 0.0-1.0 之間，收到: {self.confidence}")
