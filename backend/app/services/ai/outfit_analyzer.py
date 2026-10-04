from __future__ import annotations
import hashlib
from pydantic import ValidationError
from app.schemas.outfit import OutfitAnalysis
from app.services.ai.base import AIProvider

class InvalidAIOutputError(RuntimeError): pass

class OutfitAnalyzer:
    def __init__(self, provider: AIProvider):
        self.provider=provider
        self.cache: dict[str,OutfitAnalysis]={}

    def analyze(self,image_bytes:bytes,mime_type:str)->OutfitAnalysis:
        key=hashlib.sha256(image_bytes).hexdigest()
        if key in self.cache: return self.cache[key]
        last_error=None
        for correction in (False,True):
            try:
                parsed=OutfitAnalysis.model_validate(self.provider.analyze_outfit(image_bytes,mime_type,correction))
                self.cache[key]=parsed
                return parsed
            except (ValidationError,ValueError,TypeError) as exc:
                last_error=exc
        raise InvalidAIOutputError("AI returned invalid structured fashion data") from last_error
