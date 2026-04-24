from pathlib import Path
import shutil
import struct

from app.domain.line_scan.entities import GeneratedImage, LineScanImageSpec
from app.domain.line_scan.services import LineScanImageGenerator


class RawLineScanImageGenerator(LineScanImageGenerator):
    def generate(self, spec: LineScanImageSpec) -> GeneratedImage:
        input_path = spec.input_path
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")

        output_format = spec.output_format.lower()
        output_path = self._normalize_output_path(spec.output_path, output_format)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if input_path.suffix.lower() == ".raw":
            decoded = self._decode_raw(spec)
            self._save_image(decoded["rows"], decoded["width"], decoded["channels"], output_path, output_format)
            return GeneratedImage(
                output_path=output_path,
                image_width=decoded["width"],
                image_height=decoded["height"],
                channels=decoded["channels"],
            )
        else:
            shutil.copy2(input_path, output_path)
            return GeneratedImage(
                output_path=output_path,
                image_width=0,
                image_height=0,
                channels=spec.channels,
            )

    def _decode_raw(self, spec: LineScanImageSpec) -> dict[str, int | list[bytes]]:
        data = spec.input_path.read_bytes()
        row_width = spec.width * spec.channels

        if len(data) == 0:
            raise ValueError("Raw input is empty.")
        if len(data) % row_width != 0:
            raise ValueError(
                "Raw input size is not divisible by width * channels. "
                f"size={len(data)}, width={spec.width}, channels={spec.channels}"
            )

        height = len(data) // row_width
        rows = [
            data[index * row_width:(index + 1) * row_width]
            for index in range(height)
        ]
        if spec.trim_zero_rows:
            rows = [row for row in rows if any(byte != 0 for byte in row)]
        if not rows:
            raise ValueError("Image is empty after trimming zero rows.")
        channels = 3 if spec.channels == 4 else spec.channels
        return {
            "rows": rows,
            "width": spec.width,
            "height": len(rows),
            "channels": channels,
        }

    def _save_image(
        self,
        rows: list[bytes],
        width: int,
        channels: int,
        output_path: Path,
        output_format: str,
    ) -> None:
        if output_format == "bmp":
            self._write_bmp(rows, width, channels, output_path)
            return
        if output_format == "pgm":
            if channels != 1:
                raise ValueError("PGM only supports grayscale output.")
            self._write_pgm(rows, width, output_path)
            return
        if output_format == "ppm":
            self._write_ppm(rows, width, channels, output_path)
            return
        raise ValueError(f"Unsupported output format: {output_format}")

    @staticmethod
    def _normalize_output_path(output_path: Path, output_format: str) -> Path:
        suffix = f".{output_format}"
        if output_path.suffix.lower() != suffix:
            return output_path.with_suffix(suffix)
        return output_path

    @staticmethod
    def _write_pgm(rows: list[bytes], width: int, output_path: Path) -> None:
        header = f"P5\n{width} {len(rows)}\n255\n".encode("ascii")
        with output_path.open("wb") as file:
            file.write(header)
            for row in rows:
                file.write(row)

    def _write_ppm(self, rows: list[bytes], width: int, channels: int, output_path: Path) -> None:
        header = f"P6\n{width} {len(rows)}\n255\n".encode("ascii")
        with output_path.open("wb") as file:
            file.write(header)
            for row in rows:
                file.write(self._to_rgb_bytes(row, channels))

    def _write_bmp(self, rows: list[bytes], width: int, channels: int, output_path: Path) -> None:
        if channels == 1:
            self._write_grayscale_bmp(rows, width, output_path)
            return
        self._write_rgb_bmp(rows, width, channels, output_path)

    @staticmethod
    def _write_grayscale_bmp(rows: list[bytes], width: int, output_path: Path) -> None:
        height = len(rows)
        row_stride = (width + 3) & ~3
        pixel_bytes = row_stride * height
        color_table_size = 256 * 4
        file_size = 14 + 40 + color_table_size + pixel_bytes

        with output_path.open("wb") as file:
            file.write(b"BM")
            file.write(struct.pack("<IHHI", file_size, 0, 0, 14 + 40 + color_table_size))
            file.write(struct.pack("<IIIHHIIIIII", 40, width, height, 1, 8, 0, pixel_bytes, 2835, 2835, 256, 0))
            for value in range(256):
                file.write(bytes((value, value, value, 0)))
            padding = b"\x00" * (row_stride - width)
            for row in reversed(rows):
                file.write(row)
                file.write(padding)

    def _write_rgb_bmp(self, rows: list[bytes], width: int, channels: int, output_path: Path) -> None:
        height = len(rows)
        rgb_rows = [self._to_rgb_bytes(row, channels) for row in rows]
        row_stride = ((width * 3) + 3) & ~3
        pixel_bytes = row_stride * height
        file_size = 14 + 40 + pixel_bytes

        with output_path.open("wb") as file:
            file.write(b"BM")
            file.write(struct.pack("<IHHI", file_size, 0, 0, 14 + 40))
            file.write(struct.pack("<IIIHHIIIIII", 40, width, height, 1, 24, 0, pixel_bytes, 2835, 2835, 0, 0))
            for row in reversed(rgb_rows):
                bgr = bytearray()
                for index in range(0, len(row), 3):
                    red, green, blue = row[index:index + 3]
                    bgr.extend((blue, green, red))
                padding = b"\x00" * (row_stride - len(bgr))
                file.write(bgr)
                file.write(padding)

    @staticmethod
    def _to_rgb_bytes(row: bytes, channels: int) -> bytes:
        if channels == 1:
            rgb = bytearray()
            for value in row:
                rgb.extend((value, value, value))
            return bytes(rgb)
        if channels == 3:
            return row
        if channels == 4:
            rgb = bytearray()
            for index in range(0, len(row), 4):
                rgb.extend(row[index:index + 3])
            return bytes(rgb)
        raise ValueError(f"Unsupported channel count: {channels}")
