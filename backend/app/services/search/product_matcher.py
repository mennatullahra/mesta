from dataclasses import dataclass
from app.db.models import Product
from app.schemas.search import SearchItem
from app.services.search.embedding_service import EmbeddingService
from app.services.search.representation import product_representation

@dataclass(frozen=True)
class MatchWeights:
    semantic: float = 0.25
    category: float = 0.30
    color: float = 0.15
    style: float = 0.10
    attributes: float = 0.10
    modesty: float = 0.10

class ProductMatcher:
    def __init__(self, embeddings: EmbeddingService | None = None, weights: MatchWeights | None = None):
        self.embeddings = embeddings or EmbeddingService()
        self.w = weights or MatchWeights()

    def _query_text(self, q: SearchItem) -> str:
        parts=[q.query,q.category,q.color,q.color_family,q.fit,q.length,q.sleeve_length,q.neckline,q.pattern,*q.style_tags,*q.modesty_tags]
        return " ".join(str(x).replace("_"," ") for x in parts if x)

    @staticmethod
    def _category(q: SearchItem, p: Product) -> tuple[float,list[str]]:
        if not q.category: return 0.5, []
        if q.category == p.category: return 1.0, ["same category"]
        # Strong gate: unrelated categories receive no category credit and later penalty.
        return 0.0, []

    @staticmethod
    def _color(q: SearchItem, p: Product) -> tuple[float,list[str]]:
        if q.color and p.primary_color == q.color: return 1.0, [f"same {q.color} color"]
        if q.color_family and p.color_family == q.color_family: return 0.75, [f"same {q.color_family} color family"]
        return (0.5,[]) if not (q.color or q.color_family) else (0.0,[])

    @staticmethod
    def _set_overlap(requested: list[str], actual: list[str] | None) -> float:
        if not requested: return 0.5
        if not actual: return 0.0
        return len(set(requested)&set(actual))/len(set(requested))

    def score(self, q: SearchItem, p: Product):
        semantic=self.embeddings.similarity(self.embeddings.embed(self._query_text(q)), self.embeddings.embed(product_representation(p)))
        category, reasons=self._category(q,p)
        color, color_reasons=self._color(q,p); reasons += color_reasons
        style=self._set_overlap(q.style_tags,p.style_tags)
        if style > 0 and q.style_tags: reasons.append("similar style")
        modesty=self._set_overlap(q.modesty_tags,p.modesty_tags)
        if modesty > 0 and q.modesty_tags: reasons.append("compatible modesty features")
        attrs=[]
        for field in ("fit","length","sleeve_length","neckline","pattern"):
            wanted=getattr(q,field); actual=getattr(p,field)
            if wanted is not None and actual is not None:
                attrs.append(1.0 if wanted==actual else 0.0)
                if wanted==actual: reasons.append(f"same {field.replace('_',' ')}")
        attributes=sum(attrs)/len(attrs) if attrs else 0.5
        total=(semantic*self.w.semantic+category*self.w.category+color*self.w.color+style*self.w.style+attributes*self.w.attributes+modesty*self.w.modesty)
        if q.category and q.category != p.category:
            total *= 0.45
        return max(0.0,min(1.0,total)), semantic, reasons

    def rank(self, q: SearchItem, products: list[Product], top_k: int=5):
        scored=[]
        for p in products:
            score, semantic, reasons=self.score(q,p)
            scored.append((p,score,semantic,reasons))
        return sorted(scored,key=lambda x:x[1],reverse=True)[:top_k]
