from pathlib import Path

from app.application.line_scan_dto import (
    GenerateLineScanImageCommand,
    GeneratedLineScanImageResponse,
)
from app.domain.line_scan.entities import LineScanImageSpec
from app.domain.line_scan.services import LineScanImageGenerator


class GenerateLineScanImageUseCase:
    def __init__(self, image_generator: LineScanImageGenerator) -> None:
        self._image_generator = image_generator

    def execute(
        self,
        command: GenerateLineScanImageCommand,
    ) -> GeneratedLineScanImageResponse:
        output_path = Path(command.output_path) if command.output_path else self._build_default_output_path()
        generated = self._image_generator.generate(
            LineScanImageSpec(
                input_path=Path(command.input_path),
                output_path=output_path,
                width=command.width,
                channels=command.channels,
                output_format=command.output_format,
                trim_zero_rows=command.trim_zero_rows,
            )
        )
        return GeneratedLineScanImageResponse(
            output_path=str(generated.output_path),
            image_width=generated.image_width,
            image_height=generated.image_height,
            channels=generated.channels,
        )

    @staticmethod
    def _build_default_output_path() -> Path:
        output_dir = Path("output") / "generated"
        output_dir.mkdir(parents=True, exist_ok=True)
        return output_dir / "line_scan_output.bmp"
