from app.db.models import Product
from app.schemas.search import SearchItem
from app.services.search.product_matcher import ProductMatcher

m=ProductMatcher()
def p(id,category,color,family="red",**kw):
    return Product(id=id,brand="Demo",name=id,category=category,price=100,currency="EGP",primary_color=color,color_family=family,is_active=True,**kw)

def test_category_mismatch_strongly_penalized():
    q=SearchItem(category="blouse",color="burgundy",color_family="red",sleeve_length="long")
    blouse=p("b","blouse","burgundy",sleeve_length="long")
    skirt=p("s","skirt","burgundy",length="maxi")
    ranked=m.rank(q,[skirt,blouse],2)
    assert ranked[0][0].id == "b"
    assert ranked[0][1] > ranked[1][1]

def test_exact_color_beats_unrelated_color_same_category():
    q=SearchItem(category="blouse",color="burgundy",color_family="red")
    exact=p("exact","blouse","burgundy")
    cream=p("cream","blouse","cream","neutral")
    assert m.rank(q,[cream,exact],2)[0][0].id == "exact"

def test_unknown_attributes_not_counted_as_mismatch():
    q=SearchItem(category="blouse",color="burgundy")
    product=p("x","blouse","burgundy",material=None)
    score,_,_=m.score(q,product)
    assert score > 0.5
