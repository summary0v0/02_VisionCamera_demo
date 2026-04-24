from dataclasses import dataclass


@dataclass(frozen=True)
class Greeting:
    message: str
