from app.db.models import Product

def product_representation(p: Product) -> str:
    parts = [p.category, p.primary_color, p.color_family, p.fit, p.length, p.sleeve_length, p.neckline, p.pattern]
    parts += p.style_tags or []
    parts += p.occasion_tags or []
    parts += p.modesty_tags or []
    return " ".join(str(x).replace("_", " ") for x in parts if x)
