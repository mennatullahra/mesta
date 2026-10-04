import pytest
from pydantic import ValidationError
from app.schemas.product import ProductCreate

def valid_product(**overrides):
    data={"id":"x","brand":"Demo","name":"Blouse","category":"blouse","price":100,"currency":"egp"}
    data.update(overrides)
    return ProductCreate(**data)

def test_schema_normalizes_currency():
    assert valid_product().currency == "EGP"

def test_price_must_be_positive():
    with pytest.raises(ValidationError):
        valid_product(price=0)

def test_unknown_category_fails():
    with pytest.raises(ValidationError):
        valid_product(category="random")
