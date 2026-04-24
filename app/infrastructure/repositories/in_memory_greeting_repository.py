from app.domain.greeting.entities import Greeting
from app.domain.greeting.repositories import GreetingRepository


class InMemoryGreetingRepository(GreetingRepository):
    def get_health(self) -> Greeting:
        return Greeting(message="ok")

    def build_greeting(self, name: str) -> Greeting:
        cleaned_name = name.strip() or "world"
        return Greeting(message=f"Hello, {cleaned_name}!")
