from fastapi import APIRouter, File, HTTPException, UploadFile
from PIL import Image, UnidentifiedImageError
from io import BytesIO
from app.core.config import settings
from app.services.ai.outfit_analyzer import InvalidAIOutputError, OutfitAnalyzer
from app.services.ai.provider import OpenAIProvider

router=APIRouter(prefix="/api",tags=["visual-search"])
ALLOWED={"image/jpeg","image/png","image/webp"}

def validate_image(data:bytes,mime:str):
    if mime not in ALLOWED: raise HTTPException(415,"Please upload a JPG, PNG or WebP image.")
    if len(data)>settings.max_upload_mb*1024*1024: raise HTTPException(413,f"Image must be {settings.max_upload_mb} MB or smaller.")
    try:
        im=Image.open(BytesIO(data)); im.verify()
    except (UnidentifiedImageError,OSError):
        raise HTTPException(400,"That file does not appear to be a valid image.")

@router.post("/analyze-outfit")
async def analyze_outfit(file:UploadFile=File(...)):
    data=await file.read(); validate_image(data,file.content_type or "")
    try:
        analysis=OutfitAnalyzer(OpenAIProvider()).analyze(data,file.content_type or "image/jpeg")
        return analysis
    except RuntimeError as exc:
        if isinstance(exc,InvalidAIOutputError): raise HTTPException(502,"We couldn't understand this look reliably. Please try another image.")
        raise HTTPException(503,"Outfit analysis is temporarily unavailable.")
