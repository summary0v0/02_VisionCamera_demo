from app.application.use_cases.greeting import BuildGreetingUseCase, GetHealthUseCase
from app.application.use_cases.line_scan import GenerateLineScanImageUseCase
from app.infrastructure.repositories.in_memory_greeting_repository import (
    InMemoryGreetingRepository,
)
from app.infrastructure.services.raw_line_scan_image_generator import (
    RawLineScanImageGenerator,
)


def get_health_use_case() -> GetHealthUseCase:
    repository = InMemoryGreetingRepository()
    return GetHealthUseCase(greeting_repository=repository)


def get_build_greeting_use_case() -> BuildGreetingUseCase:
    repository = InMemoryGreetingRepository()
    return BuildGreetingUseCase(greeting_repository=repository)


def get_generate_line_scan_image_use_case() -> GenerateLineScanImageUseCase:
    generator = RawLineScanImageGenerator()
    return GenerateLineScanImageUseCase(image_generator=generator)
