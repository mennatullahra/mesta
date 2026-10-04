"""Create the local database and load the clearly fictional MESTA demo catalog."""
from __future__ import annotations
import json
import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))
from pydantic import TypeAdapter
from sqlalchemy import select
from app.db.database import Base, SessionLocal, engine
from app.db.models import Product
from app.schemas.product import ProductCreate

DATA_FILE = BACKEND_DIR / "data" / "products.json"

def load_seed_data() -> list[ProductCreate]:
    raw = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    products = TypeAdapter(list[ProductCreate]).validate_python(raw)
    ids = [p.id for p in products]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate product IDs in seed data")
    return products

def seed() -> int:
    products = load_seed_data()
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        existing = set(db.scalars(select(Product.id)).all())
        added = 0
        for item in products:
            if item.id in existing:
                continue
            db.add(Product(**item.model_dump()))
            added += 1
        db.commit()
    return added

if __name__ == "__main__":
    count = seed()
    print(f"MESTA demo catalog ready. Added {count} products.")
