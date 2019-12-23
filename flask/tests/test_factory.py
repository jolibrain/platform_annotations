from app import create_app

def test_hello(client):
    response = client.get('/')
    assert response.data == b'Annotation tool'
