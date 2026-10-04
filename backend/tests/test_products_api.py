from fastapi.testclient import TestClient
from app.main import app
from app.db.database import Base, engine, SessionLocal
from app.db.models import Product

client=TestClient(app)

def setup_function():
    Base.metadata.drop_all(bind=engine); Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        db.add(Product(id="p1",brand="Demo (Demo)",name="Burgundy Blouse",category="blouse",price=890,currency="EGP",is_active=True))
        db.commit()

def test_list_products():
    r=client.get("/api/products")
    assert r.status_code == 200
    assert r.json()[0]["id"] == "p1"

def test_product_404():
    assert client.get("/api/products/missing").status_code == 404

def test_products_can_filter_by_brand_and_price():
    all_products = client.get('/api/products').json()
    brand = all_products[0]['brand']
    filtered = client.get('/api/products', params={'brand': brand, 'max_price': 5000}).json()
    assert filtered
    assert all(p['brand'] == brand and p['price'] <= 5000 for p in filtered)
