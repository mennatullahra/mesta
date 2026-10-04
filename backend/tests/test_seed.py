from scripts.seed_products import load_seed_data

def test_seed_catalog_is_valid_and_unique():
    products=load_seed_data()
    assert 30 <= len(products) <= 50
    assert len({p.id for p in products}) == len(products)
    assert all("(Demo)" in p.brand for p in products)
    assert {"blouse","skirt","hijab","bag","shoes"}.issubset({p.category for p in products})
