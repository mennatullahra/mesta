from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.models import Product
from app.services.styling.compatibility import pair_compatibility

COMPLEMENTS={
 "skirt":["blouse","shirt","top","hijab","bag","shoes"],
 "pants":["blouse","shirt","top","blazer","hijab","bag","shoes"],
 "blouse":["skirt","pants","hijab","bag","shoes"],
 "shirt":["skirt","pants","hijab","bag","shoes"],
 "top":["skirt","pants","blazer","hijab","bag","shoes"],
 "dress":["hijab","bag","shoes","blazer"],
 "blazer":["top","blouse","pants","skirt","hijab","bag","shoes"],
 "cardigan":["top","dress","pants","skirt","hijab","bag","shoes"],
 "jacket":["top","dress","pants","skirt","hijab","bag","shoes"],
 "hijab":["dress","blouse","shirt","skirt","pants","bag"],
 "bag":["dress","blouse","skirt","pants","hijab","shoes"],
 "shoes":["dress","blouse","skirt","pants","hijab","bag"],
}

def complete_look(db:Session,anchor:Product,limit:int=6,budget:float|None=None):
    cats=COMPLEMENTS.get(anchor.category,[])
    products=list(db.scalars(select(Product).where(Product.is_active.is_(True),Product.category.in_(cats))).all())
    if budget is not None: products=[p for p in products if p.price<=budget]
    ranked=sorted(products,key=lambda p:pair_compatibility(anchor,p),reverse=True)
    result=[]; used=set()
    for p in ranked:
        if p.category in used: continue
        used.add(p.category); result.append(p)
        if len(result)>=limit: break
    return result
