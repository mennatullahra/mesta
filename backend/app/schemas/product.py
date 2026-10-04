from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator
from app.domain.fashion_taxonomy import normalize_category

class ProductBase(BaseModel):
    brand: str = Field(min_length=1, max_length=120)
    name: str = Field(min_length=1, max_length=180)
    description: str | None = None
    category: str
    subcategory: str | None = None
    price: float = Field(gt=0)
    currency: str = Field(default="EGP", min_length=3, max_length=3)
    image_url: str | None = None
    local_image_path: str | None = None
    product_url: str | None = None
    available_sizes: list[str] | None = None
    colors: list[str] | None = None
    primary_color: str | None = None
    color_family: str | None = None
    style_tags: list[str] | None = None
    occasion_tags: list[str] | None = None
    fit: str | None = None
    length: str | None = None
    sleeve_length: str | None = None
    neckline: str | None = None
    pattern: str | None = None
    material: str | None = None
    modesty_tags: list[str] | None = None
    is_active: bool = True

    @field_validator("category")
    @classmethod
    def valid_category(cls, value: str) -> str:
        return normalize_category(value)

    @field_validator("currency")
    @classmethod
    def normalize_currency(cls, value: str) -> str:
        return value.upper()

class ProductCreate(ProductBase):
    id: str = Field(min_length=1, max_length=64)

class ProductRead(ProductCreate):
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
