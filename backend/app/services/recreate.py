from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.models import Product
from app.schemas.search import SearchItem
from app.schemas.outfit import OutfitAnalysis
from app.services.search.product_matcher import ProductMatcher
from app.services.styling.outfit_builder import OutfitBuilder

class RecreateLookService:
    def __init__(self,matcher=None,builder=None):
        self.matcher=matcher or ProductMatcher(); self.builder=builder or OutfitBuilder()
    def recreate(self,analysis:OutfitAnalysis,db:Session,top_k:int=3):
        products=list(db.scalars(select(Product).where(Product.is_active.is_(True))).all())
        groups=[]
        for item in analysis.items:
            q=SearchItem(category=item.category,color=item.color,color_family=item.color_family,fit=item.fit,length=item.length,sleeve_length=item.sleeve_length,neckline=item.neckline,pattern=item.pattern,style_tags=item.style_tags,modesty_tags=item.modesty_tags)
            ranked=self.matcher.rank(q,products,top_k)
            # Category is a hard availability constraint for reconstructed garments.
            ranked=[r for r in ranked if r[0].category==item.category]
            groups.append(ranked)
        if any(not g for g in groups): return {"source_analysis":analysis,"look":[],"total_price":0,"currency":"EGP","message":"No catalog match exists for at least one detected item."}
        selected=self.builder.select(groups)
        look=[]
        for requested,group,chosen in zip(analysis.items,groups,selected):
            cp,cs,_,cr=chosen
            look.append({"requested_item":requested,"selected_product":cp,"score":round(cs,4),"match_reasons":cr,"alternatives":[{"product":p,"score":round(s,4),"match_reasons":reasons} for p,s,_,reasons in group if p.id!=cp.id]})
        return {"source_analysis":analysis,"look":look,"total_price":round(sum(x[0].price for x in selected),2),"currency":"EGP"}
