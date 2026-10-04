"""Small, explainable POC outfit compatibility rules."""
NEUTRALS={"neutral","black","white","brown"}

def color_compatibility(a,b):
    if not a or not b: return 0.6
    if a==b: return 0.85
    if a in NEUTRALS or b in NEUTRALS: return 1.0
    pairs={frozenset(("red","pink")),frozenset(("blue","neutral")),frozenset(("green","neutral"))}
    return 0.85 if frozenset((a,b)) in pairs else 0.55

def pair_compatibility(a,b):
    color=color_compatibility(a.color_family,b.color_family)
    sa=set(a.style_tags or []); sb=set(b.style_tags or [])
    style=0.8 if not sa or not sb else (1.0 if sa&sb else 0.55)
    oa=set(a.occasion_tags or []); ob=set(b.occasion_tags or [])
    occasion=0.8 if not oa or not ob else (1.0 if oa&ob else 0.6)
    silhouette=1.0
    if a.category in {"skirt","pants"} and a.fit in {"flowy","loose"} and b.category in {"blouse","shirt","top"} and b.fit in {"oversized","loose"}:
        silhouette=0.65
    if b.category in {"skirt","pants"} and b.fit in {"flowy","loose"} and a.category in {"blouse","shirt","top"} and a.fit in {"oversized","loose"}:
        silhouette=0.65
    return 0.35*color+0.25*style+0.25*occasion+0.15*silhouette
