from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import Product
from app.schemas.product import ProductRead
from app.schemas.search import SearchItem
from app.services.search.product_matcher import ProductMatcher

router=APIRouter(prefix="/api/search",tags=["search"])
matcher=ProductMatcher()

@router.post("/similar")
def search_similar(item: SearchItem, top_k: int=Query(5,ge=1,le=20), db: Session=Depends(get_db)):
    products=list(db.scalars(select(Product).where(Product.is_active.is_(True))).all())
    results=matcher.rank(item,products,top_k)
    return [{"product":ProductRead.model_validate(p),"score":round(score,4),"semantic_score":round(semantic,4),"match_reasons":reasons} for p,score,semantic,reasons in results]
