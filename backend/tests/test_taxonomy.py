import pytest
from app.domain.fashion_taxonomy import normalize_category

def test_normalize_category_alias():
    assert normalize_category("handbag") == "bag"

def test_unknown_category_rejected():
    with pytest.raises(ValueError):
        normalize_category("spacesuit")
