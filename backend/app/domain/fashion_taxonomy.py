"""Central normalized fashion vocabulary for the MESTA POC."""
from __future__ import annotations

CATEGORIES = {
    "blouse", "shirt", "top", "skirt", "dress", "pants", "blazer",
    "cardigan", "jacket", "hijab", "bag", "shoes",
}
COLOR_FAMILIES = {"red", "pink", "orange", "yellow", "green", "blue", "purple", "brown", "neutral", "black", "white", "metallic"}
COLORS = {"burgundy", "red", "rose", "blush", "cream", "beige", "camel", "taupe", "brown", "black", "white", "off_white", "grey", "navy", "blue", "denim_blue", "sage", "olive", "green", "lilac", "purple", "gold", "silver"}
STYLES = {"casual", "minimal", "elegant", "classic", "streetwear", "romantic", "workwear", "evening", "smart_casual"}
FITS = {"fitted", "regular", "relaxed", "loose", "oversized", "flowy"}
LENGTHS = {"cropped", "regular", "longline", "mini", "midi", "maxi"}
SLEEVE_LENGTHS = {"sleeveless", "short", "elbow", "three_quarter", "long"}
NECKLINES = {"crew", "round", "v_neck", "square", "boat", "collared", "high", "mock", "turtleneck"}
PATTERNS = {"solid", "striped", "floral", "printed", "checked", "polka_dot", "textured"}
OCCASIONS = {"everyday", "work", "smart_casual", "special_occasion", "engagement", "evening", "weekend"}
MODESTY_TAGS = {"long_sleeve", "maxi_length", "midi_length", "loose_fit", "high_neckline", "opaque", "hip_coverage", "hijab_friendly", "layering_friendly"}

ALIASES = {
    "maxi_skirt": ("skirt", "maxi"),
    "trousers": ("pants", None),
    "handbag": ("bag", None),
    "scarf": ("hijab", None),
}

def normalize_category(value: str) -> str:
    """Normalize a category and reject vocabulary outside the POC taxonomy."""
    normalized = value.strip().lower().replace("-", "_").replace(" ", "_")
    if normalized in ALIASES:
        normalized = ALIASES[normalized][0]
    if normalized not in CATEGORIES:
        raise ValueError(f"Unsupported category: {value}")
    return normalized
