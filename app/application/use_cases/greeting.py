from app.application.dto import MessageResponse
from app.domain.greeting.repositories import GreetingRepository


class GetHealthUseCase:
    def __init__(self, greeting_repository: GreetingRepository) -> None:
        self._greeting_repository = greeting_repository

    def execute(self) -> MessageResponse:
        greeting = self._greeting_repository.get_health()
        return MessageResponse(message=greeting.message)


class BuildGreetingUseCase:
    def __init__(self, greeting_repository: GreetingRepository) -> None:
        self._greeting_repository = greeting_repository

    def execute(self, name: str) -> MessageResponse:
        greeting = self._greeting_repository.build_greeting(name=name)
        return MessageResponse(message=greeting.message)
