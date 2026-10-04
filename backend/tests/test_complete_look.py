from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.db.database import Base
from app.db.models import Product
from app.services.styling.complete_look import complete_look

def test_skirt_does_not_recommend_skirt():
 e=create_engine("sqlite:///:memory:",connect_args={"check_same_thread":False},poolclass=StaticPool); Base.metadata.create_all(e);S=sessionmaker(bind=e)
 with S() as db:
  anchor=Product(id="s1",brand="D",name="Skirt",category="skirt",price=100,currency="EGP",color_family="neutral",is_active=True)
  db.add_all([anchor,Product(id="s2",brand="D",name="Other skirt",category="skirt",price=100,currency="EGP",is_active=True),Product(id="b",brand="D",name="Blouse",category="blouse",price=100,currency="EGP",color_family="red",is_active=True),Product(id="h",brand="D",name="Hijab",category="hijab",price=100,currency="EGP",color_family="neutral",is_active=True)]);db.commit()
  result=complete_look(db,anchor)
  assert result and all(p.category!="skirt" for p in result)
