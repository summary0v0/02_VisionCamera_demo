from fastapi import APIRouter, Depends

from app.application.line_scan_dto import (
    GenerateLineScanImageCommand,
    GeneratedLineScanImageResponse,
)
from app.application.use_cases.line_scan import GenerateLineScanImageUseCase
from app.interfaces.http.dependencies import get_generate_line_scan_image_use_case


router = APIRouter(prefix="/api/line-scan", tags=["line-scan"])


@router.post("/generate", response_model=GeneratedLineScanImageResponse)
def generate_line_scan_image(
    command: GenerateLineScanImageCommand,
    use_case: GenerateLineScanImageUseCase = Depends(get_generate_line_scan_image_use_case),
) -> GeneratedLineScanImageResponse:
    return use_case.execute(command)
