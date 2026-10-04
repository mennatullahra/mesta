from pydantic import BaseModel, Field, field_validator
from app.domain.fashion_taxonomy import CATEGORIES, COLOR_FAMILIES

class DetectedFashionItem(BaseModel):
    category: str
    color: str | None = None
    color_family: str | None = None
    fit: str | None = None
    length: str | None = None
    sleeve_length: str | None = None
    neckline: str | None = None
    pattern: str | None = None
    material: str | None = None
    style_tags: list[str] = []
    modesty_tags: list[str] = []
    confidence: float | None = Field(default=None, ge=0, le=1)

    @field_validator("category")
    @classmethod
    def valid_category(cls,v):
        if v not in CATEGORIES: raise ValueError("Unsupported fashion category")
        return v

    @field_validator("color_family")
    @classmethod
    def valid_family(cls,v):
        if v is not None and v not in COLOR_FAMILIES: raise ValueError("Unsupported color family")
        return v

class OutfitAnalysis(BaseModel):
    overall_style: list[str] = []
    occasion: list[str] = []
    dominant_colors: list[str] = []
    items: list[DetectedFashionItem] = Field(min_length=1)
