from pydantic import BaseModel, Field
class StyleConstraints(BaseModel):
    occasion: str | None=None
    modesty: list[str]=[]
    styles: list[str]=[]
    avoid: list[str]=[]
    colors: list[str]=[]
    color_families: list[str]=[]
    budget: float | None=Field(default=None,gt=0)
    currency: str="EGP"
class StyleMeRequest(BaseModel):
    query: str=Field(min_length=3,max_length=1000)
