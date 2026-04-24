from fastapi import APIRouter, Depends

from app.application.dto import MessageResponse
from app.application.use_cases.greeting import BuildGreetingUseCase, GetHealthUseCase
from app.interfaces.http.dependencies import (
    get_build_greeting_use_case,
    get_health_use_case,
)


router = APIRouter(prefix="/api", tags=["greeting"])


@router.get("/health", response_model=MessageResponse)
def health_check(
    use_case: GetHealthUseCase = Depends(get_health_use_case),
) -> MessageResponse:
    return use_case.execute()


@router.get("/hello/{name}", response_model=MessageResponse)
def say_hello(
    name: str,
    use_case: BuildGreetingUseCase = Depends(get_build_greeting_use_case),
) -> MessageResponse:
    return use_case.execute(name=name)
