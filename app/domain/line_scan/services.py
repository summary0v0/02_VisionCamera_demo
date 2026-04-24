from abc import ABC, abstractmethod

from app.domain.line_scan.entities import GeneratedImage, LineScanImageSpec


class LineScanImageGenerator(ABC):
    @abstractmethod
    def generate(self, spec: LineScanImageSpec) -> GeneratedImage:
        raise NotImplementedError
