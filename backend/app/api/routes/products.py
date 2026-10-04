from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import Product
from app.schemas.product import ProductRead

router = APIRouter(prefix="/api/products", tags=["products"])

@router.get("", response_model=list[ProductRead])
def list_products(
    category: str | None = None,
    brand: str | None = None,
    active_only: bool = True,
    color: str | None = None,
    size: str | None = None,
    min_price: float | None = Query(default=None, ge=0),
    max_price: float | None = Query(default=None, ge=0),
    limit: int = Query(default=100, ge=1, le=200),
    db: Session = Depends(get_db),
):
    stmt = select(Product)
    if active_only:
        stmt = stmt.where(Product.is_active.is_(True))
    if category:
        stmt = stmt.where(Product.category == category)
    if brand:
        stmt = stmt.where(Product.brand == brand)
    if color:
        stmt = stmt.where(Product.color_family == color)
    if size:
        stmt = stmt.where(Product.available_sizes.contains(size))
    if min_price is not None:
        stmt = stmt.where(Product.price >= min_price)
    if max_price is not None:
        stmt = stmt.where(Product.price <= max_price)
    return list(db.scalars(stmt.order_by(Product.brand, Product.name).limit(limit)).all())

@router.get("/{product_id}", response_model=ProductRead)
def get_product(product_id: str, db: Session = Depends(get_db)):
    product = db.get(Product, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.get("/{product_id}/complete-look", response_model=list[ProductRead])
def product_complete_look(product_id: str, budget: float | None = Query(default=None, gt=0), db: Session = Depends(get_db)):
    from app.services.styling.complete_look import complete_look
    product = db.get(Product, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return complete_look(db, product, budget=budget)
