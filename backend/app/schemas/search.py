from pydantic import BaseModel, Field

class SearchItem(BaseModel):
    category: str | None = None
    color: str | None = None
    color_family: str | None = None
    fit: str | None = None
    length: str | None = None
    sleeve_length: str | None = None
    neckline: str | None = None
    pattern: str | None = None
    style_tags: list[str] = []
    modesty_tags: list[str] = []
    query: str | None = None

class MatchResult(BaseModel):
    product_id: str
    score: float = Field(ge=0, le=1)
    semantic_score: float = Field(ge=0, le=1)
    match_reasons: list[str]
