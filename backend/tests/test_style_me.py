from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.db.database import Base
from app.db.models import Product
from app.schemas.styling import StyleConstraints
from app.services.styling.style_me import build_style_outfits

def test_budget_and_catalog_truth():
 e=create_engine("sqlite:///:memory:",connect_args={"check_same_thread":False},poolclass=StaticPool);Base.metadata.create_all(e);S=sessionmaker(bind=e)
 with S() as db:
  for i,(cat,price) in enumerate([("dress",1400),("hijab",200),("bag",500),("shoes",600)]): db.add(Product(id=str(i),brand="D",name=cat,category=cat,price=price,currency="EGP",primary_color="burgundy" if cat=="dress" else "beige",color_family="red" if cat=="dress" else "neutral",style_tags=["elegant"],occasion_tags=["engagement"],modesty_tags=["hijab_friendly"],is_active=True))
  db.commit(); c=StyleConstraints(occasion="engagement",styles=["elegant"],budget=3000)
  outfits=build_style_outfits(db,c)
  assert outfits and all(o["total_price"]<=3000 for o in outfits)
  assert all(db.get(Product,p.id) is not None for o in outfits for p in o["products"])

def test_impossible_budget_returns_none():
 e=create_engine("sqlite:///:memory:",connect_args={"check_same_thread":False},poolclass=StaticPool);Base.metadata.create_all(e);S=sessionmaker(bind=e)
 with S() as db:
  db.add(Product(id="d",brand="D",name="Dress",category="dress",price=5000,currency="EGP",is_active=True));db.commit()
  assert build_style_outfits(db,StyleConstraints(budget=1000))==[]
