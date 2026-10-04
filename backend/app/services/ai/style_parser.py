import json
from app.core.config import settings
from app.schemas.styling import StyleConstraints

def parse_style_query(query:str)->StyleConstraints:
    if not settings.ai_api_key or not settings.ai_model: raise RuntimeError("AI configuration required")
    try:
        from openai import OpenAI
    except ImportError as exc: raise RuntimeError("OpenAI SDK not installed") from exc
    client=OpenAI(api_key=settings.ai_api_key)
    prompt="""Parse the fashion request into JSON only: occasion (string|null), modesty[], styles[], avoid[], colors[], color_families[], budget (number|null), currency. Do not recommend or invent products."""
    r=client.chat.completions.create(model=settings.ai_model,response_format={"type":"json_object"},messages=[{"role":"system","content":prompt},{"role":"user","content":query}],temperature=0)
    return StyleConstraints.model_validate(json.loads(r.choices[0].message.content))
