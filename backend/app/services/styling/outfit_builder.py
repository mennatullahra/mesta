from __future__ import annotations
import itertools
from app.services.styling.compatibility import pair_compatibility

class OutfitBuilder:
    def select(self,candidate_groups):
        """Choose a coherent combination from small top-k groups by exhaustive scoring."""
        if not candidate_groups or any(not g for g in candidate_groups): return []
        best=None; best_score=-1.0
        for combo in itertools.product(*candidate_groups):
            match=sum(x[1] for x in combo)/len(combo)
            products=[x[0] for x in combo]
            pairs=list(itertools.combinations(products,2))
            coherence=sum(pair_compatibility(a,b) for a,b in pairs)/len(pairs) if pairs else 1.0
            score=0.72*match+0.28*coherence
            if score>best_score: best,best_score=combo,score
        return list(best)
