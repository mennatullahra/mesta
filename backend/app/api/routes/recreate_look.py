from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.api.routes.visual_search import validate_image
from app.services.ai.outfit_analyzer import InvalidAIOutputError, OutfitAnalyzer
from app.services.ai.provider import OpenAIProvider
from app.services.recreate import RecreateLookService

router=APIRouter(prefix="/api",tags=["recreate-look"])
@router.post("/recreate-look")
async def recreate_look(file:UploadFile=File(...),db:Session=Depends(get_db)):
    data=await file.read(); validate_image(data,file.content_type or "")
    try: analysis=OutfitAnalyzer(OpenAIProvider()).analyze(data,file.content_type or "image/jpeg")
    except InvalidAIOutputError: raise HTTPException(502,"We couldn't understand this look reliably.")
    except RuntimeError: raise HTTPException(503,"Outfit analysis is temporarily unavailable.")
    return RecreateLookService().recreate(analysis,db)
