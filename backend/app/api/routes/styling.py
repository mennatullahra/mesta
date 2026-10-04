from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.styling import StyleMeRequest
from app.services.ai.style_parser import parse_style_query
from app.services.styling.style_me import build_style_outfits
router=APIRouter(prefix="/api",tags=["styling"])
@router.post("/style-me")
def style_me(req:StyleMeRequest,db:Session=Depends(get_db)):
    try: constraints=parse_style_query(req.query)
    except Exception: raise HTTPException(503,"Style interpretation is temporarily unavailable.")
    outfits=build_style_outfits(db,constraints)
    if not outfits: return {"constraints":constraints,"outfits":[],"message":"No catalog outfit satisfies these constraints and budget yet."}
    return {"constraints":constraints,"outfits":outfits}
