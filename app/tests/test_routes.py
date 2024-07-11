import pytest
from app import app, db
from app.models import Product

# Setup and teardown for testing
@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()


def test_add_product(client):
    # Create a sample product
    product_data = {
        'name': 'Test Product',
        'description': 'Test Description',
        'price': 29.99,
        'stock': 100
    }

    # Send POST request to add product
    response = client.post('/products', json=product_data)
    assert response.status_code == 201
    assert 'Product added successfully' in response.json['message']
    assert response.json['product']['name'] == product_data['name']


def test_get_products(client):
    # Add sample products
    product1 = Product(name='Product 1', price=19.99, stock=50)
    product2 = Product(name='Product 2', price=24.99, stock=75)
    db.session.add(product1)
    db.session.add(product2)
    db.session.commit()

    # Send GET request to retrieve products
    response = client.get('/products')
    assert response.status_code == 200
    assert len(response.json) == 2  # Assuming two products are returned
