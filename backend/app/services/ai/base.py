from abc import ABC, abstractmethod

class AIProvider(ABC):
    @abstractmethod
    def analyze_outfit(self, image_bytes: bytes, mime_type: str, correction: bool=False) -> dict:
        raise NotImplementedError
