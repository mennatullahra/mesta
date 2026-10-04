from fastapi.testclient import TestClient
from app.main import app

def test_python_only_frontend_is_served():
    client = TestClient(app)
    root = client.get('/')
    assert root.status_code == 200
    assert 'MESTA' in root.text
    assert client.get('/static/app.js').status_code == 200
    assert client.get('/static/products/demo-001.svg').status_code == 200
