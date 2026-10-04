import pytest
from fastapi import HTTPException
from app.api.routes.visual_search import validate_image

def test_unsupported_file_type():
    with pytest.raises(HTTPException) as e: validate_image(b"hello","text/plain")
    assert e.value.status_code==415

def test_invalid_image_bytes():
    with pytest.raises(HTTPException) as e: validate_image(b"not image","image/jpeg")
    assert e.value.status_code==400
