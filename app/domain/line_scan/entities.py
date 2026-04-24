from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class LineScanImageSpec:
    input_path: Path
    output_path: Path
    width: int
    channels: int
    output_format: str = "bmp"
    trim_zero_rows: bool = True


@dataclass(frozen=True)
class GeneratedImage:
    output_path: Path
    image_width: int
    image_height: int
    channels: int
