"""OpenAI multimodal adapter. Imported lazily so catalog/search works without AI SDK."""
from __future__ import annotations
import base64, json
from app.core.config import settings
from app.services.ai.base import AIProvider

SYSTEM = """You are MESTA's fashion image analyzer. Identify only visible garments/accessories.
Return JSON only. Never invent attributes: use null or [] when not visually inferable.
Use normalized categories: blouse, shirt, top, skirt, dress, pants, blazer, cardigan, jacket, hijab, bag, shoes.
Use normalized color_family: red, pink, orange, yellow, green, blue, purple, brown, neutral, black, white, metallic.
Output: overall_style[], occasion[], dominant_colors[], items[]. Each item may contain category,color,color_family,fit,length,sleeve_length,neckline,pattern,material,style_tags[],modesty_tags[],confidence.
Confidence must only be supplied when you can genuinely estimate it; otherwise null."""

class OpenAIProvider(AIProvider):
    def __init__(self):
        if not settings.ai_api_key or not settings.ai_model:
            raise RuntimeError("AI_API_KEY and AI_MODEL are required for live outfit analysis")
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError("OpenAI SDK is not installed") from exc
        self.client=OpenAI(api_key=settings.ai_api_key)

    def analyze_outfit(self,image_bytes:bytes,mime_type:str,correction:bool=False)->dict:
        data=base64.b64encode(image_bytes).decode()
        extra=" Previous output failed schema validation. Correct it strictly." if correction else ""
        response=self.client.chat.completions.create(
            model=settings.ai_model,
            response_format={"type":"json_object"},
            messages=[{"role":"system","content":SYSTEM+extra},{"role":"user","content":[{"type":"text","text":"Analyze this outfit."},{"type":"image_url","image_url":{"url":f"data:{mime_type};base64,{data}"}}]}],
            temperature=0,
        )
        return json.loads(response.choices[0].message.content)
