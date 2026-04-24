from abc import ABC, abstractmethod

from app.domain.greeting.entities import Greeting


class GreetingRepository(ABC):
    @abstractmethod
    def get_health(self) -> Greeting:
        raise NotImplementedError

    @abstractmethod
    def build_greeting(self, name: str) -> Greeting:
        raise NotImplementedError
