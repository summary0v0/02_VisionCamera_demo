from pydantic import BaseModel, Field


class GenerateLineScanImageCommand(BaseModel):
    input_path: str = Field(..., description="Path to the source .raw or image file.")
    output_path: str | None = Field(
        default=None,
        description="Optional output path. If omitted, a file is created under output/generated.",
    )
    width: int = Field(..., gt=0, description="Image width in pixels.")
    channels: int = Field(default=1, ge=1, le=4, description="Number of channels in the raw image.")
    output_format: str = Field(
        default="bmp",
        description="Output image format. Supported values: bmp, pgm, ppm.",
    )
    trim_zero_rows: bool = Field(
        default=True,
        description="Remove rows that are entirely zero after decoding the raw stream.",
    )


class GeneratedLineScanImageResponse(BaseModel):
    output_path: str
    image_width: int
    image_height: int
    channels: int
