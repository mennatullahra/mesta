from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.db.database import Base
from app.db.models import Product
from app.schemas.outfit import OutfitAnalysis
from app.services.recreate import RecreateLookService

engine=create_engine("sqlite:///:memory:",connect_args={"check_same_thread":False},poolclass=StaticPool)
Session=sessionmaker(bind=engine)

def test_recreate_returns_only_catalog_products_and_total():
    Base.metadata.create_all(engine)
    with Session() as db:
        db.add_all([
          Product(id="b",brand="A (Demo)",name="Burgundy Blouse",category="blouse",price=890,currency="EGP",primary_color="burgundy",color_family="red",sleeve_length="long",style_tags=["elegant"],is_active=True),
          Product(id="s",brand="B (Demo)",name="Cream Maxi Skirt",category="skirt",price=1150,currency="EGP",primary_color="cream",color_family="neutral",length="maxi",fit="flowy",style_tags=["elegant"],is_active=True),
          Product(id="h",brand="C (Demo)",name="Beige Hijab",category="hijab",price=220,currency="EGP",primary_color="beige",color_family="neutral",style_tags=["elegant"],is_active=True),
        ]);db.commit()
        a=OutfitAnalysis.model_validate({"items":[{"category":"blouse","color":"burgundy","color_family":"red","sleeve_length":"long","style_tags":["elegant"]},{"category":"skirt","color":"cream","color_family":"neutral","length":"maxi","style_tags":["elegant"]},{"category":"hijab","color":"beige","color_family":"neutral","style_tags":["elegant"]}]})
        result=RecreateLookService().recreate(a,db)
        ids=[x["selected_product"].id for x in result["look"]]
        assert ids==["b","s","h"]
        assert result["total_price"]==2260
        assert all(db.get(Product,x) is not None for x in ids)
