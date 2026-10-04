from __future__ import annotations
import itertools
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.models import Product
from app.schemas.styling import StyleConstraints
from app.services.styling.compatibility import pair_compatibility

BASE_GROUPS=[["dress"],["blouse","shirt","top"],["skirt","pants"]]

def _product_fit(p,c):
    score=0.0
    if c.colors and p.primary_color in c.colors: score+=2
    if c.color_families and p.color_family in c.color_families: score+=1.5
    if c.styles and set(c.styles)&set(p.style_tags or []): score+=1.5
    if c.occasion and c.occasion in (p.occasion_tags or []): score+=1.5
    if c.modesty and set(c.modesty)&set(p.modesty_tags or []): score+=1
    return score

def build_style_outfits(db:Session,c:StyleConstraints,max_outfits=3):
    products=list(db.scalars(select(Product).where(Product.is_active.is_(True))).all())
    outfits=[]
    # Candidate structures: dress+hijab+bag+shoes OR top+bottom+hijab+bag+shoes.
    structures=[["dress","hijab","bag","shoes"],["blouse","skirt","hijab","bag","shoes"],["blouse","pants","hijab","bag","shoes"],["shirt","skirt","hijab","bag","shoes"]]
    for structure in structures:
        groups=[]
        for cat in structure:
            candidates=[p for p in products if p.category==cat]
            candidates=sorted(candidates,key=lambda p:_product_fit(p,c),reverse=True)[:4]
            if not candidates: groups=[]; break
            groups.append(candidates)
        for combo in itertools.product(*groups) if groups else []:
            total=sum(p.price for p in combo)
            if c.budget is not None and total>c.budget: continue
            pairs=list(itertools.combinations(combo,2)); coherence=sum(pair_compatibility(a,b) for a,b in pairs)/len(pairs)
            relevance=sum(_product_fit(p,c) for p in combo)
            outfits.append((combo,relevance+coherence,total))
    outfits.sort(key=lambda x:x[1],reverse=True)
    unique=[]; seen=set()
    for combo,score,total in outfits:
        key=tuple(p.id for p in combo)
        if key in seen: continue
        seen.add(key); unique.append({"products":list(combo),"total_price":round(total,2),"currency":c.currency,"reason":"Built from catalog products matching the requested style, occasion, colors and budget where available."})
        if len(unique)>=max_outfits: break
    return unique
